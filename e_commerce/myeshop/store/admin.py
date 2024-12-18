from django.contrib import admin
from .models import Product
from django.contrib.auth.models import User

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'stock', 'created_at')
    search_fields = ['name']  # Listeye çevrildi


def save_model(self, request, obj, form, change):
        if not obj.user:
            obj.user = request.user  # Ürünü ekleyen kullanıcıyı kaydet
        super().save_model(request, obj, form, change)