# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from django.db.models.signals import post_save,post_delete
from django.dispatch import receiver
from django.core.cache import cache
from django.contrib.sessions.models import Session
from django.core.exceptions import ValidationError

class Organismo(models.Model):
    nombre=models.CharField(max_length=250)
    siglas=models.CharField(max_length=20)
    activo=models.BooleanField(default=True)
    hijode = models.ForeignKey('self', blank=True, null=True)

    def __unicode__(self):
        return self.nombre

    class Meta:
         ordering=["nombre"]

class Categoria_usuario(models.Model):
    nombre=models.CharField(max_length=256)

    def __unicode__(self):
        return self.nombre

class Provincia(models.Model):
    nombre=models.CharField(max_length=250)
    siglas=models.CharField(max_length=255)

    def __unicode__(self):
        return self.nombre

    class Meta:
         ordering=["id"]


class Perfil_usuario(models.Model):
    usuario=models.OneToOneField(User)
    foto=models.ImageField(upload_to='uploads/img_usuarios/',blank=True, null=True)
    organismo=models.ForeignKey(Organismo)
    telefono=models.CharField(max_length=250,blank=True, null=True)
    categoria=models.ForeignKey(Categoria_usuario)
    provincia=models.ForeignKey(Provincia,blank=True, null=True)
    activo=models.BooleanField(default=True)

    def __unicode__(self):
        return self.usuario.username
    class Meta:
        verbose_name_plural="Perfiles de usuarios"
        verbose_name="Perfil de usuario"



class Notificacion(models.Model):
    emisor=models.ForeignKey(User,related_name="emisores")
    remitente=models.ForeignKey(User,related_name="remitentes")
    texto=models.TextField(blank=True,null=True)
    fecha=models.DateTimeField(auto_now_add=True)
    revisado=models.BooleanField(default=False)


class Municipio(models.Model):
    codigo_mes=models.CharField(max_length=100,blank=True,null=True)
    nombre=models.CharField(max_length=250)
    provincia=models.ForeignKey(Provincia)

    def __unicode__(self):
        return "%s"%(self.nombre)

    class Meta:
         ordering=["nombre"]



class Centro_estudio(models.Model):
    codigo_mes=models.CharField(max_length=100,blank=True,null=True)
    nombre=models.CharField(max_length=1000)
    siglas=models.CharField(max_length=20,blank=True,null=True)
    activo=models.BooleanField(default=True)
    provincia=models.ForeignKey(Provincia,blank=True,null=True)

    def __unicode__(self):
        return "%s"%(self.nombre)



class Carrera(models.Model):
    codigo_mes=models.CharField(max_length=100,blank=True,null=True)
    nombre=models.CharField(max_length=1000)
    activo=models.BooleanField(default=True)

    def __unicode__(self):
        return self.nombre

    class Meta:
         ordering=["nombre"]



class Causal_movimiento(models.Model):
     nombre=models.CharField(max_length=500)
     activo=models.BooleanField(default=True)


     class Meta:
         ordering=["nombre"]
         verbose_name_plural="Causales"

     def __unicode__(self):
        return self.nombre




class Persona(models.Model):
    nombre=models.CharField(max_length=250)

    class Meta:
          ordering=["nombre"]

    def __unicode__(self):
        return "%s"%(self.nombre)

from django.core.validators import RegexValidator
class Graduado(Persona):
    ci=models.CharField(max_length=11,blank=True,null=True,validators= [RegexValidator(
                regex='^[0-9]{2}(0[1-9]|1[0-2])(31|30|(0[1-9]|[1-2][0-9]))[0-9]{5}$',
                message='CI incorrecto',
            )])
    carrera=models.ForeignKey(Carrera,null=True,blank=True)
    anno_graduacion=models.IntegerField()
    centro_estudio=models.ForeignKey(Centro_estudio,null=True,blank=True)
    codigo_boleta=models.CharField(null=True,blank=True,max_length=250)
    imagen_boleta=models.ImageField(upload_to='uploads/img_boletas/',blank=True, null=True)
    detalle_direccion_residencia=models.CharField(max_length=500,null=True,blank=True)
    provincia_direccion_residencia=models.ForeignKey(Provincia,null=True,blank=True)
    municipio_direccion_residencia=models.ForeignKey(Municipio,null=True,blank=True)



class Facultado(Persona):
     cargo=models.CharField(max_length=250,blank=True,null=True)
     activo=models.BooleanField(default=True)
     organismo=models.ForeignKey(Organismo)



class Expediente(models.Model):
    graduado=models.OneToOneField(Graduado,null=True,blank=True)
    entidad_liberacion=models.CharField(max_length=500,null=True,blank=True)
    entidad_aceptacion=models.CharField(max_length=500,null=True,blank=True)
    mun_entidad_liberacion=models.ForeignKey(Municipio,related_name="municipio_liberacion",null=True,blank=True)
    mun_entidad_aceptacion=models.ForeignKey(Municipio,related_name="municipio_aceptacion",null=True,blank=True)
    causal_movimiento=models.ForeignKey(Causal_movimiento,null=True,blank=True)
    sintesis_causal_movimiento=models.CharField(max_length=1000,blank=True,null=True)
    fecha_registro=models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return "Expediente del graudado %s"%(self.graduado.nombre)


class Expediente_movimiento_interno(Expediente):
    aprobado_por=models.CharField(max_length=500)
    organismo=models.ForeignKey(Organismo)


class Expediente_movimiento_externo(Expediente):
    organismo_liberacion=models.ForeignKey(Organismo,related_name="organismo_liberacion")
    organismo_aceptacion=models.ForeignKey(Organismo,related_name="organismo_aceptacion")
    facultado_liberacion=models.CharField(max_length=250,null=True,blank=True)
    facultado_aceptacion=models.CharField(max_length=250,null=True,blank=True)
    comprimido=models.FileField(upload_to='uploads/adjuntos_expedientes/',null=True,blank=True)


class Expediente_rechazado(models.Model):
    expediente=models.ForeignKey(Expediente_movimiento_externo)
    fecha_rechazo=models.DateTimeField(auto_now=True)
    sintesis_rechazo=models.CharField(max_length=500)

    def __unicode__(self):
        return "Expediente del graudado %s"%(self.expediente.graduado.nombre)


class Expediente_pendiente(models.Model):
    expediente=models.ForeignKey(Expediente_movimiento_externo)
    fecha_pendiente=models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return "Expediente del graudado %s"%(self.expediente.graduado.nombre)



class Expediente_aprobado(models.Model):
    codigo_DE_RE=models.CharField(max_length=250,null=True,blank=True)
    codigo_DE_RS=models.CharField(max_length=250,null=True,blank=True,unique_for_year=True)
    expediente=models.ForeignKey(Expediente_movimiento_externo)
    fecha_aprobado=models.DateTimeField(default=datetime.now())
    carta_expediente=models.FileField(upload_to='uploads/cartas_expedientes/',blank=True, null=True)

    def __unicode__(self):
        return "Expediente del graudado %s"%(self.expediente.graduado.nombre)


    class Meta:
        ordering=['-fecha_aprobado']


class Expediente_no_aprobado(models.Model):
    expediente=models.ForeignKey(Expediente_movimiento_externo)
    fecha_no_aprobado=models.DateTimeField(auto_now=True)
    sintesis_no_aprobado=models.CharField(max_length=500)

    def __unicode__(self):
        return "Expediente del graudado %s"%(self.expediente.graduado.nombre)


class Direccion_trabajo(models.Model):
     provincia=models.OneToOneField(Provincia)
     director=models.CharField(max_length=256,blank=True, null=True)
     sexo_director=models.CharField(max_length=30,blank=True,null=True)
     especialista=models.CharField(max_length=256,blank=True, null=True)
     correo_director=models.EmailField(blank=True, null=True)
     correo_especialista=models.EmailField(blank=True, null=True)
     activo=models.BooleanField(default=True)


     def __unicode__(self):
        return "Dirección de Trabajo de %s".decode("utf-8")%(self.provincia.nombre)


class UbicacionLaboral(models.Model):

    ESTADOS_SEXO = [
        ('M', 'Masculino'),
        ('F', 'Femenino'),
    ]

    boleta=models.CharField(max_length=15,blank=True,null=True)
    anno_graduado=models.IntegerField()
    centro_estudio=models.ForeignKey(Centro_estudio)
    carrera=models.ForeignKey(Carrera)
    ci=models.CharField(
        max_length=11,
        validators= [RegexValidator(regex='^[0-9]{2}(0[1-9]|1[0-2])(31|30|(0[1-9]|[1-2][0-9]))[0-9]{5}$',message='CI incorrecto',)],
        unique=True
    )
    nombre_apellidos=models.CharField(max_length=256)
    cumple_servicio_social=models.BooleanField()
    entidad=models.CharField(max_length=256)
    organismo=models.ForeignKey(Organismo)
    municipio_residencia=models.ForeignKey(Municipio,related_name="ubicacion_municipio_residencia")
    provincia_ubicacion=models.ForeignKey(Provincia,related_name="ubicacion_provincia_ubicacion")
    sexo=models.CharField(max_length=20)
    direccion_particular=models.CharField(max_length=256)
    presentado=models.BooleanField(default=True)
    fecha_registro=models.DateTimeField(auto_now_add=True)
    causa_no_presentacion=models.TextField(null=True,blank=True)
    estado_ubicacion=models.CharField(max_length=20,choices=(('desfasado','Desfasado'),('graduado','Graduado')))



    def sexo_verbose(self):
        return dict(UbicacionLaboral.ESTADOS_SEXO)[self.sexo]


    def css(self):
        if self.cumple_servicio_social:
            return "Si"
        else:
            return "No"

    def is_presentado(self):
        if self.presentado:
            return "Si"
        else:
            return "No"

    def __unicode__(self):
        return "Ubicacion de %s "%self.nombre_apellidos

    class Meta:
        ordering=["-fecha_registro"]





class DisponibilidadGraduados(models.Model):

    ESTADOS_SEXO = [
        ('M', 'Masculino'),
        ('F', 'Femenino'),
    ]

    centro_estudio=models.ForeignKey(Centro_estudio)
    carrera=models.ForeignKey(Carrera)
    cumple_servicio_social=models.BooleanField()
    ci=models.CharField(max_length=11,blank=True,null=True,validators= [RegexValidator(
                regex='^[0-9]{2}(0[1-9]|1[0-2])(31|30|(0[1-9]|[1-2][0-9]))[0-9]{5}$',
                message='CI incorrecto',
            )],unique=True)
    nombre_apellidos=models.CharField(max_length=256)
    municipio_residencia=models.ForeignKey(Municipio,related_name="disponibilidad_municipio_residencia")
    sexo=models.CharField(max_length=20)
    direccion_particular=models.CharField(max_length=256)
    fecha_registro=models.DateTimeField(auto_now_add=True)


    def sexo_verbose(self):
        return dict(DisponibilidadGraduados.ESTADOS_SEXO)[self.sexo]


    def __unicode__(self):
        return self.nombre_apellidos

    class Meta:
        ordering=["-fecha_registro"]






@receiver(post_save)
def limpiar_cache0(sender, instance, created, **kwargs):
        if created:
             if sender != Session:
                cache.clear()

@receiver(post_save)
def limpiar_cache1(sender, instance, **kwargs):
       if sender != Session:
            cache.clear()

@receiver(post_delete)
def limpiar_cache2(sender, **kwargs):
        if sender != Session:
          cache.clear()

@receiver(post_save, sender=User)
def actualizar_perfil(sender, instance, **kwargs):
        #instance.perfil_usuario.save()
        pass