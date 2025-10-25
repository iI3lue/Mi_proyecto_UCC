#crud_app /forms.py
from django import forms
from .models import Producto

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre', 'descripcion', 'precio', 'marca', 'categoria', 'especificaciones', 'stock', 'imagen']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'precio': forms.NumberInput(attrs={'class': 'form-control'}),
            'marca': forms.TextInput(attrs={'class': 'form-control'}),
            'categoria': forms.TextInput(attrs={'class': 'form-control'}),
            'especificaciones': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'stock': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class CheckoutForm(forms.Form):
    direccion = forms.CharField(label='Dirección de envío', max_length=200, widget=forms.TextInput(attrs={'class': 'form-control'}))
    telefono = forms.CharField(label='Teléfono de contacto', max_length=20, widget=forms.TextInput(attrs={'class': 'form-control'}))