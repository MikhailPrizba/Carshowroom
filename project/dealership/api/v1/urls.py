from django.urls import include, path
from rest_framework import routers

from dealership.api.v1.views import (
    DealershipViewSet,
    DealershipCarViewSet,
    DealershipOfferViewSet,
)

router = routers.DefaultRouter()
router.register(r"offer", DealershipOfferViewSet, basename="offer")
router.register(r"cars", DealershipCarViewSet, basename="cars")
router.register(r"", DealershipViewSet, basename="dealership")


urlpatterns = [
    path("", include(router.urls)),
]
