from rest_framework import routers

from apps.api.income.views import ReporterApiView

reporter_router = routers.DefaultRouter()
reporter_router.register('reporter', ReporterApiView, basename='reporter')
reporter_urlpatterns = reporter_router.urls
