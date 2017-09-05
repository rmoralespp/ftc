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
def gestion_demanda(request):
    demandas=DemandaGraduados.objects.filter(activo=True)
    demandas=paginar(request,demandas)
    context = {'demandas': demandas,'paginas':crear_lista_pages(demandas)}
    return render(request, "Demandas/gestion_demanda.html", context)






