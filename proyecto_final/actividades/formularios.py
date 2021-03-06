# -*- coding: utf-8 -*-

from forms import FiltroForm, PerfilForm


# Crea un formulario para actualizar las actividades
def ActuActividadesForm():
    salida = '\n\t<FORM action="/todas" name = "actualizaractsform" '
    salida += 'method="POST" accept-charset="UTF-8">\n\t\t'
    salida += '<input type="hidden" name="tipo" value="actualizaracts" />'
    salida += '<input type="submit" value="Actualizar actividades">\n\t'
    salida += '</form><br>'
    return salida


# Formulario de eleccion de actividad
def ElegirActForm(nombre_usuario, id_actividad):
    salida = '\n\t<FORM action="/' + nombre_usuario + '" name="elegiractform" '
    salida += 'method="POST" accept-charset="UTF-8">\n\t\t'
    salida += '<input type="hidden" name="tipo" value="elegiract" />'
    salida += '<input type="hidden" name="idactividad" value="'
    salida += str(id_actividad) + '" />'
    salida += '\n\t\t<input type="submit" value="Elegir">\n\t</form><br>'
    return salida


# Formulario para filtrar actividades
def FormFiltrar():
    salida = '\n\t<FORM action="/todas" name="formfiltrar" '
    salida += 'method="POST" accept-charset="UTF-8">\n\t\t<fieldset>\t'
    salida += '<legend>Filtrar actividades</legend>'
    salida += '<input type="hidden" name="tipo" value="filtrar" />'
    salida += FiltroForm().as_p()
    salida += '\n\t\t\t<input type="submit" value="Filtrar">\n\t\t</fieldset>'
    salida += '\n\t</form><br>'
    return salida


# Formulario para cambiar los datos del perfil
def CambiarPerfilForm(nombre_usuario):
    salida = '\n\t<FORM action="/' + nombre_usuario + '" name="perfilform" '
    salida += 'method="POST" accept-charset="UTF-8">\n\t\t'
    salida += '<input type="hidden" name="tipo" value="cambiarperfil" />'
    salida += PerfilForm().as_p()
    salida += '\n\t\t<input type="submit" value="Cambiar">\n\t</form><br>'
    return salida


# Formulario para escribir un comentario
def ComentarioForm(nombre_usuario, id_actividad):
    salida = '\n\t<FORM action="/actividad/' + str(id_actividad) + '" name='
    salida += '"elegiractform" method="POST" accept-charset="UTF-8">\n\t\t'
    salida += '<input type="hidden" name="tipo" value="comentario" />'
    salida += '<input type="hidden" name="usuario" value="' + nombre_usuario
    salida += '" />'
    salida += '<textarea name="message" rows="10" cols="30" '
    salida += 'placeholder="Introduce tu comentario"></textarea>'
    salida += '\n\t\t<input type="submit" value="Comentar">\n\t</form><br>'
    return salida
