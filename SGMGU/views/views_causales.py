# -*- coding: utf-8 -*-

from django.shortcuts import render,redirect,get_object_or_404,get_list_or_404
from django.contrib.auth.decorators import login_required
from SGMGU.forms import *
from SGMGU.models import *
from django.contrib import messages


def permission_required(lista_categorias_permitidas):
    def _permission_required(function):
        def apply_function(request,*args, **kwargs):
            if lista_categorias_permitidas.__contains__(request.user.perfil_usuario.categoria.nombre):
                return function(request,*args, **kwargs)
            else:
                return redirect("/inicio")
        return apply_function
    return _permission_required

@login_required
@permission_required(['administrador','especialista'])
def gestion_causales(request):
    causales=Causal_movimiento.objects.filter(activo=True)
    context = {'causales': causales}
    return render(request, "Causales/gestion_causales.html", context)

@login_required
@permission_required(['administrador','especialista'])
def registrar_causal(request):
    if request.method == 'POST':
        form=RegistrarCausalForm(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, "La causal ha sido registrada con éxito.")
            return redirect('/causales')
    else:
        form = RegistrarCausalForm()
    context = {'form':form}
    return render(request, "Causales/registrar_causal.html", context)



@login_required
@permission_required(['administrador','especialista'])
def modificar_causal(request,id_causal):
    causal=Causal_movimiento.objects.get(id=id_causal)
    if request.method == 'POST':
        form=RegistrarCausalForm(request.POST,instance=causal)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, "La causal ha sido modificada con éxito.")
            return redirect('/causales')
    else:
        form = RegistrarCausalForm(instance=causal)
    context = {'form':form}
    return render(request, "Causales/modificar_causal.html", context)



@login_required
@permission_required(['administrador','especialista'])
def eliminar_causal(request,id_causal):
    causal=Causal_movimiento.objects.get(id=id_causal)
    causal.activo=False
    causal.save()
    messages.add_message(request, messages.SUCCESS, "La causal ha sido eliminada con éxito.")
    return redirect('/causales')





