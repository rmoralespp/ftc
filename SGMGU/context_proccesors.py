# -*- coding: utf-8 -*-
from SGMGU.models import Perfil_usuario
from django.core.urlresolvers import reverse
import datetime


def profile(request):
    current_url = request.resolver_match.url_name
    if current_url!="login" and request.path != "/":
        profile=request.user.perfil_usuario
        return {'profile': profile}
    else:
        return {}

def menu(request):
    MENU={'menu':[]}
    url_actual=request.path
    try:
        cat=request.user.perfil_usuario.categoria.nombre
    except:
        cat="anonimo"
    menu_dict={'menu':[
            {'name':'Inicio','url':reverse('inicio'),'icon':'glyphicon glyphicon-home','visible':['administrador','especialista','invitado','organismo','dpts']},
            {'name':'Movimiento Laboral','url':reverse('movimiento_laboral'),'icon':'glyphicon glyphicon-briefcase','visible':['administrador','especialista','invitado','organismo','dpts'],
               'menu':[
                    {'name':'Pendientes','url':reverse('pendientes'),'icon':'glyphicon glyphicon-chevron-right','visible':['administrador','especialista','invitado','organismo']},
                    {'name':'Rechazados','url':reverse('rechazados'),'icon':'glyphicon glyphicon-chevron-right','visible':['administrador','especialista','invitado','organismo']},
                    {'name':'No Aprobados','url':reverse('no_aprobados'),'icon':'glyphicon glyphicon-chevron-right','visible':['administrador','especialista','invitado','organismo']},
                    {'name':'Aprobados','url':reverse('aprobados'),'icon':'glyphicon glyphicon-chevron-right','visible':['administrador','especialista','invitado','organismo','dpts']},
                    {'name':'Gestión de Externos','url':reverse('expedientes'),'icon':'glyphicon glyphicon-chevron-right','visible':['administrador','especialista']},
                    {'name':'Gestión de Internos','url':reverse('movimientos_internos'),'icon':'glyphicon glyphicon-chevron-right','visible':['administrador','especialista','organismo']},
                    {'name':'Registrar Expediente','url':reverse('registrar_expediente_estandar'),'icon':'glyphicon glyphicon-chevron-right','visible':['organismo']},
               ]
             },

            {'name':'Ubicación Laboral','url':reverse('ubicacion_laboral'),'icon':'glyphicon glyphicon-briefcase','visible':['administrador','especialista','organismo','dpts','mes'],
              'menu':[
                  {'name':'Disponibles','url':reverse('disponibles'),'icon':'glyphicon glyphicon-chevron-right','visible':['administrador','especialista','dpts','mes']},
                  {'name':'Ubicados','url':reverse('ubicados'),'icon':'glyphicon glyphicon-chevron-right','visible':['administrador','especialista','organismo','dpts','mes']},
              ]
             },
            {'name':'Inhabilitaciones','url':reverse('inhabilitaciones'),'icon':'glyphicon glyphicon-briefcase','visible':['administrador','especialista','juridico']},

            {'name':'Reportes','url':reverse('reportes'),'icon':'glyphicon glyphicon-menu-hamburger','visible':['administrador','especialista','organismo','dpts','invitado','mes','juridico']},

            {'name':'Nomencladores','url':reverse('nomencladores'),'icon':'glyphicon glyphicon-bookmark','visible':['administrador','especialista'],
               'menu':[
                    {'name':'Gestión de Organismos','url':reverse('organismos'),'icon':'glyphicon glyphicon-chevron-right','visible':['administrador','especialista']},
                    {'name':'Gestión de Causales','url':reverse('causales'),'icon':'glyphicon glyphicon-chevron-right','visible':['administrador','especialista']},
                    {'name':'Gestión de Dir Trabajo','url':reverse('dir_trabajo'),'icon':'glyphicon glyphicon-chevron-right','visible':['administrador','especialista']},
                    {'name':'Gestión de Carreras','url':reverse('carreras'),'icon':'glyphicon glyphicon-chevron-right','visible':['administrador','especialista']},
                    {'name':'Gestión de Centros de Estudios','url':reverse('carreras'),'icon':'glyphicon glyphicon-chevron-right','visible':['administrador','especialista']},
               ]
             },
            {'name':'Usuarios','url':reverse('usuarios'),'icon':'glyphicon glyphicon-user','visible':['administrador','especialista']}

             ]}
    return procesar_menu(menu_dict,url_actual,cat,MENU)

def procesar_menu(menu_main,url_actual,cat,MENU):
   for item in menu_main['menu']:
        if is_visible(item,cat):
            item['active']= is_activo(item,url_actual)
            if item.get('menu')!= None:
                submenus=[]
                for i,item2 in enumerate(item.get('menu')):
                    if is_visible(item2,cat):
                        item2['active']= is_activo(item2,url_actual)
                        submenus.append(item2)
                item['menu']=submenus
            MENU['menu'].append(item)
   return MENU

def is_activo(item,url_actual):
    control=False
    if item['url'] == url_actual:
            control=  True
    elif url_actual.split("/")[1] == item['url'].split("/")[1]:
            control = True
    elif item.get('menu') != None:
        for item2 in item.get('menu'):
            if is_activo(item2,url_actual)==True:
                control=True
                break
    return control


def is_visible(item,cat):
        control=False
        if item['visible'].__contains__(cat):
            control=True
        return control








from .models import Notificacion
from .models import User

def notificaciones(request):
    current_url = request.resolver_match.url_name
    if current_url!="login" and request.path != "/":
        notificaciones=Notificacion.objects.filter(remitente=request.user).order_by("-fecha")
        notificaciones={'notificaciones':notificaciones,'cantidad_no_revisadas':Notificacion.objects.filter(revisado=False,remitente=request.user).count()}
        return notificaciones
    else:
        notificaciones={'notificaciones':[]}
        return notificaciones



def lista_usuarios(request):
    current_url = request.resolver_match.url_name
    if current_url!="login" and request.path != "/":
        usuarios=User.objects.filter(perfil_usuario__activo=True).exclude(id=request.user.id)
        usuarios={'usuarios':usuarios}
        return usuarios
    else:
        usuarios={'usuarios':[]}
        return usuarios


def annos(request):
    anno_actual=datetime.datetime.today().year
    return {'annos':range(2015,anno_actual+1)}
