# -*- coding: utf-8 -*-
from django.shortcuts import render,redirect
from SGMGU.models import *
from SGMGU.forms import *
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .utiles import *
from django.http import HttpResponse,Http404
from django.db.models import Q
from django.db import models


@login_required
@permission_required(['administrador','especialista'])
def buscar_carreras(request):
    if request.method == "POST":
        texto=request.POST['texto_carrera'].lower()

        carreras=Carrera.objects.filter(activo=True,nombre__icontains=texto)
    else:
        carreras=[]
    carreras=paginar(request,carreras)
    context = {'carreras': carreras,'paginas':crear_lista_pages(carreras),'busqueda':True, 'texto':request.POST['texto_carrera']}
    return render(request, "Carreras/gestion_carreras.html", context)





@login_required
@permission_required(['administrador','especialista'])
def gestion_carreras(request):
    carreras=Carrera.objects.filter(activo=True)
    carreras=paginar(request,carreras)
    context = {'carreras': carreras,'paginas':crear_lista_pages(carreras)}
    return render(request, "Carreras/gestion_carreras.html", context)

@login_required
@permission_required(['administrador','especialista'])
def registrar_carrera(request):
    if request.method == 'POST':
        form=CarreraForm(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, "La carrera se ha registrado con éxito.")
            return redirect('/carreras')
    else:
        form = CarreraForm()
    context = {'form':form,'nombre_accion':'Registrar'}
    return render(request, "carreras/form_carrera.html", context)


@login_required
@permission_required(['administrador','especialista'])
def modificar_carrera(request,id_carrera):
    carrera=Carrera.objects.get(id=id_carrera)
    if request.method == 'POST':
        form=CarreraForm(request.POST,instance=carrera)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, "La carrera se ha modificado con éxito.")
            return redirect('/carreras')
    else:
        form = CarreraForm(instance=carrera)
    # Creamos el contexto
    context = {'form':form,'nombre_accion':'Modificar'}
    # Y mostramos los datos
    return render(request, "carreras/form_carrera.html", context)



@login_required
@permission_required(['administrador','especialista'])
def eliminar_carrera(request,id_carrera):
    carrera=Carrera.objects.get(id=id_carrera)
    carrera.activo=False
    carrera.save()
    messages.add_message(request, messages.SUCCESS, "La carrera ha sido eliminada con éxito.")
    return redirect('/carreras')



