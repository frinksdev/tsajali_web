from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from .models import Artesano, Artesania
from .forms import RegistroArtesanoForm, ArtesaniaForm

def index(request):
    ultimos_artesanos = Artesano.objects.all().order_by('-fecha_registro')[:6]
    return render(request, 'app_artesanos/index.html', {
        'ultimos_artesanos': ultimos_artesanos
    })

def registro_artesano(request):
    if request.method == 'POST':
        form = RegistroArtesanoForm(request.POST)
        if form.is_valid():
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
                email=form.cleaned_data['email']
            )
            # Autenticar y loguear
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
    artesania = get_object_or_404(Artesania, pk=pk, artesano__usuario=request.user)
    if request.method == 'POST':
        form = ArtesaniaForm(request.POST, request.FILES, instance=artesania)
        if form.is_valid():
            form.save()
            messages.success(request, '¡Artesanía actualizada exitosamente!')
            return redirect('perfil_artesano')
    else:
        form = ArtesaniaForm(instance=artesania)
    return render(request, 'app_artesanos/editar_artesania.html', {'form': form})

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
