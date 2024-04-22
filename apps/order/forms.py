from django import forms

from .models import Cart


class CartAddProductForm(forms.ModelForm):
    class Meta:
        model = Cart
        fields = ('user', 'product', 'quantity')
        widgets = {
            'user': forms.HiddenInput(), 
            'product': forms.HiddenInput(), 
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 100, 'value': 1})
        }
        
    def clean(self):
        cleaned_data = super().clean()
        product = cleaned_data.get('product')
        quantity = cleaned_data.get('quantity')
        
        if product.quantity < quantity:
            raise forms.ValidationError('Not enough product in store')
        
        return cleaned_data