from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from .models import Artesano, Artesania
from .forms import RegistroArtesanoForm, ArtesaniaForm, EditarPerfilArtesanoForm
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderUnavailable

def index(request):
    ultimos_artesanos = Artesano.objects.all().order_by('-fecha_registro')[:6]
    return render(request, 'app_artesanos/index.html', {
        'ultimos_artesanos': ultimos_artesanos
    })

def registro_artesano(request):
    if request.method == 'POST':
        form = RegistroArtesanoForm(request.POST)
        if form.is_valid():
            try:
                # Geocodificar la dirección
                geolocator = Nominatim(user_agent="tsajali_app")
                direccion_completa = f"{form.cleaned_data['direccion']}, Veracruz, México"
                location = geolocator.geocode(direccion_completa)
                
                # Crear usuario
                user = User.objects.create_user(
                    username=form.cleaned_data['username'],
                    password=form.cleaned_data['password1'],
                    email=form.cleaned_data['email']
                )
                
                # Crear artesano asociado
                artesano = Artesano.objects.create(
                    usuario=user,
                    nombre=form.cleaned_data['nombre'],
                    direccion=form.cleaned_data['direccion'],
                    telefono=form.cleaned_data['telefono'],
                    email=form.cleaned_data['email'],
                    latitud=location.latitude if location else None,
                    longitud=location.longitude if location else None
                )
                
                # Autenticar y loguear
                user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password1'])
                if user is not None:
                    login(request, user)
                    messages.success(request, '¡Registro exitoso!')
                    return redirect('app_artesanos:perfil_artesano')
            except (GeocoderTimedOut, GeocoderUnavailable) as e:
                messages.warning(request, 'No se pudo obtener la ubicación exacta. Por favor, verifica tu dirección.')
                # Crear el usuario y artesano sin coordenadas
                user = User.objects.create_user(
                    username=form.cleaned_data['username'],
                    password=form.cleaned_data['password1'],
                    email=form.cleaned_data['email']
                )
                artesano = Artesano.objects.create(
                    usuario=user,
                    nombre=form.cleaned_data['nombre'],
                    direccion=form.cleaned_data['direccion'],
                    telefono=form.cleaned_data['telefono'],
                    email=form.cleaned_data['email']
                )
                user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password1'])
                if user is not None:
                    login(request, user)
                    messages.success(request, '¡Registro exitoso!')
                    return redirect('app_artesanos:perfil_artesano')
    else:
        form = RegistroArtesanoForm()
    return render(request, 'app_artesanos/registro_artesano.html', {'form': form})

@login_required
def perfil_artesano(request):
    try:
        artesano = Artesano.objects.get(usuario=request.user)
        artesanias = artesano.artesanias.all()
        return render(request, 'app_artesanos/perfil_artesano.html', {
            'artesano': artesano,
            'artesanias': artesanias
        })
    except Artesano.DoesNotExist:
        return redirect('registro_artesano')

@login_required
def agregar_artesania(request):
    if request.method == 'POST':
        form = ArtesaniaForm(request.POST, request.FILES)
        if form.is_valid():
            artesania = form.save(commit=False)
            artesania.artesano = request.user.artesano
            artesania.save()
            messages.success(request, '¡Artesanía agregada exitosamente!')
            return redirect('app_artesanos:perfil_artesano')
    else:
        form = ArtesaniaForm()
    return render(request, 'app_artesanos/agregar_artesania.html', {'form': form})

@login_required
def editar_artesania(request, pk):
    try:
        artesania = get_object_or_404(Artesania, pk=pk, artesano__usuario=request.user)
        if request.method == 'POST':
            form = ArtesaniaForm(request.POST, request.FILES, instance=artesania)
            if form.is_valid():
                form.save()
                messages.success(request, '¡Artesanía actualizada exitosamente!')
                return redirect('app_artesanos:perfil_artesano')
            else:
                messages.error(request, 'Por favor, corrige los errores en el formulario.')
        else:
            form = ArtesaniaForm(instance=artesania)
        return render(request, 'app_artesanos/agregar_artesania.html', {
            'form': form,
            'artesania': artesania
        })
    except Exception as e:
        messages.error(request, 'Ocurrió un error al editar la artesanía. Por favor, intenta de nuevo.')
        return redirect('app_artesanos:perfil_artesano')

@login_required
def eliminar_artesania(request, pk):
    try:
        artesania = get_object_or_404(Artesania, pk=pk, artesano__usuario=request.user)
        if request.method == 'POST':
            artesania.delete()
            messages.success(request, '¡Artesanía eliminada exitosamente!')
            return redirect('app_artesanos:perfil_artesano')
        return render(request, 'app_artesanos/eliminar_artesania.html', {
            'artesania': artesania
        })
    except Exception as e:
        messages.error(request, 'Ocurrió un error al eliminar la artesanía. Por favor, intenta de nuevo.')
        return redirect('app_artesanos:perfil_artesano')

def catalogo_artesanos(request):
    artesanos_list = Artesano.objects.all().order_by('nombre')
    paginator = Paginator(artesanos_list, 9)  # 9 artesanos por página
    page = request.GET.get('page')
    artesanos = paginator.get_page(page)
    return render(request, 'app_artesanos/catalogo_artesanos.html', {
        'artesanos': artesanos
    })

def detalle_artesano(request, pk):
    artesano = get_object_or_404(Artesano, pk=pk)
    artesanias = artesano.artesanias.filter(disponible=True)
    return render(request, 'app_artesanos/detalle_artesano.html', {
        'artesano': artesano,
        'artesanias': artesanias
    })

@login_required
def editar_perfil(request):
    try:
        artesano = Artesano.objects.get(usuario=request.user)
        if request.method == 'POST':
            form = EditarPerfilArtesanoForm(request.POST, instance=artesano)
            if form.is_valid():
                # Geocodificar la nueva dirección
                try:
                    geolocator = Nominatim(user_agent="tsajali_app")
                    direccion_completa = f"{form.cleaned_data['direccion']}, Veracruz, México"
                    location = geolocator.geocode(direccion_completa)
                    
                    if location:
                        artesano = form.save(commit=False)
                        artesano.latitud = location.latitude
                        artesano.longitud = location.longitude
                        artesano.save()
                        messages.success(request, '¡Perfil actualizado exitosamente!')
                    else:
                        messages.warning(request, 'No se pudo obtener la ubicación exacta. Por favor, verifica tu dirección.')
                        form.save()
                except (GeocoderTimedOut, GeocoderUnavailable) as e:
                    messages.warning(request, 'No se pudo obtener la ubicación exacta. Por favor, verifica tu dirección.')
                    form.save()
                return redirect('app_artesanos:perfil_artesano')
        else:
            form = EditarPerfilArtesanoForm(instance=artesano)
        return render(request, 'app_artesanos/editar_perfil.html', {
            'form': form,
            'artesano': artesano
        })
    except Artesano.DoesNotExist:
        messages.error(request, 'No se encontró el perfil del artesano.')
        return redirect('app_artesanos:perfil_artesano')
