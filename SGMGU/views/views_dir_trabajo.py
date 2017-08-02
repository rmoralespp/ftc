# -*- coding: utf-8 -*-
from SGMGU.models import Direccion_trabajo
from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from SGMGU.forms import *
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
def gestion_dir_trabajo(request):
    direcciones=Direccion_trabajo.objects.filter(activo=True)
    context = {'direcciones': direcciones}
    return render(request, "DireccionesTrabajo/gestion_dir_trabajo.html", context)



@login_required
@permission_required(['administrador','especialista'])
def modificar_dir_trabajo(request,id_dir):
    dir=Direccion_trabajo.objects.get(id=id_dir)
    if request.method == 'POST':
        form=ModificarDireccionTrabajo(request.POST,instance=dir)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, "La dirección de trabajo ha sido modificada con éxito.")
            return redirect('/direcciones_trabajo')
    else:
        form = ModificarDireccionTrabajo(instance=dir)
    # Creamos el contexto
    context = {'form':form}
    # Y mostramos los datos
    return render(request, "DireccionesTrabajo/modificar_dir_trabajo.html", context)

