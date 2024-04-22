from django.db import models


class Cart(models.Model):
    user = models.ForeignKey(
        to='auth.User', 
        on_delete=models.CASCADE, 
        verbose_name='User',
        help_text='Owner of the cart.'
    )
    
    product = models.ForeignKey(
        to='catalog.Product', 
        on_delete=models.CASCADE, 
        verbose_name='Product',
        help_text='Cart product.',
    )
    
    quantity = models.PositiveIntegerField(
        verbose_name='Quantity',
        help_text='Quantity of product.',
    )
    
    def __str__(self):
        return f'{self.product.name} - {self.quantity}'
    
    class Meta:
        verbose_name = 'Cart'
        verbose_name_plural = 'Carts'
        ordering = ('id',)
        unique_together = ('user', 'product')
    
    def total_price(self):
        return self.product.price * self.quantity