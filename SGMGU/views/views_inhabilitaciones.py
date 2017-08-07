# -*- coding: utf-8 -*-
from django.shortcuts import render,redirect
from SGMGU.models import *
from SGMGU.forms import *
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .utiles import *
from django.http import HttpResponse,Http404
from xlsxwriter.workbook import Workbook
from xlsxwriter.utility import xl_range
import datetime
from django.db.models import Q
from django.db import models


MESES={
     1:'Enero',
     2:'Febrero',
     3:'Marzo',
     4:'Abril',
     5:'Mayo',
     6:'Junio',
     7:'Julio',
     8:'Agosto',
     9:'Septiembre',
     10:'Octubre',
     11:'Noviembre',
     12:'Diciembre',
}

@login_required
def inhabilitaciones(request):
     inhabilitaciones=ProcesoInhabilitacion.objects.all().order_by("-fecha")
     inhabilitaciones=paginar(request,inhabilitaciones)
     context={'inhabilitaciones':inhabilitaciones,'paginas':crear_lista_pages(inhabilitaciones)}
     return render(request, "Inhabilitaciones/inhabilitaciones.html", context)


@login_required
def autocompletar_inhabilitado(request):
    if request.method == 'POST':
            ci=request.POST['ci']
            try:
                graduado_inhabilitado=GraduadoInhabilitacion.objects.filter(ci=ci)
                graduado_inhabilitado=graduado_inhabilitado[0]
                entrada= {
                    'nombre_apellidos':graduado_inhabilitado.nombre_apellidos,
                    'carrera':graduado_inhabilitado.carrera.id,
                    'provincia':graduado_inhabilitado.provincia.id,
                    'organismo':graduado_inhabilitado.organismo.id,
                    'nivel_educacional':graduado_inhabilitado.nivel_educacional,
                    'ci':graduado_inhabilitado.ci,
                    'cumple_servicio_social':graduado_inhabilitado.cumple_servicio_social,
                    }
                form = ProcesoInhabilitacionForm(initial=entrada)
                contexto={'form':form,'nombre_form':'Autocompletar','url':'/inhabilitaciones/registrar'}
                return render(request, "Inhabilitaciones/form.html", contexto)
            except:
                  try:
                      ubicados=UbicacionLaboral.objects.filter(ci=ci)
                      ubicacion=ubicados[0]
                      entrada= {
                          'nombre_apellidos':ubicacion.nombre_apellidos,
                          'carrera':ubicacion.carrera.id,
                          'provincia':ubicacion.municipio_residencia.provincia.id,
                          'organismo':ubicacion.organismo.id,
                          'nivel_educacional':"Superior",
                          'ci':ubicacion.ci,
                          'cumple_servicio_social':'Si' if ubicacion.cumple_servicio_social else 'No',
                          }

                      form = ProcesoInhabilitacionForm(initial=entrada)
                      contexto={'form':form,'nombre_form':'Autocompletar','url':'/inhabilitaciones/registrar'}
                      return render(request, "Inhabilitaciones/form.html", contexto)
                  except:
                      messages.add_message(request, messages.ERROR, "No se encontró ningún graduado registrado con ese ci")
                      return redirect("/inhabilitaciones/registrar")

    else:
         return redirect("/inicio")


@login_required
@permission_required(['administrador','especialista','juridico'])
def registrar_inhabilitacion(request):
    if request.method == 'POST':
        form=ProcesoInhabilitacionForm(request.POST)
        if form.is_valid():
            graduados=GraduadoInhabilitacion.objects.filter(ci=form.cleaned_data['ci'])
            if graduados.count() == 0:
                graduado=form.save(commit=False)
                graduado.save()
            else:
                graduado=graduados[0]
            ProcesoInhabilitacion.objects.create(
                graduado=graduado,
                numero_resolucion=form.cleaned_data['numero_resolucion'],
                causal=form.cleaned_data['causal'],
                proceso=form.cleaned_data['proceso'],
            )
            messages.add_message(request, messages.SUCCESS, "El proceso se ha registrado con éxito.")
            return redirect('/inhabilitaciones')

    else:
        form=ProcesoInhabilitacionForm()
    return render(request, "Inhabilitaciones/form.html", {'form':form,'nombre_form':'Registar','url':'/inhabilitaciones/registrar'})



def detalle_proceso(request,id_proceso):
    proceso=ProcesoInhabilitacion.objects.get(id=id_proceso)
    return render(request, "Inhabilitaciones/detalle.html", {'proceso':proceso})


@login_required
@permission_required(['administrador','especialista','juridico'])
def modificar_proceso(request,id_proceso):
    proceso=ProcesoInhabilitacion.objects.get(id=id_proceso)
    if request.method == "POST":
        form=ProcesoInhabilitacionForm(request.POST)
        if form.is_valid():
                proceso=ProcesoInhabilitacion.objects.get(id=id_proceso)
                proceso.graduado.nombre_apellidos=form.cleaned_data['nombre_apellidos']
                proceso.graduado.carrera=form.cleaned_data['carrera']
                proceso.graduado.provincia=form.cleaned_data['provincia']
                proceso.graduado.organismo=form.cleaned_data['organismo']
                proceso.graduado.nivel_educacional=form.cleaned_data['nivel_educacional']
                proceso.graduado.ci=form.cleaned_data['ci']
                proceso.graduado.cumple_servicio_social=form.cleaned_data['cumple_servicio_social']
                proceso.causal=form.cleaned_data['causal']
                proceso.proceso=form.cleaned_data['proceso']
                proceso.numero_resolucion=form.cleaned_data['numero_resolucion']
                proceso.graduado.save()
                proceso.save()
                messages.add_message(request, messages.SUCCESS, "El proceso se ha editado con exito.")
                return redirect('/inhabilitaciones')
    else:
        entrada= {
                    'nombre_apellidos':proceso.graduado.nombre_apellidos,
                    'carrera':proceso.graduado.carrera.id,
                    'provincia':proceso.graduado.provincia.id,
                    'organismo':proceso.graduado.organismo.id,
                    'nivel_educacional':proceso.graduado.nivel_educacional,
                    'ci':proceso.graduado.ci,
                    'cumple_servicio_social':proceso.graduado.cumple_servicio_social,
                    'causal':proceso.causal,
                    'proceso':proceso.proceso,
                    'numero_resolucion':proceso.numero_resolucion,
                    }
        form=ProcesoInhabilitacionForm(initial=entrada)

    return render(request, "Inhabilitaciones/form.html", {'form':form,'nombre_form':'Editar','url':'/inhabilitaciones/%s/editar'%id_proceso})

@login_required
def buscar_ci_inhabilitado(request,ci):
  inhabilitaciones=ProcesoInhabilitacion.objects.filter(graduado__ci=ci).order_by("-fecha")
  context={'inhabilitaciones':inhabilitaciones,'busqueda':'si','termino_busqueda':'por CI',"valor_busqueda":ci}
  return render(request, "Inhabilitaciones/inhabilitaciones.html", context)


@login_required
def buscar_no_inhabilitado(request,no):
  inhabilitaciones=ProcesoInhabilitacion.objects.filter(numero_resolucion=no).order_by("-fecha")
  context={'inhabilitaciones':inhabilitaciones,'busqueda':'si','termino_busqueda':'por No Resolución',"valor_busqueda":no}
  return render(request, "Inhabilitaciones/inhabilitaciones.html", context)


@login_required
@permission_required(['administrador','especialista','juridico'])
def eliminar_proceso(request,id_proceso):
    proceso=ProcesoInhabilitacion.objects.get(id=id_proceso)
    proceso.delete()
    messages.add_message(request, messages.SUCCESS, "El proceso se ha eliminado con éxito.")
    return redirect('/inhabilitaciones')


@login_required
def exportar_total_procesos(request):
    if request.method== "POST":
        anno=int(request.POST['anno'])
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = "attachment; filename=Totales_procesos_%s.xlsx"%anno
        book = Workbook(response, {'in_memory': True})
        bold = book.add_format({'bold': True, 'border': 1})
        format = book.add_format({'border': 1})
        sheet = book.add_worksheet("Procesos")
        sheet.set_column('A:A', 20)
        sheet.set_column('B:B', 15)
        sheet.set_column('C:C', 15)
        sheet.set_column('D:D', 15)
        sheet.write(0, 0,  "Meses",bold)
        sheet.write(0, 1,  "Inhabilitaciones",bold)
        sheet.write(0, 2,  "Suspensiones",bold)
        sheet.write(0, 3,  "Total",bold)
        for i in range(1,13):
            where = '%(year)s =  EXTRACT(YEAR FROM fecha) AND %(month)s =  EXTRACT(MONTH FROM fecha)'%{'year': anno, 'month': i}
            procesos=ProcesoInhabilitacion.objects.filter().extra(where=[where])
            total_inhabilitaciones=procesos.filter(proceso='i').count()
            total_suspensiones=procesos.filter(proceso='s').count()
            total=total_inhabilitaciones+total_suspensiones
            sheet.write(i, 0, MESES[i],format)
            sheet.write(i, 1, total_inhabilitaciones,format)
            sheet.write(i, 2, total_suspensiones,format)
            sheet.write(i, 3, total,bold)
        formula_1 = '=SUM(%s)' % xl_range(1, 1,12, 1)
        formula_2 = '=SUM(%s)' % xl_range(1, 2,12, 2)
        formula_3 = '=SUM(%s)' % xl_range(1, 3,12, 3)
        sheet.write(13, 0, "Total",bold)
        sheet.write(13, 1, formula_1,bold)
        sheet.write(13, 2, formula_2,bold)
        sheet.write(13, 3, formula_3,bold)
        book.close()
        return response
    else:
        return Http404


@login_required
def exportar_total_procesos_causales(request):

    causales=Causal_movimiento.objects.filter(activo=True,tipo='i')
    if request.method== "POST":
        anno=int(request.POST['anno'])
        tipo=request.POST.get('tipo', None)
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = "attachment; filename=Totales_procesos_causales_%s.xlsx"%anno
        book = Workbook(response, {'in_memory': True})
        bold = book.add_format({'bold': True, 'border': 1})
        format = book.add_format({'border': 1})
        sheet = book.add_worksheet("Procesos")
        sheet.set_column('A:A', 20)
        sheet.write(0, 0,  "Causales",bold)
        if tipo == 'mensual':
            sheet.write(1, 0,  "I/S/Total",bold)
            control=True
            for i,causal in enumerate(causales):
                sheet.write(i+2, 0, causal.nombre,format)
                no=1
                for j in range(1,13):
                    if control==True:
                        sheet.merge_range(0,no,0,no+2, MESES[j],bold)
                        sheet.write(1, no, "I",bold)
                        sheet.write(1, no+1, "S",bold)
                        sheet.write(1, no+2, "Total",bold)
                    where = '%(year)s =  EXTRACT(YEAR FROM fecha) AND %(month)s =  EXTRACT(MONTH FROM fecha)'%{'year': anno, 'month': j}
                    procesos=ProcesoInhabilitacion.objects.filter(causal=causal).extra(where=[where])
                    total_inhabilitaciones=procesos.filter(proceso='i').count()
                    total_suspensiones=procesos.filter(proceso='s').count()
                    total=total_inhabilitaciones+total_suspensiones
                    sheet.write(i+2, no, total_inhabilitaciones,format)
                    sheet.write(i+2, no+1, total_suspensiones,format)
                    sheet.write(i+2, no+2, total,format)
                    no=(j*3)+1
                control=False
        else:
            sheet.write(0, 1,  "Inhabilitaciones",bold)
            sheet.write(0, 2,  "Suspensiones",bold)
            sheet.write(0, 3,  "Total",bold)
            sheet.set_column('B:B', 20)
            sheet.set_column('C:C', 20)
            for i,causal in enumerate(causales):
                sheet.write(i+1, 0, causal.nombre,format)
                procesos=ProcesoInhabilitacion.objects.filter(causal=causal,fecha__year=anno)
                total_inhabilitaciones=procesos.filter(proceso='i').count()
                total_suspensiones=procesos.filter(proceso='s').count()
                total=total_inhabilitaciones+total_suspensiones
                sheet.write(i+1, 1, total_inhabilitaciones,format)
                sheet.write(i+1, 2, total_suspensiones,format)
                sheet.write(i+1, 3, total,format)
            formula_1 = '=SUM(%s)' % xl_range(1, 1,len(causales), 1)
            formula_2 = '=SUM(%s)' % xl_range(1, 2,len(causales), 2)
            formula_3 = '=SUM(%s)' % xl_range(1, 3,len(causales), 3)
            sheet.write(len(causales)+1, 0, "Total",bold)
            sheet.write(len(causales)+1, 1, formula_1,bold)
            sheet.write(len(causales)+1, 2, formula_2,bold)
            sheet.write(len(causales)+1, 3, formula_3,bold)
        book.close()
        return response

    else:
        return Http404

@login_required
def exportar_total_procesos_organismos(request):

    organismos=Organismo.objects.filter(activo=True)

    if request.method== "POST":
        anno=int(request.POST['anno'])
        tipo=request.POST.get('tipo', None)
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = "attachment; filename=Totales_procesos_organismos_%s.xlsx"%anno
        book = Workbook(response, {'in_memory': True})
        bold = book.add_format({'bold': True, 'border': 1})
        format = book.add_format({'border': 1})
        sheet = book.add_worksheet("Procesos")
        sheet.set_column('A:A', 20)
        sheet.write(0, 0,  "Organismos",bold)
        if tipo == 'mensual':
            sheet.write(1, 0,  "I/S/Total",bold)
            control=True
            for i,organimo in enumerate(organismos):
                sheet.write(i+2, 0, organimo.siglas,format)
                no=1
                for j in range(1,13):
                    if control==True:
                        sheet.merge_range(0,no,0,no+2, MESES[j],bold)
                        sheet.write(1, no, "I",bold)
                        sheet.write(1, no+1, "S",bold)
                        sheet.write(1, no+2, "Total",bold)
                    where = '%(year)s = EXTRACT(YEAR FROM  fecha) AND %(month)s =  EXTRACT(MONTH FROM fecha)'%{'year': anno, 'month': j}
                    procesos=ProcesoInhabilitacion.objects.filter(graduado__organismo=organimo).extra(where=[where])
                    total_inhabilitaciones=procesos.filter(proceso='i').count()
                    total_suspensiones=procesos.filter(proceso='s').count()
                    total=total_inhabilitaciones+total_suspensiones
                    sheet.write(i+2, no, total_inhabilitaciones,format)
                    sheet.write(i+2, no+1, total_suspensiones,format)
                    sheet.write(i+2, no+2, total,format)
                    no=(j*3)+1
                control=False
        else:
            total_orgsanismos=len(organismos)
            sheet.write(0, 1,  "Inhabilitaciones",bold)
            sheet.write(0, 2,  "Suspensiones",bold)
            sheet.write(0, 3,  "Total",bold)
            sheet.set_column('B:B', 20)
            sheet.set_column('C:C', 20)
            for i,organismo in enumerate(organismos):
                sheet.write(i+1, 0, organismo.siglas,format)
                procesos=ProcesoInhabilitacion.objects.filter(graduado__organismo=organismo,fecha__year=anno)
                total_inhabilitaciones=procesos.filter(proceso='i').count()
                total_suspensiones=procesos.filter(proceso='s').count()
                total=total_inhabilitaciones+total_suspensiones
                sheet.write(i+1, 1, total_inhabilitaciones,format)
                sheet.write(i+1, 2, total_suspensiones,format)
                sheet.write(i+1, 3, total,format)
            formula_1 = '=SUM(%s)' % xl_range(1, 1,total_orgsanismos, 1)
            formula_2 = '=SUM(%s)' % xl_range(1, 2,total_orgsanismos, 2)
            formula_3 = '=SUM(%s)' % xl_range(1, 3,total_orgsanismos, 3)
            sheet.write(total_orgsanismos+1, 0, "Total",bold)
            sheet.write(total_orgsanismos+1, 1, formula_1,bold)
            sheet.write(total_orgsanismos+1, 2, formula_2,bold)
            sheet.write(total_orgsanismos+1, 3, formula_3,bold)
        book.close()
        return response

    else:
        return Http404


@login_required
def exportar_total_procesos_niveles(request):

    niveles=['Medio','Superior']
    if request.method== "POST":
        anno=int(request.POST['anno'])
        tipo=request.POST.get('tipo', None)
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = "attachment; filename=Totales_procesos_nivel_%s.xlsx"%anno
        book = Workbook(response, {'in_memory': True})
        bold = book.add_format({'bold': True, 'border': 1})
        format = book.add_format({'border': 1})
        sheet = book.add_worksheet("Procesos")
        sheet.set_column('A:A', 20)
        sheet.write(0, 0,  "Nivel",bold)
        if tipo == 'mensual':
            sheet.write(1, 0,  "I/S/Total",bold)
            control=True
            for i,nivel in enumerate(niveles):
                sheet.write(i+2, 0, nivel,format)
                no=1
                for j in range(1,13):
                    if control==True:
                        sheet.merge_range(0,no,0,no+2, MESES[j],bold)
                        sheet.write(1, no, "I",bold)
                        sheet.write(1, no+1, "S",bold)
                        sheet.write(1, no+2, "Total",bold)
                    where = '%(year)s =  EXTRACT(YEAR FROM fecha) AND %(month)s =  EXTRACT(MONTH FROM fecha)'%{'year': anno, 'month': j}
                    procesos=ProcesoInhabilitacion.objects.filter(graduado__nivel_educacional=nivel).extra(where=[where])
                    total_inhabilitaciones=procesos.filter(proceso='i').count()
                    total_suspensiones=procesos.filter(proceso='s').count()
                    total=total_inhabilitaciones+total_suspensiones
                    sheet.write(i+2, no, total_inhabilitaciones,format)
                    sheet.write(i+2, no+1, total_suspensiones,format)
                    sheet.write(i+2, no+2, total,format)
                    no=(j*3)+1
                control=False
        else:
            sheet.write(0, 1,  "Inhabilitaciones",bold)
            sheet.write(0, 2,  "Suspensiones",bold)
            sheet.write(0, 3,  "Total",bold)
            sheet.set_column('B:B', 20)
            sheet.set_column('C:C', 20)
            for i,nivel in enumerate(niveles):
                sheet.write(i+1, 0, nivel,format)
                procesos=ProcesoInhabilitacion.objects.filter(graduado__nivel_educacional=nivel,fecha__year=anno)
                total_inhabilitaciones=procesos.filter(proceso='i').count()
                total_suspensiones=procesos.filter(proceso='s').count()
                total=total_inhabilitaciones+total_suspensiones
                sheet.write(i+1, 1, total_inhabilitaciones,format)
                sheet.write(i+1, 2, total_suspensiones,format)
                sheet.write(i+1, 3, total,format)
            formula_1 = '=SUM(%s)' % xl_range(1, 1,len(niveles), 1)
            formula_2 = '=SUM(%s)' % xl_range(1, 2,len(niveles), 2)
            formula_3 = '=SUM(%s)' % xl_range(1, 3,len(niveles), 3)
            sheet.write(len(niveles)+1, 0, "Total",bold)
            sheet.write(len(niveles)+1, 1, formula_1,bold)
            sheet.write(len(niveles)+1, 2, formula_2,bold)
            sheet.write(len(niveles)+1, 3, formula_3,bold)
        book.close()
        return response

    else:
        return Http404

@login_required
def exportar_procesos_registro_nominal(request):
    if request.method== "POST":
            anno=int(request.POST['anno'])
            response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response['Content-Disposition'] = "attachment; filename=Registro_nominal_procesos_%s.xlsx"%anno
            book = Workbook(response, {'in_memory': True})
            bold = book.add_format({'bold': True, 'border': 1})
            format = book.add_format({'border': 1})
            for j in range(1,13):
                    sheet = book.add_worksheet(MESES[j])
                    sheet.set_column('A:A', 5)
                    sheet.set_column('B:B', 15)
                    sheet.set_column('C:C', 30)
                    sheet.set_column('D:D', 20)
                    sheet.set_column('E:E', 10)
                    sheet.set_column('F:F', 10)
                    sheet.set_column('G:G', 50)
                    sheet.set_column('H:H', 30)
                    sheet.set_column('I:I', 10)
                    sheet.set_column('J:J', 20)


                    sheet.write(0, 0,  "No",bold)
                    sheet.write(0, 1,  "CI",bold)
                    sheet.write(0, 2,  "Nombre y Apellidos",bold)
                    sheet.write(0, 3,  "OACE",bold)
                    sheet.write(0, 4,  "MN/NS",bold)
                    sheet.write(0, 5,  "S/I",bold)
                    sheet.write(0, 6,  "Especialidades",bold)
                    sheet.write(0, 7,  "Causales de Incumplimiento",bold)
                    sheet.write(0, 8,  "C/NC",bold)
                    sheet.write(0, 9,  "Provincias",bold)
                    where = '%(year)s =  EXTRACT(YEAR FROM fecha) AND %(month)s =  EXTRACT(MONTH FROM fecha)'%{'year': anno, 'month': j}
                    procesos=ProcesoInhabilitacion.objects.all().extra(where=[where])
                    for i, proceso in enumerate(procesos):
                        sheet.write(i+1, 0,  proceso.numero_resolucion,format)
                        sheet.write(i+1, 1,  proceso.graduado.ci,bold)
                        sheet.write(i+1, 2,  proceso.graduado.nombre_apellidos,format)
                        sheet.write(i+1, 3,  proceso.graduado.organismo.siglas,format)
                        sheet.write(i+1, 4,  proceso.graduado.nm_ns(),format)
                        sheet.write(i+1, 5,  proceso.proceso.capitalize(),format)
                        sheet.write(i+1, 6,  proceso.graduado.carrera.nombre,format)
                        sheet.write(i+1, 7,  proceso.causal.nombre,format)
                        sheet.write(i+1, 8,  proceso.graduado.c_nc(),format)
                        sheet.write(i+1, 9,  proceso.graduado.provincia.nombre,format)

            book.close()
            return response

    else:
        return Http404