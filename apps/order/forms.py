from typing import Any

from django import forms

from .models import CartProduct
from ..catalog.models import Product


class CartAddProductForm(forms.ModelForm):
    class Meta:
        model = CartProduct
        fields = ('cart', 'product', 'quantity')
        
    def clean(self) -> dict[str, Any]:
        cleaned_data: dict[str, Any] = super().clean()
        product: Product = cleaned_data.get('product')
        quantity: int = cleaned_data.get('quantity')
        
        if product.quantity < quantity:
            raise forms.ValidationError('Not enough product in store')
        
        return cleaned_data