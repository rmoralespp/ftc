# -*- coding: utf-8 -*-

from django.shortcuts import render,redirect,get_object_or_404,get_list_or_404
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required,permission_required
from SGMGU.forms import *
from SGMGU.models import *
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger,InvalidPage
from django.core.cache import cache
from .utiles import *




#@cache_per_user(ttl=3600, cache_post=False)
def movimientos_internos(request):
    perfil=Perfil_usuario.objects.get(usuario=request.user)
    foto=perfil.foto
    organismo=perfil.organismo

    if perfil.categoria.nombre == "organismo":
       movimientos_internos=paginar(request,Expediente_movimiento_interno.objects.filter(organismo=organismo).order_by("-fecha_registro"))
    else:
      movimientos_internos=paginar(request,Expediente_movimiento_interno.objects.all().order_by("-fecha_registro"))
    context = {'categoria':perfil.categoria.nombre,'foto':foto,'expedientes':movimientos_internos,'paginas':crear_lista_pages(movimientos_internos)}
    return render(request, "MovimietosInternos/movimientos_internos.html", context)


#Busqueda---------------------------------------------------------------------------------------------------------------
@login_required
def buscar_movimientos_internos_ci(request,ci):
  expedientes=paginar(request,Expediente_movimiento_interno.objects.filter(graduado__ci=ci).order_by("-fecha_registro"))
  context={'expedientes':expedientes,'busqueda':'si','termino_busqueda':'por CI',"valor_busqueda":ci,'paginas':crear_lista_pages(expedientes)}
  return render(request, "MovimietosInternos/movimientos_internos.html", context)



@login_required
def eliminar_movimiento_interno(request,id_expediente):
    exp=Expediente_movimiento_interno.objects.get(id=id_expediente)
    graduado=exp.graduado
    exp.delete()
    graduado.delete()
    messages.add_message(request, messages.SUCCESS, "El movimiento ha sido eliminado con éxito.")
    return redirect("/movimientos_internos")





@login_required
def modificar_movimiento_interno(request,id_expediente):
    expediente=Expediente_movimiento_interno.objects.get(id=id_expediente)
    perfil=Perfil_usuario.objects.get(usuario=request.user)
    foto=perfil.foto

    if request.method == 'POST':
       form=RegistroMovimientoInternoForm(request.POST,request.FILES)
       if form.is_valid():
            nombre_graduado=form.cleaned_data['nombre_graduado']
           # apellidos_graduado=form.cleaned_data['apellidos_graduado']
            carrera_graduado=form.cleaned_data['carrera_graduado']
            anno_graduacion=form.cleaned_data['anno_graduacion']
            codigo_boleta=form.cleaned_data['codigo_boleta']
            imagen_boleta=form.cleaned_data['imagen_boleta']
            entidad_liberacion=form.cleaned_data['entidad_liberacion']
            entidad_aceptacion=form.cleaned_data['entidad_aceptacion']
            aprobado=form.cleaned_data['aprobado']
            municipio_entidad_liberacion=form.cleaned_data['municipio_entidad_liberacion']
            municipio_entidad_aceptacion=form.cleaned_data['municipio_entidad_aceptacion']
            causal_movimiento=form.cleaned_data['causal_movimiento']
            sintesis_causal_movimiento=form.cleaned_data['sintesis_causal_movimiento']
            detalle_direccion_residencia=form.cleaned_data['detalle_direccion_residencia']
            centro_estudio=form.cleaned_data['centro_estudio']
            municipio_residencia=form.cleaned_data['municipio_residencia']
            ci=form.cleaned_data['ci']

            expediente.graduado.nombre=nombre_graduado
          #  expediente.graduado.apellidos=apellidos_graduado
            expediente.graduado.carrera=carrera_graduado
            expediente.graduado.anno_graduacion=anno_graduacion
            expediente.graduado.detalle_direccion_residencia=detalle_direccion_residencia
            expediente.graduado.ci=ci
            expediente.graduado.codigo_boleta=codigo_boleta
            expediente.graduado.imagen_boleta=imagen_boleta
            expediente.graduado.centro_estudio=centro_estudio
            expediente.graduado.municipio_direccion_residencia=municipio_residencia
            expediente.graduado.provincia_direccion_residencia=municipio_residencia.provincia
            expediente.graduado.save()

            expediente.aprobado_por=aprobado
            expediente.entidad_liberacion=entidad_liberacion
            expediente.entidad_aceptacion=entidad_aceptacion
            expediente.mun_entidad_liberacion= municipio_entidad_liberacion
            expediente.mun_entidad_aceptacion=municipio_entidad_aceptacion
            expediente.causal_movimiento=causal_movimiento
            expediente.sintesis_causal_movimiento=sintesis_causal_movimiento

            expediente.save()
            messages.add_message(request, messages.SUCCESS, "El movimiento ha sido modificado con éxito.")
            return redirect("/movimientos_internos")

    else:
        form = RegistroMovimientoInternoForm(
        { 'nombre_graduado':expediente.graduado.nombre,
       # 'apellidos_graduado':expediente.graduado.apellidos,
        'carrera_graduado':expediente.graduado.carrera.id,
        'anno_graduacion':expediente.graduado.anno_graduacion,
        'codigo_boleta':expediente.graduado.codigo_boleta,
        'imagen_boleta':expediente.graduado.imagen_boleta,
        'entidad_liberacion':expediente.entidad_liberacion,
        'entidad_aceptacion':expediente.entidad_aceptacion,
        'aprobado':expediente.aprobado_por,
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

    # Creamos el contexto
    context = {'foto':foto,'form':form,'categoria':perfil.categoria.nombre}
    # Y mostramos los datos
    return render(request, "MovimietosInternos/modificar_movimiento_interno.html", context)




@login_required
def registrar_movimiento_interno(request):
    foto=""
    if request.user.is_authenticated():
         perfil=Perfil_usuario.objects.get(usuario=request.user)
         foto=perfil.foto
    if request.method == 'POST':
        form=RegistroMovimientoInternoForm(request.POST,request.FILES)
        if form.is_valid():
            nombre_graduado=form.cleaned_data['nombre_graduado']
           # apellidos_graduado=form.cleaned_data['apellidos_graduado']
            carrera_graduado=form.cleaned_data['carrera_graduado']
            anno_graduacion=form.cleaned_data['anno_graduacion']
            codigo_boleta=form.cleaned_data['codigo_boleta']
            imagen_boleta=form.cleaned_data['imagen_boleta']
            entidad_liberacion=form.cleaned_data['entidad_liberacion']
            entidad_aceptacion=form.cleaned_data['entidad_aceptacion']
            aprobado=form.cleaned_data['aprobado']
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
              #  apellidos=apellidos_graduado,
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
            expediente=Expediente_movimiento_interno(
                graduado=graduado,
                organismo=perfil.organismo,
                aprobado_por=aprobado,
                entidad_liberacion=entidad_liberacion,
                entidad_aceptacion=entidad_aceptacion,
                mun_entidad_liberacion= municipio_entidad_liberacion,
                mun_entidad_aceptacion=municipio_entidad_aceptacion,
                causal_movimiento=causal_movimiento,
                sintesis_causal_movimiento=sintesis_causal_movimiento,
            )

            expediente.save()
            messages.add_message(request, messages.SUCCESS, "El movimiento ha sido registrado con éxito.")

            return redirect("/movimientos_internos")

    else:
        form = RegistroMovimientoInternoForm()
    # Creamos el contexto
    context = {'foto':foto,'form':form,'categoria':perfil.categoria.nombre}
    # Y mostramos los datos
    return render(request, "MovimietosInternos/registrar_movimiento_interno.html", context)



