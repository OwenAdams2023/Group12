from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, SetPasswordForm
from django.core.validators import MinValueValidator
from django.db.models.functions import Lower
from django import forms
from .models import Product, ShippingAddress, ReturnRequest, UserProfile, Order, Category

class SignUpForm(UserCreationForm):
	email = forms.EmailField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Email Address'}))
	first_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'First Name'}))
	last_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Last Name'}))
	#account_type = forms.ChoiceField(label="", choices=(('buyer', 'Buyer'), ('seller', 'Seller')), widget=forms.Select(attrs={'class': 'form-control'}))

	class Meta:
		model = User
		fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

	def __init__(self, *args, **kwargs):
		super(SignUpForm, self).__init__(*args, **kwargs)

		self.fields['username'].widget.attrs['class'] = 'form-control'
		self.fields['username'].widget.attrs['placeholder'] = 'User Name'
		self.fields['username'].label = ''
		self.fields['username'].help_text = '<span class="form-text text-muted"><small>Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.</small></span>'

		self.fields['password1'].widget.attrs['class'] = 'form-control'
		self.fields['password1'].widget.attrs['placeholder'] = 'Password'
		self.fields['password1'].label = ''
		self.fields['password1'].help_text = '<ul class="form-text text-muted small"><li>Your password can\'t be too similar to your other personal information.</li><li>Your password must contain at least 8 characters.</li><li>Your password can\'t be a commonly used password.</li><li>Your password can\'t be entirely numeric.</li></ul>'

		self.fields['password2'].widget.attrs['class'] = 'form-control'
		self.fields['password2'].widget.attrs['placeholder'] = 'Confirm Password'
		self.fields['password2'].label = ''
		self.fields['password2'].help_text = '<span class="form-text text-muted"><small>Enter the same password as before, for verification.</small></span>'

#needs changes and testing
class ProductForm(forms.ModelForm):

	name = forms.CharField(label="", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Product Name'}), required=True)
	price = forms.DecimalField(label="", widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Price'}), required=True)
	quantity = forms.IntegerField(label="", widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Quantity'}), required=True)
	category = forms.ModelChoiceField(label="", queryset=Category.objects.all().order_by(Lower('product_type')), widget=forms.Select(attrs={'class': 'form-control', 'placeholder': 'Category'}), required=True)
	brand = forms.CharField(label="", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Brand'}), required=True)
	image = forms.ImageField(label="", widget=forms.FileInput(attrs={'class': 'form-control-file'}), required=True)
	description = forms.CharField(label="", widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Description'}), required=True)
	
	class Meta:
		model = Product
		fields = ('name', 'price', 'quantity', 'category', 'brand', 'image', 'description')

		exclude = ('seller', )


#need to complete
"""
class ShippingForm(forms.ModelForm):

	class Meta:
		model = ShippingAddress
		fields = ('shipping_full_name', 'shipping_email', 'shipping_address1', 'shipping_address2', 'shipping_city', 'shipping_state', 'shipping_zipcode', 'shipping_country')

		exclude = ('user', )"""

class ShippingAddressForm(forms.ModelForm):
    class Meta:
        model = ShippingAddress
        fields = ('shipping_full_name', 'shipping_email', 'shipping_address1', 'shipping_address2', 'shipping_city', 'shipping_state', 'shipping_zipcode', 'shipping_country')

    def __init__(self, *args, **kwargs):
        super(ShippingAddressForm, self).__init__(*args, **kwargs)
        self.fields['user'].widget = forms.HiddenInput()  # Assuming you don't want the user to modify this field
        
        # Conditionally set fields as required
        if self.instance and self.instance.user:
            self.fields['shipping_email'].required = True
            self.fields['shipping_address1'].required = True
            self.fields['shipping_city'].required = True
            self.fields['shipping_state'].required = True
            self.fields['shipping_zipcode'].required = True
            self.fields['shipping_country'].required = True

"""
class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['full_name', 'email', 'shipping_address', 'billing_address',]

    def __init__(self, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)
        #self.fields['product'].widget.attrs['readonly'] = True  # Assuming product should not be editable in the form
        self.fields['shipping_address'].required = True
        self.fields['billing_address'].required = True
        self.fields['card_number'].required = True
        self.fields['cvv'].required = True
        self.fields['expiration'].required = True"""
	    
class ReturnForm(forms.ModelForm):
    class Meta:
        model = ReturnRequest
        fields = ['reason']


class UpdateUserInfoForm(forms.ModelForm):
	phone = forms.CharField(label = "", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Phone'}), required=False)
	address1 = forms.CharField(label = "", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Address 1'}), required=False)
	address2 = forms.CharField(label = "", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Address 2'}), required=False)
	city = forms.CharField(label = "", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':'City'}), required=False)
	state = forms.CharField(label = "", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':'State'}), required=False)
	zipcode = forms.CharField(label = "", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Zipcode'}), required=False)
	country = forms.CharField(label = "", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Country'}), required=False)

	class Meta:
		model = UserProfile
		fields = ('phone', 'address1', 'address2', 'city', 'state', 'zipcode', 'country')

class UpdateProductInfoForm(forms.ModelForm):
	name = forms.CharField(label = "", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Name'}), required=False)
	price = forms.DecimalField(label = "", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Price'}), required=False)
	quantity = forms.IntegerField(label = "", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Quanity'}), required=False)
	brand = forms.CharField(label = "", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Brand'}), required=False)
	description = forms.CharField(label = "", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Description'}), required=False)
	#image = forms.ImageField(label = "", widget=forms.FileInput(attrs={'class': 'form-control-file', 'placeholder':'Image'}), required=False)

	class Meta:
		model = Product
		fields = ('name', 'price', 'quantity', 'brand', 'description')

class UpdatePasswordForm(SetPasswordForm):
	class Meta:
		model = User
		fields = ['new_password1', 'new_password2']

	def __init__(self, *args, **kwargs):
		super(UpdatePasswordForm, self).__init__(*args, **kwargs)


		self.fields['new_password1'].widget.attrs['class'] = 'form-control'
		self.fields['new_password1'].widget.attrs['placeholder'] = 'Password'
		self.fields['new_password1'].label = ''
		self.fields['new_password1'].help_text = '<ul class="form-text text-muted small"><li>Your password can\'t be too similar to your other personal information.</li><li>Your password must contain at least 8 characters.</li><li>Your password can\'t be a commonly used password.</li><li>Your password can\'t be entirely numeric.</li></ul>'

		self.fields['new_password2'].widget.attrs['class'] = 'form-control'
		self.fields['new_password2'].widget.attrs['placeholder'] = 'Confirm Password'
		self.fields['new_password2'].label = ''
		self.fields['new_password2'].help_text = '<span class="form-text text-muted"><small>Enter the same password as before, for verification.</small></span>'


class UpdateUserForm(UserChangeForm):
	password = None #Hiding password update

	#Everything else for the update account info
	email = forms.EmailField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Email Address'}), required=False)
	first_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'First Name'}), required=False)
	last_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Last Name'}), required=False)
	#account_type = forms.ChoiceField(label="", choices=(('buyer', 'Buyer'), ('seller', 'Seller')), widget=forms.Select(attrs={'class': 'form-control'}))

	class Meta:
		model = User
		fields = ('username', 'first_name', 'last_name', 'email')

	def __init__(self, *args, **kwargs):
		super(UpdateUserForm, self).__init__(*args, **kwargs)

		self.fields['username'].widget.attrs['class'] = 'form-control'
		self.fields['username'].widget.attrs['placeholder'] = 'User Name'
		self.fields['username'].label = ''
		self.fields['username'].help_text = '<span class="form-text text-muted"><small>Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.</small></span>'