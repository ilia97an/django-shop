from django.contrib import admin

from .models import Manufacturer, GPU, CPU, Product, CartItem, ProductImage, ProductRating

admin.site.register(Manufacturer)
admin.site.register(GPU)
admin.site.register(CPU)
admin.site.register(Product)
admin.site.register(CartItem)
admin.site.register(ProductImage)

# Register your models here.

#class CartAdmin(admin.ModelAdmin):
#  pass

#class CartItemAdmin(admin.ModelAdmin):
#  pass

