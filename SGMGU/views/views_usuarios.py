# -*- coding: utf-8 -*-
__author__ = 'Rolando.Morales'


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
def eliminar_usuario(request,id_usuario):
    usuario=User.objects.get(id=id_usuario)
    perfil=Perfil_usuario.objects.get(usuario=usuario)
    perfil.activo=False
    perfil.save()
    messages.add_message(request, messages.SUCCESS, "El usuario ha sido eliminado con éxito.")
    return redirect('/usuarios')



@login_required
@permission_required(['administrador','especialista'])
def registrar_usuario(request):
    if request.method == 'POST':
        form = RegistroUserForm(request.POST, request.FILES)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            username = cleaned_data.get('username')
            password = cleaned_data.get('password')
            first_name = cleaned_data.get('first_name')
            last_name = cleaned_data.get('last_name')
            email = cleaned_data.get('email')
            photo = cleaned_data.get('foto')
            telefono = cleaned_data.get('telefono')
            organismo = cleaned_data.get('organismo')
            categoria = cleaned_data.get('categoria')
            provincia = cleaned_data.get('provincia')
            user_model = User.objects.create_user(username=username, password=password)
            user_model.email = email
            user_model.first_name=first_name
            user_model.last_name=last_name
            user_model.save()
            user_profile = Perfil_usuario()
            user_profile.usuario = user_model
            user_profile.foto = photo
            user_profile.telefono = telefono
            user_profile.organismo=organismo
            user_profile.categoria=categoria
            user_profile.provincia=provincia
            user_profile.save()
            messages.add_message(request, messages.SUCCESS, "El usuario ha sido registrado con éxito.")
            return redirect('/usuarios')
    else:

        form = RegistroUserForm()
    context = {'foto':Perfil_usuario.objects.get(usuario=request.user).foto,'form':form}
    return render(request, "Usuarios/registrar_usuario.html", context)


#-------------------------------------------------

from django.contrib.auth import authenticate,login

@login_required
def cambiar_contrasenna_user_actual(request):
     if request.method=='POST':
          form=ModificarContrasennaUserForm(request.POST)
          if form.is_valid():
               cleaned_data = form.cleaned_data
               usuario=User.objects.get(id=request.user.id)
               passowrd=cleaned_data.get('password')
               usuario.set_password(passowrd)
               usuario.save()
               return redirect('/inicio')
     else:
         form=ModificarContrasennaUserForm()
     context = {'form':form}
     return render(request, "Usuarios/cambiar_contrasenna_user_actual.html",context)



@login_required
def modificar_usuario_actual(request):
    user_model=User.objects.get(id=request.user.id)
    user_profile = Perfil_usuario.objects.get(usuario=user_model)

    if request.method == 'POST':
        form = ModificarUserFormActual(request.POST,instance=user_model)
        form_perfil=ModificarUserPerfilFormActual(request.POST,request.FILES,instance=user_profile)
        if form.is_valid() and form_perfil.is_valid():
            cleaned_data = form.cleaned_data
            cleaned_data2 = form_perfil.cleaned_data
            first_name = cleaned_data.get('first_name')
            last_name = cleaned_data.get('last_name')
            email = cleaned_data.get('email')
            photo = cleaned_data2.get('foto')
            telefono = cleaned_data2.get('telefono')
            user_model.email = email
            user_model.first_name=first_name
            user_model.last_name=last_name
            user_profile.foto = photo
            user_profile.telefono = telefono
            user_model.save()
            user_profile.save()
            #messages.add_message(request, messages.SUCCESS, "El usuario ha sido modificado con éxito.")
            return redirect('/inicio')

    form = ModificarUserFormActual(instance=user_model)
    user_profile = Perfil_usuario.objects.get(usuario=user_model)
    form_perfil=ModificarUserPerfilFormActual(instance=user_profile)

    context = {'form':form,'form_perfil':form_perfil}
    return render(request, "Usuarios/modificar_usuario_actual.html", context)

#-----------------------------------------------------------------------------------

@login_required
@permission_required(['administrador','especialista'])
def cambiar_contrasenna(request,id_usuario):
     if request.method=='POST':
          form=ModificarContrasennaUserForm(request.POST)
          if form.is_valid():
               cleaned_data = form.cleaned_data
               usuario=User.objects.get(id=id_usuario)
               passowrd=cleaned_data.get('password')
               usuario.set_password(passowrd)
               usuario.save()
               messages.add_message(request, messages.SUCCESS, "La contrasenna ha sido modificada con éxito.")
               return redirect('/usuarios')
     else:
         form=ModificarContrasennaUserForm()
     context = {'form':form}
     return render(request, "Usuarios/cambiar_contrasenna.html",context)



@login_required
@permission_required(['administrador','especialista'])
def modificar_usuario(request,id_usuario):
    user_model=User.objects.get(id=id_usuario)
    user_profile = Perfil_usuario.objects.get(usuario=user_model)

    if request.method == 'POST':
        form = ModificarUserForm(request.POST,instance=user_model)
        form_perfil=ModificarUserPerfilForm(request.POST,request.FILES,instance=user_profile)
        if form.is_valid() and form_perfil.is_valid():
            cleaned_data = form.cleaned_data
            cleaned_data2 = form_perfil.cleaned_data

            username = cleaned_data.get('username')
            first_name = cleaned_data.get('first_name')
            last_name = cleaned_data.get('last_name')
            email = cleaned_data.get('email')
            photo = cleaned_data2.get('foto')
            telefono = cleaned_data2.get('telefono')
            organismo = cleaned_data2.get('organismo')
            categoria = cleaned_data2.get('categoria')
            user_model.username=username
            user_model.email = email
            user_model.first_name=first_name
            user_model.last_name=last_name
            user_profile.foto = photo
            user_profile.telefono = telefono
            user_profile.organismo=organismo
            user_profile.categoria=categoria
            user_model.save()
            user_profile.save()
            messages.add_message(request, messages.SUCCESS, "El usuario ha sido modificado con éxito.")
            return redirect('/usuarios')

    form = ModificarUserForm(instance=user_model)
    user_profile = Perfil_usuario.objects.get(usuario=id_usuario)
    form_perfil=ModificarUserPerfilForm(instance=user_profile)
    context = {'form':form,'form_perfil':form_perfil}
    return render(request, "Usuarios/modificar_usuario.html", context)


@login_required
@permission_required(['administrador','especialista'])
def gestion_usuarios(request):
    usuarios=User.objects.filter(perfil_usuario__activo=True)
    context = {'usuarios': usuarios}
    return render(request, "Usuarios/gestion_usuarios.html", context)




