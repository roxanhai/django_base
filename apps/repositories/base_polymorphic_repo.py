from django.contrib.contenttypes.models import ContentType
from django.db import models


# from apps.core.pagination import DefaultLimitOffsetPagination


class BasePolymorphicRepo(object):
    class Meta:
        model = models.Model

    @classmethod
    def create_polymorphic(cls, content_object_instance, **data):
        data['content_type'] = ContentType.objects.get_for_model(content_object_instance)
        data['object_id'] = content_object_instance.id
        return cls.Meta.model.objects.create(**data)
