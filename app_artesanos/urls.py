from django.urls import path
from . import views

app_name = 'app_artesanos'

urlpatterns = [
    path('', views.index, name='index'),
    path('catalogo/', views.catalogo_artesanos, name='catalogo_artesanos'),
    path('artesano/<int:pk>/', views.detalle_artesano, name='detalle_artesano'),
    path('registro/', views.registro_artesano, name='registro_artesano'),
    path('perfil/', views.perfil_artesano, name='perfil_artesano'),
    path('agregar-artesania/', views.agregar_artesania, name='agregar_artesania'),
    path('editar-artesania/<int:pk>/', views.editar_artesania, name='editar_artesania'),
] 