__author__ = 'Rolando.Morales'
from django.conf.urls import  include, url

from django.contrib import admin
admin.autodiscover()
from SGMGU.views.views_usuarios import *
from SGMGU.views.views_expedientes import *
from SGMGU.views.views import *
from SGMGU.views.views_organismos import *
from SGMGU.views.views_causales import *
from SGMGU.views.view_movimientos_internos import *
from SGMGU.views.views_dir_trabajo import *
from SGMGU.views.views_reportes import *
from SGMGU.views.views_ubicados import *
from SGMGU.views.views_inhabilitaciones import *
from SGMGU.views.views_disponibles import *
from django.conf import settings
from django.views.static import  serve


urlpatterns = [
    url(r'^media/(?P<path>.*)$',serve,{'document_root':settings.MEDIA_ROOT,}),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^inicio$',inicio, name='inicio'),
    url(r'^$',login_view, ),
    url(r'^login$',login_view, name="login"),
    url(r'^logout$',logout_view),
    url(r'^contacto',contacto,name='contacto'),


    url(r'^enviar_notificacion$',enviar_notificacion),
    url(r'^revisar_notificacion/(?P<id_notificacion>[\w]+)$',revisar_notificacion),
    url(r'^eliminar_notificacion/(?P<id_notificacion>[\w]+)$',eliminar_notificacion),




    url(r'^usuarios$',gestion_usuarios,name='usuarios'),
    url(r'^usuarios/(?P<id_usuario>[\w]+)/modificar/$',modificar_usuario),
    url(r'^usuarios/(?P<id_usuario>[\w]+)/cambiar_contrasenna/$',cambiar_contrasenna),
    url(r'^usuarios/(?P<id_usuario>[\w]+)/eliminar/$',eliminar_usuario),
    url(r'^usuarios/registrar_usuario/$',registrar_usuario),
    url(r'^usuario/cambiar_contrasenna/$',cambiar_contrasenna_user_actual),
    url(r'^usuario/modificar/$',modificar_usuario_actual),


    url(r'^gestion_expedientes$',gestion_expedientes,name='expedientes'),
    url(r'^autocompletar_expediente$',autocompletar_expediente,{'vista':'avanzada'}),
    url(r'^autocompletar_movimiento_interno$',autocompletar_expediente,{'vista':'interno'}),

    url(r'^autocompletar_expediente_estandar$',autocompletar_expediente,{'vista':'estandar'}),
    url(r'^gestion_expedientes/registrar_expediente$',registrar_expediente,{'vista':'avanzada'}),
    url(r'^gestion_expedientes/(?P<id_expediente>[\w]+)/modificar/$',editar_expediente,{'vista':'estandar'} ),
    url(r'^gestion_expedientes/(?P<id_expediente>[\w]+)/eliminar/$',eliminar_expediente),
    url(r'^registrar_expediente_estandar/$',registrar_expediente ,{'vista':'estandar'},name="registrar_expediente_estandar",),
    url(r'^gestion_expedientes/ci/(?P<ci>[\w]+)$',buscar_expediente_ci),
    url(r'^gestion_expedientes/id/(?P<id>[\w]+)$',buscar_expediente_id),
    url(r'^gestion_expedientes/(?P<id_expediente>[\w]+)$',detalle_expediente),

    url(r'^organismos$',gestion_organismos,name='organismos'),
    url(r'^organismos/registrar_organismo/$',registrar_organismo),
    url(r'^organismos/(?P<id_organismo>[\w]+)/eliminar/$',eliminar_organismo),
    url(r'^organismos/(?P<id_organismo>[\w]+)/modificar/$',modificar_organismo),


    url(r'^causales$',gestion_causales,name='causales'),
    url(r'^causales/registrar_causal/$',registrar_causal),
    url(r'^causales/(?P<id_causal>[\w]+)/eliminar/$',eliminar_causal),
    url(r'^causales/(?P<id_causal>[\w]+)/modificar/$',modificar_causal),


    url(r'^descargar_comprimido/(?P<id_expediente>[\w]+)$',descargar_comprimido),
    url(r'^descargar_informe/(?P<id_expediente>[\w]+)$',descargar_informe),
    url(r'^ver_informe/(?P<id_expediente>[\w]+)$',ver_informe),
    url(r'^exportar_resumen_mensual$',exportar_resumen_mensual),
    url(r'^exportar_carreras_expedientes$',exportar_carreras_expedientes),
    url(r'^exportar_causales_expedientes$',exportar_causales_expedientes),
    url(r'^exportar_provincias_expedientes$',exportar_provincias_expedientes),
    url(r'^exportar_organismos_expedientes$',exportar_organismos_expedientes),
    url(r'^exportar_expedientes_carrera$',exportar_expedientes_segun_carrera),
    url(r'^exportar_expedientes_causal$',exportar_expedientes_segun_causal),






    url(r'^expedientes_pendientes$',listado_expedientes_pendientes,name='pendientes'),
    url(r'^expedientes_pendientes/(?P<id_expediente>[\w]+)$',detalle_expediente_pendiente),
    url(r'^aprobar_expediente_pendiente/(?P<id_expediente_pend>[\w]+)$',aprobar_expediente_pendiente),
    url(r'^rechazar_expediente_pendiente/(?P<id_expediente_pend>[\w]+)$',rechazar_expediente_pendiente),
    url(r'^no_aprobar_expediente_pendiente/(?P<id_expediente_pend>[\w]+)$',no_aprobar_expediente_pendiente),
    url(r'^exportar_expediente/(?P<id_expediente>[\d]+)$',exportar_expediente),
    url(r'^exportar_expediente_aprobado/(?P<id_expediente>[\d]+)$',exportar_expediente_aprobado),


    url(r'^expedientes_pendientes/(?P<id_expediente>[\w]+)/editar$',editar_expediente,{'vista':'pendiente'}),
    url(r'^expedientes_rechazados/(?P<id_expediente>[\w]+)/editar$',editar_expediente,{'vista':'rechazado'}),
    url(r'^expedientes_aprobados/(?P<id_expediente>[\w]+)/editar$',editar_expediente,{'vista':'aprobado'}),
    url(r'^expedientes_no_aprobados/(?P<id_expediente>[\w]+)/editar$',editar_expediente,{'vista':'no_aprobado'}),
    url(r'^expedientes_pendientes/ci/(?P<ci>[\w]+)$',buscar_expedientes_pendientes_ci),


    url(r'^expedientes_rechazados$',listado_expedientes_rechazado,name='rechazados'),
    url(r'^aprobar_expediente_rechazado/(?P<id_expediente_rech>[\w]+)$',aprobar_expediente_rechazado),
    url(r'^no_aprobar_expediente_rechazado/(?P<id_expediente_rech>[\w]+)$',no_aprobar_expediente_rechazado),
    url(r'^pasar_a_pendientes_de_rechazo/(?P<id_expediente>[\w]+)$',pasar_a_pendientes_from_rechazo),
    url(r'^expedientes_rechazados/(?P<id_expediente>[\w]+)$',detalle_expediente_rechazado),
    url(r'^expedientes_rechazados/ci/(?P<ci>[\w]+)$',buscar_expedientes_rechazados_ci),


    url(r'^expedientes_no_aprobados$',listado_expedientes_no_aprobados,name='no_aprobados'),
    url(r'^pasar_a_pendientes_de_no_aprobado/(?P<id_expediente>[\w]+)$',pasar_a_pendientes_de_no_aprobado),
    url(r'^expedientes_no_aprobados/detalle_expediente_no_aprobado/(?P<id_expediente>[\w]+)$',detalle_expediente_no_aprobado),
    url(r'^aprobar_expediente_no_aprobado/(?P<id_expediente_no_aprob>[\w]+)$',aprobar_expediente_no_aprobado),
    url(r'^rechazar_expediente_no_aprobado/(?P<id_expediente_no_aprob>[\w]+)$',rechazar_expediente_no_aprobado),
    url(r'^expedientes_no_aprobados/(?P<id_expediente>[\w]+)$',detalle_expediente_no_aprobado),
    url(r'^expedientes_no_aprobados/ci/(?P<ci>[\w]+)$',buscar_expedientes_no_aprobados_ci),


    url(r'^expedientes_aprobados$',listado_expedientes_aprobados,name='aprobados'),
    url(r'^pasar_a_pendientes/(?P<id_expediente>[\w]+)$',pasar_a_pendientes),
    url(r'^no_aprobar_expediente_aprobado/(?P<id_expediente_aprob>[\w]+)$',no_aprobar_expediente_aprobado),
    url(r'^rechazar_expediente_aprobado/(?P<id_expediente_aprob>[\w]+)$',rechazar_expediente_aprobado),
    url(r'^expedientes_aprobados/ci/(?P<ci>[\w]+)$',buscar_expedientes_aprobados_ci),
    url(r'^expedientes_aprobados/rs/(?P<rs>[\w]+)$',buscar_expedientes_aprobados_rs),
    url(r'^expedientes_aprobados/(?P<id_expediente>[\w]+)$',detalle_expediente_aprobado),


    url(r'^movimientos_internos$',movimientos_internos,name='movimientos_internos'),
    url(r'^movimientos_internos/(?P<id_expediente>[\w]+)/eliminar/$',eliminar_movimiento_interno),
    url(r'^movimientos_internos/(?P<id_expediente>[\w]+)/modificar/$',modificar_movimiento_interno),
    url(r'^movimientos_internos/registrar/$',registrar_movimiento_interno),
    url(r'^movimientos_internos/ci/(?P<ci>[\w]+)$',buscar_movimientos_internos_ci),

    url(r'^reportes$',reportes,name='reportes'),
    url(r'^reportes/reporte_exp_org_carrera$',reporte_exp_organismo_carrera),
    url(r'^reportes/reporte_exp_organismos$',reporte_exp_organismo),
    url(r'^reportes/reporte_exp_org_provincia$',reporte_exp_org_provincia),

    url(r'^reportes/reporte_noexp_org_carrera$',reporte_noexp_organismo_carrera),
    url(r'^reportes/reporte_noexp_organismos$',reporte_noexp_organismo),
    url(r'^reportes/reporte_mov_int_organismos$',reporte_mov_int_organismos),
    url(r'^direcciones_trabajo$',gestion_dir_trabajo,name='dir_trabajo'),
    url(r'^direcciones_trabajo/(?P<id_dir>[\w]+)/modificar$',modificar_dir_trabajo),
    url(r'^ubicados$',m_ubicados, {'filtro':''},name="ubicados"),
    url(r'^ubicados/desfasados$',m_ubicados, {'filtro':'desfasados'},name="ubicados"),
    url(r'^ubicados/graduados$',m_ubicados, {'filtro':'graduados'},name="ubicados"),
    url(r'^ubicados/registrar$',registrar_ubicacion),
    url(r'^ubicados/no_presentacion',no_presentacion),
    url(r'^ubicados/(?P<id_ubicacion>[\d]+)/presentacion$',presentacion),
    url(r'^ubicados/todos$',m_ubicados,{'filtro':'todos'}),
    url(r'^ubicados/ci/(?P<ci>[\d]+)$',buscar_ci_ubicado),
    url(r'^ubicados/(?P<id_ubicacion>[\d]+)/modificar$',modificar_ubicacion),
    url(r'^ubicados/(?P<id_ubicacion>[\d]+)/pasar_a_disponibles',pasar_a_disponibles),
    url(r'^ubicados/(?P<id_ubicacion>[\d]+)/eliminar$',eliminar_ubicacion),
    url(r'^ubicados/propios/(?P<opcion>(organismo|carrera|provincia_residencia|provincia_ubicacion|centro_estudio){1})/(?P<id_opcion>[\w]+)$',filtrar_ubicados),


     url(r'^inhabilitaciones$',inhabilitaciones,name="inhabilitaciones"),
     url(r'^inhabilitaciones/registrar$',registrar_inhabilitacion),
     url(r'^inhabilitaciones/autocompletar_inhabilitado$',autocompletar_inhabilitado),
     url(r'^inhabilitaciones/ci/(?P<ci>[\d]+)$',buscar_ci_inhabilitado),
     url(r'^inhabilitaciones/no/(?P<no>[\d]+)$',buscar_no_inhabilitado),
     url(r'^inhabilitaciones/(?P<id_proceso>[\d]+)$',detalle_proceso),
     url(r'^inhabilitaciones/(?P<id_proceso>[\d]+)/editar$',modificar_proceso),
     url(r'^inhabilitaciones/(?P<id_proceso>[\d]+)/eliminar$',eliminar_proceso),
     url(r'^exportar_total_procesos$',exportar_total_procesos),
     url(r'^exportar_total_procesos_causales$',exportar_total_procesos_causales),
     url(r'^exportar_total_procesos_organismos$',exportar_total_procesos_organismos),
     url(r'^exportar_total_procesos_niveles$',exportar_total_procesos_niveles),
     url(r'^exportar_procesos_registro_nominal$',exportar_procesos_registro_nominal),



     url(r'^disponibles/registrar$',registrar_disponibilidad),
     url(r'^disponibles$',m_disponibles,name="disponibles"),
     url(r'^disponibles/(?P<id_disponibilidad>[\d]+)/ubicar$',ubicar_disponibilidad),
     url(r'^disponibles/(?P<id_disponibilidad>[\d]+)/eliminar',eliminar_disponibilidad),
     url(r'^disponibles/(?P<id_disponibilidad>[\d]+)$',detalle_disponibilidad),
     url(r'^disponibles/ci/(?P<ci>[\d]+)$',buscar_ci_disponible),
     url(r'^disponibles/importar$',importar_disponibilidad),
     url(r'^disponibles/buscar_disponibles_carrera$',buscar_disponibles,{'opcion':'carrera'}),
     url(r'^disponibles/buscar_disponibles_municipio_residencia$',buscar_disponibles,{'opcion':'municipio_residencia'}),
     url(r'^disponibles/buscar_disponibles_centro_estudio$',buscar_disponibles,{'opcion':'centro_estudio'}),
     url(r'^disponibles/(?P<opcion>(carrera|organismo|municipio_residencia|centro_estudio){1})/(?P<id_opcion>[\d]+)$',filtrar_disponibles),


    url(r'^ubicados/buscar_ubicados_organismo$',buscar_ubicados,{'opcion':'organismo'}),
    url(r'^ubicados/buscar_ubicados_provincia_carrera$',buscar_ubicados,{'opcion':'carrera'}),
    url(r'^ubicados/buscar_ubicados_provincia_residencia$',buscar_ubicados,{'opcion':'provincia_residencia'}),
    url(r'^ubicados/buscar_ubicados_provincia_ubicacion$',buscar_ubicados,{'opcion':'provincia_ubicacion'}),
    url(r'^ubicados/buscar_ubicados_centro_estudio$',buscar_ubicados,{'opcion':'centro_estudio'}),

    url(r'^exportar_ubicados_provincia_residencia$',exportar_ubicados_provincia,{'opcion':'residencia'}),
    url(r'^exportar_ubicados_provincia_ubicacion$',exportar_ubicados_provincia,{'opcion':'ubicacion'}),
    url(r'^exportar_ubicados_organismo$',exportar_ubicados_organismo),
    url(r'^exportar_total_ubicados_organismos$',exportar_total_ubicados_organismos),
    url(r'^exportar_total_ubicados_provincias_ubicacion$',exportar_total_ubicados_provincias,{'opcion':'ubicacion'}),
    url(r'^exportar_total_ubicados_provincias_residencia$',exportar_total_ubicados_provincias,{'opcion':'residencia'}),
    url(r'^exportar_ubicados$',exportar_ubicados),
    url(r'^exportar_ubicados_universidades$',exportar_ubicados_universidades),
    url(r'^ubicados/(?P<id_ubicacion>[\d]+)$',detalle_ubicacion),

    url(r'^graduado/ci/(?P<ci>[\d]+)$',ficha_graduado,name='ficha_graduado'),
    url(r'^movimiento_laboral$',movimiento_laboral,name='movimiento_laboral'),
    url(r'^ubicacion_laboral$',ubicacion_laboral,name='ubicacion_laboral'),
    url(r'^nomencladores$',nomencladores,name='nomencladores'),


]
