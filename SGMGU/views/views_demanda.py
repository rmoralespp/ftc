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
    carreras=paginar(request,carreras)
    context = {'carreras': carreras,'paginas':crear_lista_pages(carreras)}
    return render(request, "Carreras/gestion_carreras.html", context)






