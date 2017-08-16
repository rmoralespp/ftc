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
def gestion_centros_estudios(request):
    centro_estudio=Centro_estudio.objects.filter(activo=True)
    context = {'centros_estudios': centros_estudios}
    return render(request, "centros_estudios/gestion_centro_estudios.html", context)

@login_required
@permission_required(['administrador','especialista'])
def registrar_centro_estudios(request):
    if request.method == 'POST':
        form=RegistrarCentroEstudioForm(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, "El centro de estudios ha sido registrado con éxito.")
            return redirect('/centros_estudios')
    else:
        form = RegistrarCentroEstudioForm()
    context = {'form':form}
    return render(request, "centros_estudios/registrar_centro_estudios.html", context)


@login_required
@permission_required(['administrador','especialista'])
def modificar_centro_estudios(request,id_centro_estudio):
    centros_estudios=Centro_estudio.objects.get(id=id_centro_estudio)
    if request.method == 'POST':
        form=RegistrarCentroEstudioForm(reques.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, "El centro de estudios ha sido modificado con éxito.")
            return redirect('/centros_estudios')
    else:
        form = RegistrarCentroEstudioForm(instance=centro_estudio)
    # Creamos el contexto
    context = {'form':form}
    # Y mostramos los datos
    return render(request, "centros_estudios/modificar_centro_estudios.html", context)



@login_required
@permission_required(['administrador','especialista'])
def eliminar_centro_estudios(request,id_centro_estudios):
    centro_estudios=Centro_estudio.objects.get(id=id_centro_estudios)
    centro_estudios.activo=False
    centro_estudios.save()
    messages.add_message(request, messages.SUCCESS, "El centro de estudios ha sido eliminado con éxito.")
    return redirect('/centros_estudios')
