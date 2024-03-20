from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import Product, ShippingAddress, Order, ShippingAddress, ReturnRequest

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

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['product', 'quantity', 'address', 'phone',]

    def __init__(self, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)
        self.fields['product'].widget.attrs['readonly'] = True  # Assuming product should not be editable in the form
        self.fields['address'].required = True
        self.fields['phone'].required = True
        self.fields['card_number'].required = True
        self.fields['cvv'].required = True
        self.fields['expiration'].required = True
	    
class ReturnForm(forms.ModelForm):
    class Meta:
        model = ReturnRequest
        fields = ['reason']
