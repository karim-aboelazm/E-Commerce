from django import forms
from ecommerce.models import Order,Customer,Products,Category
from django.contrib.auth.models import User

class CheckOutForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = [
            'ordered_by',
            'shopping_address',
            'phone_num',
            'email',
            'payment_method'
        ]
   
class CustomerRegisterForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput())
    email = forms.CharField(widget=forms.EmailInput())
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = Customer
        fields = [
            'username',
            'full_name',
            'email',
            'password',
            'address'
        ]
    def clean_username(self):
        user_name = self.cleaned_data["username"]
        if User.objects.filter(username=user_name).exists():
            raise forms.ValidationError("Customer with this username already exists.")
        return user_name

class CustomerLoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput())
    password = forms.CharField(widget=forms.PasswordInput())
    
    def clean_username(self):
        user_name = self.cleaned_data["username"]
        if User.objects.filter(username=user_name).exists():
           pass
        else:
            raise forms.ValidationError('Customer with this username is not exists.')
        return user_name
             
class AdminLoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput())
    password = forms.CharField(widget=forms.PasswordInput())
    
class ProductForm(forms.ModelForm):
    more_images = forms.FileField(required=False,widget=forms.FileInput(attrs={
        "class":"form-control",
        "multiple":True,
        
    }))
    class Meta:
        model = Products
        fields=['title','title_ar','category','image','price','discount','description','description_ar','warranty','return_policy']
        widgets = {
            "title" : forms.TextInput(attrs={
                "class":"form-control",
                "placeholder":"Enter product title here .."
            }),
            
            "image" : forms.ClearableFileInput(attrs={
                "class":"form-control",
            }),
            
            "category" : forms.Select(attrs={
                "class":"form-control",
                "placeholder":"Enter product category here .."
            }),
            
            "price" : forms.NumberInput(attrs={
                "class":"form-control",
                "placeholder":"Enter product price here .."
            }),
            
            "discount" : forms.NumberInput(attrs={
                "class":"form-control",
                "placeholder":"Enter product discount here .."
            }),
            
            "description" : forms.Textarea(attrs={
                "class":"form-control",
                "placeholder":"Enter product description here ..",
                "row":5
            }),
            
            "warranty" : forms.TextInput(attrs={
                "class":"form-control",
                "placeholder":"Enter product warranty here .."
            }),
            
            "return_policy" : forms.TextInput(attrs={
                "class":"form-control",
                "placeholder":"Enter product return_policy here .."
            }),
            
        }

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['title']

class PasswordForm(forms.Form):
    email = forms.CharField(widget=forms.EmailInput(attrs={
        "class":"form-control",
        "placeholder":"Enter Your Email here..."
    })) 
    
    def clean_email(self):
        e = self.cleaned_data.get("email")
        if Customer.objects.filter(user__email=e).exists():
            pass
        else:
            raise forms.ValidationError("Customer with this account does not exists ....")
        return e

class PasswordResetForm(forms.Form):
    new_password = forms.CharField(widget=forms.PasswordInput(attrs={
        "class":"form-control",
        "autocomplete" : "new-password",
        "placeholder":"Enter your new password here.."
    }),label = "New Password")
    
    confirm_new_password = forms.CharField(widget=forms.PasswordInput(attrs={
        "class":"form-control",
        "autocomplete" : "new-password",
        "placeholder":"Confirm your new password here.."
    }),label = "Confirm New Password")
    
    def clean_confirm_new_password(self):
        new_password = self.cleaned_data.get('new_password')
        confirm_new_password = self.cleaned_data.get('confirm_new_password')
        if new_password != confirm_new_password:
            raise forms.ValidationError('New passwords did not match !')
        return confirm_new_password
    
class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['full_name','address','image','phone']
                    