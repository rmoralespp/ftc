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



QUERY_ANALISIS_PROCESO_UBICADO= """

select
id,
nombre_provincia,
sum(pendientes) over (Partition by nombre_provincia) as pendientes_provincia,
sum(ubicados)   over (Partition by nombre_provincia) as ubicados_provincia,
sum( pendientes + ubicados) over (Partition by nombre_provincia) as total_provincia,
nombre_centro,
pendientes as pendientes_centro,
ubicados   as ubicados_centro,
total      as total_centro

from (
select
id,
nombre_provincia,
nombre_centro,
sum(pendientes) as pendientes,
sum(ubicados) as ubicados,
sum (pendientes + ubicados ) AS total
from (

SELECT
p.id,
p.nombre    as nombre_provincia,
ce.nombre   as nombre_centro,
count(d.id) as pendientes,
0           as ubicados

FROM "SGMGU_disponibilidadgraduados" d,  "SGMGU_centro_estudio" ce, "SGMGU_provincia" p

where
d.centro_estudio_id=ce.id and
ce.provincia_id=p.id and
EXTRACT (YEAR FROM d.fecha_registro) = '%(anno)s'

group by p.id,p.nombre, ce.nombre


UNION ALL


SELECT
p.id,
p.nombre    as nombre_provincia,
ce.nombre   as nombre_centro,
0           as pendientes,
count(u.id) as ubicados

FROM  "SGMGU_ubicacionlaboral" u, "SGMGU_centro_estudio" ce, "SGMGU_provincia" p

where

u.centro_estudio_id=ce.id and
ce.provincia_id=p.id and
EXTRACT (YEAR FROM u.fecha_registro) = '%(anno)s'
group by p.id,p.nombre, ce.nombre
) q

group by  q.id,q.nombre_provincia, q.nombre_centro
order by  q.nombre_provincia, q.nombre_centro
) q1 order by  q1.id, q1.nombre_centro
"""
