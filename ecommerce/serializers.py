from django.contrib.auth.models import User
from ecommerce.models import *
from rest_framework import serializers

class AdminSerializer(serializers.ModelSerializer):
    class Meta:
       model = Admin
       fields = ['user','full_name','image','mobile']

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'

class ProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = '__all__'       

class OrdersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = [
            'ordered_by',
            'shopping_address',
            'phone_num',
            'email',
            'payment_method'
        ]
        
class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = '__all__'
        
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
