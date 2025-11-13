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

    def create(self, request, *args, **kwargs):
        try:
            product_id = request.data.get("product_id")
            if not product_id:
                return Response({"error": "Product ID required"}, status=status.HTTP_400_BAD_REQUEST)
            product = Product.objects.get(id=product_id)
            if Favorite.objects.filter(user=request.user, product=product).exists():
                return Response({"message": "Already in favorites"}, status=status.HTTP_200_OK)
            favorite = Favorite.objects.create(user=request.user, product=product)
            serializer = self.get_serializer(favorite)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Product.DoesNotExist:
            return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception:
            return Response({"error": "Server error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def destroy(self, request, *args, **kwargs):
        try:
            favorite = self.get_object()
            favorite.delete()
            return Response({"message": "Removed from favorites"}, status=status.HTTP_204_NO_CONTENT)
        except Favorite.DoesNotExist:
            return Response({"error": "Favorite not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception:
            return Response({"error": "Server error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)