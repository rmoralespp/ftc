# -*- coding: utf-8 -*-
from django.shortcuts import render,redirect
from SGMGU.models import *
from SGMGU.forms import *
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .utiles import *
import datetime

from  django.http import  HttpResponse

def indicaciones(request,id_categoria=None):
    if id_categoria == None:
         indicaciones=Indicacion.objects.all()
         filtro='Indicaciones'
    else:
         indicaciones=Indicacion.objects.filter(categoria__id=id_categoria)
         id_categoria=int(id_categoria)

         filtro='Indicaciones sobre '+CategoriaIndicacion.objects.get(id=id_categoria).nombre

    categorias=CategoriaIndicacion.objects.all().order_by('nombre')
    indicaciones=paginar(request,indicaciones)

    contexto={
        'categorias':categorias,
        'id_categoria_actual':id_categoria,
        'indicaciones':indicaciones,
        'paginas':crear_lista_pages(indicaciones),
        'filtro':filtro
    }
    return render(request,'Indicaciones/listado.html',contexto)




def download_indicacion(request,id_indicacion):
    indicacion=Indicacion.objects.get(id=id_indicacion)
    if indicacion.fichero:
        filename = unicode(indicacion.fichero.name.split('/')[-1])
        response = HttpResponse(indicacion.fichero.file, content_type='text/plain')
        response['Content-Disposition'] = 'attachment; filename=%s' % filename
        return response
    else:
        redirect("/indicaciones")



@login_required
def eliminar_indicacion(request, id_indicacion):
    try:
      indicacion=Indicacion.objects.get(id=id_indicacion)
      indicacion.delete()
    except:
       pass
    return redirect("/indicaciones")

@login_required
def registrar_indicacion(request):
    if request.method == "POST":
        form=IndicacionForm(request.POST,request.FILES)
        if form.is_valid():
            indicacion=form.save(commit=False)
            indicacion.autor=request.user
            indicacion.save()
            return redirect("/indicaciones")

    else:
        form=IndicacionForm()
    contexto={'form':form,"nombre":"Registrar nueva indicacion"}
    return render(request, "Indicaciones/form_indicacion.html", contexto)

@login_required
def registar_castegoria_indicacion(request):
    if request.method == "POST":
        form=CategoriaIndicacionForm(request.POST)
        if form.is_valid():
            indicacion=form.save(commit=False)
            indicacion.autor=request.user
            indicacion.save()
            return redirect("/indicaciones")

    else:
        form=CategoriaIndicacionForm()
    contexto={'form':form,"nombre":"Registrar nueva categoria"}
    return render(request, "Indicaciones/form_indicacion.html", contexto)



@login_required
def editar_indicacion(request,id_indicacion):
        indicacion=Indicacion.objects.get(id=id_indicacion)
        if request.method== "POST":
            form=IndicacionForm(request.POST,request.FILES,instance=indicacion)
            if form.is_valid():
                form.save()
                return  redirect("/indicaciones")

        else:
            form=IndicacionForm(instance=indicacion)
        contexto={  'form':form,
                    "nombre":"Editar indicacion"
                      }
        return render(request, "Indicaciones/form_indicacion.html", contexto)



