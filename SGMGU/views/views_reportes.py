# -*- coding: utf-8 -*-

from django.shortcuts import render,redirect,get_object_or_404,get_list_or_404
from SGMGU.models import *
from SGMGU.forms import Expedientes_segun_carrera_form,Expedientes_segun_causal_form
from django.core.cache import cache
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger,InvalidPage
from django.http import Http404
from django.db.models import Count,Prefetch
from django.http import HttpResponse
from xlsxwriter.workbook import Workbook
from xlsxwriter.utility import xl_range


def paginar(request,lista_objetos):
    paginator=Paginator(lista_objetos,100)
    try:
        pagina=int(request.GET.get("pagina","1"))
    except ValueError:
        pagina=1
    try:
        lista_objetos=paginator.page(pagina)
    except(InvalidPage, EmptyPage):
        lista_objetos=paginator.page(paginator.num_pages)
    return lista_objetos

def reportes(request):
    return render(request,"Reportes/reportes.html",{})


def reporte_exp_organismo_carrera(request):
    try:
        fecha_inicio=request.POST['fecha_inicio']
        fecha_fin=request.POST['fecha_fin']
        messages.add_message(request,messages.SUCCESS,"Reporte filtrado entre las fechas %s y %s"%(fecha_inicio,fecha_fin))
    except:
        fecha_inicio=None
        fecha_fin=None

    if fecha_inicio!=None and fecha_fin!=None:
         par=" and ea.fecha_aprobado BETWEEN \'"+ unicode(fecha_inicio)+ "\' and \'"+unicode(fecha_fin)+"\'"
    else:
        par=""
    query="""select o.id, o.nombre as nombre_org, c.id ,c.nombre as nombre_car, count(*) as cant_exp_lib, 0 as  cant_exp_acep from
            "SGMGU_expediente_aprobado" ea,
            "SGMGU_expediente_movimiento_externo" e,
            "SGMGU_organismo" o,
            "SGMGU_expediente" exp,
            "SGMGU_carrera" c,
            "SGMGU_graduado" g
            where
            ea.expediente_id=e.expediente_ptr_id and
            e.organismo_liberacion_id=o.id and
            exp.id=e.expediente_ptr_id and
            exp.graduado_id=g.persona_ptr_id and
            g.carrera_id=c.id"""+ par +"""
            group by o.id,c.id
            union all
        select o.id, o.nombre as nombre_org, c.id, c.nombre as nombre_car, 0 as cant_exp_lib, count(*) as  cant_exp_acep from
            "SGMGU_expediente_aprobado" ea,
            "SGMGU_expediente_movimiento_externo" e,
            "SGMGU_organismo" o,
            "SGMGU_expediente" exp,
            "SGMGU_carrera" c,
            "SGMGU_graduado" g
            where
            ea.expediente_id=e.expediente_ptr_id and
            e.organismo_aceptacion_id=o.id and
            exp.id=e.expediente_ptr_id and
            exp.graduado_id=g.persona_ptr_id and
            g.carrera_id=c.id"""+ par +"""
            group by o.id,c.id;"""

    datos=list(Organismo.objects.raw(query))
    contexto = {'control':'aprobado',"datos":paginar(request,datos)}

    return render(request, "Reportes/reporte_exp_org_carrera.html", contexto)

def reporte_noexp_organismo_carrera(request):
    try:
        fecha_inicio=request.POST['fecha_inicio']
        fecha_fin=request.POST['fecha_fin']
        messages.add_message(request,messages.SUCCESS,"Reporte filtrado entre las fechas %s y %s"%(fecha_inicio,fecha_fin))
    except:
        fecha_inicio=None
        fecha_fin=None

    if fecha_inicio!=None and fecha_fin!=None:
         par=" and ea.fecha_no_aprobado BETWEEN \'"+ unicode(fecha_inicio)+ "\' and \'"+unicode(fecha_fin)+"\'"
    else:
        par=""

    query="""select o.id, o.nombre as nombre_org, c.id,c.nombre as nombre_car, count(*) as cant_exp from
            "SGMGU_expediente_no_aprobado" ea,
            "SGMGU_expediente_movimiento_externo" e,
            "SGMGU_organismo" o,
            "SGMGU_expediente" exp,
            "SGMGU_carrera" c,
            "SGMGU_graduado" g
            where
            ea.expediente_id=e.expediente_ptr_id and
            e.organismo_liberacion_id=o.id and
            exp.id=e.expediente_ptr_id and
            exp.graduado_id=g.persona_ptr_id and
            g.carrera_id=c.id"""+ par +"""
            group by o.id, o.nombre,c.id """

    datos=Organismo.objects.raw(query)
    contexto = {'control':'no_aprobado',"datos":paginar(request,list(datos))}
    return render(request, "Reportes/reporte_exp_org_carrera.html", contexto)

def reporte_exp_organismo(request):
    datos=[]
    sum_lib=0
    sum_acep=0
    organismos=Organismo.objects.all()
    try:
        fecha_inicio=request.POST['fecha_inicio']
        fecha_fin=request.POST['fecha_fin']
        messages.add_message(request,messages.SUCCESS,"Reporte filtrado entre las fechas %s y %s"%(fecha_inicio,fecha_fin))
    except:
        fecha_inicio=None
        fecha_fin=None
    for organismo in organismos:
        if fecha_inicio!=None and fecha_fin!=None:
            cant_expedientes_lib=Expediente_aprobado.objects.filter(expediente__organismo_liberacion=organismo,expediente__expediente_aprobado__fecha_aprobado__range=(fecha_inicio,fecha_fin)).count()
            cant_expedientes_acep=Expediente_aprobado.objects.filter(expediente__organismo_aceptacion=organismo,expediente__expediente_aprobado__fecha_aprobado__range=(fecha_inicio,fecha_fin)).count()
        else:
            cant_expedientes_lib=Expediente_aprobado.objects.filter(expediente__organismo_liberacion=organismo).count()
            cant_expedientes_acep=Expediente_aprobado.objects.filter(expediente__organismo_aceptacion=organismo).count()
        diferencia=int(cant_expedientes_lib)-int(cant_expedientes_acep)
        sum_lib+=int(cant_expedientes_lib)
        sum_acep+=int(cant_expedientes_acep)
        datos.append({'org_nombre':organismo.nombre,'siglas':organismo.siglas,'cant_expedientes_lib':cant_expedientes_lib,'cant_expedientes_acep':cant_expedientes_acep,'diferencia':diferencia })
    dif_total=sum_lib-sum_acep

    contexto = {'control':'aprobado',"datos":datos,"sum_lib":sum_lib,"sum_acep":sum_acep,'dif_total':dif_total}
    return render(request, "Reportes/reporte_exp_organismos.html", contexto)

def reporte_exp_org_provincia(request):
    provincias=Provincia.objects.all()
    try:
        fecha_inicio=request.POST['fecha_inicio']
        fecha_fin=request.POST['fecha_fin']
        messages.add_message(request,messages.SUCCESS,"Reporte filtrado entre las fechas %s y %s"%(fecha_inicio,fecha_fin))
    except:
        fecha_inicio=None
        fecha_fin=None

    if fecha_inicio!=None and fecha_fin!=None:
         par=" and ea.fecha_aprobado BETWEEN \'"+ unicode(fecha_inicio)+ "\' and \'"+unicode(fecha_fin)+"\'"
    else:
        par=""

    query="""select o.id, p.id, o.nombre as nombre_org, p.siglas as nombre_prov, count(*) as cant_exp from
      "SGMGU_expediente_aprobado" ea,
      "SGMGU_expediente_movimiento_externo" e,
      "SGMGU_organismo" o,
      "SGMGU_provincia" p,
      "SGMGU_municipio" m,
      "SGMGU_expediente" exp
      where
      ea.expediente_id=e.expediente_ptr_id and
      e.organismo_aceptacion_id=o.id and
      exp.id=e.expediente_ptr_id and
      exp.mun_entidad_aceptacion_id=m.id and
      m.provincia_id=p.id"""+ par +""" group by o.id, p.id, o.nombre, p.siglas order by nombre_org, nombre_prov; """

    datos=Provincia.objects.raw(query)
    lista=[]
    organismo_analizados=[]
    for dato in list(datos):
        prov={
        'PR':{'nombre':'PR','cantidad':0},
        'ART':{'nombre':'ART','cantidad':0},
        'LH':{'nombre':'LH','cantidad':0},
        'MAY':{'nombre':'MAY','cantidad':0},
        'MTZ':{'nombre':'MTZ','cantidad':0},
        'VC':{'nombre':'VC','cantidad':0},
        'CFG':{'nombre':'CFG','cantidad':0},
        'SS':{'nombre':'SS','cantidad':0},
        'CA':{'nombre':'CA','cantidad':0},
        'CMG':{'nombre':'CMG','cantidad':0},
        'LT':{'nombre':'LT','cantidad':0},
        'HOLG':{'nombre':'HOLG','cantidad':0},
        'GRM':{'nombre':'GRM','cantidad':0},
        'SC':{'nombre':'SC','cantidad':0},
        'GTM':{'nombre':'GTM','cantidad':0},
        'IJ':{'nombre':'IJ','cantidad':0},
    }
        result={'organismo':{'provincias':prov}}
        if not organismo_analizados.__contains__(dato.nombre_org):
            result['organismo']['nombre']=dato.nombre_org
            result['organismo']['provincias'][dato.nombre_prov]['cantidad']=dato.cant_exp
            lista.append(result)
            organismo_analizados.append(dato.nombre_org)
        else:
           for item in lista:
               if item['organismo']['nombre'] == dato.nombre_org:
                  item['organismo']['provincias'][dato.nombre_prov]['cantidad']=dato.cant_exp

    contexto = {"datos":lista,"provincias":provincias}
    return render(request, "Reportes/reporte_exp_org_provincia.html", contexto)

def reporte_noexp_organismo(request):
    datos=[]
    sum_lib=0
    organismos=Organismo.objects.all()
    try:
        fecha_inicio=request.POST['fecha_inicio']
        fecha_fin=request.POST['fecha_fin']
        messages.add_message(request,messages.SUCCESS,"Reporte filtrado entre las fechas %s y %s"%(fecha_inicio,fecha_fin))
    except:
        fecha_inicio=None
        fecha_fin=None
    for organismo in organismos:
        if fecha_inicio!=None and fecha_fin!=None:
            cant_expedientes_lib=Expediente_no_aprobado.objects.filter(expediente__organismo_liberacion=organismo,expediente__expediente_no_aprobado__fecha_no_aprobado__range=(fecha_inicio,fecha_fin)).count()
        else:
            cant_expedientes_lib=Expediente_no_aprobado.objects.filter(expediente__organismo_liberacion=organismo).count()
        sum_lib+=int(cant_expedientes_lib)

        datos.append({'org_nombre':organismo.nombre,'siglas':organismo.siglas,'cant_expedientes_lib':cant_expedientes_lib })

    contexto = {'control':'no_aprobado',"datos":datos,"sum_lib":sum_lib}
    return render(request, "Reportes/reporte_exp_organismos.html", contexto)

def reporte_mov_int_organismos(request):
    datos=[]
    suma=0
    organismos=Organismo.objects.all()
    try:
        fecha_inicio=request.POST['fecha_inicio']
        fecha_fin=request.POST['fecha_fin']
        messages.add_message(request,messages.SUCCESS,"Reporte filtrado entre las fechas %s y %s"%(fecha_inicio,fecha_fin))
    except:
        fecha_inicio=None
        fecha_fin=None
    for organismo in organismos:
        if fecha_inicio!=None and fecha_fin!=None:
            cant_expedientes=Expediente_movimiento_interno.objects.filter(organismo=organismo,fecha_registro__range=(fecha_inicio,fecha_fin)).count()
        else:
            cant_expedientes=Expediente_movimiento_interno.objects.filter(organismo=organismo).count()
        datos.append({'org_nombre':organismo.nombre,'org_siglas':organismo.siglas,'cant_expedientes':cant_expedientes})
        suma+=int(cant_expedientes)

    contexto = {"datos":datos,"suma":suma}
    return render(request, "Reportes/reporte_mov_int_organismos.html", contexto)

def exportar_resumen_mensual(request):
    organismos=Organismo.objects.filter(activo=True)
    total_organismos=len(organismos)
    meses={
         'Enero':1,
         'Febrero':2,
         'Marzo':3,
         'Abril':4,
         'Mayo':5,
         'Junio':6,
         'Julio':7,
         'Agosto':8,
         'Septiembre':9,
         'Octubre':10,
         'Noviembre':11,
         'Diciembre':12
    }

    if request.method == "POST":
        anno=int(request.POST["anno"])
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = "attachment; filename=resumen_mensual_exp_aprobados_%s.xlsx"%anno
        book = Workbook(response, {'in_memory': True})
        bold = book.add_format({'bold': True, 'border': 1})
        format = book.add_format({'border': 1})

        for nombre_mes in meses.keys():
            mes=meses[nombre_mes]
            sheet = book.add_worksheet(nombre_mes)
            sheet.set_column('A:A', 80)
            sheet.set_column('B:B', 10)
            sheet.set_column('C:C', 10)
            sheet.set_column('D:D', 10)
            sheet.write(0, 0, "Organismos",bold)
            sheet.write(0, 1, "Liberados",bold)
            sheet.write(0, 2, "Aceptados",bold)
            sheet.write(0, 3, "Internos",bold)
            where1 = '%(year)s =  EXTRACT(YEAR FROM fecha_aprobado) AND %(month)s =  EXTRACT(MONTH FROM fecha_aprobado)'%{'year': anno, 'month': mes}
            for i,organismo in enumerate(organismos):
                cant_liberados=Expediente_aprobado.objects.filter(expediente__organismo_liberacion=organismo).extra(where=[where1]).count()
                cant_aceptados=Expediente_aprobado.objects.filter(expediente__organismo_aceptacion=organismo).extra(where=[where1]).count()
                cant_internos=Expediente_movimiento_interno.objects.filter(organismo=organismo,fecha_registro__year=anno).count()

                sheet.write(i+1, 0, organismo.nombre,format)
                sheet.write(i+1, 1, cant_liberados,format)
                sheet.write(i+1, 2, cant_aceptados,format)
                sheet.write(i+1, 3, 0,format)


            formula_total_liberados = '=SUM(%s)' % xl_range(1, 1,total_organismos, 1)
            formula_total_aceptados = '=SUM(%s)' % xl_range(1, 2,total_organismos, 2)
            formula_total_internos = '=SUM(%s)' % xl_range(1, 3,total_organismos, 3)

            sheet.write(total_organismos+1, 0, "Total",bold)
            sheet.write(total_organismos+1, 1, formula_total_liberados,bold)
            sheet.write(total_organismos+1, 2, formula_total_aceptados,bold)
            sheet.write(total_organismos+1, 3, formula_total_internos,bold)
        book.close()
        return response
    else:
        return Http404

def exportar_organismos_expedientes(request):
    organismos=Organismo.objects.all()
    total=len(organismos)
    if request.method == "POST":
        perfil=request.user.perfil_usuario

        anno=int(request.POST["anno"])
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = "attachment; filename=resumen_exp_aprobados_organismos_%s.xlsx"%anno
        book = Workbook(response, {'in_memory': True})
        bold = book.add_format({'bold': True, 'border': 1})
        format = book.add_format({'border': 1})
        sheet = book.add_worksheet("Resumen")
        sheet.set_column('A:A', 60)
        sheet.set_column('B:B', 10)
        sheet.set_column('B:B', 10)
        sheet.set_column('C:C', 10)

        sheet.write(0, 0,  "Organismos",bold)
        sheet.write(0, 1,  "Liberados",bold)
        sheet.write(0, 2,  "Aceptados",bold)
        sheet.write(0, 3,  "Internos",bold)


        if perfil.categoria.nombre == "organismo" and perfil.organismo.hijode == None:
            organismos=list(Organismo.objects.filter(hijode=perfil.organismo))
            organismos.insert(0,perfil.organismo)
            total=len(organismos)
            for i,organismo in enumerate(organismos):
                liberados=Expediente_aprobado.objects.filter(expediente__organismo_liberacion=organismo,fecha_aprobado__year=anno).count()
                aceptados=Expediente_aprobado.objects.filter(expediente__organismo_aceptacion=organismo,fecha_aprobado__year=anno).count()
                internos=Expediente_movimiento_interno.objects.filter(organismo=organismo,fecha_registro__year=anno).count()
                sheet.write(i+1, 0, organismo.nombre,format)
                sheet.write(i+1, 1, liberados,format)
                sheet.write(i+1, 2, aceptados,format)
                sheet.write(i+1, 3, internos,format)
        else:

            for i,organismo in enumerate(organismos):
                liberados=Expediente_aprobado.objects.filter(expediente__organismo_liberacion=organismo,fecha_aprobado__year=anno).count()
                aceptados=Expediente_aprobado.objects.filter(expediente__organismo_aceptacion=organismo,fecha_aprobado__year=anno).count()
                internos=Expediente_movimiento_interno.objects.filter(organismo=organismo,fecha_registro__year=anno).count()
                sheet.write(i+1, 0, organismo.nombre,format)
                sheet.write(i+1, 1, liberados,format)
                sheet.write(i+1, 2, aceptados,format)
                sheet.write(i+1, 3, internos,format)

        formula_rango_total_liberados = '=SUM(%s)' % xl_range(1, 1,total, 1)
        formula_rango_rango_total_aceptados = '=SUM(%s)' % xl_range(1, 2,total, 2)
        formula_rango_rango_total_internos = '=SUM(%s)' % xl_range(1, 3,total, 3)

        sheet.write(total+1, 0, "Total",bold)
        sheet.write(total+1, 1, formula_rango_total_liberados,bold)
        sheet.write(total+1, 2, formula_rango_rango_total_aceptados,bold)
        sheet.write(total+1, 3, formula_rango_rango_total_internos,bold)
        book.close()
        return response
    else:
        return Http404

def exportar_carreras_expedientes(request):
    carreras=Carrera.objects.filter(tipo='ns')
    total_carreras=len(carreras)

    if request.method == "POST":
        anno=int(request.POST["anno"])
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = "attachment; filename=resumen_exp_aprobados_carreras_%s.xlsx"%anno
        book = Workbook(response, {'in_memory': True})
        bold = book.add_format({'bold': True, 'border': 1})
        format = book.add_format({'border': 1})
        sheet = book.add_worksheet("Resumen")
        sheet.set_column('A:A', 60)
        sheet.write(0, 0, "Carreras",bold)
        sheet.write(0, 1, "Externos",bold)
        sheet.write(0, 2, "Internos",bold)
        perfil=request.user.perfil_usuario
        if perfil.categoria.nombre == "organismo":
            for i,carrera in enumerate(carreras):
                cant=Expediente_aprobado.objects.filter(expediente__organismo_liberacion=perfil.organismo,expediente__graduado__carrera=carrera,fecha_aprobado__year=anno).count()
                cant+=Expediente_aprobado.objects.filter(expediente__organismo_aceptacion=perfil.organismo,expediente__graduado__carrera=carrera,fecha_aprobado__year=anno).count()
                cant_internos=Expediente_movimiento_interno.objects.filter(organismo=perfil.organismo,graduado__carrera=carrera,fecha_registro__year=anno).count()

                sheet.write(i+1, 0, carrera.nombre,format)
                sheet.write(i+1, 1, cant,format)
                sheet.write(i+1, 2, cant_internos,format)
        else:
            for i,carrera in enumerate(carreras):
                cant=Expediente_aprobado.objects.filter(expediente__graduado__carrera=carrera,fecha_aprobado__year=anno).count()
                cant_internos=Expediente_movimiento_interno.objects.filter(graduado__carrera=carrera,fecha_registro__year=anno).count()

                sheet.write(i+1, 0, carrera.nombre,format)
                sheet.write(i+1, 1, cant,format)
                sheet.write(i+1, 2, cant_internos,format)

        formula_rango_total_externos = '=SUM(%s)' % xl_range(1, 1,total_carreras, 1)
        formula_rango_total_internos = '=SUM(%s)' % xl_range(1, 2,total_carreras, 2)
        sheet.write(total_carreras+1, 0, "Total",bold)
        sheet.write(total_carreras+1, 1, formula_rango_total_externos,bold)
        sheet.write(total_carreras+1, 2, formula_rango_total_internos,bold)
        book.close()
        return response
    else:
        return Http404

def exportar_causales_expedientes(request):
    causales=Causal_movimiento.objects.filter(activo=True,tipo='ml')
    total_causales=len(causales)

    if request.method == "POST":
        anno=int(request.POST["anno"])
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = "attachment; filename=resumen_exp_aprobados_causales_%s.xlsx"%anno
        book = Workbook(response, {'in_memory': True})
        bold = book.add_format({'bold': True, 'border': 1})
        format = book.add_format({'border': 1})
        sheet = book.add_worksheet("Resumen")
        sheet.set_column('A:A', 60)
        sheet.write(0, 0, "Causales",bold)
        sheet.write(0, 1, "Externos",bold)
        sheet.write(0, 2, "Internos",bold)
        perfil=request.user.perfil_usuario
        if perfil.categoria.nombre == "organismo":
            for i,causal in enumerate(causales):
                cant=Expediente_aprobado.objects.filter(expediente__organismo_liberacion=perfil.organismo,expediente__causal_movimiento=causal,fecha_aprobado__year=anno).count()
                cant+=Expediente_aprobado.objects.filter(expediente__organismo_aceptacion=perfil.organismo,expediente__causal_movimiento=causal,fecha_aprobado__year=anno).count()
                cant_internos=Expediente_movimiento_interno.objects.filter(organismo=perfil.organismo,causal_movimiento=causal,fecha_registro__year=anno).count()

                sheet.write(i+1, 0, causal.nombre,format)
                sheet.write(i+1, 1, cant,format)
                sheet.write(i+1, 2, cant_internos,format)
        else:
            for i,causal in enumerate(causales):
                cant=Expediente_aprobado.objects.filter(expediente__causal_movimiento=causal,fecha_aprobado__year=anno).count()
                cant_internos=Expediente_movimiento_interno.objects.filter(causal_movimiento=causal,fecha_registro__year=anno).count()

                sheet.write(i+1, 0, causal.nombre,format)
                sheet.write(i+1, 1, cant,format)
                sheet.write(i+1, 2, cant_internos,format)

        formula_rango_total_externos = '=SUM(%s)' % xl_range(1, 1,total_causales, 1)
        formula_rango_total_internos = '=SUM(%s)' % xl_range(1, 2,total_causales, 2)
        sheet.write(total_causales+1, 0, "Total",bold)
        sheet.write(total_causales+1, 1, formula_rango_total_externos,bold)
        sheet.write(total_causales+1, 2, formula_rango_total_internos,bold)
        book.close()
        return response
    else:
        return Http404

def exportar_provincias_expedientes(request):
    provincias=Provincia.objects.all()
    total_provincias=len(provincias)

    if request.method == "POST":
        anno=int(request.POST["anno"])
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = "attachment; filename=resumen_exp_aprobados_provincias_%s.xlsx"%anno
        book = Workbook(response, {'in_memory': True})
        bold = book.add_format({'bold': True, 'border': 1})
        format = book.add_format({'border': 1})
        sheet = book.add_worksheet("Datos")
        sheet.set_column('A:A', 60)
        sheet.set_column('B:B', 20)
        sheet.set_column('C:C', 20)
        sheet.set_column('D:D', 20)
        sheet.set_column('E:E', 20)

        sheet.write(0, 0, "Provincias",bold)
        sheet.write(0, 1, "Externos Liberados",bold)
        sheet.write(0, 2, "Externos Aceptados",bold)
        sheet.write(0, 3, "Internos Liberados",bold)
        sheet.write(0, 4, "Internos Aceptados",bold)

        perfil=request.user.perfil_usuario
        if perfil.categoria.nombre == "organismo":
                for i,prov in enumerate(provincias):
                    cant_lib=Expediente_aprobado.objects.filter(expediente__organismo_liberacion=perfil.organismo,expediente__mun_entidad_liberacion__provincia=prov,fecha_aprobado__year=anno).count()
                    cant_lib+=Expediente_aprobado.objects.filter(expediente__organismo_aceptacion=perfil.organismo,expediente__mun_entidad_liberacion__provincia=prov,fecha_aprobado__year=anno).count()
                    cant_acept=Expediente_aprobado.objects.filter(expediente__organismo_liberacion=perfil.organismo,expediente__mun_entidad_aceptacion__provincia=prov,fecha_aprobado__year=anno).count()
                    cant_acept+=Expediente_aprobado.objects.filter(expediente__organismo_aceptacion=perfil.organismo,expediente__mun_entidad_aceptacion__provincia=prov,fecha_aprobado__year=anno).count()

                    cant_internos_lib=Expediente_movimiento_interno.objects.filter(organismo=perfil.organismo,mun_entidad_liberacion__provincia=prov,fecha_registro__year=anno).count()
                    cant_internos_acept=Expediente_movimiento_interno.objects.filter(organismo=perfil.organismo,mun_entidad_aceptacion__provincia=prov,fecha_registro__year=anno).count()

                    sheet.write(i+1, 0, prov.nombre,format)
                    sheet.write(i+1, 1, cant_lib,format)
                    sheet.write(i+1, 2, cant_acept,format)
                    sheet.write(i+1, 3, cant_internos_lib,format)
                    sheet.write(i+1, 4, cant_internos_acept,format)

        else:
                for i,prov in enumerate(provincias):
                    cant_lib=Expediente_aprobado.objects.filter(expediente__mun_entidad_liberacion__provincia=prov,fecha_aprobado__year=anno).count()
                    cant_acept=Expediente_aprobado.objects.filter(expediente__mun_entidad_aceptacion__provincia=prov,fecha_aprobado__year=anno).count()

                    cant_internos_lib=Expediente_movimiento_interno.objects.filter(mun_entidad_liberacion__provincia=prov,fecha_registro__year=anno).count()
                    cant_internos_acept=Expediente_movimiento_interno.objects.filter(mun_entidad_aceptacion__provincia=prov,fecha_registro__year=anno).count()

                    sheet.write(i+1, 0, prov.nombre,format)
                    sheet.write(i+1, 1, cant_lib,format)
                    sheet.write(i+1, 2, cant_acept,format)
                    sheet.write(i+1, 3, cant_internos_lib,format)
                    sheet.write(i+1, 4, cant_internos_acept,format)


        formula_rango_total_provincias = '=SUM(%s)' % xl_range(1, 1,total_provincias, 1)
        formula_rango_total_provincias1 = '=SUM(%s)' % xl_range(1, 2,total_provincias, 2)
        formula_rango_total_provincias2 = '=SUM(%s)' % xl_range(1, 3,total_provincias, 3)
        formula_rango_total_provincias3 = '=SUM(%s)' % xl_range(1, 4,total_provincias, 4)
        sheet.write(total_provincias+1, 0, "Total",bold)
        sheet.write(total_provincias+1, 1, formula_rango_total_provincias,bold)
        sheet.write(total_provincias+1, 2, formula_rango_total_provincias1,bold)
        sheet.write(total_provincias+1, 3, formula_rango_total_provincias2,bold)
        sheet.write(total_provincias+1, 4, formula_rango_total_provincias3,bold)
        book.close()
        return response
    else:
        return Http404

def exportar_expedientes_segun_causal(request):
    if request.method == "POST":
        form=Expedientes_segun_causal_form(request.POST)

        if form.is_valid():
            anno=form.cleaned_data['anno']
            causal=form.cleaned_data['causal']
            perfil=request.user.perfil_usuario
            if perfil.categoria.nombre == "organismo":
                 expedientes=Expediente_aprobado.objects.filter(expediente__organismo_liberacion=perfil.organismo,expediente__causal_movimiento=causal,fecha_aprobado__year=anno)
                 expedientes1=Expediente_aprobado.objects.filter(expediente__organismo_aceptacion=perfil.organismo,expediente__causal_movimiento=causal,fecha_aprobado__year=anno)
                 expedientes=list(expedientes)+list(expedientes1)
                 internos=Expediente_movimiento_interno.objects.filter(organismo=perfil.organismo,causal_movimiento=causal,fecha_registro__year=anno)
            else:
                 expedientes=Expediente_aprobado.objects.filter(expediente__causal_movimiento=causal,fecha_aprobado__year=anno)
                 internos=Expediente_movimiento_interno.objects.filter(causal_movimiento=causal,fecha_registro__year=anno)
            response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response['Content-Disposition'] = "attachment; filename=datos_exp_aprobados_%s_%s.xlsx"%(causal.nombre.replace(" ","_"),anno)
            book = Workbook(response, {'in_memory': True})
            bold = book.add_format({'bold': True, 'border': 1})
            format = book.add_format({'border': 1})
            sheet = book.add_worksheet("Externos")
            sheet.write(0, 0, "Nombre y Apellidos",bold)
            sheet.write(0, 1, "Organismo Lib",bold)
            sheet.write(0, 2, "Organismo Acep",bold)
            sheet.write(0, 3, "Carrera",bold)
            sheet.set_column('A:A', 40)
            sheet.set_column('B:B', 25)
            sheet.set_column('C:D', 25)
            sheet.set_column('D:D', 40)
            for i,expediente in enumerate(expedientes):
                sheet.write(i+1, 0, expediente.expediente.graduado.nombre,format)
                sheet.write(i+1, 1, expediente.expediente.organismo_liberacion.siglas,format)
                sheet.write(i+1, 2, expediente.expediente.organismo_aceptacion.siglas,format)
                sheet.write(i+1, 3, expediente.expediente.graduado.carrera.nombre,format)

            sheet = book.add_worksheet("Internos")
            sheet.write(0, 0, "Nombre y Apellidos",bold)
            sheet.write(0, 1, "Organismo",bold)
            sheet.write(0, 2, "Entidad Lib",bold)
            sheet.write(0, 3, "Entidad Acep",bold)
            sheet.write(0, 4, "Carrera",bold)
            sheet.set_column('A:A', 40)
            sheet.set_column('B:B', 25)
            sheet.set_column('C:D', 25)
            sheet.set_column('D:D', 25)
            sheet.set_column('E:E', 40)
            for i,expediente in enumerate(internos):
                sheet.write(i+1, 0, expediente.graduado.nombre,format)
                sheet.write(i+1, 1, expediente.organismo.siglas,format)
                sheet.write(i+1, 2, expediente.entidad_liberacion,format)
                sheet.write(i+1, 3, expediente.entidad_aceptacion,format)
                sheet.write(i+1, 4, expediente.graduado.carrera.nombre,format)

            book.close()
            return response
    else:
        form=Expedientes_segun_causal_form()
    contexto={'form':form}
    return render(request,"Reportes/exp_segun_causal.html",contexto)

def exportar_expedientes_segun_carrera(request):
    if request.method == "POST":
        form=Expedientes_segun_carrera_form(request.POST)

        if form.is_valid():
            anno=form.cleaned_data['anno']
            carrera=form.cleaned_data['carrera']
            perfil=request.user.perfil_usuario
            if perfil.categoria.nombre == "organismo":
                 expedientes=Expediente_aprobado.objects.filter(expediente__organismo_liberacion=perfil.organismo,expediente__graduado__carrera=carrera,fecha_aprobado__year=anno)
                 expedientes1=Expediente_aprobado.objects.filter(expediente__organismo_aceptacion=perfil.organismo,expediente__graduado__carrera=carrera,fecha_aprobado__year=anno)
                 expedientes=list(expedientes)+list(expedientes1)
                 internos=Expediente_movimiento_interno.objects.filter(organismo=perfil.organismo,graduado__carrera=carrera,fecha_registro__year=anno)
            else:
                 expedientes=Expediente_aprobado.objects.filter(expediente__graduado__carrera=carrera,fecha_aprobado__year=anno)
                 internos=Expediente_movimiento_interno.objects.filter(graduado__carrera=carrera,fecha_registro__year=anno)


            response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response['Content-Disposition'] = "attachment; filename=datos_exp_aprobados_%s_%s.xlsx"%(carrera.nombre.replace(" ","_"),anno)
            book = Workbook(response, {'in_memory': True})
            bold = book.add_format({'bold': True, 'border': 1})
            format = book.add_format({'border': 1})
            sheet = book.add_worksheet("Externos")
            sheet.write(0, 0, "Nombre y Apellidos",bold)
            sheet.write(0, 1, "Organismo Lib",bold)
            sheet.write(0, 2, "Organismo Acep",bold)
            sheet.write(0, 3, "Causal Movimiento",bold)
            sheet.set_column('A:A', 40)
            sheet.set_column('B:B', 25)
            sheet.set_column('C:C', 25)
            sheet.set_column('D:D', 75)
            for i,expediente in enumerate(expedientes):
                sheet.write(i+1, 0, expediente.expediente.graduado.nombre,format)
                sheet.write(i+1, 1, expediente.expediente.organismo_liberacion.siglas,format)
                sheet.write(i+1, 2, expediente.expediente.organismo_aceptacion.siglas,format)
                sheet.write(i+1, 3, expediente.expediente.causal_movimiento.nombre,format)

            sheet = book.add_worksheet("Internos")
            sheet.write(0, 0, "Nombre y Apellidos",bold)
            sheet.write(0, 1, "Organismo",bold)
            sheet.write(0, 2, "Entidad Lib",bold)
            sheet.write(0, 3, "Entidad Acep",bold)
            sheet.write(0, 4, "Causal Movimiento",bold)
            sheet.set_column('A:A', 40)
            sheet.set_column('B:B', 20)
            sheet.set_column('C:C', 40)
            sheet.set_column('D:D', 40)
            sheet.set_column('E:E', 75)
            for i,expediente in enumerate(internos):
                sheet.write(i+1, 0, expediente.graduado.nombre,format)
                sheet.write(i+1, 1, expediente.organismo.siglas,format)
                sheet.write(i+1, 2, expediente.entidad_liberacion,format)
                sheet.write(i+1, 3, expediente.entidad_aceptacion,format)
                sheet.write(i+1, 4, expediente.causal_movimiento.nombre,format)
            book.close()
            return response
    else:
        form=Expedientes_segun_carrera_form()
    contexto={'form':form}
    return render(request,"Reportes/exp_segun_carrera.html",contexto)