# from django.shortcuts import render
#

# from django.views import View
# from django.shortcuts import get_object_or_404
# from .models import Product

# from django.http import JsonResponse
# from django.views.decorators.csrf import csrf_exempt


# class ProductView(View):
#     def get(self, request, product_id=None):
#         if product_id:
#             product = get_object_or_404(Product, id=product_id)
#             return JsonResponse(product_to_dict(product))
#         products = Product.objects.all().values()
#         return JsonResponse(list(products), safe=False)

#     @csrf_exempt
#     def post(self, request):
#         data = json.loads(request.body)
#         product = Product.objects.create(**data)
#         return JsonResponse(product_to_dict(product))

#     @csrf_exempt
#     def put(self, request, product_id):
#         product = get_object_or_404(Product, id=product_id)
#         data = json.loads(request.body)
#         for key, value in data.items():
#             setattr(product, key, value)
#         product.save()
#         return JsonResponse(product_to_dict(product))

#     @csrf_exempt
#     def delete(self, request, product_id):
#         product = get_object_or_404(Product, id=product_id)
#         product.delete()
#         return JsonResponse({"message": "Product deleted"})

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django.core.paginator import EmptyPage

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .authentication import JWTAuthentication
from .serializers import CartItemCreateSerializer


from .serializers import *
from .models import *


class ProductListPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "pageSize"
    page_query_param = "pageNumber"

    def get_paginated_response(self, data):
        return Response({
            'totalPages': self.page.paginator.count,  
            'currentPage': self.page.number,             
            'content': data,
        })


class ProductListAPIView(APIView):
    pagination_class = ProductListPagination
    def get(self, request):
        
        
        min_price = request.GET.get('min_price')
        max_price = request.GET.get('max_price')
        manufacturers = request.GET.getlist("manufacturers")

        products = Product.objects.all()

        # Применяем фильтрацию, если параметры переданы
        if min_price is not None:
            products = products.filter(price__gte=min_price)
        if max_price is not None:
            products = products.filter(price__lte=max_price)
        if manufacturers:
            products = products.filter(manufacturer__in=manufacturers)

        paginator = self.pagination_class()
        page = paginator.paginate_queryset(products, request)
        if page is not None:
            serializer = ProductSerializer(page, many=True)
        else:
            serializer = ProductSerializer(Product.objects.none(), many=True)
            
        return paginator.get_paginated_response(serializer.data)


class ProductDetailAPIView(APIView):
    def get_object(self, pk: int):
        try:
            return Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return None

    def get(self, request: Request, pk: int):
        product = self.get_object(pk)
        if not product:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(ProductSerializer(product).data)


class PickUpPointView(APIView):
    def get(self, request: Request) -> Response:
        pickup_points = list(PickUpPointSerializer(p).data for p in PickUpPoint.objects.all())
        return Response(pickup_points)


class OrderView(APIView):
    def post(self, request: Request) -> Response:
        user_id = 1
        user = User.objects.get(pk=user_id)
        order_items = list(user.cart.items.all())

        # Order(status=Order.Status.FORMED, pickup_point_id)
        #
        # for item in order_items:

    def get(self, request: Request) -> Response:
        user_orders = Order.objects.all()
        return Response(list(user_orders))


class SignUpView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        if serializer.is_valid():

            user = serializer.save()
            return Response(
                {"user": UserSerializer(user).data, "token": user.generate_jwt()},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SignInView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = SignInSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data["user"]
            return Response({"user": UserSerializer(user).data, "token": user.generate_jwt()})
        return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)


class CartItemView(APIView):
    authentication_classes = [JWTAuthentication]

    def post(self, request: Request):
        serializer = CartItemCreateSerializer(data=request.data | {"user_id": request.user.id})
        if serializer.is_valid():
            cart_item = serializer.save()
            return Response(
                {
                    "id": cart_item.id,
                    "product": cart_item.product.name,
                    "quantity": cart_item.quantity,
                    "total_price": str(cart_item.total_price()),
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # def delete(self):

    def get(self, request: Request) -> Response:
        items = CartItem.objects.filter(cart__user=request.user).prefetch_related("product")
        return Response(CartItemSerializer(items, many=True).data)
