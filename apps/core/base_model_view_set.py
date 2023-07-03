from django.db.models import Q
from django_filters import utils
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.filters import OrderingFilter
from rest_framework.response import Response
from rest_framework.serializers import Serializer
from rest_framework.settings import api_settings
from rest_framework.viewsets import GenericViewSet

from apps.core.response_resource import ResponseResource
from apps.repositories.base_repo import BaseRepo


class BaseGenericViewSet(GenericViewSet):
    filterset_class = None
    ordering_fields = None
    serializer_class = Serializer
    permission_action_classes = {}
    serializer_action_classes = {}
    repository_class = BaseRepo

    def get_permissions(self):
        try:
            permission_classes = self.permission_action_classes[self.action]
            return [permission() for permission in permission_classes]
        except (KeyError, AttributeError):
            return super().get_permissions()

    def get_serializer_class(self):
        try:
            return self.serializer_action_classes[self.action]
        except (KeyError, AttributeError):
            return super().get_serializer_class()

    def finalize_response(self, request, response, *args, **kwargs):
        response = super().finalize_response(request, response, args, kwargs)
        if isinstance(response, Response) and not response.exception:
            response.data = ResponseResource(data=response.data).data
        return response

    def get_queryset(self):
        self.queryset = self.repository_class.all()
        return self.queryset

    def get_object(self):
        queryset = self.get_queryset()
        filter_kwargs = {self.lookup_field: self.kwargs[self.lookup_field]}
        obj = self.repository_class.get_object_or_404(queryset.model, filter_kwargs)
        self.check_object_permissions(self.request, obj)
        return obj


class BaseCreateModelMixin:
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = self.repository_class.create(serializer.validated_data)
        headers = self.get_success_headers(serializer.data)
        return Response(self.get_serializer(instance).data, status=status.HTTP_201_CREATED, headers=headers)

    def get_success_headers(self, data):
        try:
            return {'Location': str(data[api_settings.URL_FIELD_NAME])}
        except (TypeError, KeyError):
            return {}


class BaseRetrieveModelMixin:
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class BaseUpdateModelMixin:
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        instance = self.repository_class.update(instance, serializer.validated_data)

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}

        return Response(self.get_serializer(instance).data)


class BaseDestroyModelMixin:
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.repository_class.delete(instance)
        return Response()


class FilterMixin:
    def get_filter_kwargs(self):
        if not self.filterset_class:
            return Q()

        kwargs = DjangoFilterBackend().get_filterset_kwargs(self.request,
                                                            self.queryset,
                                                            self)
        filterset = self.filterset_class(**kwargs)
        if not filterset.is_valid():
            raise utils.translate_validation(filterset.errors)

        return self.filterset_class.get_filter_kwargs(filterset.form.cleaned_data)


class BaseListModelMixin(FilterMixin):
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        filter_kwargs = self.get_filter_kwargs()
        queryset = self.repository_class.filter_queryset(queryset, filter_kwargs=filter_kwargs)

        if self.ordering_fields:
            ordering = OrderingFilter().get_ordering(self.request, queryset, self)
            queryset = self.repository_class.ordering_queryset(queryset, ordering)
        if self.pagination_class is not None:
            page = self.paginate_queryset(queryset)
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class BaseModelViewSet(BaseCreateModelMixin,
                       BaseRetrieveModelMixin,
                       BaseUpdateModelMixin,
                       BaseDestroyModelMixin,
                       BaseListModelMixin,
                       BaseGenericViewSet):
    pass
