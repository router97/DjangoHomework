from django.db import models
from django.core.validators import MinValueValidator

from ..catalog.models import Product


class Cart(models.Model):
    """
    Represents a shopping cart.

    Each cart is associated with a user and contains multiple products.
    """
    
    user = models.OneToOneField(
        to='auth.User', 
        on_delete=models.CASCADE, 
        verbose_name='User', 
        primary_key=True, 
        help_text='User this cart belongs to.'
    )
    created_at = models.DateTimeField(
        verbose_name='Created at', 
        auto_now_add=True, 
        help_text='Time when cart was created.', 
    )
    updated_at = models.DateTimeField(
        verbose_name='Updated at', 
        auto_now=True, 
        help_text='Time when cart was last updated.', 
    )
    
    class Meta:
        verbose_name = 'Cart'
        verbose_name_plural = 'Carts'
        ordering = ['updated_at']
    
    def clear_cart(self) -> None:
        """Clear the cart."""
        self.products.all().delete()
    
    def get_total_quantity(self) -> int:
        """Get the total quantity of all products in the cart."""
        return self.products.aggregate(result=models.Sum('quantity')).get('result', 0)
    
    def get_total_price(self) -> float:
        """Calculate total price of all cart products combined considering their quantity."""
        return self.products.aggregate(total_price=models.Sum(models.F('product__price') * models.F('quantity'))).get('total_price', 0)
    
    def __str__(self) -> str:
        return f"{self.user}'s cart"

class CartProduct(models.Model):
    """
    Represents a product in a shopping cart.

    Each CartProduct instance is associated with a cart and a product, adding a quantity parameter.
    """
    
    cart = models.ForeignKey(
        to=Cart,
        on_delete=models.CASCADE,
        verbose_name='Cart',
        related_name='products',
        help_text='The cart associated with this instance.'
    )
    product = models.ForeignKey(
        to=Product,
        on_delete=models.CASCADE, 
        verbose_name='Product', 
        help_text='The product assosiated with this instance.',
    )
    quantity = models.PositiveIntegerField(
        verbose_name='Quantity', 
        editable=True, 
        help_text='Quantity of the product in its cart.', 
        default=1, 
        validators=[MinValueValidator(1)], 
    )
    
    class Meta:
        verbose_name = 'Cart product'
        verbose_name_plural = 'Cart products'
        ordering = ['cart', 'product']
        unique_together = ['cart', 'product']

    def get_total_price(self) -> float:
        """Calculate the price of this product, considering it's quantity"""
        return self.product.price * self.quantity
    
    def __str__(self) -> str:
        return f'{self.cart.user.username} -> {self.product.name}'