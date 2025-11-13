from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from .models import Favorite
from products.models import Product
from .serializers import FavoriteSerializer

class FavoriteViewSet(viewsets.ModelViewSet):
    serializer_class = FavoriteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Favorite.objects.filter(user=self.request.user)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["products_queryset"] = Product.objects.all()
        return context

    def perform_create(self, serializer):
        try:
            serializer.save(user=self.request.user)
        except Exception:
            raise Exception("Server error while adding favorite")