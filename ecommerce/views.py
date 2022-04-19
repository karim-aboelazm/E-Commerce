from django.shortcuts import render,redirect
from django.views.generic.edit import DeleteView
from django.views.generic import TemplateView,View,CreateView,FormView,DetailView,ListView,UpdateView
from django.urls import reverse_lazy,reverse
from django.contrib.auth import authenticate , login ,logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.conf import settings
from ecommerce.utils import password_reset_token
from django.core.mail import send_mail
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse,HttpResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.translation import gettext
from django.views import View
from ecommerce.forms import *
from .models import *
import requests
import json
import stripe
import re

stripe.api_key = settings.STRIPE_SECRET_KEY


# Mixin for Admins Pages
class AdminRequiredMixin(object):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and Admin.objects.filter(user=request.user).exists():
            pass
        else:
            return redirect("/admin-login/")
        return super().dispatch(request, *args, **kwargs)

# Admins Login Page
class AdminLoginView(FormView):
    template_name = "Admins/admin_login.html"
    form_class = AdminLoginForm
    success_url = reverse_lazy('ecom:admin_home')
    
    def form_valid(self, form):
        user_name = form.cleaned_data.get('username')
        pass_word = form.cleaned_data['password']
        usr = authenticate(username=user_name,password=pass_word)
        if usr is not None and Admin.objects.filter(user=usr).exists():
            login(self.request, usr)
        else:
            return render(self.request,self.template_name,{'form':self.form_class})
        return super().form_valid(form)

# Admins Home Page
class AdminHomeView(AdminRequiredMixin,TemplateView):
    template_name = "Admins/admin_home.html"
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and Admin.objects.filter(user=request.user).exists():
            pass
        else:
            return redirect("/admin-login/?next=/admin-home/")
        return super().dispatch(request, *args, **kwargs)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["all_orders"] = Order.objects.filter(order_status = "Order Received").order_by('-id') 
        return context
   
# Admins Orders Details Page
class AdminOrderDetailView(AdminRequiredMixin,DetailView):
    template_name = "Admins/admin_order_detail.html"
    model = Order
    context_object_name = "order_object"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["all_status"] = ORDER_STATUS 
        return context
   
# Admins All products page
class AdminAllOrderView(AdminRequiredMixin,ListView):
    template_name = "Admins/admin_all_order.html"
    queryset = Order.objects.all().order_by('-id')
    context_object_name = "all_orders"

# Admins Control status form
class AdminOrderStatusChangeView(AdminRequiredMixin,View):
    def post(self,request, *args, **kwargs):
        order_id = self.kwargs['pk']
        order_object = Order.objects.get(id=order_id)
        updated_status = request.POST.get('status')
        order_object.order_status = updated_status
        order_object.save()
        return redirect(reverse_lazy('ecom:admin_order_detail',kwargs={'pk':order_id}))
    
# Admin Products List page
class AdminProductList(AdminRequiredMixin,ListView):
    template_name = 'Admins/admin_product_list.html'
    queryset = Products.objects.all().order_by('-id')
    context_object_name = "all_products"
    
# Admin Add New Product Page
class AdminProductAdd(AdminRequiredMixin,CreateView):
    template_name = "Admins/add_new_product.html"
    form_class = ProductForm
    success_url = reverse_lazy("ecom:admin_product_list")
    def form_valid(self,form):
        pf = form.save()
        mi = self.request.FILES.getlist("more_images")
        for i in mi:
            Product_Images.objects.create(product=pf,image=i)
            
        return super().form_valid(form)

class UpdateAdminProduct(UpdateView):
    model = Products
    form_class = ProductForm
    template_name = 'Admins/edit_product.html'
    
    def get_object(self, *args, **kwargs):
        product = get_object_or_404(Products, pk=self.kwargs['pk'])
        return product
    
    def get_success_url(self, *args, **kwargs):
        success_url = reverse_lazy("ecom:admin_product_list")
        return success_url

def dell(request,id):
    product = Products.objects.get(id=id)
    product.delete()
    return redirect('ecom:admin_product_list')


# Admin Products List page
class AdminCategoryList(AdminRequiredMixin,ListView):
    template_name = 'Admins/admin_category_list.html'
    queryset = Category.objects.all().order_by('-id')
    context_object_name = "all_categories"
    
# Admin Add New Product Page
class AdminCategoryAdd(AdminRequiredMixin,CreateView):
    template_name = "Admins/add_new_category.html"
    form_class = CategoryForm
    success_url = reverse_lazy("ecom:admin_category_list")
    def form_valid(self,form):    
        return super().form_valid(form)


# -----------------------------------------------------

# mixin class
class EcomMixin():
    def dispatch(self, request, *args, **kwargs):
        cart_id = request.session.get("cart_id")
        current_user = request.user
        if cart_id:
            cart_obj = Cart.objects.get(id=cart_id)
            if current_user.is_authenticated and Customer.objects.filter(user=current_user).exists():
                cart_obj.customer = current_user
                cart_obj.save()
        return super().dispatch(request, *args, **kwargs)

# Home Page view
class HomeView(EcomMixin,TemplateView):
    template_name = "home_pages/home.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["some_products"] = Products.objects.all().order_by('-id')
        return context

# About page view
class AboutView(EcomMixin,TemplateView):
    template_name = "home_pages/about.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context[""] = 
        return context

# why us page view
class WhyUsView(EcomMixin,TemplateView):
    template_name = 'home_pages/why_us.html'

# contact us page view
class ContactUsView(EcomMixin,TemplateView):
    template_name = "contact/contact_us.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context[""] = 
        return context
  
# All products page view
class AllProductsView(EcomMixin,TemplateView):
    template_name = "products/allproducts.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        all_products = Products.objects.all().order_by('-id')
        paginator = Paginator(all_products,9)
        page_number = self.request.GET.get('page')
        product_list = paginator.get_page(page_number)
        context["list_products"] = product_list 
        return context
    
# product details page view
class ProductDetailView(EcomMixin,TemplateView):
    template_name = "products/productdetail.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product_slug = kwargs['slug']
        product = Products.objects.get(slug=product_slug)
        context["product"] =  product
        return context
 
# all categories page view
class CategoriesView(EcomMixin,TemplateView):
    template_name = "products/categories.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['all_categories'] = Category.objects.all() 
        return context

# add product to my cart
class AddToCartView(EcomMixin,TemplateView):
    template_name = "cart/add_to_cart.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product_id = kwargs['pro_id']
        product_obj = Products.objects.get(id=product_id)
        cart_id = self.request.session.get('cart_id',None)
        if cart_id:
            cart = Cart.objects.get(id = cart_id)
            this_product_in_cart = cart.cartproduct_set.filter(product=product_obj)
            if this_product_in_cart.exists():
                cartproduct = this_product_in_cart.last()
                cartproduct.quantity += 1
                cartproduct.subtotal += product_obj.price
                cartproduct.save()
                cart.total += product_obj.price
                cart.save()
            else:
                cartproduct = CartProduct.objects.create(cart=cart,product=product_obj,
                                                         rate=product_obj.price,quantity=1,
                                                         subtotal=product_obj.price)
                cart.total += product_obj.price
                cart.save()
        else:
            cart = Cart.objects.create(total=0)
            self.request.session['cart_id'] = cart.id
            cartproduct = CartProduct.objects.create(cart=cart,product=product_obj,
                                                         rate=product_obj.price,quantity=1,
                                                         subtotal=product_obj.price)
            cart.total += product_obj.price
            cart.save()
        return context
    
# my cart page view
class CartView(EcomMixin,TemplateView):
    template_name = "cart/mycart.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart_id = self.request.session.get('cart_id',None)
        if cart_id:
            cart = Cart.objects.get(id=cart_id)
        else:
            cart = None
        
        context["cart"] = cart 
        return context

# manage in items that are in cart 
class ManageCartView(EcomMixin,View):
    def get(self,request,*args, **kwargs):
        cp_id = self.kwargs['cp_id']
        action = request.GET.get('action')
        cp_obj = CartProduct.objects.get(id = cp_id)
        cart_obj = cp_obj.cart
          
        if action == 'acr':
             cp_obj.quantity += 1
             cp_obj.subtotal += cp_obj.rate
             cp_obj.save()
             cart_obj.total += cp_obj.rate
             cart_obj.save()
             
        elif action == 'dcr':
             cp_obj.quantity -= 1
             cp_obj.subtotal -= cp_obj.rate
             cp_obj.save()
             cart_obj.total -= cp_obj.rate
             cart_obj.save()
             if cp_obj.quantity == 0:
                 cp_obj.delete()
                 
        elif action == 'rcr':
            cart_obj.total -= cp_obj.subtotal
            cart_obj.save()
            cp_obj.delete()
        else:
            pass
        return redirect('/my-cart/')

# empty the cart form orders 
class EmptyCartView(EcomMixin,View):
    def get(self, request, *args, **kwargs):
        cart_id = request.session.get('cart_id',None)
        if cart_id:
            cart = Cart.objects.get(id=cart_id)
            cart.cartproduct_set.all().delete()
            cart.total = 0
            cart.save()
        return redirect('/my-cart/')

# check out page view
class CheckOutView(EcomMixin, CreateView):
    template_name = "cart/check_out.html"
    form_class = CheckOutForm
    success_url = reverse_lazy('ecom:home')
    
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated or request.user.customer or request.user.admin:
            pass
        else:
            return redirect("/customer-login/?next=/check-out/")
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart_id = self.request.session.get('cart_id',None)
        if cart_id:
            cart_obj = Cart.objects.get(id=cart_id)
        else:
            cart_obj = None
        context["cart"] = cart_obj
        return context
    
    def form_valid(self, form):
        cart_id = self.request.session.get('cart_id')
        if cart_id:
            cart_obj = Cart.objects.get(id=cart_id)
            form.instance.cart = cart_obj
            form.instance.subtotal = cart_obj.total
            form.instance.discount = 0
            form.instance.total = cart_obj.total
            form.instance.order_status = 'Order Received'
            del self.request.session['cart_id']
            pm = form.cleaned_data.get("payment_method")
            order = form.save()
            if pm == "Khalti":
                return redirect(reverse('ecom:khalti_request')+ "?o_id=" +str(order.id))
            elif pm == "Esewa":
                return redirect(reverse('ecom:esewa_request')+ "?o_id=" +str(order.id))
            elif pm == "paypal":
                return redirect(reverse('ecom:paypal_request')+ "?o_id=" +str(order.id))
            
        else:
            return redirect('ecom:home')
        return super().form_valid(form)

# ------------------------------------------------------

# # Khalti payment method request 
# class KhaltiRequestView(EcomMixin,View):
#     def get(self, request,*args, **kwargs):
#         o_id = request.GET.get("o_id")
#         order = Order.objects.get(id = o_id)
#         context={
#             "order":order
#         }
#         return render(request,'payment/khaltirequest.html',context)
   
# # Khalti payment method verify 
# class KhaltiVerifyView(EcomMixin,View):
#     def get(self,request,*args, **kwargs):
#         token = request.GET.get("token")
#         amount = request.GET.get("amount")
#         o_id = request.GET.get("order_id")
#         url = "https://khalti.com/api/v2/payment/verify/"
#         payload = {
#         "token": token,
#         "amount": amount
#         }
#         order_object = Order.objects.get(id = o_id)
#         headers = {
#         "Authorization": "Key test_secret_key_f59e8b7d18b4499ca40f68195a846e9b"
#         }

#         response = requests.post(url, payload, headers = headers)
#         resp_dict = response.json()
#         if resp_dict.get("idx"):
#             success = True
#             order_object.payment_completed = True
#             order_object.save()
#         else:
#             success = False
            
#         data = {
#             "success": success
#         }
#         return JsonResponse(data)

# # Esewa payment method request
# class EsewaRequestView(EcomMixin,View):
#     def get(self,request,*args,**kwargs):
#         o_id = request.GET.get("o_id")
#         order = Order.objects.get(id = o_id)
#         context = {
#             "order":order
#         }
#         return render(request,'payment/esewarequest.html',context)

# # Esewa payment method verify
# class EsewaVerifyView(EcomMixin,View):
#     def get(self,request,*args,**kwargs):
#         import xml.etree.ElementTree as ET
#         oid = request.GET.get("oid")
#         amt = request.GET.get("amt")
#         refId = request.GET.get("refId")
#         url ="https://uat.esewa.com.np/epay/transrec"
#         d = {
#             'amt': amt,
#             'scd': 'EPAYTEST',
#             'rid': refId,
#             'pid':oid,
#         }
#         resp = requests.post(url, d)
#         root = ET.fromstring(resp.content)
#         status = root[0].text.strip()
#         order_id = oid.split("_")[1]
#         order_object = Order.objects.get(id=order_id)
#         print(status)
#         if status == "Success":
#             order_object.payment_completed = True 
#             order_object.save()
#             return redirect('/')
#         else:
#             return redirect('/esewa-request/?o_id='+order_id)


# ------------------------------------------------------
 
# customer registeration
class CustomerRegisterView(CreateView):
    template_name = 'customer/signup.html'
    form_class = CustomerRegisterForm
    success_url = reverse_lazy('ecom:home')
    
    def form_valid(self, form):
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        email = form.cleaned_data.get('email')
        user = User.objects.create_user(username,email,password)
        form.instance.user = user
        login(self.request , user)
        return super().form_valid(form)

# customer logout
class CustomerLogoutView(View):
    def get(self,request):
        logout(request)
        return redirect('ecom:home')

# customer logout
class CustomerLoginView(FormView):
    template_name = 'customer/login.html'
    form_class = CustomerLoginForm
    success_url = reverse_lazy('ecom:home')
    
    def form_valid(self,form):
        user_name = form.cleaned_data.get('username')
        pass_word = form.cleaned_data['password']
        usr = authenticate(username=user_name,password=pass_word)
        if usr is not None and Customer.objects.filter(user=usr).exists():
            login(self.request, usr)
        else:
            return render(self.request,self.template_name,{'form':self.form_class})
        return super().form_valid(form)
    
    def get_success_url(self):
        if 'next' in self.request.GET:
            next_url = self.request.GET.get('next')
            return next_url
        else:
            return self.success_url

# customer profile
class CustomerProfileView(TemplateView):
    template_name = "customer/profile.html"
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.customer:
            pass
        else:
            return redirect("/customer-login/?next=/customer-profile/")
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_user = self.request.user
        context["profile"] = Customer.objects.get(user=current_user) 
        order = Order.objects.filter(cart__customer=current_user).order_by('-id')
        context["orders"] = order
        return context
 
# customer update profile
class UpdateProfileView(UpdateView):
    model = Customer
    form_class = ProfileUpdateForm
    template_name = 'customer/edit_profile.html'
    
    def get_object(self, *args, **kwargs):
        customer = get_object_or_404(Customer, pk=self.kwargs['pk'])
        return customer
    
    def get_success_url(self, *args, **kwargs):
        success_url = reverse_lazy('ecom:customer_profile')
        return success_url
   
# customer order detail 
class CustomerOrderDetailView(DetailView):
    template_name = "customer/order_detail.html"
    model = Order
    context_object_name = "order_object"
    
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.customer:
            order_id = self.kwargs['pk']
            order = Order.objects.get(id = order_id)
            if request.user.customer == order.cart.customer:
                return redirect("ecom:customer_profile")
        else:
            return redirect("/customer-login/?next=/customer-profile/")
        return super().dispatch(request, *args, **kwargs)

# -------------------------------------------------------


# customer forgot password 
class ForgotPasswordView(FormView):
    template_name = 'customer/forgot_password.html'
    form_class = PasswordForm
    success_url = "/forgot-password/?m=s"
    def form_valid(self,form):
        # get email from user
        email = form.cleaned_data.get("email")
        # get current host ip/Domain [127.0.0.1:8000]
        url = self.request.META['HTTP_HOST']
        # get customer and then user
        customer = Customer.objects.get(user__email = email)
        user = customer.user
        # sent mail to customer with email
        text_content = 'Please click the link below to reset your password.  '
        html_content = url + "/reset-password/" + email +"/" + password_reset_token.make_token(user)+"/"
        send_mail(
            'Password Reset Link | KOGO Ecommerce',
            text_content + html_content,
            settings.EMAIL_HOST_USER,
            [email],
            fail_silently = False,
            
        )
        return super().form_valid(form)

# customer reset password 
class ResetPasswordView(FormView):
    template_name = 'customer/reset_password.html'
    form_class = PasswordResetForm
    success_url = '/customer-login/'
    
    def dispatch(self, request, *args, **kwargs):
        email = self.kwargs.get("email")
        user = User.objects.get(email=email)
        token = self.kwargs.get("token")
        if user is not None and password_reset_token.check_token(user,token):
           pass
        else:
            return redirect(reverse('ecom:forgot_password')+'?m=e')
        return super().dispatch(request, *args, **kwargs)
        
    
    def form_valid(self,form):
        password = form.cleaned_data['new_password']
        email = self.kwargs.get("email")
        user = User.objects.get(email=email)
        user.set_password(password)
        user.save()
        return super().form_valid(form)

# --------------------------------------------------------

# search view
class SearchView(TemplateView):
    template_name = "products/search.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        kw = self.request.GET.get("keyword")
        search_result = Products.objects.filter(
            Q(title__icontains=kw)|
            Q(title_ar__icontains=kw)|
            Q(description__icontains=kw)|
            Q(warranty__icontains=kw)|
            Q(return_policy__icontains=kw))
        
        context["results"] = search_result 
        return context
        