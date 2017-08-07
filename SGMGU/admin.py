from django.contrib import admin
from .models import *


class ProvinciaAdmin(admin.ModelAdmin):
    list_display=["nombre","siglas"]
    search_fields = ['nombre',"siglas"]


class MunicipioAdmin(admin.ModelAdmin):
    list_display=["nombre"]
    search_fields = ['nombre']


class CausalAdmin(admin.ModelAdmin):
    list_display=["nombre","activo"]
    search_fields = ['nombre']


class OrganismoAdmin(admin.ModelAdmin):
    list_display=["nombre","activo"]
    search_fields = ['nombre']


class CarreraAdmin(admin.ModelAdmin):
    list_display=["nombre","activo"]
    search_fields = ['nombre']

class CentroEstudioAdmin(admin.ModelAdmin):
    list_display=["nombre","activo"]
    search_fields = ['nombre']

class ExpedienteMovimientoExternoAdmin(admin.ModelAdmin):
     list_display=[
         "graduado",
         "causal_movimiento",
         "fecha_registro"
     ]
     search_fields = ['graduado__nombre']


class ExpedienteMovimientoInternoAdmin(admin.ModelAdmin):
     list_display=[
         "graduado",
         "causal_movimiento",
         "fecha_registro"
     ]
     search_fields = ['graduado__nombre']


class Expediente_pendienteAdmin(admin.ModelAdmin):
     list_display=[
         "expediente",
         "fecha_pendiente",
     ]
     search_fields = ['expediente__graduado__nombre']


class Expediente_aprobadoAdmin(admin.ModelAdmin):
     list_display=[
         "expediente",
         'codigo_DE_RE',
         'codigo_DE_RS',
         "fecha_aprobado",
     ]
     search_fields = ['expediente__graduado__nombre','codigo_DE_RE','codigo_DE_RS']

class Expediente_rechazadoAdmin(admin.ModelAdmin):
     list_display=[
         "expediente",
         "fecha_rechazo",
         "sintesis_rechazo",
     ]
     search_fields = ['expediente__graduado__nombre']



class Expediente_no_aprobadoAdmin(admin.ModelAdmin):
     list_display=[
         "expediente",
         "fecha_no_aprobado",
         'sintesis_no_aprobado',
     ]
     search_fields = ['expediente__graduado__nombre']

admin.site.register(Municipio,MunicipioAdmin)
admin.site.register(Provincia,ProvinciaAdmin)
admin.site.register(Causal_movimiento,CausalAdmin)
admin.site.register(Organismo,OrganismoAdmin)
admin.site.register(Carrera,CarreraAdmin)
admin.site.register(Centro_estudio,CentroEstudioAdmin)
admin.site.register(Expediente_movimiento_externo,ExpedienteMovimientoExternoAdmin)
admin.site.register(Expediente_movimiento_interno,ExpedienteMovimientoInternoAdmin)
admin.site.register(Expediente_pendiente,Expediente_pendienteAdmin)
admin.site.register(Expediente_aprobado,Expediente_aprobadoAdmin)
admin.site.register(Expediente_rechazado,Expediente_rechazadoAdmin)
admin.site.register(Expediente_no_aprobado)


admin.site.register(Perfil_usuario)
admin.site.register(Facultado)
admin.site.register(Graduado)
admin.site.register(Expediente)
admin.site.register(Categoria_usuario)
admin.site.register(Direccion_trabajo)

admin.site.register(Notificacion)
admin.site.register(UbicacionLaboral)
admin.site.register(DisponibilidadGraduados)
admin.site.register(ProcesoInhabilitacion)
admin.site.register(GraduadoInhabilitacion)