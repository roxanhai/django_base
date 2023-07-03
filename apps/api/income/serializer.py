from rest_framework import serializers

from apps.models import Reporter


class ReporterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reporter
        fields = ('id', 'name', 'type', 'created', 'modified')