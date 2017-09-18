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

#para buscar entre las entidades



#para imprimir en la tabla las entidades

@login_required
@permission_required(['administrador','especialista'])
def gestion_entidades(request):
    entidades=Entidad.objects.filter(activo=True)
    entidades=paginar(request,entidades)
    context = {'entidades': entidades,'paginas':crear_lista_pages(entidades)}
    return render(request, "Entidades/gestion_entidades.html", context)