from django.contrib import admin
from .models import Artesano, Artesania

@admin.register(Artesano)
class ArtesanoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'email', 'telefono', 'fecha_registro')
    search_fields = ('nombre', 'email')
    list_filter = ('fecha_registro',)

@admin.register(Artesania)
class ArtesaniaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'artesano', 'precio', 'disponible', 'fecha_creacion')
    list_filter = ('disponible', 'fecha_creacion')
    search_fields = ('nombre', 'descripcion')
