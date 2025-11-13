from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Cart, CartItem, Order, OrderItem
from .serializers import CartSerializer, CartItemSerializer, OrderSerializer
from products.models import Product

class CartViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request):
        cart, _ = Cart.objects.get_or_create(user=request.user)
        serializer = CartSerializer(cart)
        return Response(serializer.data)

    @action(detail=False, methods=["post"])
    def add(self, request):
        try:
            product_id = request.data.get("product_id")
            quantity = int(request.data.get("quantity", 1))
            if not product_id:
                return Response({"error": "Product ID required"}, status=400)
            product = Product.objects.get(id=product_id)
            if product.stock < quantity:
                return Response({"error": "Not enough stock"}, status=400)
            cart, _ = Cart.objects.get_or_create(user=request.user)
            item, created = CartItem.objects.get_or_create(cart=cart, product=product, defaults={"quantity": quantity})
            if not created:
                item.quantity += quantity
                item.save()
            return Response({"message": "Product added to cart"})
        except Product.DoesNotExist:
            return Response({"error": "Product not found"}, status=404)
        except ValueError:
            return Response({"error": "Quantity must be integer"}, status=400)
        except Exception:
            return Response({"error": "Server error"}, status=500)

    @action(detail=False, methods=["put"])
    def update_item(self, request):
        try:
            product_id = request.data.get("product_id")
            quantity = int(request.data.get("quantity", 1))
            cart = Cart.objects.get(user=request.user)
            item = CartItem.objects.get(cart=cart, product_id=product_id)
            item.quantity = quantity
            item.save()
            return Response({"message": "Cart updated"})
        except CartItem.DoesNotExist:
            return Response({"error": "Item not found"}, status=404)
        except Exception:
            return Response({"error": "Server error"}, status=500)

    @action(detail=False, methods=["delete"])
    def remove(self, request):
        try:
            product_id = request.data.get("product_id")
            cart = Cart.objects.get(user=request.user)
            item = CartItem.objects.get(cart=cart, product_id=product_id)
            item.delete()
            return Response({"message": "Item removed"})
        except CartItem.DoesNotExist:
            return Response({"error": "Item not found"}, status=404)
        except Exception:
            return Response({"error": "Server error"}, status=500)

    @action(detail=False, methods=["post"])
    def checkout(self, request):
        try:
            cart = Cart.objects.get(user=request.user)
            if not cart.items.exists():
                return Response({"error": "Cart is empty"}, status=400)
            order = Order.objects.create(user=request.user, total=0)
            total = 0
            for item in cart.items.all():
                OrderItem.objects.create(order=order, product=item.product, quantity=item.quantity, price=item.product.price)
                total += item.quantity * item.product.price
                item.product.stock -= item.quantity
                item.product.save()
            order.total = total
            order.status = "completed"
            order.save()
            cart.items.all().delete()
            serializer = OrderSerializer(order)
            return Response(serializer.data)
        except Cart.DoesNotExist:
            return Response({"error": "Cart not found"}, status=404)
        except Exception:
            return Response({"error": "Server error"}, status=500)


class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)