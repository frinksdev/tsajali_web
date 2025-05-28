from django.urls import path
from . import views

app_name = 'app_artesanos'

urlpatterns = [
    path('', views.index, name='index'),
    path('catalogo/', views.catalogo_artesanos, name='catalogo_artesanos'),
    path('artesano/<int:pk>/', views.detalle_artesano, name='detalle_artesano'),
    path('registro/', views.registro_artesano, name='registro_artesano'),
    path('perfil/', views.perfil_artesano, name='perfil_artesano'),
    path('perfil/editar/', views.editar_perfil, name='editar_perfil'),
    path('agregar-artesania/', views.agregar_artesania, name='agregar_artesania'),
    path('editar-artesania/<int:pk>/', views.editar_artesania, name='editar_artesania'),
    path('eliminar-artesania/<int:pk>/', views.eliminar_artesania, name='eliminar_artesania'),
    path('carrito/', views.ver_carrito, name='ver_carrito'),
    path('carrito/agregar/<int:artesania_id>/', views.agregar_al_carrito, name='agregar_al_carrito'),
    path('carrito/actualizar/<int:item_id>/', views.actualizar_cantidad, name='actualizar_cantidad'),
    path('carrito/eliminar/<int:item_id>/', views.eliminar_del_carrito, name='eliminar_del_carrito'),
] 