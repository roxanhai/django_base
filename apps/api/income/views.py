from django_filters.rest_framework import DjangoFilterBackend

from apps.api.income.filters import ReporterFilter
from apps.api.income.serializer import ReporterSerializer
from apps.core.base_model_view_set import BaseModelViewSet
from apps.repositories.reporter_repo import ReporterRepo


class ReporterApiView(BaseModelViewSet):
    serializer_class = ReporterSerializer
    repository_class = ReporterRepo
    filter_backends = [DjangoFilterBackend]
    filterset_class = ReporterFilter