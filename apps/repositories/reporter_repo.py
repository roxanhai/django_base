from apps.models import Reporter
from apps.repositories.base_repo import BaseRepo


class ReporterRepo(BaseRepo):
    class Meta:
        model = Reporter