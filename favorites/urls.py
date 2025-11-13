from rest_framework import routers
from .views import FavoriteViewSet

router = routers.DefaultRouter()
router.register(r'', FavoriteViewSet, basename='favorites')

urlpatterns = router.urls