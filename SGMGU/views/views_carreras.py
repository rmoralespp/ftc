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
def gestion_carreras(request):
    carreras=Carrera.objects.filter(activo=True)
    context = {'carreras': carreras}
    return render(request, "carreras/gestion_carreras.html", context)

@login_required
@permission_required(['administrador','especialista'])
def registrar_carrera(request):
    if request.method == 'POST':
        form=RegistrarCarreraForm(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, "La carrera ha sido registrada con éxito.")
            return redirect('/carreras')
    else:
        form = RegistrarCarreraForm()
    context = {'form':form}
    return render(request, "carreras/registrar_carrera.html", context)


@login_required
@permission_required(['administrador','especialista'])
def modificar_carrera(request,id_carrera):
    carrera=Carrera.objects.get(id=id_carrera)
    if request.method == 'POST':
        form=RegistrarCarreraForm(reques.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, "La carrera ha sido modificada con éxito.")
            return redirect('/carreras')
    else:
        form = RegistrarCarreraForm(instance=carrera)
    # Creamos el contexto
    context = {'form':form}
    # Y mostramos los datos
    return render(request, "carreras/modificar_carrera.html", context)



@login_required
@permission_required(['administrador','especialista'])
def eliminar_carrera(request,id_carrera):
    carrera=Carrera.objects.get(id=id_carrera)
    carrera.activo=False
    carrera.save()
    messages.add_message(request, messages.SUCCESS, "La carrera ha sido eliminada con éxito.")
    return redirect('/carreras')
