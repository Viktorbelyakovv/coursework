from django.urls import path, include
from .views import AccountViewSet, DivisionViewSet, ClubsLibViewSet, ClubsTableViewSet, ForwardsTableViewSet,\
    PartnerViewSet
from rest_framework import routers

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'user', AccountViewSet, basename='')
router.register(r'division', DivisionViewSet, basename='')
router.register(r'clubs_lib', ClubsLibViewSet, basename='')
router.register(r'clubs_table', ClubsTableViewSet, basename='')
router.register(r'forwards_table', ForwardsTableViewSet, basename='')
router.register(r'partners', PartnerViewSet, basename='')

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls'))
]