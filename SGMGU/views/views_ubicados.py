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



@login_required
@permission_required(['administrador','especialista','dpts','mes','organismo'])
def buscar_ubicados(request,opcion):
    ClassForm=FormFactory.build(opcion)
    if request.method == "POST":
        form=ClassForm(request.POST)
        if form.is_valid():
           id_opcion=request.POST[opcion]
           return  redirect("/ubicados/propios/%s/%s"%(opcion,id_opcion))
    else:
        form=ClassForm()
    contexto= {'form':form, 'nombre_form':"Buscar ubicados por %s"%opcion.replace("_", " de ")}
    return render(request, "Ubicados/form_ubicado.html",contexto)


@login_required
@permission_required(['administrador','especialista','dpts','mes','organismo'])
def filtrar_ubicados(request,opcion,id_opcion):
      ubicados=UbicacionLaboral.objects.filter(Q(fecha_registro__year=datetime.date.today().year))

      if opcion == 'centro_estudio':
          objeto_opcion=Centro_estudio.objects.get(id=id_opcion)
          ubicados=ubicados.filter(centro_estudio__id=id_opcion)

      elif opcion == 'provincia_residencia':
          objeto_opcion=Provincia.objects.get(id=id_opcion)
          ubicados=ubicados.filter(municipio_residencia__provincia__id=id_opcion)

      elif opcion == 'provincia_ubicacion':
          objeto_opcion=Provincia.objects.get(id=id_opcion)
          ubicados=ubicados.filter(provincia_ubicacion__id=id_opcion)

      elif opcion == 'carrera':
          objeto_opcion=Carrera.objects.get(id=id_opcion)
          ubicados=ubicados.filter(carrera__id=id_opcion)

      elif opcion == 'organismo':
          objeto_opcion=Organismo.objects.get(id=id_opcion)
          ubicados=ubicados.filter(organismo__id=id_opcion)


      if request.user.perfil_usuario.categoria.nombre == "dpts":
          ubicados=ubicados.filter(centro_estudio__provincia=request.user.perfil_usuario.provincia)
      elif request.user.perfil_usuario.categoria.nombre == "organismo":
          ubicados=ubicados.filter(organismo=request.user.perfil_usuario.organismo)
      ubicados=paginar(request,ubicados)
      context={'opcion':opcion,'id_opcion':id_opcion,'ubicados':ubicados,'nombre_pag':"Listado de ubicados por %s: %s"%(opcion.replace("_", " de "),objeto_opcion.nombre),'paginas':crear_lista_pages(ubicados),'tab':'ubicados'}
      return render(request, "Ubicados/GestionUbicadosBusqueda.html", context)


@login_required
@permission_required(['administrador','especialista','dpts','organismo','mes'])
def m_ubicados(request,filtro):
    categoria=request.user.perfil_usuario.categoria.nombre
    ubicados=UbicacionLaboral.objects.filter(Q(fecha_registro__year=datetime.date.today().year))
    if categoria == "dpts":
        ubicados=ubicados.filter(centro_estudio__provincia=request.user.perfil_usuario.provincia)
    elif categoria == "organismo":
        ubicados=ubicados.filter(organismo=request.user.perfil_usuario.organismo)

    if  filtro == 'desfasados':
        ubicados=ubicados.filter(estado_ubicacion='desfasado')
    elif filtro == 'graduados':
        ubicados=ubicados.filter(estado_ubicacion='graduado')

    ubicados=paginar(request,ubicados)
    context={'ubicados':ubicados,'nombre_pag':"Listado de ubicados %s"%filtro,'paginas':crear_lista_pages(ubicados),'filtro':filtro}
    return render(request, "Ubicados/GestionUbicados.html", context)



@login_required
@permission_required(['administrador','especialista','dpts','organismo','mes'])
def buscar_ci_ubicado(request,ci):
  ubicados=UbicacionLaboral.objects.filter(Q(fecha_registro__year=datetime.date.today().year))
  if request.user.perfil_usuario.categoria.nombre == 'dpts':
      ubicados=ubicados.filter(centro_estudio__provincia=request.user.perfil_usuario.provincia)
  elif request.user.perfil_usuario.categoria.nombre == 'organismo':
      ubicados=ubicados.filter(organismo=request.user.perfil_usuario.organismo)
  ubicados=ubicados.filter(ci=ci)
  context={'ubicados':ubicados,'nombre_pag':"Listado de ubicados por ci: %s"%ci,'busqueda':'si',"valor_busqueda":ci}
  return render(request, "Ubicados/GestionUbicados.html", context)





@login_required
@permission_required(['administrador','especialista','dpts'])
def registrar_ubicacion(request):
    if request.method == 'POST':
        form = UbicadoForm(request.POST)
        if form.is_valid():
            ubicado=form.save(commit=False)
            ubicado.anno_graduado=datetime.date.today().year
            ubicado.save()
            messages.add_message(request, messages.SUCCESS, "La ubicación ha sido registrada con éxito.")
            return redirect('/ubicados')
    else:
        form = UbicadoForm()
    context = {'form':form,'nombre_form':"Registrar ubicado"}
    return render(request, "Ubicados/form_ubicado.html", context)


@login_required
@permission_required(['administrador','especialista','organismo'])
def no_presentacion(request):
     if request.method == 'POST':
        id_graduado=request.POST['graduado']
        causa=request.POST['causa']
        print causa
        ubicado=UbicacionLaboral.objects.get(id=id_graduado)
        ubicado.presentado=False
        ubicado.causa_no_presentacion=causa
        ubicado.save()
        messages.add_message(request, messages.SUCCESS, "La no presentación del ubicado en la entidad asignada se ha confirmado con éxito.")
        return redirect('/ubicados/%s'%id_graduado)
     else:
      return redirect('/ubicados')


@login_required
@permission_required(['administrador','especialista','organismo'])
def presentacion(request,id_ubicacion):
        ubicado=UbicacionLaboral.objects.get(id=id_ubicacion)
        ubicado.presentado=True
        ubicado.causa_no_presentacion=None
        ubicado.save()
        messages.add_message(request, messages.SUCCESS, "La presentación del ubicado en la entidad asignada se ha confirmado con éxito.")
        return redirect('/ubicados/%s'%id_ubicacion)


@login_required
@permission_required(['administrador','especialista'])
def eliminar_ubicacion(request,id_ubicacion):
        ubicacion=UbicacionLaboral.objects.get(id=id_ubicacion)
        ubicacion.delete()
        messages.add_message(request, messages.SUCCESS, "La ubicación ha sido eliminada con éxito.")
        return redirect('/ubicados')


@login_required
@permission_required(['administrador','especialista','dpts'])
def pasar_a_disponibles(request,id_ubicacion):
        ubicacion=UbicacionLaboral.objects.get(id=id_ubicacion)
        disponibilidad=DisponibilidadGraduados(
            centro_estudio=ubicacion.centro_estudio,
            carrera=ubicacion.carrera,
            ci=ubicacion.ci,
            nombre_apellidos=ubicacion.nombre_apellidos,
            municipio_residencia=ubicacion.municipio_residencia,
            sexo=ubicacion.sexo,
            direccion_particular=ubicacion.direccion_particular,
            cumple_servicio_social=ubicacion.cumple_servicio_social
        )
        try:
            disponibilidad.save()
            ubicacion.delete()
            messages.add_message(request, messages.SUCCESS, "Operación exitosa. El graduado ahora se encuentra disponible")
        except Exception as e:
            messages.add_message(request, messages.ERROR, "Error. Ya está registrado en el módulo de disponibles ese ci y boleta")


        return redirect('/ubicados')


@login_required
@permission_required(['administrador','especialista'])
def modificar_ubicacion(request,id_ubicacion):
        ubicacion=UbicacionLaboral.objects.get(id=id_ubicacion)
        if request.method == 'POST':
                form=UbicadoForm(request.POST,instance=ubicacion)
                if form.is_valid():
                    ubicado=form.save(commit=False)
                    ubicado.save()
                    messages.add_message(request, messages.SUCCESS, "La ubicación ha sido modificada con éxito.")
                    return redirect('/ubicados')
        else:
            form = UbicadoForm(instance=ubicacion)
        context = {'form':form,'nombre_form':"Modificar ubicado"}
        return render(request, "Ubicados/form_ubicado.html", context)




@login_required
@permission_required(['administrador','especialista','dpts','organismo','mes'])
def detalle_ubicacion(request,id_ubicacion):
        ubicacion=UbicacionLaboral.objects.get(id=id_ubicacion)
        context = {'ubicacion':ubicacion}
        return render(request, "Ubicados/detalle_ubicado.html", context)



def exportar_ubicados_provincia(request,opcion):
    if request.method == "POST":
       form=ExportarUbicadosProvinciaForm(request.POST)
       if form.is_valid():
           anno=form.cleaned_data['anno']
           provincia=form.cleaned_data['provincia']
           if opcion== "ubicacion":
                ubicados=UbicacionLaboral.objects.filter(anno_graduado=anno,provincia_ubicacion=provincia)
           else:
                ubicados=UbicacionLaboral.objects.filter(anno_graduado=anno,municipio_residencia__provincia=provincia)

           response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
           response['Content-Disposition'] = "attachment; filename=Registro_ubicados_provincia_%s_%s_%s.xlsx"%(opcion,provincia.nombre,anno)
           book = Workbook(response, {'in_memory': True})
           bold = book.add_format({'bold': True, 'border': 1})
           format = book.add_format({'border': 1})
           sheet = book.add_worksheet("Ubicados")
           sheet.set_column('A:A', 5)
           sheet.set_column('B:B', 10)
           sheet.set_column('C:C', 30)
           sheet.set_column('D:D', 50)
           sheet.set_column('E:E', 30)
           sheet.set_column('F:F', 50)
           sheet.set_column('G:G', 10)
           sheet.set_column('H:H', 40)
           sheet.set_column('I:I', 20)
           sheet.set_column('J:J', 22)
           sheet.set_column('K:K', 15)
           sheet.set_column('L:L', 15)
           sheet.set_column('M:M', 40)
           sheet.set_column('N:N', 20)
           sheet.set_column('O:O', 60)
           sheet.write(0, 0, "Anno",bold)
           sheet.write(0, 1, "Boleta",bold)
           sheet.write(0, 2, "Centro Estudio",bold)
           sheet.write(0, 3, "Carrera",bold)
           sheet.write(0, 4, "Carnet de identidad",bold)
           sheet.write(0, 5, "Nombre Apellidos",bold)
           sheet.write(0, 6,  "CSS",bold)
           sheet.write(0, 7, "Entidad",bold)
           sheet.write(0, 8, "Organismo",bold)
           sheet.write(0, 9, "Municipio de Residencia",bold)
           sheet.write(0, 10, "Provincia de Ubicacion",bold)
           sheet.write(0, 11, "Sexo",bold)
           sheet.write(0, 12, "Direccion Particular",bold)
           sheet.write(0, 13, "Presentado",bold)
           sheet.write(0, 14, "Causa No Pres",bold)
           for i,ubicado in enumerate(ubicados):
               i=i+1
               sheet.write(i, 0, ubicado.anno_graduado,format)
               sheet.write(i, 1, ubicado.boleta,format)
               sheet.write(i, 2, ubicado.centro_estudio.nombre,format)
               sheet.write(i, 3, ubicado.carrera.nombre,format)
               sheet.write(i, 4, ubicado.ci,format)
               sheet.write(i, 5, ubicado.nombre_apellidos,format)
               sheet.write(i, 6, ubicado.css(),format)
               sheet.write(i, 7, ubicado.entidad,format)
               sheet.write(i, 8, ubicado.organismo.siglas,format)
               sheet.write(i, 9, ubicado.municipio_residencia.nombre,format)
               sheet.write(i, 10, ubicado.provincia_ubicacion.siglas,format)
               sheet.write(i, 11, ubicado.sexo,format)
               sheet.write(i, 12, ubicado.direccion_particular,format)
               sheet.write(i, 13, ubicado.is_presentado(),format)
               sheet.write(i, 14, ubicado.causa_no_presentacion,format)
           book.close()
           return response
    else:
       form=ExportarUbicadosProvinciaForm()
    context={'form':form,'opcion_form':opcion}
    return render(request,"Reportes/ubicado_segun_provincia.html",context)

def exportar_ubicados_organismo(request):
    if request.method == "POST":
       form=ExportarUbicadosOrganismoForm(request.POST)
       if form.is_valid():
           anno=form.cleaned_data['anno']
           organismo=form.cleaned_data['organismo']
           ubicados=UbicacionLaboral.objects.filter(anno_graduado=anno,organismo=organismo)
           response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
           response['Content-Disposition'] = "attachment; filename=Registro_ubicados_organismo_%s_%s.xlsx"%(organismo.siglas,anno)
           book = Workbook(response, {'in_memory': True})
           bold = book.add_format({'bold': True, 'border': 1})
           format = book.add_format({'border': 1})
           sheet = book.add_worksheet("Ubicados")
           sheet.set_column('A:A', 5)
           sheet.set_column('B:B', 10)
           sheet.set_column('C:C', 30)
           sheet.set_column('D:D', 50)
           sheet.set_column('E:E', 30)
           sheet.set_column('F:F', 50)
           sheet.set_column('G:G', 10)
           sheet.set_column('H:H', 40)
           sheet.set_column('I:I', 20)
           sheet.set_column('J:J', 22)
           sheet.set_column('K:K', 15)
           sheet.set_column('L:L', 15)
           sheet.set_column('M:M', 40)
           sheet.set_column('N:N', 20)
           sheet.set_column('O:O', 60)
           sheet.write(0, 0, "Anno",bold)
           sheet.write(0, 1, "Boleta",bold)
           sheet.write(0, 2, "Centro Estudio",bold)
           sheet.write(0, 3, "Carrera",bold)
           sheet.write(0, 4, "Carnet de identidad",bold)
           sheet.write(0, 5, "Nombre Apellidos",bold)
           sheet.write(0, 6,  "CSS",bold)
           sheet.write(0, 7, "Entidad",bold)
           sheet.write(0, 8, "Organismo",bold)
           sheet.write(0, 9, "Municipio de Residencia",bold)
           sheet.write(0, 10, "Provincia de Ubicacion",bold)
           sheet.write(0, 11, "Sexo",bold)
           sheet.write(0, 12, "Direccion Particular",bold)
           sheet.write(0, 13, "Presentado",bold)
           sheet.write(0, 14, "Causa No Pres",bold)

           for i,ubicado in enumerate(ubicados):
               i=i+1
               sheet.write(i, 0, ubicado.anno_graduado,format)
               sheet.write(i, 1, ubicado.boleta,format)
               sheet.write(i, 2, ubicado.centro_estudio.nombre,format)
               sheet.write(i, 3, ubicado.carrera.nombre,format)
               sheet.write(i, 4, ubicado.ci,format)
               sheet.write(i, 5, ubicado.nombre_apellidos,format)
               sheet.write(i, 6, ubicado.css(),format)
               sheet.write(i, 7, ubicado.entidad,format)
               sheet.write(i, 8, ubicado.organismo.siglas,format)
               sheet.write(i, 9, ubicado.municipio_residencia.nombre,format)
               sheet.write(i, 10, ubicado.provincia_ubicacion.siglas,format)
               sheet.write(i, 11, ubicado.sexo,format)
               sheet.write(i, 12, ubicado.direccion_particular,format)
               sheet.write(i, 13, ubicado.is_presentado(),format)
               sheet.write(i, 14, ubicado.causa_no_presentacion,format)
           book.close()
           return response
    else:
       form=ExportarUbicadosOrganismoForm()
    context={'form':form}
    return render(request,"Reportes/ubicado_segun_organismo.html",context)

def exportar_total_ubicados_organismos(request):
    organismos=Organismo.objects.all()
    total=len(organismos)
    if request.method == "POST":
        anno=int(request.POST["anno"])
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = "attachment; filename=Totales_ubicados_organismos_%s.xlsx"%anno
        book = Workbook(response, {'in_memory': True})
        bold = book.add_format({'bold': True, 'border': 1})
        format = book.add_format({'border': 1})
        sheet = book.add_worksheet("Ubicados")
        sheet.set_column('A:A', 60)
        sheet.set_column('B:B', 20)
        sheet.set_column('C:C', 20)
        sheet.write(0, 0,  "Organismos",bold)
        sheet.write(0, 1,  "Total Ubicados",bold)
        sheet.write(0, 2,  "Presentados",bold)
        for i,organismo in enumerate(organismos):
            total_ubicados=UbicacionLaboral.objects.filter(organismo=organismo,anno_graduado=int(anno)).count()
            presentados=UbicacionLaboral.objects.filter(organismo=organismo,anno_graduado=int(anno),presentado=True).count()
            sheet.write(i+1, 0, organismo.nombre,format)
            sheet.write(i+1, 1, total_ubicados,format)
            sheet.write(i+1, 2, presentados,format)
        formula_rango_total = '=SUM(%s)' % xl_range(1, 1,total, 1)
        formula_rango_presentados = '=SUM(%s)' % xl_range(1, 2,total, 2)
        sheet.write(total+1, 0, "Total",bold)
        sheet.write(total+1, 1, formula_rango_total,bold)
        sheet.write(total+1, 2, formula_rango_presentados,bold)
        book.close()
        return response
    else:
        return Http404

def exportar_total_ubicados_provincias(request,opcion):
    provincias=Provincia.objects.all()
    total=len(provincias)
    total_ubicados=0
    if request.method == "POST":
        anno=int(request.POST["anno"])
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = "attachment; filename=Totales_ubicados_provincia_%s_%s.xlsx"%(opcion,anno)
        book = Workbook(response, {'in_memory': True})
        bold = book.add_format({'bold': True, 'border': 1})
        format = book.add_format({'border': 1})
        sheet = book.add_worksheet("Ubicados")
        sheet.write(0, 0,  "Provincias",bold)
        sheet.write(0, 1,  "Total Ubicados",bold)
        sheet.write(0, 2,  "Presentados",bold)
        sheet.set_column('A:A', 30)
        sheet.set_column('B:B', 20)
        sheet.set_column('C:C', 20)
        for i,provincia in enumerate(provincias):
            if opcion == "ubicacion":
                total_ubicados=UbicacionLaboral.objects.filter(provincia_ubicacion=provincia,anno_graduado=int(anno)).count()
                presentados=UbicacionLaboral.objects.filter(presentado=True,provincia_ubicacion=provincia,anno_graduado=int(anno)).count()

            elif opcion == "residencia":
                total_ubicados=UbicacionLaboral.objects.filter(municipio_residencia__provincia=provincia,anno_graduado=int(anno)).count()
                presentados=UbicacionLaboral.objects.filter(presentado=True,municipio_residencia__provincia=provincia,anno_graduado=int(anno)).count()

            sheet.write(i+1, 0, provincia.siglas,format)
            sheet.write(i+1, 1, total_ubicados,format)
            sheet.write(i+1, 2, presentados,format)
        formula_rango_total = '=SUM(%s)' % xl_range(1, 1,total, 1)
        formula_rango_presentados = '=SUM(%s)' % xl_range(1, 2,total, 2)
        sheet.write(total+1, 0, "Total",bold)
        sheet.write(total+1, 1, formula_rango_total,bold)
        sheet.write(total+1, 2, formula_rango_presentados,bold)

        book.close()
        return response
    else:
        return Http404

def exportar_ubicados(request):
    ubicados=[]
    anno=int(request.POST["anno"])
    if request.method == "POST":
        categoria=request.user.perfil_usuario.categoria.nombre
        if categoria == "organismo":
            ubicados=UbicacionLaboral.objects.filter(organismo=request.user.perfil_usuario.organismo,anno_graduado=anno)
        elif categoria == "dpts":
            ubicados=UbicacionLaboral.objects.filter(provincia_ubicacion=request.user.perfil_usuario.provincia,anno_graduado=anno)
        
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = "attachment; filename=registro_ubicados_%s.xlsx"%anno
        book = Workbook(response, {'in_memory': True})
        bold = book.add_format({'bold': True, 'border': 1})
        format = book.add_format({'border': 1})
        sheet = book.add_worksheet("Ubicados")
        sheet.set_column('A:A', 5)
        sheet.set_column('B:B', 10)
        sheet.set_column('C:C', 30)
        sheet.set_column('D:D', 50)
        sheet.set_column('E:E', 30)
        sheet.set_column('F:F', 50)
        sheet.set_column('G:G', 10)
        sheet.set_column('H:H', 40)
        sheet.set_column('I:I', 20)
        sheet.set_column('J:J', 22)
        sheet.set_column('K:K', 15)
        sheet.set_column('L:L', 15)
        sheet.set_column('M:M', 40)
        sheet.set_column('N:N', 20)
        sheet.set_column('O:O', 60)
        sheet.write(0, 0, "Anno",bold)
        sheet.write(0, 1, "Boleta",bold)
        sheet.write(0, 2, "Centro Estudio",bold)
        sheet.write(0, 3, "Carrera",bold)
        sheet.write(0, 4, "Carnet de identidad",bold)
        sheet.write(0, 5, "Nombre Apellidos",bold)
        sheet.write(0, 6,  "CSS",bold)
        sheet.write(0, 7, "Entidad",bold)
        sheet.write(0, 8, "Organismo",bold)
        sheet.write(0, 9, "Municipio de Residencia",bold)
        sheet.write(0, 10, "Provincia de Ubicacion",bold)
        sheet.write(0, 11, "Sexo",bold)
        sheet.write(0, 12, "Direccion Particular",bold)
        sheet.write(0, 13, "Presentado",bold)
        sheet.write(0, 14, "Causa No Pres",bold)
        for i,ubicado in enumerate(ubicados):
               i=i+1
               sheet.write(i, 0, ubicado.anno_graduado,format)
               sheet.write(i, 1, ubicado.boleta,format)
               sheet.write(i, 2, ubicado.centro_estudio.nombre,format)
               sheet.write(i, 3, ubicado.carrera.nombre,format)
               sheet.write(i, 4, ubicado.ci,format)
               sheet.write(i, 5, ubicado.nombre_apellidos,format)
               sheet.write(i, 6, ubicado.css(),format)
               sheet.write(i, 7, ubicado.entidad,format)
               sheet.write(i, 8, ubicado.organismo.siglas,format)
               sheet.write(i, 9, ubicado.municipio_residencia.nombre,format)
               sheet.write(i, 10, ubicado.provincia_ubicacion.siglas,format)
               sheet.write(i, 11, ubicado.sexo,format)
               sheet.write(i, 12, ubicado.direccion_particular,format)
               sheet.write(i, 13, ubicado.is_presentado(),format)
               sheet.write(i, 14, ubicado.causa_no_presentacion,format)
        book.close()
        return response
    else:
        return Http404

#solo dpts
def exportar_ubicados_universidades(request):
    anno=int(request.POST["anno"])
    if request.method == "POST":
        ubicados=UbicacionLaboral.objects.filter(centro_estudio__provincia=request.user.perfil_usuario.provincia,anno_graduado=anno)
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = "attachment; filename=registro_ubicados_universidades_%s.xlsx"%anno
        book = Workbook(response, {'in_memory': True})
        bold = book.add_format({'bold': True, 'border': 1})
        format = book.add_format({'border': 1})
        sheet = book.add_worksheet("Ubicados")
        sheet.set_column('A:A', 5)
        sheet.set_column('B:B', 10)
        sheet.set_column('C:C', 30)
        sheet.set_column('D:D', 50)
        sheet.set_column('E:E', 30)
        sheet.set_column('F:F', 50)
        sheet.set_column('G:G', 10)
        sheet.set_column('H:H', 40)
        sheet.set_column('I:I', 20)
        sheet.set_column('J:J', 22)
        sheet.set_column('K:K', 15)
        sheet.set_column('L:L', 15)
        sheet.set_column('M:M', 40)
        sheet.set_column('N:N', 20)
        sheet.set_column('O:O', 60)
        sheet.write(0, 0, "Anno",bold)
        sheet.write(0, 1, "Boleta",bold)
        sheet.write(0, 2, "Centro Estudio",bold)
        sheet.write(0, 3, "Carrera",bold)
        sheet.write(0, 4, "Carnet de identidad",bold)
        sheet.write(0, 5, "Nombre Apellidos",bold)
        sheet.write(0, 6,  "CSS",bold)
        sheet.write(0, 7, "Entidad",bold)
        sheet.write(0, 8, "Organismo",bold)
        sheet.write(0, 9, "Municipio de Residencia",bold)
        sheet.write(0, 10, "Provincia de Ubicacion",bold)
        sheet.write(0, 11, "Sexo",bold)
        sheet.write(0, 12, "Direccion Particular",bold)
        sheet.write(0, 13, "Presentado",bold)
        sheet.write(0, 14, "Causa No Pres",bold)
        for i,ubicado in enumerate(ubicados):
               i=i+1
               sheet.write(i, 0, ubicado.anno_graduado,format)
               sheet.write(i, 1, ubicado.boleta,format)
               sheet.write(i, 2, ubicado.centro_estudio.nombre,format)
               sheet.write(i, 3, ubicado.carrera.nombre,format)
               sheet.write(i, 4, ubicado.ci,format)
               sheet.write(i, 5, ubicado.nombre_apellidos,format)
               sheet.write(i, 6, ubicado.css(),format)
               sheet.write(i, 7, ubicado.entidad,format)
               sheet.write(i, 8, ubicado.organismo.siglas,format)
               sheet.write(i, 9, ubicado.municipio_residencia.nombre,format)
               sheet.write(i, 10, ubicado.provincia_ubicacion.siglas,format)
               sheet.write(i, 11, ubicado.sexo,format)
               sheet.write(i, 12, ubicado.direccion_particular,format)
               sheet.write(i, 13, ubicado.is_presentado(),format)
               sheet.write(i, 14, ubicado.causa_no_presentacion,format)
        book.close()
        return response
    else:
        return Http404