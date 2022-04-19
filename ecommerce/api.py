from ecommerce.serializers import *
from ecommerce.models import *
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import (ListCreateAPIView,
                                     RetrieveUpdateDestroyAPIView,
                                     RetrieveDestroyAPIView,
                                     ListAPIView )
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication,BasicAuthentication


# All Admins Retrive Api
class AdminListApi(ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Admin.objects.all()
    serializer_class = AdminSerializer
    
# Admin Detail Api
class AdminDetailApi(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Admin.objects.all()
    serializer_class = AdminSerializer
  
# Admin filter search Api  
class AdminFilterApi(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request,kw,format=None):
        admin = Admin.objects.filter(
            Q(full_name__icontains=kw))
        serializer = AdminSerializer(admin,many=True,context={'request':request})
        return Response({'admin_filter':serializer.data})

# All Customer Retrive Api
class CustomersListApi(ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

# customer details Api
class CustomerDetailApi(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

# customer filter search Api
class CustomerFilterApi(APIView):
    permission_classes = [IsAuthenticated]
    def get(eslf,request,kw,format=None):
        customer = Customer.objects.filter(
            Q(full_name__icontains=kw)|
            Q(address__icontains=kw))
        serializer = CustomerSerializer(customer,many=True,context={'request':request})
        return Response({'customer_filter':serializer.data}) 

# All Products Retrive Api
class ProductsListAPI(ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Products.objects.all()
    serializer_class = ProductsSerializer
   
# Product Detail Api
class ProductDetailApi(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Products.objects.all()
    serializer_class = ProductsSerializer
   
# Product Filter search Api
class ProductFilterApi(APIView):
    permission_classes = [IsAuthenticated]
    def get(eslf,request,kw,format=None):
        product = Products.objects.filter(
            Q(title__icontains=kw)|
            Q(description__icontains=kw)|
            Q(warranty__icontains=kw)|
            Q(return_policy__icontains=kw))
        serializer = ProductsSerializer(product,many=True)
        return Response({'product_filter':serializer.data})

# All orders Retrive Api
class OrdersListApi(ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Order.objects.all()
    serializer_class = OrdersSerializer
    
# order detail Api
class OrderDetailApi(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Order.objects.all()
    serializer_class = OrdersSerializer
   
# order filter search Api
class OrdersFilterApi(APIView):
    permission_classes = [IsAuthenticated]
    def get(eslf,request,kw,format=None):
        order = Order.objects.filter(
            Q(ordered_by__icontains=kw)|
            Q(email__icontains=kw)|
            Q(payment_method__icontains=kw)|
            Q(shopping_address__icontains=kw))
        serializer = OrdersSerializer(order,many=True)
        return Response({'order_filter':serializer.data})
    
# all Carts retrieve  Api
class CartListApi(ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Cart.objects.all() 
    serializer_class = CartSerializer
    
# cart deatail api
class CartDetailApi(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Cart.objects.all() 
    serializer_class = CartSerializer
    
# all categories api
class CategoryListApi(ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    
# category details api 
class CategoryDetailApi(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

# category filter search api
class CategoryFilterApi(APIView):
    permission_classes = [IsAuthenticated]
    def get(eslf,request,kw,format=None):
        category = Category.objects.filter(
            Q(title__icontains=kw)|
            Q(slug__icontains=kw))
        serializer = CategorySerializer(category,many=True)
        return Response({'category_filter':serializer.data})

    