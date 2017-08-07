# -*- coding: utf-8 -*-

from django.shortcuts import render,redirect,get_object_or_404,get_list_or_404
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required,permission_required
from SGMGU.forms import *
from SGMGU.models import *
from django.http import Http404,HttpResponse
from django.core.paginator import Paginator, InvalidPage, EmptyPage
import json
from django.contrib import messages
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
from django.core.mail import EmailMessage
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger,InvalidPage
from itertools import chain
from django.conf import settings
from .utiles import *

fields=['id','graduado__nombre','organismo_liberacion__siglas','organismo_aceptacion__siglas','fecha_registro']

#@cache_por_user(ttl=3600, cache_post=False)
@login_required
@permission_required(['administrador','especialista'])
def gestion_expedientes(request):
    expedientes=paginar(request,Expediente_movimiento_externo.objects.all().order_by("-fecha_registro").values(*fields))
    context = {'expedientes': expedientes,'paginas':crear_lista_pages(expedientes)}
    return render(request, "Expedientes/gestion_expedientes.html", context)


#Busqueda---------------------------------------------------------------------------------------------------------------
@login_required
def buscar_expediente_ci(request,ci):
  expedientes=paginar(request,Expediente_movimiento_externo.objects.filter(graduado__ci=ci).order_by("-fecha_registro").values(*fields))
  context={'expedientes':expedientes,'busqueda':'si','termino_busqueda':'por CI',"valor_busqueda":ci,'paginas':crear_lista_pages(expedientes)}
  return render(request, "Expedientes/gestion_expedientes.html", context)


@login_required
def buscar_expediente_id(request,id):
  expedientes=paginar(request,Expediente_movimiento_externo.objects.filter(id=id).order_by("-fecha_registro").values(*fields))
  context={'expedientes':expedientes,'busqueda':'si','termino_busqueda':'por ID',"valor_busqueda":id,'paginas':crear_lista_pages(expedientes)}
  return render(request, "Expedientes/gestion_expedientes.html", context)


def autocompletar_expediente(request,vista):
    if request.method == 'POST':
            ci=request.POST['ci']
            try:
                ubicados=UbicacionLaboral.objects.filter(ci=ci)
                ubicacion=ubicados[0]
                entrada= {
                    'nombre_graduado':ubicacion.nombre_apellidos,
                    'carrera_graduado':ubicacion.carrera.id,
                    'anno_graduacion':ubicacion.anno_graduado,
                    'codigo_boleta':ubicacion.boleta,
                    'detalle_direccion_residencia':ubicacion.direccion_particular,
                    'centro_estudio':ubicacion.centro_estudio.id,
                    'provincia_residencia':ubicacion.municipio_residencia.provincia.id,
                    'municipio_residencia':ubicacion.municipio_residencia.id,
                    'organismo_liberacion':ubicacion.organismo.id,
                    'entidad_liberacion':ubicacion.entidad,
                    'ci':ubicacion.ci,
                    }
                if vista!='interno':
                    form = RegistroExpedienteForm(initial=entrada)
                else:
                    form = RegistroMovimientoInternoForm(initial=entrada)
                contexto={'form':form,'autocompletar':True}
                if vista == "avanzada":
                    return render(request, "Expedientes/registrar_expediente.html", contexto)
                elif vista == "estandar":
                    return render(request, "Expedientes/registrar_expediente_estandar.html", contexto)
                else:
                   return render(request, "MovimietosInternos/registrar_movimiento_interno.html", contexto)
            except:
                messages.add_message(request, messages.ERROR, "No se encontró ningún ubicado registrado con ese ci")
                if vista == "avanzada":
                    return redirect("/gestion_expedientes/registrar_expediente")
                elif vista == "estandar":
                    return redirect("/registrar_expediente_estandar")
                else:
                    return redirect("/movimientos_internos/registrar/")
    else:
         return redirect("/inicio")

@login_required
def registrar_expediente(request,vista):
    if request.method == 'POST':
        form=RegistroExpedienteForm(request.POST,request.FILES)
        if form.is_valid():
            nombre_graduado=form.cleaned_data['nombre_graduado']
            carrera_graduado=form.cleaned_data['carrera_graduado']
            anno_graduacion=form.cleaned_data['anno_graduacion']
            codigo_boleta=form.cleaned_data['codigo_boleta']
            imagen_boleta=form.cleaned_data['imagen_boleta']
            organismo_liberacion=form.cleaned_data['organismo_liberacion']
            organismo_aceptacion=form.cleaned_data['organismo_aceptacion']
            entidad_liberacion=form.cleaned_data['entidad_liberacion']
            entidad_aceptacion=form.cleaned_data['entidad_aceptacion']
            facultado_liberacion=form.cleaned_data['facultado_liberacion']
            facultado_aceptacion=form.cleaned_data['facultado_aceptacion']
            comprimido=form.cleaned_data['comprimido']
            municipio_entidad_liberacion=form.cleaned_data['municipio_entidad_liberacion']
            municipio_entidad_aceptacion=form.cleaned_data['municipio_entidad_aceptacion']
            causal_movimiento=form.cleaned_data['causal_movimiento']
            sintesis_causal_movimiento=form.cleaned_data['sintesis_causal_movimiento']
            detalle_direccion_residencia=form.cleaned_data['detalle_direccion_residencia']
            centro_estudio=form.cleaned_data['centro_estudio']
            municipio_residencia=form.cleaned_data['municipio_residencia']

            ci=form.cleaned_data['ci']


            graduado=Graduado(
                    nombre=nombre_graduado,
                    carrera=carrera_graduado,
                    anno_graduacion=anno_graduacion,
                    detalle_direccion_residencia=detalle_direccion_residencia,
                    ci=ci,
                    codigo_boleta=codigo_boleta,
                    imagen_boleta=imagen_boleta,
                    centro_estudio=centro_estudio,
                    municipio_direccion_residencia=municipio_residencia,
                    provincia_direccion_residencia=municipio_residencia.provincia,
            )
            graduado.save()
            expediente=Expediente_movimiento_externo(
                    graduado=graduado,
                    organismo_liberacion=organismo_liberacion,
                    organismo_aceptacion=organismo_aceptacion,
                    facultado_liberacion=facultado_liberacion,
                    facultado_aceptacion=facultado_aceptacion,
                    comprimido=comprimido,
                    entidad_liberacion=entidad_liberacion,
                    entidad_aceptacion=entidad_aceptacion,
                    mun_entidad_liberacion= municipio_entidad_liberacion,
                    mun_entidad_aceptacion=municipio_entidad_aceptacion,
                    causal_movimiento=causal_movimiento,
                    sintesis_causal_movimiento=sintesis_causal_movimiento,
            )

            expediente.save()
            expediente_pendiente=Expediente_pendiente(expediente=expediente)
            expediente_pendiente.save()
            messages.add_message(request, messages.SUCCESS, "El expediente ha sido registrado con éxito.")
            notificar_accion_expediente(request,"registrar",expediente)
            if vista == "estandar":
                 return redirect("/registrar_expediente_estandar")
            else:
                 return redirect("/gestion_expedientes")

    else:
        form = RegistroExpedienteForm()
    context = {'form':form}
    if vista != "estandar":
       return render(request, "Expedientes/registrar_expediente.html", context)
    else:
       return render(request, "Expedientes/registrar_expediente_estandar.html", context)

@login_required
@permission_required(['administrador','especialista'])
def eliminar_expediente(request,id_expediente):
    exp=Expediente_movimiento_externo.objects.get(id=id_expediente)
    graduado=exp.graduado
    exp.delete()
    graduado.delete()
    messages.add_message(request, messages.SUCCESS, "El expediente ha sido eliminado con éxito.")
    return redirect('/gestion_expedientes')

@login_required
def editar_expediente(request,id_expediente,vista):
  categoria=Perfil_usuario.objects.get(usuario=request.user).categoria.nombre
  if vista == "estandar":
    expediente=Expediente_movimiento_externo.objects.get(id=id_expediente)
  elif vista == "rechazado":
    expediente=Expediente_rechazado.objects.get(id=id_expediente).expediente
  elif vista == "pendiente":
    expediente=Expediente_pendiente.objects.get(id=id_expediente).expediente
  elif vista == "aprobado":
    expediente=Expediente_aprobado.objects.get(id=id_expediente).expediente
  elif vista == "no_aprobado":
    expediente=Expediente_no_aprobado.objects.get(id=id_expediente).expediente

  if request.method == 'POST':
       form=RegistroExpedienteForm(request.POST,request.FILES)
       if form.is_valid():
            nombre_graduado=form.cleaned_data['nombre_graduado']
            carrera_graduado=form.cleaned_data['carrera_graduado']
            anno_graduacion=form.cleaned_data['anno_graduacion']
            codigo_boleta=form.cleaned_data['codigo_boleta']
            imagen_boleta=form.cleaned_data['imagen_boleta']
            organismo_liberacion=form.cleaned_data['organismo_liberacion']
            organismo_aceptacion=form.cleaned_data['organismo_aceptacion']
            entidad_liberacion=form.cleaned_data['entidad_liberacion']
            entidad_aceptacion=form.cleaned_data['entidad_aceptacion']
            facultado_liberacion=form.cleaned_data['facultado_liberacion']
            facultado_aceptacion=form.cleaned_data['facultado_aceptacion']
            comprimido=form.cleaned_data['comprimido']
            municipio_entidad_liberacion=form.cleaned_data['municipio_entidad_liberacion']
            municipio_entidad_aceptacion=form.cleaned_data['municipio_entidad_aceptacion']
            causal_movimiento=form.cleaned_data['causal_movimiento']
            sintesis_causal_movimiento=form.cleaned_data['sintesis_causal_movimiento']
            detalle_direccion_residencia=form.cleaned_data['detalle_direccion_residencia']
            centro_estudio=form.cleaned_data['centro_estudio']
            municipio_residencia=form.cleaned_data['municipio_residencia']
            ci=form.cleaned_data['ci']

            expediente.graduado.nombre=nombre_graduado
            expediente.graduado.carrera=carrera_graduado
            expediente.graduado.anno_graduacion=anno_graduacion
            expediente.graduado.detalle_direccion_residencia=detalle_direccion_residencia
            expediente.graduado.ci=ci
            expediente.graduado.codigo_boleta=codigo_boleta
            if imagen_boleta!=None:
                expediente.graduado.imagen_boleta=imagen_boleta
            expediente.graduado.centro_estudio=centro_estudio
            expediente.graduado.municipio_direccion_residencia=municipio_residencia
            expediente.graduado.provincia_direccion_residencia=municipio_residencia.provincia
            expediente.graduado.save()
            expediente.organismo_liberacion=organismo_liberacion
            expediente.organismo_aceptacion=organismo_aceptacion
            expediente.facultado_liberacion=facultado_liberacion
            expediente.facultado_aceptacion=facultado_aceptacion
            if comprimido!=None:
                expediente.comprimido=comprimido
            expediente.entidad_liberacion=entidad_liberacion
            expediente.entidad_aceptacion=entidad_aceptacion
            expediente.mun_entidad_liberacion= municipio_entidad_liberacion
            expediente.mun_entidad_aceptacion=municipio_entidad_aceptacion
            expediente.causal_movimiento=causal_movimiento
            expediente.sintesis_causal_movimiento=sintesis_causal_movimiento

            expediente.save()
            messages.add_message(request, messages.SUCCESS, "El expediente ha sido modificado con éxito.")

            if vista == "estandar":
              return redirect("/gestion_expedientes")

            elif vista == "pendiente":
                if categoria == "organismo":
                  exp=Expediente_pendiente.objects.get(id=id_expediente)
                  exp.fecha_pendiente=datetime.now()
                  exp.save()
                return redirect("/expedientes_pendientes")

            elif vista == "rechazado":
                  if categoria == "organismo":
                        exp_rech=Expediente_rechazado.objects.get(id=id_expediente)
                        exp_rech.delete()

                        exp_pend=Expediente_pendiente(expediente=expediente)
                        exp_pend.save()
                        notificar_accion_expediente(request,"pasar_a_pendientes_editar",exp_pend.expediente)

                  return redirect("/expedientes_rechazados")

            elif vista == "aprobado":
                return redirect("/expedientes_aprobados")

            elif vista == "no_aprobado":
                return redirect("/expedientes_no_aprobados")

  else:
        form = RegistroExpedienteForm(
        {
        'nombre_graduado':expediente.graduado.nombre,
        'carrera_graduado':expediente.graduado.carrera.id,
        'anno_graduacion':expediente.graduado.anno_graduacion,
        'codigo_boleta':expediente.graduado.codigo_boleta,
        'imagen_boleta':expediente.graduado.imagen_boleta,
        'organismo_liberacion':expediente.organismo_liberacion.id,
        'organismo_aceptacion':expediente.organismo_aceptacion.id,
        'entidad_liberacion':expediente.entidad_liberacion,
        'entidad_aceptacion':expediente.entidad_aceptacion,
        'facultado_liberacion':expediente.facultado_liberacion,
        'facultado_aceptacion':expediente.facultado_aceptacion,
        'comprimido':expediente.comprimido,
        'municipio_entidad_liberacion':expediente.mun_entidad_liberacion.id,
        'municipio_entidad_aceptacion':expediente.mun_entidad_aceptacion.id,
        'provincia_entidad_liberacion':expediente.mun_entidad_liberacion.provincia.id,
        'provincia_entidad_aceptacion':expediente.mun_entidad_aceptacion.provincia.id,
        'causal_movimiento':expediente.causal_movimiento.id,
        'sintesis_causal_movimiento':expediente.sintesis_causal_movimiento,
        'detalle_direccion_residencia':expediente.graduado.detalle_direccion_residencia,
        'centro_estudio':expediente.graduado.centro_estudio.id,
        'provincia_residencia':expediente.graduado.provincia_direccion_residencia.id,
        'municipio_residencia':expediente.graduado.municipio_direccion_residencia.id,
        'ci':expediente.graduado.ci
        }
        )



  context = {'id_exp':id_expediente,'form':form}

  if vista == "pendiente":
       return render(request, "ExpedientesPendientes/editar_expediente_pendiente.html", context)
  elif vista == "rechazado":
       return render(request, "ExpedientesRechazados/editar_expediente_rechazado.html", context)

  elif vista == "aprobado":
       return render(request, "ExpedientesAprobados/editar_expediente_aprobado.html", context)

  elif vista == "no_aprobado":
       return render(request, "ExpedientesNoAprobados/editar_expediente_no_aprobado.html", context)

  else:
       return render(request, "Expedientes/editar_expediente.html", context)


#listados--------------------------------------------------------------------------------------------------------

@login_required()
def listado_expedientes_aprobados(request):
    perfil=Perfil_usuario.objects.get(usuario=request.user)
    foto=perfil.foto
    fields=['id','codigo_DE_RS','expediente__graduado__nombre','expediente__organismo_liberacion__siglas','expediente__organismo_aceptacion__siglas','expediente__graduado__carrera__nombre','fecha_aprobado']
    if perfil.categoria.nombre == "organismo":
        expedientes_liberados=Expediente_aprobado.objects.filter(expediente__organismo_liberacion=perfil.organismo).order_by("-fecha_aprobado").values(*fields)
        expedientes_aceptados=Expediente_aprobado.objects.filter(expediente__organismo_aceptacion=perfil.organismo).order_by("-fecha_aprobado").values(*fields)
        expedientes = list(chain(expedientes_aceptados,expedientes_liberados))
        expedientes=paginar(request,expedientes)
        context = {'categoria':perfil.categoria.nombre,'foto':foto,'expedientes':expedientes}

    elif perfil.categoria.nombre == "dpts":
        expedientes=paginar(request,Expediente_aprobado.objects.filter(expediente__mun_entidad_aceptacion__provincia=perfil.provincia).order_by("-fecha_aprobado").values(*fields))
        context = {'categoria':perfil.categoria.nombre,'foto':foto,'expedientes':expedientes}

    else:
        expedientes=paginar(request,Expediente_aprobado.objects.all().order_by("-fecha_aprobado").values(*fields))
        context = {'categoria':perfil.categoria.nombre,'foto':foto,'expedientes':expedientes,'paginas':crear_lista_pages(expedientes)}
    return render(request, "ExpedientesAprobados/expedientes_aprobados.html", context)





@login_required
def buscar_expedientes_aprobados_ci(request,ci):
  fields=['id','codigo_DE_RS','expediente__graduado__nombre','expediente__organismo_liberacion__siglas','expediente__organismo_aceptacion__siglas','expediente__graduado__carrera__nombre','fecha_aprobado']
  expedientes=paginar(request,Expediente_aprobado.objects.filter(expediente__graduado__ci=ci).order_by("-fecha_aprobado").values(*fields))
  context={'expedientes':expedientes,'busqueda':'si','termino_busqueda':'por CI',"valor_busqueda":ci,'paginas':crear_lista_pages(expedientes)}
  return render(request, "ExpedientesAprobados/expedientes_aprobados.html", context)


@login_required
def buscar_expedientes_aprobados_rs(request,rs):
  rs_inicial=rs
  rs="DE-RS %s"%rs
  fields=['id','codigo_DE_RS','expediente__graduado__nombre','expediente__organismo_liberacion__siglas','expediente__organismo_aceptacion__siglas','expediente__graduado__carrera__nombre','fecha_aprobado']
  expedientes=paginar(request,Expediente_aprobado.objects.filter(codigo_DE_RS=rs).order_by("-fecha_aprobado").values(*fields))
  context={'expedientes':expedientes,'busqueda':'si','termino_busqueda':'por RS',"valor_busqueda":rs_inicial,'paginas':crear_lista_pages(expedientes)}
  return render(request, "ExpedientesAprobados/expedientes_aprobados.html", context)




@login_required()
def listado_expedientes_pendientes(request):
    perfil=Perfil_usuario.objects.get(usuario=request.user)
    foto=perfil.foto
    organismo=perfil.organismo
    if perfil.categoria.nombre == "organismo":
       expedientes_pendientes=paginar(request,Expediente_pendiente.objects.filter(expediente__organismo_liberacion=organismo).order_by("-fecha_pendiente"))
       context = {'categoria':perfil.categoria.nombre,'foto':foto,'expedientes_pendientes':expedientes_pendientes,'organismo':organismo}
    else:
      expedientes_pendientes=paginar(request,Expediente_pendiente.objects.all().order_by("-fecha_pendiente"))
      context = {'categoria':perfil.categoria.nombre,'foto':foto,'expedientes_pendientes':expedientes_pendientes,'paginas':crear_lista_pages(expedientes_pendientes)}
    return render(request, "ExpedientesPendientes/expedientes_pendientes.html", context)

@login_required
def buscar_expedientes_pendientes_ci(request,ci):
  expedientes=paginar(request,Expediente_pendiente.objects.filter(expediente__graduado__ci=ci).order_by("-fecha_pendiente"))
  context={'expedientes_pendientes':expedientes,'busqueda':'si','termino_busqueda':'por CI',"valor_busqueda":ci,'paginas':crear_lista_pages(expedientes)}
  return render(request, "ExpedientesPendientes/expedientes_pendientes.html", context)


@login_required()
def listado_expedientes_rechazado(request):
    perfil=Perfil_usuario.objects.get(usuario=request.user)
    foto=perfil.foto
    organismo=perfil.organismo
    if perfil.categoria.nombre == "organismo":
       expedientes_rechazados=paginar(request,Expediente_rechazado.objects.filter(expediente__organismo_liberacion=organismo).order_by("-fecha_rechazo"),)
       context = {'categoria':perfil.categoria.nombre,'foto':foto,'expedientes_rechazados':expedientes_rechazados,'organismo':organismo}
    else:
      expedientes_rechazados=paginar(request,Expediente_rechazado.objects.all().order_by("-fecha_rechazo"))
      context = {'categoria':perfil.categoria.nombre,'foto':foto,'expedientes_rechazados':expedientes_rechazados,'paginas':crear_lista_pages(expedientes_rechazados)}
    return render(request, "ExpedientesRechazados/expedientes_rechzados.html", context)



@login_required
def buscar_expedientes_rechazados_ci(request,ci):
  expedientes=paginar(request,Expediente_rechazado.objects.filter(expediente__graduado__ci=ci).order_by("-fecha_rechazo"))
  context={'expedientes_rechazados':expedientes,'busqueda':'si','termino_busqueda':'por CI',"valor_busqueda":ci,'paginas':crear_lista_pages(expedientes)}
  return render(request, "ExpedientesRechazados/expedientes_rechzados.html", context)


@login_required()
def listado_expedientes_no_aprobados(request):
    perfil=Perfil_usuario.objects.get(usuario=request.user)
    foto=perfil.foto
    organismo=perfil.organismo
    if perfil.categoria.nombre == "organismo":
       expedientes_no_aprob=paginar(request,Expediente_no_aprobado.objects.filter(expediente__organismo_liberacion=organismo).order_by("-fecha_no_aprobado"))
       context = {'categoria':perfil.categoria.nombre,'foto':foto,'expedientes_no_aprob':expedientes_no_aprob,'organismo':organismo}
    else:
      expedientes_no_aprob=paginar(request,Expediente_no_aprobado.objects.all().order_by("-fecha_no_aprobado"))
      context = {'categoria':perfil.categoria.nombre,'foto':foto,'expedientes_no_aprob':expedientes_no_aprob,'paginas':crear_lista_pages(expedientes_no_aprob)}
    return render(request, "ExpedientesNoAprobados/expedientes_no_aprobados.html", context)


@login_required
def buscar_expedientes_no_aprobados_ci(request,ci):
  expedientes=paginar(request,Expediente_no_aprobado.objects.filter(expediente__graduado__ci=ci).order_by("-fecha_no_aprobado"))
  context={'expedientes_no_aprob':expedientes,'busqueda':'si','termino_busqueda':'por CI',"valor_busqueda":ci,'paginas':crear_lista_pages(expedientes)}
  return render(request, "ExpedientesNoAprobados/expedientes_no_aprobados.html", context)

#Detalle------------------------------------------------------------------------------------------
@login_required
def detalle_expediente(request,id_expediente):
    expediente=Expediente_movimiento_externo.objects.get(id=id_expediente)
    perfil=Perfil_usuario.objects.get(usuario=request.user)
    foto=perfil.foto
    context = {'categoria':perfil.categoria.nombre,'foto':foto,'expediente':expediente}
    return render(request, "Expedientes/detalle_expediente.html", context)

@login_required
def detalle_expediente_pendiente(request,id_expediente):
    expediente=Expediente_pendiente.objects.get(id=id_expediente)
    perfil=Perfil_usuario.objects.get(usuario=request.user)
    foto=perfil.foto
    context = {'categoria':perfil.categoria.nombre,'foto':foto,'expediente':expediente}
    return render(request, "ExpedientesPendientes/detalle_expediente_pendiente.html", context)

@login_required
def detalle_expediente_rechazado(request,id_expediente):
    expediente=Expediente_rechazado.objects.get(id=id_expediente)
    perfil=Perfil_usuario.objects.get(usuario=request.user)
    foto=perfil.foto
    context = {'categoria':perfil.categoria.nombre,'foto':foto,'expediente':expediente}
    return render(request, "ExpedientesRechazados/detalle_expediente_rechzado.html", context)

@login_required
def detalle_expediente_no_aprobado(request,id_expediente):
    expediente=Expediente_no_aprobado.objects.get(id=id_expediente)
    perfil=Perfil_usuario.objects.get(usuario=request.user)
    foto=perfil.foto
    context = {'categoria':perfil.categoria.nombre,'foto':foto,'expediente':expediente}
    return render(request, "ExpedientesNoAprobados/detalle_expediente_no_aprobado.html", context)

@login_required
def detalle_expediente_aprobado(request,id_expediente):
    expediente=Expediente_aprobado.objects.get(id=id_expediente)
    perfil=Perfil_usuario.objects.get(usuario=request.user)
    foto=perfil.foto
    context = {'categoria':perfil.categoria.nombre,'foto':foto,'expediente':expediente}
    return render(request, "ExpedientesAprobados/detalle_expediente_aprobado.html", context)

#Pasar_a_pendientes------------------------------------------------------------------------------------------
def pasar_a_pendientes(request,id_expediente):
    exp_aprobado=Expediente_aprobado.objects.get(id=id_expediente)
    exp_mov_ext=exp_aprobado.expediente
    exp_aprobado.delete()
    expediente_pendiente=Expediente_pendiente(expediente=exp_mov_ext)
    expediente_pendiente.save()
    messages.add_message(request, messages.SUCCESS, "El expediente ha sido pasado a pendientes con éxito.")
    return redirect("/expedientes_aprobados")

def pasar_a_pendientes_from_rechazo(request,id_expediente):
    exp_re=Expediente_rechazado.objects.get(id=id_expediente)
    exp_mov_ext=exp_re.expediente
    exp_re.delete()
    expediente_pendiente=Expediente_pendiente(expediente=exp_mov_ext)
    expediente_pendiente.save()
    messages.add_message(request, messages.SUCCESS, "El expediente ha sido pasado a pendientes con éxito.")
    return redirect("/expedientes_rechazados")

def pasar_a_pendientes_de_no_aprobado(request,id_expediente):
    exp_no=Expediente_no_aprobado.objects.get(id=id_expediente)
    exp_mov_ext=exp_no.expediente
    exp_no.delete()
    expediente_pendiente=Expediente_pendiente(expediente=exp_mov_ext)
    expediente_pendiente.save()
    messages.add_message(request, messages.SUCCESS, "El expediente ha sido pasado a pendientes con éxito.")
    return redirect("/expedientes_no_aprobados")

#rechazar_expediente-------------------------------------------------------------------------------------------
#from django.db.models import Q
def notificar_accion_expediente(request,tipo_accion,expediente):
    usuarios_ftc=[]
    if tipo_accion == "rechazar":
        accion="ha rechazado"
    elif tipo_accion == "aprobar":
        accion="ha aprobado"
    elif tipo_accion == "no_aprobar":
        accion="no ha aprobado"
    elif tipo_accion == "pasar_a_pendientes":
        accion="ha pasado a pendientes"
    elif tipo_accion == "registrar":
        accion="ha registrado"
        usuarios_ftc=User.objects.filter(perfil_usuario__categoria__nombre="especialista").exclude(id=request.user.id)
    elif tipo_accion == "pasar_a_pendientes_editar":
         accion="ha editado lo corregido en"
         usuarios_ftc=User.objects.filter(perfil_usuario__categoria__nombre="especialista").exclude(id=request.user.id)

    nombre=request.user.first_name+" "+request.user.last_name+" ("+request.user.perfil_usuario.organismo.siglas+")"
    texto_notificacion="%s %s el expediente referente al graduado %s"%(nombre,accion,expediente.graduado.nombre)
    usuarios_exp_liberado=User.objects.filter(perfil_usuario__organismo=expediente.organismo_liberacion,perfil_usuario__categoria__nombre="organismo").exclude(id=request.user.id)
    usuarios_exp_aceptado=User.objects.filter(perfil_usuario__organismo=expediente.organismo_aceptacion,perfil_usuario__categoria__nombre="organismo").exclude(id=request.user.id)
    usuarios=list(usuarios_exp_liberado)+list(usuarios_exp_aceptado)+list(usuarios_ftc)
    for user in usuarios:
       Notificacion.objects.create(
           emisor=request.user,
           remitente=user,
           texto=texto_notificacion
       )


def rechazar_expediente_pendiente(request,id_expediente_pend):
    if request.method=="POST":
     sintesis_rechazo=request.POST['causa_rechazo']
     expediente_pendiente=Expediente_pendiente.objects.get(id=id_expediente_pend)
     expediente_mov_externo=expediente_pendiente.expediente
     expediente_pendiente.delete()
     exp_rechazado=Expediente_rechazado(sintesis_rechazo=sintesis_rechazo, expediente=expediente_mov_externo)
     exp_rechazado.save()
     messages.add_message(request, messages.SUCCESS, "El expediente ha sido rechazado con éxito.")
     notificar_accion_expediente(request,"rechazar",exp_rechazado.expediente)
     data={'redirect':"/expedientes_pendientes"}
     return HttpResponse(json.dumps(data), content_type="application/json")

def rechazar_expediente_aprobado(request,id_expediente_aprob):
    if request.method=="POST":
     sintesis_rechazo=request.POST['causa_rechazo']
     expediente_aprobado=Expediente_aprobado.objects.get(id=id_expediente_aprob)
     expediente_mov_externo=expediente_aprobado.expediente
     expediente_aprobado.delete()
     exp_rechazado=Expediente_rechazado(sintesis_rechazo=sintesis_rechazo, expediente=expediente_mov_externo)
     exp_rechazado.save()
     messages.add_message(request, messages.SUCCESS, "El expediente ha sido rechazado con éxito.")
     notificar_accion_expediente(request,"rechazar",exp_rechazado.expediente)
     data={'redirect':"/expedientes_aprobados"}
     return HttpResponse(json.dumps(data), content_type="application/json")

def rechazar_expediente_no_aprobado(request,id_expediente_no_aprob):
    if request.method=="POST":
     sintesis_rechazo=request.POST['causa_rechazo']
     expediente_no_aprobado=Expediente_no_aprobado.objects.get(id=id_expediente_no_aprob)
     expediente_mov_externo=expediente_no_aprobado.expediente
     expediente_no_aprobado.delete()
     exp_rechazado=Expediente_rechazado(sintesis_rechazo=sintesis_rechazo, expediente=expediente_mov_externo)
     exp_rechazado.save()
     messages.add_message(request, messages.SUCCESS, "El expediente ha sido rechazado con éxito.")
     notificar_accion_expediente(request,"rechazar",exp_rechazado.expediente)
     data={'redirect':"/expedientes_no_aprobados"}
     return HttpResponse(json.dumps(data), content_type="application/json")

#no_aprobar-----------------------------------------------------------------------------------------------------
def no_aprobar_expediente_pendiente(request,id_expediente_pend):
    if request.method=="POST":
     sintesis_no_aprobado=request.POST['causa_no_aprobado']
     expediente_pendiente=Expediente_pendiente.objects.get(id=id_expediente_pend)
     expediente_mov_externo=expediente_pendiente.expediente
     expediente_pendiente.delete()
     exp_no_aprobado=Expediente_no_aprobado(sintesis_no_aprobado=sintesis_no_aprobado, expediente=expediente_mov_externo)
     exp_no_aprobado.save()
     messages.add_message(request, messages.SUCCESS, "El expediente ha sido no aprobado con éxito.")
     notificar_accion_expediente(request,"no_aprobar",exp_no_aprobado.expediente)
     data={'redirect':"/expedientes_pendientes"}
     return HttpResponse(json.dumps(data), content_type="application/json")

def no_aprobar_expediente_aprobado(request,id_expediente_aprob):
    if request.method=="POST":
     sintesis_no_aprobado=request.POST['causa_no_aprobado']
     expediente_aprobado=Expediente_aprobado.objects.get(id=id_expediente_aprob)
     expediente_mov_externo=expediente_aprobado.expediente
     expediente_aprobado.delete()
     exp_no_aprobado=Expediente_no_aprobado(sintesis_no_aprobado=sintesis_no_aprobado, expediente=expediente_mov_externo)
     exp_no_aprobado.save()
     messages.add_message(request, messages.SUCCESS, "El expediente ha sido no aprobado con éxito.")
     notificar_accion_expediente(request,"no_aprobar",exp_no_aprobado.expediente)
     data={'redirect':"/expedientes_aprobados"}
     return HttpResponse(json.dumps(data), content_type="application/json")

def no_aprobar_expediente_rechazado(request,id_expediente_rech):
    if request.method=="POST":
     sintesis_no_aprobado=request.POST['causa_no_aprobado']
     expediente_rechazado=Expediente_rechazado.objects.get(id=id_expediente_rech)
     expediente_mov_externo=expediente_rechazado.expediente
     expediente_rechazado.delete()
     exp_no_aprobado=Expediente_no_aprobado(sintesis_no_aprobado=sintesis_no_aprobado, expediente=expediente_mov_externo)
     exp_no_aprobado.save()
     messages.add_message(request, messages.SUCCESS, "El expediente ha sido no aprobado con éxito.")
     notificar_accion_expediente(request,"no_aprobar",exp_no_aprobado.expediente)
     data={'redirect':"/expedientes_rechazados"}
     return HttpResponse(json.dumps(data), content_type="application/json")

#Aprobar Expediente--------------------------------------------------------------------------------------------------
def aprobar_expediente_rechazado(request,id_expediente_rech):
    if request.method=="POST":
     registro_entrada="DE-RE "+unicode(request.POST['registro_entrada'])
     registro_salida="DE-RS "+unicode(request.POST['registro_salida'])
     fecha_aprobado=request.POST['fecha_aprobado']
     try:
        informe_expediente=request.FILES['informe_expediente']
     except:
        informe_expediente=None
     expediente_rechazado=Expediente_rechazado.objects.get(id=id_expediente_rech)
     expediente_mov_externo=expediente_rechazado.expediente
     if fecha_aprobado!="":
        exp_aprobado=Expediente_aprobado(carta_expediente=informe_expediente,codigo_DE_RE=registro_entrada,codigo_DE_RS=registro_salida,fecha_aprobado=fecha_aprobado,expediente=expediente_mov_externo)
     else:
        exp_aprobado=Expediente_aprobado(carta_expediente=informe_expediente,codigo_DE_RE=registro_entrada,codigo_DE_RS=registro_salida,expediente=expediente_mov_externo)
     procesar_expediente(request,registro_entrada,registro_salida,expediente_rechazado,exp_aprobado)
     notificar_accion_expediente(request,"aprobar",exp_aprobado.expediente)
     return redirect("/expedientes_rechazados")

def aprobar_expediente_no_aprobado(request,id_expediente_no_aprob):
    if request.method=="POST":
     registro_entrada="DE-RE "+unicode(request.POST['registro_entrada'])
     registro_salida="DE-RS "+unicode(request.POST['registro_salida'])
     fecha_aprobado=request.POST['fecha_aprobado']
     try:
        informe_expediente=request.FILES['informe_expediente']
     except:
        informe_expediente=None
     expediente_no_aprobado=Expediente_no_aprobado.objects.get(id=id_expediente_no_aprob)
     expediente_mov_externo=expediente_no_aprobado.expediente

     if fecha_aprobado!="":
        exp_aprobado=Expediente_aprobado(carta_expediente=informe_expediente,codigo_DE_RE=registro_entrada,codigo_DE_RS=registro_salida,fecha_aprobado=fecha_aprobado,expediente=expediente_mov_externo)
     else:
        exp_aprobado=Expediente_aprobado(carta_expediente=informe_expediente,codigo_DE_RE=registro_entrada,codigo_DE_RS=registro_salida,expediente=expediente_mov_externo)
     procesar_expediente(request,registro_entrada,registro_salida,expediente_no_aprobado,exp_aprobado)
     notificar_accion_expediente(request,"aprobar",exp_aprobado.expediente)
     return redirect("/expedientes_no_aprobados")

def aprobar_expediente_pendiente(request,id_expediente_pend):
    if request.method=="POST":
             registro_entrada="DE-RE "+unicode(request.POST['registro_entrada'])
             registro_salida="DE-RS "+unicode(request.POST['registro_salida'])
             fecha_aprobado=request.POST['fecha_aprobado']
             #informe_expediente=request.POST.get('informe_expediente', None)
             try:
                informe_expediente=request.FILES['informe_expediente']
             except:
                 informe_expediente=None
             expediente_pendiente=Expediente_pendiente.objects.get(id=id_expediente_pend)
             expediente_mov_externo=expediente_pendiente.expediente

             if fecha_aprobado!="":
                exp_aprobado=Expediente_aprobado(carta_expediente=informe_expediente,codigo_DE_RE=registro_entrada,codigo_DE_RS=registro_salida,fecha_aprobado=fecha_aprobado,expediente=expediente_mov_externo)
             else:
                exp_aprobado=Expediente_aprobado(carta_expediente=informe_expediente,codigo_DE_RE=registro_entrada,codigo_DE_RS=registro_salida,expediente=expediente_mov_externo)

             procesar_expediente(request,registro_entrada,registro_salida,expediente_pendiente,exp_aprobado)
             notificar_accion_expediente(request,"aprobar",exp_aprobado.expediente)
             return redirect("/expedientes_pendientes")



from datetime import date
def procesar_expediente(request,registro_entrada,registro_salida,expediente_input,expediente_output):
    if not Expediente_aprobado.objects.filter(codigo_DE_RS=registro_salida,fecha_aprobado__year=date.today().year):
            expediente_output.save()
            expediente_input.delete()
            try:
                notificacion_correo=request.POST['notificar_dir']
                if notificacion_correo == "on":
                    enviar_correo_exp_aprobado(expediente_output)
            except:
                pass
            messages.add_message(request, messages.SUCCESS, "El expediente ha sido aprobado con éxito.")
    else:
            cache.clear()
            messages.add_message(request, messages.ERROR, "El expediente con %s ya existe en la lista de aprobados"%registro_salida)


#otros----------------------------------------------------------------------------------------------------
def enviar_correo_exp_aprobado(expediente):
      prov_acept=expediente.expediente.mun_entidad_aceptacion.provincia
      asunto="Cambio de ubicación".decode('utf-8')
      cuerpo="Compañero(a): Proceder al cambio de ubicación del egresado. El organismo que libera, debe informarle al egresado que asista a la Dirección Provincial de Trabajo a recoger su nueva boleta." \
             " \n Saludos, \n Nota: Ver adjunto. \n \n Lic. Ana Eugenia González Ruizánchez. \n Especialista Superior en Gestión de los RH. \n FTC del MTSS.\n Telf. 7838 0008, ext. 2089."
      direccion=Direccion_trabajo.objects.get(provincia=prov_acept)
      destinatarios=["eugenia@mtss.cu"]
      if direccion.correo_director:
          destinatarios.append("%s"%direccion.correo_director)
      if direccion.correo_especialista:
          destinatarios.append("%s"%direccion.correo_especialista)
      if len(destinatarios)>1:
          email = EmailMessage(asunto, cuerpo,from_email="eugenia@mtss.cu", to=destinatarios)
          if expediente.carta_expediente:
             # email.attach(carta_expediente.name, carta_expediente.read(), carta_expediente.content_type)
              email.attach_file(expediente.carta_expediente.file.name)
              email.send()

def exportar_expediente(request,id_expediente,):
    expediente=Expediente_movimiento_externo.objects.get(id=id_expediente)
    rs=unicode("RS_"+request.POST['registro_salida'])
    ol=unicode(expediente.organismo_liberacion.siglas)
    pl=unicode(expediente.mun_entidad_liberacion.provincia.siglas)
    oa=unicode(expediente.organismo_aceptacion.siglas)
    pa=unicode(expediente.mun_entidad_aceptacion.provincia.siglas)
    ng=unicode(expediente.graduado.nombre).replace(" ","_")
    nombre_file=rs+"-"+ol+"-"+pl+"-"+oa+"-"+pa+"-"+ng
    nombre_file.replace(" ","_")
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="%s.pdf"'%nombre_file

    p = canvas.Canvas(response,pagesize=A4)
    PAGE_WIDTH = A4[0]
    PAGE_HEIGHT = A4[1]
    mes=get_nombre_mes(int(datetime.today().month))
    p.setTitle("informe_expediente")
    p.setFont("Times-Bold",15)
    title= "Ministerio del Trabajo y Seguridad Social"
    title2="Dirección de Empleo"

    fecha="La Habana, %s de %s de %s"%(datetime.today().day,mes,datetime.today().year)
    anno='\"%s\"' %(request.POST['nombre_anno'])
    provincia="%s"%expediente.mun_entidad_aceptacion.provincia.nombre
    dir_trabajo=Direccion_trabajo.objects.get(provincia__siglas=pa)
    nombre_funcionario=dir_trabajo.director
    p.drawString(162,770,title)
    p.drawString(232,750,title2)
    p.setFont("Times-Roman",14)
    p.drawString(60,710,fecha)
    p.drawString(60,690,anno)

    p.setFont("Times-Bold",14)
    p.drawString(60,660,"DE-RS-"+request.POST['registro_salida'])
    p.setFont("Times-Roman",14)

    try:
        sexo_funcionario=dir_trabajo.sexo_director
        if sexo_funcionario== "M":
            p.drawString(60,620,"Cro: %s"%(nombre_funcionario))
            p.drawString(60,604,"Director de Trabajo Provincial")
            p.drawString(60,555,"Estimado compañero:")
        else:
            p.drawString(60,620,"Cra: %s"%(nombre_funcionario))
            p.drawString(60,604,"Directora de Trabajo Provincial")
            p.drawString(50,555,"Estimada compañera:")

    except:
         p.drawString(60,620,"Cro: %s"%(nombre_funcionario))
         p.drawString(60,604,"Director de Trabajo Provincial")
         p.drawString(60,555,"Estimado compañero:")


    try:
        sexo_egresado=request.POST['sexo_egresado']

        if sexo_egresado == "M":
           texto1_egresado="El egresado"
           texto2_egresado="graduado"
           texto3_egresado="asignado"
           texto4_egresado="lo"

        else:
           texto1_egresado="La egresada"
           texto2_egresado="graduada"
           texto3_egresado="asignada"
           texto4_egresado="la"

    except:
         texto1_egresado="El egresado"
         texto2_egresado="graduado"
         texto3_egresado="asignado"
         texto4_egresado="lo"

    p.drawString(60,588,"%s"%(provincia))

    styles = getSampleStyleSheet()
    styleN = styles['Normal']
    styleN.alignment = TA_JUSTIFY
    styleN.leading=17
    styleN.fontName="Times-Roman"
    styleN.fontSize=14

    styleH = styles['Heading1']
    p.saveState()
    p.restoreState()
    curso1="%s-%s"%(int(expediente.graduado.anno_graduacion)-1,expediente.graduado.anno_graduacion)

    art_ent_lib="%s"%request.POST['art_ent_lib']
    if art_ent_lib == "":
        art_ent_lib = "la"

    art_ent_acep="%s"%request.POST['art_ent_acep']
    if art_ent_acep == "":
        art_ent_acep = "la"

    p2="Contamos con las cartas de ambos organismos, solicitando su reubicación. El organismo %s libera por %s." %(texto4_egresado,expediente.causal_movimiento)

    if expediente.mun_entidad_liberacion.provincia.nombre == expediente.mun_entidad_aceptacion.provincia.nombre:
        p_provincia_acept="en esta provincia."
    else:
        p_provincia_acept="en la provincia de %s."%expediente.mun_entidad_aceptacion.provincia.nombre

    if expediente.organismo_aceptacion.nombre.split(" ")[0].lower()=="cap" or expediente.organismo_aceptacion.nombre.split(" ")[0].lower()=="osde":
        p1="%s %s, %s de nivel superior de la especialidad %s, en el curso %s, fue %s a %s %s, entidad perteneciente al %s, en la provincia de %s."%(texto1_egresado,expediente.graduado.nombre,texto2_egresado,expediente.graduado.carrera.nombre,curso1,texto3_egresado,art_ent_lib,expediente.entidad_liberacion,expediente.organismo_liberacion.nombre,expediente.mun_entidad_liberacion.provincia.nombre)
        p3="Ponemos el caso a su disposición, para que se le efectúe el cambio de boleta hacia %s %s, perteneciente al %s, %s".decode('utf-8')%(art_ent_acep,expediente.entidad_aceptacion,expediente.organismo_aceptacion.nombre,p_provincia_acept)
    else:
        p1="%s %s, %s de nivel superior de la especialidad %s, en el curso %s, fue %s a %s %s, entidad perteneciente al OACE/OSDE %s, en la provincia de %s."%(texto1_egresado,expediente.graduado.nombre,texto2_egresado,expediente.graduado.carrera.nombre,curso1,texto3_egresado,art_ent_lib,expediente.entidad_liberacion,expediente.organismo_liberacion.nombre,expediente.mun_entidad_liberacion.provincia.nombre)
        p3="Ponemos el caso a su disposición, para que se le efectúe el cambio de boleta hacia %s %s, perteneciente al OACE/OSDE %s, %s".decode('utf-8')%(art_ent_acep,expediente.entidad_aceptacion,expediente.organismo_aceptacion.nombre,p_provincia_acept)

    P1 = Paragraph(p1,styleN)
    P2 = Paragraph(p2,styleN)
    P3 = Paragraph(p3,styleN)

    w, h =P1.wrap(470,PAGE_HEIGHT)
    w1,h1=P2.wrap(470,PAGE_HEIGHT)
    w2,h2=P3.wrap(470,PAGE_HEIGHT)
    P1.drawOn(p,60,450)
    P2.drawOn(p,60,385)
    P3.drawOn(p,60,315)
    p.setFont("Times-Roman",14)
    #p.drawImage(settings.BASE_DIR+"/SGMGU/static/img/firma.jpg",10,inch+30, width=400, height=200)
    p.drawString(60,inch+170,"Saludos,")
    p.drawString(60,inch+100,"Lic. Jesús Otamendiz Campos.")
    p.showPage()
    p.save()
    return response

def exportar_expediente_aprobado(request,id_expediente,):
    expediente=Expediente_movimiento_externo.objects.get(id=id_expediente)
    rs=unicode("RS_"+request.POST['registro_salida'])
    ol=unicode(expediente.organismo_liberacion.siglas)
    pl=unicode(expediente.mun_entidad_liberacion.provincia.siglas)
    oa=unicode(expediente.organismo_aceptacion.siglas)
    pa=unicode(expediente.mun_entidad_aceptacion.provincia.siglas)
    ng=unicode(expediente.graduado.nombre).replace(" ","_")
    nombre_file=rs+"-"+ol+"-"+pl+"-"+oa+"-"+pa+"-"+ng
    nombre_file.replace(" ","_")
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="%s.pdf"'%nombre_file

    p = canvas.Canvas(response,pagesize=A4)
    PAGE_WIDTH = A4[0]
    PAGE_HEIGHT = A4[1]
    mes=get_nombre_mes(int(datetime.today().month))
    p.setTitle("informe_expediente")
    p.setFont("Times-Bold",15)
    title= "Ministerio del Trabajo y Seguridad Social"
    title2="Dirección de Empleo"

    fecha="La Habana, %s de %s de %s"%(datetime.today().day,mes,datetime.today().year)
    anno='\"%s\"' %(request.POST['nombre_anno'])
    provincia="%s"%expediente.mun_entidad_aceptacion.provincia.nombre
    dir_trabajo=Direccion_trabajo.objects.get(provincia__siglas=pa)
    nombre_funcionario=dir_trabajo.director
    p.drawString(162,770,title)
    p.drawString(232,750,title2)
    p.setFont("Times-Roman",14)
    p.drawString(60,710,fecha)
    p.drawString(60,690,anno)

    p.setFont("Times-Bold",14)
    p.drawString(60,660,"DE-RS-"+request.POST['registro_salida'])
    p.setFont("Times-Roman",14)

    try:
        sexo_funcionario=dir_trabajo.sexo_director
        if sexo_funcionario== "M":
            p.drawString(60,620,"Cro: %s"%(nombre_funcionario))
            p.drawString(60,604,"Director de Trabajo Provincial")
            p.drawString(60,555,"Estimado compañero:")
        else:
            p.drawString(60,620,"Cra: %s"%(nombre_funcionario))
            p.drawString(60,604,"Directora de Trabajo Provincial")
            p.drawString(50,555,"Estimada compañera:")

    except:
         p.drawString(60,620,"Cro: %s"%(nombre_funcionario))
         p.drawString(60,604,"Director de Trabajo Provincial")
         p.drawString(60,555,"Estimado compañero:")


    try:
        sexo_egresado=request.POST['sexo_egresado']

        if sexo_egresado== "M":
           texto1_egresado="El egresado"
           texto2_egresado="graduado"
           texto3_egresado="asignado"
           texto4_egresado="lo"

        else:
           texto1_egresado="La egresada"
           texto2_egresado="graduada"
           texto3_egresado="asignada"
           texto4_egresado="la"

    except:
         texto1_egresado="El egresado"
         texto2_egresado="graduado"
         texto3_egresado="asignado"
         texto4_egresado="lo"

    p.drawString(60,588,"%s"%(provincia))

    styles = getSampleStyleSheet()
    styleN = styles['Normal']
    styleN.alignment = TA_JUSTIFY
    styleN.leading=17
    styleN.fontName="Times-Roman"
    styleN.fontSize=14

    styleH = styles['Heading1']
    p.saveState()
    p.restoreState()
    curso1="%s-%s"%(int(expediente.graduado.anno_graduacion)-1,expediente.graduado.anno_graduacion)

    art_ent_lib="%s"%request.POST['art_ent_lib']
    if art_ent_lib == "":
        art_ent_lib = "la"

    art_ent_acep="%s"%request.POST['art_ent_acep']
    if art_ent_acep == "":
        art_ent_acep = "la"

    p2="Contamos con las cartas de ambos organismos, solicitando su reubicación. El organismo %s libera por %s." %(texto4_egresado,expediente.causal_movimiento)

    if expediente.mun_entidad_liberacion.provincia.nombre == expediente.mun_entidad_aceptacion.provincia.nombre:
        p_provincia_acept="en esta provincia."
    else:
        p_provincia_acept="en la provincia de %s."%expediente.mun_entidad_aceptacion.provincia.nombre

    if expediente.organismo_aceptacion.nombre.split(" ")[0].lower()=="cap" or expediente.organismo_aceptacion.nombre.split(" ")[0].lower()=="osde":
        p1="%s %s, %s de nivel superior de la especialidad %s, en el curso %s, fue %s a %s %s, entidad perteneciente al %s, en la provincia de %s."%(texto1_egresado,expediente.graduado.nombre,texto2_egresado,expediente.graduado.carrera.nombre,curso1,texto3_egresado,art_ent_lib,expediente.entidad_liberacion,expediente.organismo_liberacion.nombre,expediente.mun_entidad_liberacion.provincia.nombre)
        p3="Ponemos el caso a su disposición, para que se le efectúe el cambio de boleta hacia %s %s, perteneciente al %s, %s".decode('utf-8')%(art_ent_acep,expediente.entidad_aceptacion,expediente.organismo_aceptacion.nombre,p_provincia_acept)
    else:
        p1="%s %s, %s de nivel superior de la especialidad %s, en el curso %s, fue %s a %s %s, entidad perteneciente al OACE/OSDE %s, en la provincia de %s."%(texto1_egresado,expediente.graduado.nombre,texto2_egresado,expediente.graduado.carrera.nombre,curso1,texto3_egresado,art_ent_lib,expediente.entidad_liberacion,expediente.organismo_liberacion.nombre,expediente.mun_entidad_liberacion.provincia.nombre)
        p3="Ponemos el caso a su disposición, para que se le efectúe el cambio de boleta hacia %s %s, perteneciente al OACE/OSDE %s, %s".decode('utf-8')%(art_ent_acep,expediente.entidad_aceptacion,expediente.organismo_aceptacion.nombre,p_provincia_acept)

    P1 = Paragraph(p1,styleN)
    P2 = Paragraph(p2,styleN)
    P3 = Paragraph(p3,styleN)

    w, h =P1.wrap(470,PAGE_HEIGHT)
    w1,h1=P2.wrap(470,PAGE_HEIGHT)
    w2,h2=P3.wrap(470,PAGE_HEIGHT)
    P1.drawOn(p,60,450)
    P2.drawOn(p,60,385)
    P3.drawOn(p,60,315)
    p.setFont("Times-Roman",14)
    p.drawImage(settings.BASE_DIR+"/SGMGU/static/img/firma.jpg",10,inch+30, width=400, height=200)
    p.showPage()
    p.save()
    return response


def get_nombre_mes(numero_mes):
    if numero_mes == 1:
        return "enero"
    elif numero_mes == 2:
        return "febrero"
    elif numero_mes == 3:
        return "marzo"
    elif numero_mes == 4:
        return "abril"

    elif numero_mes == 5:
        return "mayo"

    elif numero_mes == 6:
        return "junio"

    elif numero_mes == 7:
        return "julio"

    elif numero_mes == 8:
        return "agosto"

    elif numero_mes == 9:
        return "septiembre"

    elif numero_mes == 10:
        return "octubre"


    elif numero_mes == 11:
        return "noviembre"

    else:
        return "diciembre"







