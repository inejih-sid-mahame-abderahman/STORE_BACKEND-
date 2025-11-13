from rest_framework import serializers
from .models import Favorite
from products.serializers import ProductSerializer
from products.models import Product  # import your Product model

class FavoriteSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(
    queryset=Product.objects.all(), source="product", write_only=True
    )

    class Meta:
        model = Favorite
        fields = ("id", "user", "product", "product_id", "created_at")
        read_only_fields = ("user",)

    def _init_(self, *args, **kwargs):
        super()._init_(*args, **kwargs)
        # Dynamically set queryset for product_id
        self.fields["product_id"].queryset = self.context.get("products_queryset", Favorite.objects.none())

    def create(self, validated_data):
        user = self.context["request"].user
        validated_data["user"] = user
        return super().create(validated_data)