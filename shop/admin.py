

# Register your models here.
from django.contrib import admin
from .models import Category, Product
from .models import Cart

admin.site.register(Category)
admin.site.register(Product)


admin.site.register(Cart)