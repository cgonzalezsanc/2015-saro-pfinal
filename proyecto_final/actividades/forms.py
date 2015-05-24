# -*- coding: utf-8 -*-

from django import forms


# Formulario para hacer login
class LoginForm(forms.Form):
    username = forms.CharField(max_length=15,
                        widget=forms.TextInput(attrs={'size': '10'}))
    password = forms.CharField(max_length=15,
                        widget=forms.PasswordInput(attrs={'size': '10'}))

elecciones_filtrar = (
    ('titulo', 'Titulo'),
    ('fecha', 'Fecha (dia/mes/año)'),
    ('precio', 'Precio (en euros)'),
    ('duracion', 'Duracion (horas:min:seg)'),
)


# Formulario para filtrar actividades
class FiltroForm(forms.Form):
    Filtro = forms.ChoiceField(choices=elecciones_filtrar)
    Valor = forms.CharField(max_length=40)


elecciones_perfil = (
    ('d', 'default'),
    ('w', 'blanco'),
    ('y', 'amarillo'),
    ('r', 'rojo'),
    ('b', 'azul'),
    ('g', 'verde'),
)


# Formulario para cambiar el título y el color de fondo de un usuario
class PerfilForm(forms.Form):
    Titulo = forms.CharField(max_length=100,
                             widget=forms.TextInput(attrs={'size': '10'}))
    Color_Fondo = forms.ChoiceField(choices=elecciones_perfil)
