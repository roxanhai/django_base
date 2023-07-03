from django_filters import FilterSet, CharFilter

from apps.core.filters import FilterSetMixin


class ReporterFilter(FilterSetMixin, FilterSet):
    name = CharFilter(lookup_expr='icontains')
