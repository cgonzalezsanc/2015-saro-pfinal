from django.db import models
from django.contrib.auth.models import User


class Usuario(models.Model):
    nombre = models.ForeignKey(User)
    # tipo: b (azul), d (default), y (amarillo), r (rojo), w (blanco), g (verde)
    color_fondo = models.CharField(max_length=1, default="d")
    titulo = models.TextField(default="", blank=True)


class Actividad(models.Model):
    titulo = models.TextField()
    gratuito = models.IntegerField()
    precio = models.IntegerField()
    fecha = models.DateTimeField()
    duracion = models.CharField(max_length=40)
    larga_duracion = models.IntegerField()
    url_inf_adicional = models.URLField()
    num_visitas = models.IntegerField(default=0)


class Comentario(models.Model):
    usuario = models.ForeignKey(Usuario)
    actividad = models.ForeignKey(Actividad)
    fecha = models.DateTimeField()
    contenido = models.TextField()

 
class ActividadElegida(models.Model):
    usuario = models.ForeignKey(Usuario)
    actividad = models.ForeignKey(Actividad)
    fecha_eleccion = models.DateTimeField()


class ActualizacionEventos(models.Model):
    usuario = models.ForeignKey(Usuario)
    fecha = models.DateTimeField()
