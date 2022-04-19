from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

# Admin database fields
class Admin(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='admins/')
    mobile = models.CharField(max_length=20)
    def __str__(self):
        return self.user.username
    
# customer database fields 
class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=200)
    address = models.CharField(max_length=200, null=True, blank=True)
    image = models.ImageField(upload_to='customer_images/')
    phone = models.CharField(max_length=15,blank=True, null=True)
    join_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.full_name

# category database fields
class Category(models.Model):
    title = models.CharField(max_length=100)
    title_ar = models.CharField(max_length=200,blank=True,null=True)
    slug = models.SlugField(null=True, blank=True)
    
    # creating slug automaticaly
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Category, self).save(*args, **kwargs)

    def __unicode__(self):
        return u'{}'.format(self.title)
        
    def __str__ (self):
        return str(self.title)

# product database fields
class Products(models.Model):
    title = models.CharField(max_length = 200)
    slug = models.SlugField(null=True,blank=True)
    title_ar = models.CharField(max_length=200,blank=True, null=True)
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    image = models.ImageField(upload_to='product/')
    price = models.IntegerField(default=0)
    discount = models.IntegerField(default=0)
    description = models.TextField()
    description_ar = models.TextField(null=True,blank=True)
    warranty = models.CharField(max_length = 300,null=True,blank=True)
    return_policy = models.CharField(max_length = 300,null=True,blank=True)
    
    def get_display_price(self):
        return "{0:.2f}".format(self.price / 100)
    

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Products, self).save(*args, **kwargs)
        
    def __unicode__(self):
        return u'{}'.format(self.title)

    def __str__ (self):
        return str(self.title)

# cart database fields
class Cart(models.Model):
    customer = models.ForeignKey(User,on_delete = models.SET_NULL, blank = True, null=True)
    total = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__ (self):
        return "Cart : " + str(self.id)

# cart product database fields
class CartProduct(models.Model):
    cart = models.ForeignKey(Cart,on_delete=models.CASCADE)
    product = models.ForeignKey(Products , on_delete = models.CASCADE)
    rate = models.PositiveIntegerField()      
    quantity = models.PositiveIntegerField()      
    subtotal = models.PositiveIntegerField() 
    def __str__ (self):
        return "Cart : " + str(self.cart.id) +" CartProduct : "+ str(self.id)

# order status
ORDER_STATUS = (
    ("Order Received","Order Received"),
    ("Order Processing","Order Processing"),
    ("Order On The Way","Order On The Way"),
    ("Order Completed","Order Completed"),
    ("Order Canceled","Order Canceled"),)

# payment methods 
METHODS = (
    ("Cash On Delivery","Cash On Delivery"),
    ("Khalti","Khalti"),
    ("Esewa","Esewa"),)

# order database fields
class Order(models.Model):
    cart = models.OneToOneField(Cart,on_delete=models.CASCADE)
    ordered_by = models.CharField(max_length=200) 
    shopping_address = models.CharField(max_length = 500)
    phone_num = models.CharField(max_length=15)
    email = models.EmailField(null=True , blank = True)
    subtotal = models.PositiveIntegerField()
    discount = models.PositiveIntegerField()
    total = models.PositiveIntegerField()
    order_status = models.CharField(max_length=50,choices = ORDER_STATUS)
    created_at = models.DateTimeField(auto_now_add = True)
    payment_method = models.CharField(max_length=20,choices=METHODS,default="Cash On Delivery")
    payment_completed = models.BooleanField(default= False, null=True,blank=True)
    def __str__(self):
        return "Order : "+ str(self.id) 

# product image database fields  
class Product_Images(models.Model):
    product = models.ForeignKey(Products , on_delete = models.CASCADE)
    image = models.ImageField(upload_to = 'product_images/')
    def __str__(self):
        return str(self.product)
