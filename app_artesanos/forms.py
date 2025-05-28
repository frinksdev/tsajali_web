from django import forms
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from .models import Artesano, Artesania

class RegistroArtesanoForm(forms.ModelForm):
    username = forms.CharField(
        max_length=150,
        label='Nombre de usuario',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre de usuario'}),
        help_text='Elige un nombre de usuario único.'
    )
    password1 = forms.CharField(
        label='Contraseña',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Contraseña'}),
        help_text='La contraseña debe tener al menos 8 caracteres.'
    )
    password2 = forms.CharField(
        label='Confirmar contraseña',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Repite la contraseña'}),
        help_text='Repite la contraseña para verificar.'
    )
    nombre = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingresa tu nombre completo'}),
        help_text='Ingresa tu nombre completo como aparecerá en tu perfil'
    )
    direccion = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Ingresa tu dirección completa'}),
        help_text='Incluye calle, número, colonia, ciudad y estado'
    )
    telefono = forms.CharField(
        max_length=15,
        validators=[RegexValidator(regex=r'^\+?1?\d{9,15}$', message='El número de teléfono debe estar en formato: +999999999')],
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+52 999 999 9999'}),
        help_text='Ingresa tu número con código de país y área'
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'ejemplo@correo.com'}),
        help_text='Usaremos este correo para contactarte'
    )

    class Meta:
        model = Artesano
        fields = ['username', 'password1', 'password2', 'nombre', 'direccion', 'telefono', 'email']

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('Este nombre de usuario ya está en uso.')
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists() or Artesano.objects.filter(email=email).exists():
            raise forms.ValidationError('Este correo electrónico ya está registrado.')
        return email

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            self.add_error('password2', 'Las contraseñas no coinciden.')
        return cleaned_data

class ArtesaniaForm(forms.ModelForm):
    class Meta:
        model = Artesania
        fields = ['nombre', 'descripcion', 'precio', 'foto']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre de la artesanía'
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Describe tu artesanía, materiales, técnicas utilizadas, etc.'
            }),
            'precio': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '0.00',
                'min': '0',
                'step': '0.01'
            }),
            'foto': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
        }
        help_texts = {
            'nombre': 'Ingresa un nombre descriptivo para tu artesanía',
            'descripcion': 'Describe los detalles de tu artesanía, incluyendo materiales y técnicas',
            'precio': 'Ingresa el precio en pesos mexicanos',
            'foto': 'Sube una foto de alta calidad de tu artesanía'
        }

    def clean_precio(self):
        precio = self.cleaned_data.get('precio')
        if precio <= 0:
            raise forms.ValidationError('El precio debe ser mayor a 0')
        return precio

    def clean_foto(self):
        foto = self.cleaned_data.get('foto')
        if foto:
            if foto.size > 5 * 1024 * 1024:  # 5MB
                raise forms.ValidationError('La imagen no debe superar los 5MB')
        return foto

class EditarPerfilArtesanoForm(forms.ModelForm):
    class Meta:
        model = Artesano
        fields = ['nombre', 'direccion', 'telefono', 'email']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingresa tu nombre completo'}),
            'direccion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Ingresa tu dirección completa'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+52 999 999 9999'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'ejemplo@correo.com'}),
        } 