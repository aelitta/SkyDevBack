from django.urls import include, path
from rest_framework import routers
from .views import DomainViewSet, VacancyViewSet, VacancyReqViewSet

router = routers.DefaultRouter()
router.register(r'domains', DomainViewSet)

router.register(r'vacancies', VacancyViewSet)
router.register(r'vacanciesreq', VacancyReqViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]