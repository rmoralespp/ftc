# -*- coding: utf-8 -*-

from django.shortcuts import render,redirect,get_object_or_404,get_list_or_404
from django.contrib.auth.decorators import login_required,permission_required
from django.contrib.auth import authenticate,login,logout
from SGMGU.models import *
from django.http import Http404,HttpResponse


from django.contrib import messages



def is_auth(function):
    def apply_function(request, *args,**kwargs):
        if request.user.is_anonymous():
            response = function(request, *args, **kwargs)
        else:
            response = redirect("/inicio")
        return response
    return apply_function


@login_required()
def inicio(request):
    return render(request, "General/index.html", {})


def contacto(request):
    return  render(request,"General/contacto.html",{})

@is_auth
def login_view(request):
    sms=None
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        user=authenticate(username=username,password=password)
        if user is not None:
            if user.is_active:
                login(request,user)
                return redirect("/inicio")
            else:
                messages.add_message(request, messages.ERROR, "Su usuario esta inactivo, contacte con el administrador")
                return redirect("/login")
        else:
             messages.add_message(request, messages.ERROR, "Los datos ingresados son incorrectos.")
             return redirect("/login")

    else:
     contexto={}

     return render(request,"General/login.html",contexto)



@login_required
def logout_view(request):
       logout(request)
       return redirect("/login")


def descargar_comprimido(request,id_expediente):
    exp=Expediente_movimiento_externo.objects.get(id=id_expediente)
    comprimido=exp.comprimido
    filename = unicode(comprimido.file.name.split('/')[-1]).replace(" ","_")
    response = HttpResponse(comprimido.file, content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename=%s' % filename
    return response


def descargar_informe(request,id_expediente):
    exp=Expediente_aprobado.objects.get(id=id_expediente)
    carta_expediente=exp.carta_expediente
    response = HttpResponse(carta_expediente.file, content_type='application/pdf')
    rs=unicode(exp.codigo_DE_RS).replace("DE-RS","RS").replace(" ","_")
    ol=unicode(exp.expediente.organismo_liberacion.siglas)
    pl=unicode(exp.expediente.mun_entidad_liberacion.provincia.siglas)
    oa=unicode(exp.expediente.organismo_aceptacion.siglas)
    pa=unicode(exp.expediente.mun_entidad_aceptacion.provincia.siglas)
    ng=unicode(exp.expediente.graduado.nombre).replace(" ","_")
    nombre_file=rs+"-"+ol+"-"+pl+"-"+oa+"-"+pa+"-"+ng
    nombre_file.replace(" ","_")
    response['Content-Disposition'] = 'attachment; filename=%s.pdf' % unicode(nombre_file)

    return response


def ver_informe(request,id_expediente):
    exp=Expediente_aprobado.objects.get(id=id_expediente)
    comprimido=exp.carta_expediente
    response = HttpResponse(comprimido.file, content_type='application/pdf')
    response['X-Sendfile'] = unicode(comprimido.file.name)
    return response



def enviar_notificacion(request):
    if request.method == "POST":
        texto=request.POST['texto']
        remitentes=request.POST.getlist('remitente')
        if len(remitentes)>0:
            for remitente in remitentes:
                Notificacion.objects.create(
                    emisor=request.user,
                    remitente=User.objects.get(id=remitente),
                    texto=texto
                )
        return redirect("/inicio")
    else:
        return  Http404



from django.core.serializers import serialize
from django.http import JsonResponse
def revisar_notificacion(request,id_notificacion):
     try:
         notificacion=Notificacion.objects.get(id=id_notificacion)
     except notificacion.DoesNotExist:
         notificacion=None
     if notificacion!=None:
         notificacion.revisado=True
         notificacion.save()
         data = {
            'id': notificacion.id,
            'texto': notificacion.texto,
            'emisor': notificacion.emisor.first_name +" "+notificacion.emisor.last_name,
            'emisor_id': notificacion.emisor.id,
            'categoria_emisor':notificacion.emisor.perfil_usuario.organismo.siglas,
            'remitente': notificacion.remitente.username
         }
        # notificacion.delete()
     else:
         data={}
     return JsonResponse(data)



def eliminar_notificacion(request,id_notificacion):
     try:
         notificacion=Notificacion.objects.get(id=id_notificacion)
     except notificacion.DoesNotExist:
         notificacion=None
     if notificacion!=None:
         notificacion.delete()
     return JsonResponse({})


def ficha_graduado(request,ci):
    try:     datos_ubicado=UbicacionLaboral.objects.filter(ci=ci)[0]
    except:  datos_ubicado=None
    try:     datos_inhabilitado=GraduadoInhabilitacion.objects.filter(ci=ci)[0]
    except:  datos_inhabilitado=None
    mov_externos=Expediente_aprobado.objects.filter(expediente__graduado__ci=ci)
    mov_internos=Expediente_movimiento_interno.objects.filter(graduado__ci=ci)
    contexto={
        'datos_ubicado':datos_ubicado,
        'mov_externos':mov_externos,
        'mov_internos':mov_internos,
        'ci':ci,
        'busqueda_ficha':True,
        'datos_inhabilitado':datos_inhabilitado
    }
    return render(request,"General/ficha_graduado.html",contexto)


def movimiento_laboral(request):
    return render(request, "General/index.html", {})

def ubicacion_laboral(request):
    return render(request, "General/index.html", {})


def nomencladores(request):
    return render(request, "General/index.html", {})

def geforza(request):
    return render(request, "General/index.html", {})

