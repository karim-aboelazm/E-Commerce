from django.urls import path
from ecommerce.views import *
from . import api

app_name = 'ecommerce'

urlpatterns = [
    
    # App URLS.........
    
    # home page url
    path('',HomeView.as_view(),name='home'),
    
    # about us page url
    path('about/',AboutView.as_view(),name='about_us'),
    
    # contact us page url
    path('contact-us/',ContactUsView.as_view(),name='contact_us'),
    
    # why us page url
    path('why-us/',WhyUsView.as_view(),name='why_us'),

    # products url
    path('all-products/',AllProductsView.as_view(),name='all_products'),
    path('product/<slug:slug>/',ProductDetailView.as_view(),name='product_detail'),
    
    # categories url
    path('all-categories/',CategoriesView.as_view(),name='all_categories'),
    
    # cart url
    path('my-cart/',CartView.as_view(),name='my_cart'),
    path('add-to-cart/<int:pro_id>/',AddToCartView.as_view(),name='add_to_cart'),
    path('manage-cart/<int:cp_id>/',ManageCartView.as_view(),name='manage_cart'),
    path('empty-cart/',EmptyCartView.as_view(),name='empty_cart'),
    
    # check out url
    path('check-out/',CheckOutView.as_view(),name='check_out'),
    
    # payments methods with khalti url
    # path("khalti-request/", KhaltiRequestView.as_view(), name="khalti_request"),
    # path("khalti-verify/", KhaltiVerifyView.as_view(), name="khalti_verify"),
    
    # # payments methods with esewa url
    # path('esewa-request/',EsewaRequestView.as_view(), name="esewa_request"),
    # path('esewa-verify/',EsewaVerifyView.as_view(), name="esewa_verify"),
    
    # # payment
    # path('paypal/',Payment.as_view(),name='paypal_request'),
   
    # customers urls
    path('customer-register/',CustomerRegisterView.as_view(),name='customer_register'),
    path('customer-login/',CustomerLoginView.as_view(),name='customer_login'),
    path('customer-logout/',CustomerLogoutView.as_view(),name='customer_logout'),
    path('customer-profile/',CustomerProfileView.as_view(),name='customer_profile'),
    path('customer-edit-profile/<int:pk>',UpdateProfileView.as_view(),name='customer_edit_profile'),
    path('profile/order-<int:pk>/',CustomerOrderDetailView.as_view(),name='customer_order_detail'),
    
    # passwords urls
    path('forgot-password/',ForgotPasswordView.as_view(),name="forgot_password"),
    path('reset-password/<email>/<token>/',ResetPasswordView.as_view(),name="reset_password"),
    
    # Admins urls 
    path("admin-login/", AdminLoginView.as_view(), name="admin_login"),
    path("admin-home/", AdminHomeView.as_view(), name="admin_home"),
    path("admin-order/<int:pk>/", AdminOrderDetailView.as_view(), name="admin_order_detail"),
    path("admin-all-orders/", AdminAllOrderView.as_view(), name="admin_all_order"),
    path("admin-order-<int:pk>-change/", AdminOrderStatusChangeView.as_view(), name="admin_order_status_change"),
    path("admin-product/list/",AdminProductList.as_view(), name="admin_product_list"),
    path("admin-product/add/",AdminProductAdd.as_view(), name="admin_add_product"),
    path('admin-edit-product/<int:pk>/',UpdateAdminProduct.as_view(),name='admin_edit_product'),
    path("admin-category/list/",AdminCategoryList.as_view(), name="admin_category_list"),
    path("admin-category/add/",AdminCategoryAdd.as_view(), name="admin_add_category"),
    path('admin-product/delete/<int:id>',dell,name='admin_delete_product'),
    
    # filter by search urls 
    path("search/", SearchView.as_view(), name="search"),
    
    # Api URLS....
    
    # Admins Api url
    path('api/admin-list/',api.AdminListApi.as_view(), name='api_admin_list'),
    path('api/admin-detail/<int:pk>',api.AdminDetailApi.as_view(), name='api_admin_detail'),
    path('api/admin-filter/<str:kw>',api.AdminFilterApi.as_view(), name='api_admin_filter'),
    
    # customers Api url
    path('api/customer-list/',api.CustomersListApi.as_view(), name='api_cutomer_list'),
    path('api/customer-detail/<int:pk>',api.CustomerDetailApi.as_view(), name='api_cutomer_detail'),
    path('api/customer-filter/<str:kw>',api.CustomerFilterApi.as_view(), name='api_cutomer_filter'),
    
    # category Api url
    path("api/category-list/", api.CategoryListApi.as_view(), name="api_category_list"),
    path("api/category-detail/<int:pk>", api.CategoryDetailApi.as_view(), name="api_category_detail"),
    path("api/category-filter/<str:kw>", api.CategoryFilterApi.as_view(), name="api_category_filter"),
    
    # products Api url
    path('api/product-list/',api.ProductsListAPI.as_view(), name='api_products_list'),
    path('api/product-detail/<int:pk>',api.ProductDetailApi.as_view(), name='api_products_list'),
    path('api/product-filter/<str:kw>',api.ProductFilterApi.as_view(), name='api_products_filter'),
   
    # order Api url
    path('api/order-list/',api.OrdersListApi.as_view(), name='api_all_orders'),
    path('api/order-detail/<int:pk>',api.OrderDetailApi.as_view(), name='api_order_detail'),
    path('api/order-filter/<str:kw>',api.OrdersFilterApi.as_view(), name='api_order_filter'),
    
    # cats Api url
    path('api/cart-list/',api.CartListApi.as_view(), name='api_cart_list'),
    path('api/cart-detail/<int:pk>',api.CartDetailApi.as_view(), name='api_cart_detail'),
]