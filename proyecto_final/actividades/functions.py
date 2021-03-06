# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
from datetime import datetime
from django.contrib.auth.models import User
from django.template import Context, RequestContext
from django.template.loader import get_template
from formularios import ElegirActForm
from forms import LoginForm
from models import Actividad, Usuario, ActividadElegida, ActualizacionEventos
from models import Comentario
import math
import sys
import string
import urllib



# Muestra la información de ayuda
def InfoAyuda():
    contenido = "<p>Esta pagina web aglutina informacion sobre actividades \n"
    contenido += "culturales y de ocio que tienen lugar en el municipio de \n"
    contenido += "Madrid.</p>\n"
    contenido += "<p>Para utilizar la pagina no es necesario disponer de una\n"
    contenido += "cuenta, pero si desea almacenar las actividades que le \n"
    contenido += "interesen sera necesesario que se registre.<p>\n"
    contenido += "<p>Las paginas a las que podra acceder segun la <b>parte\n"
    contenido += "obligatoria</b> son:</p>\n"
    contenido += "<ul>\n"
    contenido += "<li><b>/</b>: Muestra las diez actividades mas proximas en "
    contenido += "el tiempo y la lista de paginas personales</li>\n"
    contenido += "<li><b>/usuario</b>: Pagina personal de un usuario</li>\n"
    contenido += "<li><b>/usuario/rss</b>: Canal RSS de un usuario</li>\n"
    contenido += "<li><b>/actividad/id</b>: Pagina de una actividad</li>\n"
    contenido += "<li><b>/todas</b>: Muestra todas las actividades disponibles"
    contenido += "</li>\n<li><b>/ayuda</b>: Muestra esta pagina de ayuda</li>\n"
    contenido += "</ul>\n<br>\n"
    contenido += "<p>Ademas, de forma opcional se han añadido las siguientes\n"
    contenido += " caracteristicas: </p>"
    contenido += "<ul>\n"
    contenido += "<li>Canal RSS para las actividades mas proximas</li>"
    contenido += "<li>Favicon</li>"
    contenido += "<li>Numero de visitas para cada actividad</li>"
    contenido += "<li>Ranking de actividades segun el numero de visitas</li>"
    contenido += "<li>Historial de actualizaciones de las actividades</li>"
    contenido += "<li>Comentarios para cada actividad</li>"
    contenido += "</ul>\n<br>\n"
    contenido += "<br><p>Esperamos que la pagina les sea de utilidad. "
    contenido += "Muchas gracias por su visita.</p>"
    return contenido


# Muestra el enlace al canal RSS de un usuario
def MostrarRSS(nombre, pag_principal=0):
    salida = "<h2>Canal RSS</h2>"
    if pag_principal == 0:
        salida += "<ul><li><a href=/" + nombre + "/rss>Canal de "
        salida += nombre + "</a></li></ul>"
    else:
        salida += "<ul><li><a href=/rss>Canal RSS de la pagina principal"
        salida += "</a></li></ul>"
    return salida


# Crea un documento RSS para el contenido de la pagina principal
def CanalRSSPrinci(actividades):
    salida = '<?xml version="1.0" encoding="UTF-8"?>\n'
    salida += '<rss version="2.0">\n'
    salida += '<channel>\n\t<title>Canal RSS de las actividades mas proximas'
    salida += '</title>\n\t<link>http://localhost:1234/</link>\n'
    salida += '\t<description>Pagina con las actividades de ocio y cultura'
    salida += ' mas proximas</description>\n\t'
    for actividad in actividades:
        salida += '<item>\n'
        salida += '\t\t<title>' + actividad.titulo + '</title>\n'
        salida += '\t\t<link>http://localhost:1234/actividad/'
        salida += str(actividad.id) + '</link>\n\t\t<description>Fecha: '
        salida += actividad.fecha.strftime('%d-%m-%Y %H:%M')
        salida += '</description>\n\t</item>\n'
    salida += '</channel>\n</rss>'
    return salida


# Crea un documento RSS para el canal de un usuario
def CanalRSS(usuario):
    actividades_el = ActividadElegida.objects.filter(usuario=usuario)
    salida = '<?xml version="1.0" encoding="UTF-8"?>\n'
    salida += '<rss version="2.0">\n'
    salida += '<channel>\n\t<title>Canal RSS del usuario '
    salida += usuario.nombre.username + '</title>\n\t<link>http://localhost:'
    salida += '1234/' + usuario.nombre.username + '</link>\n\t<description>'
    salida += 'Pagina con las actividades de ocio y cultura elegidas por el'
    salida += ' usuario ' + usuario.nombre.username + '</description>\n\t'
    for actividad_el in actividades_el:
        salida += '<item>\n'
        salida += '\t\t<title>' + actividad_el.actividad.titulo + '</title>\n'
        salida += '\t\t<link>http://localhost:1234/actividad/'
        salida += str(actividad_el.actividad.id) + '</link>\n'
        salida += '\t\t<description>Fecha: '
        salida += actividad_el.actividad.fecha.strftime('%d-%m-%Y %H:%M')
        salida += '</description>\n'
        salida += '\t</item>\n'
    salida += '</channel>\n</rss>'
    return salida


# Crea el menú de navegación en función de si es la página principal o no
def MenuNavegacion(es_princi=0):
    salida = "<ul>\n"
    if not es_princi:
        salida += "<li><a href=/>Inicio</a></li>\n"
    salida += "<li><a href=/todas>Todas las actividades</a></li>\n"
    salida += "<li><a href=/ayuda>Ayuda</a></li>\n"
    salida += "<li><a href=/ranking/visitas>Ranking visitas</a></li>\n</ul>"
    return salida


# Busca un usuario por su nombre
def BuscarUsuario(nombre_usuario):
    try:
        usuario = User.objects.get(username=nombre_usuario)
    except User.DoesNotExist:
        return 0
    usuario = Usuario.objects.get(nombre=usuario)
    return usuario


# Busca la información (precio, fecha...) de cada evento
def InfoEvento(evento):
    # Inicializo los parámetros. De momento todos serán strings
    titulo = ""
    gratuito = ""
    precio = ""
    larga_duracion = ""
    fecha = ""
    fecha_final = ""
    hora = ""
    url = ""
    # Busco cada parámetro y lo guardo en una variable
    soup = BeautifulSoup(evento)
    atributos = soup.find_all('atributo')
    for num_atributo in range(len(atributos)):
        if atributos[num_atributo]['nombre'] == "TITULO":
            titulo = atributos[num_atributo].string
        elif atributos[num_atributo]['nombre'] == "GRATUITO":
            gratuito = atributos[num_atributo].string
        elif atributos[num_atributo]['nombre'] == "PRECIO":
            precio = atributos[num_atributo].string.split()[0]
        elif atributos[num_atributo]['nombre'] == "EVENTO-LARGA-DURACION":
            larga_duracion = atributos[num_atributo].string
        elif atributos[num_atributo]['nombre'] == "FECHA-EVENTO":
            fecha = atributos[num_atributo].string
        elif atributos[num_atributo]['nombre'] == "FECHA-FIN-EVENTO":
            fecha_final = atributos[num_atributo].string
        elif atributos[num_atributo]['nombre'] == "HORA-EVENTO":
            hora = atributos[num_atributo].string
        elif atributos[num_atributo]['nombre'] == "CONTENT-URL":
            url = atributos[num_atributo].string
    salida = (titulo, gratuito, precio, larga_duracion, fecha, fecha_final,
             hora, url)
    return salida


# Consigo el primer párrafo de más información
def InfoAdicional(actividad):
    url = actividad.url_inf_adicional
    fd = urllib.urlopen(url)
    html = fd.read()
    soup = BeautifulSoup(html)
    salida = "<b>Informacion adicional: </b>"
    info = soup.find_all('p')[1].string
    if info == "Ayuntamiento de Madrid, 2011. Todos los derechos reservados":
        info = "-" 
    if info == None:
        info = "-"
    return salida + info


# Guardo el nombre de usuario y la fecha de actualizacion en la BBDD de
# actualizaciones
def GuardarActualizacion(nombre_usuario):
    fecha = datetime.now()
    usuario = BuscarUsuario(nombre_usuario)
    actualizacion = ActualizacionEventos(usuario=usuario, fecha=fecha)
    actualizacion.save()
    return "<p>Actualizacion almacenada correctamente</p>\n"


# Guardo en la base de datos de actividades    
def GuardarEvento(Info):
    titulo, gratuito, precio, larga_duracion, fecha, fecha_final, hora, url = Info
    # Inicializo el error a 0
    error = 0
    # Convierto cada parámetro al formato necesario
    try:
        gratuito = int(gratuito)
    except ValueError:
        gratuito = 0
    try:
        precio = int(precio)
    except ValueError:
        precio = 0
    fecha = datetime.strptime(fecha.split()[0] + " " + hora, '%Y-%m-%d %H:%M')
    fecha_final = datetime.strptime(fecha_final, '%Y-%m-%d %H:%M:%S.%f')
    duracion = str(fecha_final - fecha)
    try:
        larga_duracion = int(larga_duracion)
    except ValueError:
        larga_duracion = 0
    # Compruebo si dicha actividad ya está en la base de datos
    try:
        event = Actividad.objects.get(titulo=titulo)
    except Actividad.DoesNotExist:
        # Si no está, la guardo en la base de datos
        event = Actividad(titulo=titulo, gratuito=gratuito, precio=precio,
                        fecha=fecha, duracion=duracion, 
                        larga_duracion=larga_duracion, url_inf_adicional=url,
                        num_visitas=0)
        event.save()
    return error


# Función para actualizar la base de datos de actividades. Primero se parsea la
# información y luego se guarda, uno a uno, cada evento.
def RefrescarActs(xmlURL):
    # Abro el documento XML y lo leo
    fd = urllib.urlopen(xmlURL)
    xml_doc = fd.read()
    # Separo cada uno de los eventos
    eventos = xml_doc.split("<tipo>Evento</tipo>")
    salida = "La base de datos se ha actualizado"
    # Busco la información del evento y la guardo
    for num_evento in range(1, len(eventos)):
        Info = InfoEvento(eventos[num_evento])
        error = GuardarEvento(Info)
        if error:
            salida = "Error al actualizar la base de datos"
            break
    return salida


# Función que actualiza el número de visitas a una actividad
def ActuNumVisitas(actividad):
    actividad.num_visitas = actividad.num_visitas + 1;
    actividad.save()
    return "Ok"

# Función que comprueba si un usuario ya tiene almacenada una actividad
def ComprobarElegida(user, actividad):
    usuario = Usuario.objects.get(nombre=user)
    try:
        actividad_el = ActividadElegida.objects.get(usuario=usuario,
                                                    actividad=actividad)
    except ActividadElegida.DoesNotExist:
        return 0
    return 1


# Función que imprime la actividad que se le pasa
def ImprimirEvento(actividad, lista):
    salida = ""
    # Pude imprimirse o no como lista
    if lista:
        salida += "\t<li>\n\t\t"
    titulo = actividad.titulo
    id = actividad.id
    salida += "<p><b>Titulo</b>: <a href=/actividad/" + str(id) + ">" + titulo
    salida += "</a><br>\n\t\t"
    if actividad.fecha is None:
        fecha = "No especificada"
    else:
        fecha = actividad.fecha.strftime('%d-%m-%Y %H:%M')
    salida += "<b>Fecha</b>: " + fecha + "<br>\n\t\t"
    duracion = actividad.duracion
    salida += "<b>Duracion</b>: " + str(duracion) + "<br>\n\t\t"
    salida += "<b>Actividad gratuita</b>: "
    if actividad.gratuito or actividad.precio == 0:
        salida += "Si<br>\n\t\t"
    else:
        salida += "No<br>\n\t\t"
        precio = actividad.precio
        salida += "<b>Precio</b>: " + str(precio) + " euros<br>\n\t\t"
    if actividad.larga_duracion:
        larga_duracion = "Si"
    else:
        larga_duracion = "No"
    salida += "<b>Larga duracion</b>: " + larga_duracion + "<br>\n\t"
    salida += "<b>Numero de visitas</b>: " + str(actividad.num_visitas)
    salida += "<br>\n\t"
    url = actividad.url_inf_adicional
    salida += "<a href='" + url + "'>Mas informacion</a><br></p>\n\t" 
    if lista:
        salida += "</li>\n"
    return salida


# Función que imprime las actividades que se le pasan
def ImprimirEventos(actividades, request, ordenada=0):
    if ordenada:
        salida = "<ol>\n"
    else:
        salida = "<ul>\n"
    for actividad in actividades:
        salida += ImprimirEvento(actividad, 1) # imprimir como lista
        if request.user.is_authenticated():
            ya_elegida = ComprobarElegida(request.user, actividad)
            if ya_elegida:
                salida += "\t<i>Ya tienes almacenada esta actividad"
                salida += "</i><br><br>\n"
            else:
                salida += ElegirActForm(request.user.username, actividad.id)
    if ordenada:
        salida += "</ol>\n"
    else:
        salida += "</ul>\n"
    return salida


# Consigue los datos de un usuario
def DatosUsuario(usuario):
    titulo = usuario.titulo
    nombre = usuario.nombre.username
    return (titulo, nombre)


# Imprime el nombre y título del usuario que se le pasa
def ImprimirUsuario(usuario):
    titulo, nombre = DatosUsuario(usuario)
    if titulo == "":
        titulo = "Pagina de " + nombre
    salida = "\t<li>\n\t\t"
    salida += "<a href=/" + nombre + ">" + titulo + "</a><br>\n\t"
    salida += "Propietario: " + nombre
    salida += "</li>\n<br>"
    return salida


# Función que imprime el nombre y el título de los usuarios que se le pasan
def ImprimirUsuarios(usuarios):
    salida = "<ul>\n"
    for usuario in usuarios:
        salida += ImprimirUsuario(usuario)
    salida += "</ul>\n"
    return salida


# Imprime las actividades elegidas por un usuario
def ImprimirActElegidas(usuario, pagina):
    actividades_el = ActividadElegida.objects.filter(usuario=usuario)
    if len(actividades_el) == 0:
        return "<p>Este usuario todavia no ha elegido actividades</p>"
    salida = "<p>Este usuario ha almacenado " + str(len(actividades_el))
    salida += " actividades.</p>\n"
    num_paginas = math.ceil(float(len(actividades_el))/10.0)
    if num_paginas >= pagina:
        if pagina >= 1:
            actividades_el = actividades_el[10*(pagina-1):10*pagina]
        else:
            return "<p>Error en la pagina introducida</p>\n"
    else:
        return "<p>Error en la pagina introducida</p>\n"
    salida += "<ul>\n"
    for actividad_el in actividades_el:
        salida += ImprimirEvento(actividad_el.actividad, 1)
        fecha = actividad_el.fecha_eleccion.strftime('%d-%m-%Y %H:%M')
        salida += "<p>Elegida el " + fecha + "</p><br>"
    salida += '<div id="centrar">\n'
    if pagina > 1:
        salida += "<a href=/" + usuario.nombre.username + "/1"
        salida += "><< Primera pagina</a> |"
        salida += "<a href=/" + usuario.nombre.username + "/" + str(pagina-1)
        salida += ">< Pagina anterior</a> |"
    if num_paginas > 1 and num_paginas > pagina:
        salida += "| <a href=/" + usuario.nombre.username + "/" + str(pagina+1)
        salida += ">Pagina siguiente ></a>\n\t"
        salida += "| <a href=/" + usuario.nombre.username + "/"
        salida += str(int(num_paginas)) + ">Ultima pagina >></a><br>\n\t"        
    salida += "</div>\n"
    return salida


# Comprueba si la fecha de una actividad es posterior a este momento y se queda
# solo con el número que se le indique
def ComprobarFecha(actividades, num_actividades):
    # Inicializo la lista
    actividades_correctas = [None]*num_actividades 
    fecha_actual = datetime.now()
    numero = 0
    for actividad in actividades:
        if fecha_actual < actividad.fecha:
            actividades_correctas[numero] = actividad
            numero += 1
        if numero == num_actividades:
            break;
    return actividades_correctas

    
# Devuelve las actividades más próximas
def ActMasProximas(num_actividades):
    if len(Actividad.objects.all()) == 0:
        return 0
    actividades = Actividad.objects.all().order_by("fecha")
    prox_actividades = ComprobarFecha(actividades, num_actividades)
    return prox_actividades


# Devuelve la fecha
def FechaUltimaActu():
    actualizaciones = ActualizacionEventos.objects.all()
    if len(actualizaciones) == 0:
        return "Todavia no se han producido actualizaciones"
    ultima_actualizacion = actualizaciones[len(actualizaciones)-1]
    fecha = ultima_actualizacion.fecha.strftime('%d/%m/%Y %H:%M')
    return fecha


# Devuelve el historial de actualizaciones de la base de datos
def HistorialActus():
    actualizaciones = ActualizacionEventos.objects.all()
    if len(actualizaciones) == 0:
        return "<p>Todavia no ha habido actualizaciones</p>"
    salida = "<ol>\n"
    for actualizacion in actualizaciones:
        fecha = actualizacion.fecha.strftime('%d/%m/%Y %H:%M')
        salida += "<li>El <b>" + fecha + "</b>, por el usuario <b>"
        salida += actualizacion.usuario.nombre.username + "</b></li>"
    salida += "</ol>\n<br><br><br><br><br><br><br>"
    return salida

# Función que filtra los títulos en función de si contienen una cadena de texto
def FiltrarTitulo(cadena):
    actividades = Actividad.objects.all()
    actividades_filt = [None]
    for actividad in actividades:
        titulo = actividad.titulo
        if cadena in titulo:
            actividades_filt.append(actividad)
    return actividades_filt[1:], 0
    

# Función que filtra las actividades en función de la fecha
def FiltrarFecha(fecha):
    actividades = Actividad.objects.all()
    try:
        fecha = datetime.strptime(fecha, '%d/%m/%Y')
    except ValueError: 
        return actividades, 1
    actividades_filt = [None]
    for actividad in actividades:
        fecha_act = actividad.fecha.strftime('%d/%m/%Y %H:%M').split()[0]
        fecha_act = datetime.strptime(fecha_act, '%d/%m/%Y')
        if fecha == fecha_act:
            actividades_filt.append(actividad)
    return actividades_filt[1:], 0


# Función que filtra las actividades en función del precio
def FiltrarPrecio(precio):
    actividades = Actividad.objects.all()
    try:
        precio = int(precio)
    except ValueError:
        return actividades, 1
    actividades = Actividad.objects.filter(precio=precio)
    return actividades, 0


# Función que filtra las actividades en función de la duracion
def FiltrarDuracion(duracion):
    actividades = Actividad.objects.all()
    actividades = Actividad.objects.filter(duracion=duracion)
    return actividades, 0


# Función que filtra las actividades en función de cuatro campos
def FiltrarActividades(request):
    if request.POST.get("Filtro") == "titulo":
        actividades, error = FiltrarTitulo(request.POST.get("Valor"))
    elif request.POST.get("Filtro") == "fecha":
        actividades, error = FiltrarFecha(request.POST.get("Valor"))
    elif request.POST.get("Filtro") == "precio":
        actividades, error = FiltrarPrecio(request.POST.get("Valor"))
    elif request.POST.get("Filtro") == "duracion":
        actividades, error = FiltrarDuracion(request.POST.get("Valor"))
    return actividades, error


# Función que guarda la actividad que elija el usuario
def GuardarActividadElegida(request):
    user = request.user
    usuario = Usuario.objects.get(nombre=user)
    id_actividad = request.POST.get("idactividad")
    try:
        actividad = Actividad.objects.get(id=id_actividad)
    except Actividad.DoesNotExist:
        return "<p>La actividad no existe</p>\n"
    try:
        actividad = ActividadElegida.objects.get(usuario=usuario,
                                                 actividad=actividad)
    except ActividadElegida.DoesNotExist:
        actividad_elegida = ActividadElegida(usuario=usuario,
                                            actividad=actividad,
                                            fecha_eleccion=datetime.now())
        actividad_elegida.save()
        return "<p>La actividad se almaceno correctamente</p>\n"
    return "<p>La actividad ya estaba almacenada</p>\n"
    

# Cambia el título y el color de fondo de un usuario
def CambiarPerfil(request):
    titulo = request.POST.get("Titulo")
    color = request.POST.get("Color_Fondo")
    usuario = Usuario.objects.get(nombre=request.user)
    usuario.color_fondo = color
    if titulo != "":
        usuario.titulo = titulo
    usuario.save()
    return "<p>Perfil actualizado correctamente</p>\n"


# Parsea el recurso para devolver el nombre de usuario y la pagina
def ParsearRecurso(recurso):
    # Inicializo las variables
    nombre_usuario = ""
    pagina = 1
    error = 0
    # Divido por cada /
    recurso = recurso.split("/")
    nombre_usuario = recurso[0]
    if len(recurso) == 2:
        pagina = recurso[1]
        if pagina == "":  # por si nos piden el recurso usuario/
            pagina = 1
    elif len(recurso) > 2:
        error = 1
    try:
        pagina = int(pagina)
    except ValueError:
        error = 1
    return (nombre_usuario, pagina, error)


# Busca el color de fondo que tiene asignado un usuario
def ColorUsuario(request):
    color = "d"
    if request.user.is_authenticated():
        usuario = BuscarUsuario(request.user.username)
        color = usuario.color_fondo
    return color


# Renderiza los parámetros que se le pasan
def Render(request, titulo, navegacion, contenido, adicional):
    usuario = ""
    if request.user.is_authenticated():
        usuario = request.user.username
    template = get_template("index.html")
    c = RequestContext(request, {'titulo': titulo, 
                        'color': ColorUsuario(request),
                        'usuario': usuario,
                        'form': LoginForm(),
                        'menu_navegacion': navegacion,
                        'contenido': contenido,
                        'adicional': adicional,
                        'autenticado': request.user.is_authenticated()})
    rendered = template.render(c)
    return rendered


# Busca la fecha de la última actualización de la base de datos
def UltimaActu():
    return datetime.now().strftime('%d-%m-%Y %H:%M')


# Muestra los comentarios de una actividad
def MostrarComentarios(actividad):
    salida = "<h2>Comentarios</h2>\n"
    comentarios = Comentario.objects.filter(actividad=actividad)
    if len(comentarios) == 0:
        salida += "No hay comentarios."
        return salida
    salida += "<ol>\n"
    for comentario in comentarios:
        nombre_usuario = comentario.usuario.nombre.username
        fecha = comentario.fecha.strftime('%d-%m-%Y %H:%M')
        salida += "<li><b>Por <a href=/" + nombre_usuario + ">" + nombre_usuario
        salida += "</a>, con fecha " + fecha + "</b><br>\n<p>"
        salida += comentario.contenido + "</p></li>\n"
    salida += "</ol>\n"
    return salida


# Guarda un comentario en la base de datos
def GuardarComentario(request, actividad):
    usuario = BuscarUsuario(request.user.username)
    fecha = datetime.now()
    contenido = request.POST.get("message")
    comentario = Comentario(usuario=usuario, actividad=actividad, fecha=fecha,
                 contenido=contenido)
    comentario.save()
    return "<p>Mensaje guardado correctamente</p>\n"
