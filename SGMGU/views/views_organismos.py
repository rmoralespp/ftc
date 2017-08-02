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
def gestion_organismos(request):
    organismos=Organismo.objects.filter(activo=True)
    context = {'organismos': organismos}
    return render(request, "Organismos/gestion_organismos.html", context)


@login_required
@permission_required(['administrador','especialista'])
def registrar_organismo(request):
    if request.method == 'POST':
        form=RegistrarOrganismoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, "El organismo ha sido registrado con éxito.")
            return redirect('/organismos')
    else:
        form = RegistrarOrganismoForm()
    context = {'form':form}
    return render(request, "Organismos/registrar_organismo.html", context)



@login_required
@permission_required(['administrador','especialista'])
def modificar_organismo(request,id_organismo):
    organismo=Organismo.objects.get(id=id_organismo)
    if request.method == 'POST':
        form=RegistrarOrganismoForm(request.POST,instance=organismo)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, "El organismo ha sido modificado con éxito.")
            return redirect('/organismos')
    else:
        form = RegistrarOrganismoForm(instance=organismo)
    # Creamos el contexto
    context = {'form':form}
    # Y mostramos los datos
    return render(request, "Organismos/modificar_organismo.html", context)



@login_required
@permission_required(['administrador','especialista'])
def eliminar_organismo(request,id_organismo):
    organismo=Organismo.objects.get(id=id_organismo)
    organismo.activo=False
    organismo.save()
    messages.add_message(request, messages.SUCCESS, "El organismo ha sido eliminado con éxito.")
    return redirect('/organismos')







