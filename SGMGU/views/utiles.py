# -*- coding: utf-8 -*-
from django.shortcuts import render,redirect
from django.core.paginator import Paginator, EmptyPage,InvalidPage
from django.views.decorators.cache import cache_page,cache_control
from django.core.cache import cache

def crear_lista_pages(listado):
    izquiera=1
    derecha=listado.paginator.num_pages
    pagina_actual=listado.number

    if pagina_actual > 3:
        izquiera=pagina_actual-2
    if derecha-pagina_actual>3:
        derecha=pagina_actual+2
    final=list(range(izquiera,derecha+1))
    if izquiera!=1:
        final.insert(0,1)
    if derecha != listado.paginator.num_pages:
        final.append(listado.paginator.num_pages)
    return final

def paginar(request,lista_objetos):
    paginator=Paginator(lista_objetos,10)
    try:
        pagina=int(request.GET.get("pagina","1"))
    except ValueError:
        pagina=1
    try:
        lista_objetos=paginator.page(pagina)
    except(InvalidPage, EmptyPage):
        lista_objetos=paginator.page(paginator.num_pages)
    return lista_objetos


def permission_required(lista_categorias_permitidas):
    def _permission_required(function):
        def apply_function(request,*args, **kwargs):
            if lista_categorias_permitidas.__contains__(request.user.perfil_usuario.categoria.nombre):
                return function(request,*args, **kwargs)
            else:
                return redirect("/inicio")
        return apply_function
    return _permission_required


def cache_por_user(ttl=None, prefix=None, cache_post=False):
    def decorator(function):
        def apply_cache(request, *args, **kwargs):
            if request.user.is_anonymous():
                user = 'anonymous'
            else:
                user = request.user.id
            try:
                pagina=int(request.GET.get("pagina","1"))
            except ValueError:
                pagina=1

            if prefix:
                CACHE_KEY = '%s_%s_%s'%(prefix, user,pagina)
            else:
                CACHE_KEY = 'view_cache_%s_%s_%s'%(function.__name__, user,pagina)

            if not cache_post and request.method == 'POST':
                can_cache = False
            else:
                can_cache = True

            if can_cache:
                response = cache.get(CACHE_KEY, None)
            else:
                response = None

            if not response:
                response = function(request, *args, **kwargs)
                if can_cache:
                    cache.set(CACHE_KEY, response, ttl)
            return response
        return apply_cache
    return decorator