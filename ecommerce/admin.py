from django.contrib import admin
from .models import *


for model in [Admin,Customer,Category,Products,Cart,CartProduct,Order,Product_Images]:
    admin.site.register(model)
