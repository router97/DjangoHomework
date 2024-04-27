from typing import Any
from uuid import UUID

from django import forms

from .models import Cart, CartProduct
from ..catalog.models import Product


class CartAddProductForm(forms.ModelForm):
    class Meta:
        model = CartProduct
        fields = ('cart', 'product', 'quantity')
        
    def clean(self) -> dict[str, Any]:
        cleaned_data = super().clean()
        print(f'CLEANED DATA: {cleaned_data}')
        product = cleaned_data.get('product')
        print(f'TYPE OF PRODUCT FROM FORM "{type(product)}"')
        quantity: int = cleaned_data.get('quantity')
        
        if product.quantity < quantity:
            raise forms.ValidationError('Not enough product in store')
        
        return cleaned_data