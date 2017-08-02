# -*- coding: utf-8 -*-
from django.shortcuts import render,redirect
from SGMGU.models import *
from SGMGU.forms import *
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .utiles import *
from django.http import HttpResponse,Http404
import datetime
from django.db.models import Q
import xlrd
from .views_ubicados import *

@login_required
@permission_required(['administrador','especialista','dpts','mes'])
def m_disponibles(request,errors=None):
    disponibles=DisponibilidadGraduados.objects.all()
    categoria=request.user.perfil_usuario.categoria.nombre
    if categoria == "dpts":
        disponibles=disponibles.filter(centro_estudio__provincia=request.user.perfil_usuario.provincia)
    disponibles=paginar(request,disponibles)
    context={'errors':errors,'disponibles':disponibles,'nombre_pag':"Listado de disponibles",'paginas':crear_lista_pages(disponibles),'tab':'disponibles'}
    return render(request, "Ubicados/GestionUbicados.html", context)



@login_required
@permission_required(['administrador','especialista','dpts','mes'])
def buscar_ci_disponible(request,ci):
  if request.user.perfil_usuario.categoria.nombre == 'dpts':
      disponibles=DisponibilidadGraduados.objects.filter(centro_estudio__provincia=request.user.perfil_usuario.provincia)
  else:
      disponibles=DisponibilidadGraduados.objects.all()
  disponibles=disponibles.filter(ci=ci)
  context={'disponibles':disponibles,'nombre_pag':"Listado de disponibles por ci: %s"%ci,'busqueda':'si','tab':'disponibles'}
  return render(request, "Ubicados/GestionUbicados.html", context)



@login_required
@permission_required(['administrador','especialista','mes'])
def registrar_disponibilidad(request):
    if request.method == 'POST':
        form = DisponibleForm(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, "La disponibilidad ha sido registrada con éxito.")
            return redirect('/disponibles')
    else:
        form = DisponibleForm()
    context = {'form':form,'nombre_form':"Registrar disponibilidad",'tab':'disponibles'}
    return render(request, "Ubicados/form_ubicado.html", context)


@login_required
@permission_required(['administrador','especialista','dpts','mes'])
def filtrar_disponibles(request,opcion,id_opcion):
      disponibles=DisponibilidadGraduados.objects.all()
      if opcion == 'centro_estudio':
          objeto_opcion=Centro_estudio.objects.get(id=id_opcion)
          disponibles=disponibles.filter(centro_estudio__id=id_opcion)
      elif opcion == 'municipio_residencia':
          objeto_opcion=Municipio.objects.get(id=id_opcion)
          disponibles=disponibles.filter(municipio_residencia__id=id_opcion)
      elif opcion == 'carrera':
          objeto_opcion=Carrera.objects.get(id=id_opcion)
          disponibles=disponibles.filter(carrera__id=id_opcion)
      if request.user.perfil_usuario.categoria.nombre == "dpts":
          disponibles=disponibles.filter(centro_estudio__provincia=request.user.perfil_usuario.provincia)
      disponibles=paginar(request,disponibles)
      context={'opcion':opcion,'id_opcion':id_opcion,'disponibles':disponibles,'nombre_pag':"Listado de disponibles por %s: %s"%(opcion.replace("_", " de "),objeto_opcion.nombre),'paginas':crear_lista_pages(disponibles),'tab':'disponibles'}
      return render(request, "Ubicados/GestionDisponiblesBusqueda.html", context)




@login_required
@permission_required(['administrador','especialista','dpts','mes'])
def buscar_disponibles(request,opcion):
    ClassForm=FormFactory.build(opcion)
    if request.method == "POST":
        form=ClassForm(request.POST)
        if form.is_valid():
           id_opcion=request.POST[opcion]
           return  redirect("/disponibles/%s/%s"%(opcion,id_opcion))
    else:
        form=ClassForm()
    contexto= {'form':form, 'nombre_form':"Buscar disponibles por %s"%opcion.replace("_", " de ")}
    return render(request, "Ubicados/form_ubicado.html",contexto)













@login_required
@permission_required(['administrador','especialista'])
def eliminar_disponibilidad(request,id_disponibilidad):
        disponibilidad=DisponibilidadGraduados.objects.get(id=id_disponibilidad)
        disponibilidad.delete()
        messages.add_message(request, messages.SUCCESS, "La disponibilidad ha sido eliminada con éxito.")
        return redirect('/disponibles')



@login_required
@permission_required(['administrador','especialista','dpts'])
def ubicar_disponibilidad(request,id_disponibilidad):
        disponibilidad=DisponibilidadGraduados.objects.get(id=id_disponibilidad)
        if request.method == 'POST':
                form=UbicadoForm(request.POST)
                if form.is_valid():
                    ubicado=form.save(commit=False)
                    ubicado.anno_graduado=datetime.date.today().year
                    ubicado.save()
                    disponibilidad.delete()
                    messages.add_message(request, messages.SUCCESS, "El graduado ha sido ubicado con éxito.")
                    return redirect('/disponibles')
        else:
            if request.user.perfil_usuario.categoria.nombre == "dpts":
                form = UbicadoForm(instance=disponibilidad)
            else:
                 form = UbicadoForm(instance=disponibilidad)
        context = {'form':form,'nombre_form':"Ubicar graduado",'tab':'disponibles'}
        return render(request, "Ubicados/form_ubicado.html", context)


@login_required
@permission_required(['administrador','especialista'])
def importar_disponibilidad(request):
    if request.method == 'POST':
        errors=[]
        excel=request.FILES['disponibles_file']

        if excel.name.split(".")[-1] != 'xlsx' and excel.name.split(".")[-1] != 'xls':
            messages.add_message(request, messages.ERROR, "El archivo subido es incorrecto")
            return redirect('/disponibles')
        else:
            book = xlrd.open_workbook(file_contents=excel.read())
            matriz=book.sheet_by_index(0)._cell_values
            for i,fila in enumerate(matriz):
                if i>0:
                     disponibilidad=DisponibilidadGraduados(
                            centro_estudio=get_value_field('centro_estudio',matriz,i,request.POST),
                            carrera=get_value_field('carrera',matriz,i,request.POST),
                            ci=get_value_field('ci',matriz,i,request.POST),
                            nombre_apellidos=get_value_field('nombre_apellidos',matriz,i,request.POST),
                            municipio_residencia=get_value_field('municipio_residencia',matriz,i,request.POST),
                            sexo=get_value_field('sexo',matriz,i,request.POST),
                            direccion_particular=get_value_field('direccion_residencia',matriz,i,request.POST),
                            cumple_servicio_social=get_value_field('css',matriz,i,request.POST),
                     )

                     try:
                         disponibilidad.save()
                     except Exception, e:
                         errors.append((i+1,e.message))
        if len(errors)>0:
            response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response['Content-Disposition'] = "attachment; filename=Errores_encontrados_importar_disponibilidad.xlsx"
            book = Workbook(response, {'in_memory': True})
            bold = book.add_format({'bold': True, 'border': 1})
            format = book.add_format({'border': 1})
            sheet = book.add_worksheet("Errores")

            sheet.set_column('A:A', 10)
            sheet.set_column('B:B', 80)
            sheet.write(0, 0,  "No.Fila",bold)
            sheet.write(0, 1,  "Error",bold)

            for i,error in enumerate(errors):
                sheet.write(i+1, 0, unicode(error[0]),format)
                sheet.write(i+1, 1, error[1].decode('utf-8'),format)
            book.close()
            return response
        else:
            messages.add_message(request, messages.SUCCESS, "La disponibilidad ha sido importada con éxito.")
            return redirect("/disponibles")






def get_value_field(clave,matriz,pos_fila,request_post):
         field=None
         pos_columna=int(request_post[clave])-1
         valor_celda=(unicode(matriz[pos_fila][pos_columna]).strip()).replace(".0",'')

         if clave == "centro_estudio":
             try:
                field=Centro_estudio.objects.filter(codigo_mes=valor_celda)[0]
             except:
                 pass
         elif clave == "carrera":
             try:
                field=Carrera.objects.filter(codigo_mes=valor_celda)[0]
             except:
                pass
         elif clave == "municipio_residencia":
             try:
                 field=Municipio.objects.filter(codigo_mes=valor_celda)[0]
             except:
                 pass
         elif clave == "css":
            if valor_celda=='T':
                field=True
            else:
                field=False
         else:
                field=valor_celda
         return field




@login_required
@permission_required(['administrador','especialista','dpts','mes'])
def detalle_disponibilidad(request,id_disponibilidad):
        disponibilidad=DisponibilidadGraduados.objects.get(id=id_disponibilidad)
        context = {'disponibilidad':disponibilidad}
        return render(request, "Ubicados/detalle_disponible.html", context)







