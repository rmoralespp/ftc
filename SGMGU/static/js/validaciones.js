/**
 * Created by Rolando.Morales on 12/05/2016.
 */


function revisar_notificacion(id_notificacion){
    $.ajax(
          {
              url: "/revisar_notificacion/"+id_notificacion+"",
              type: "get",
              success:function(data)
              {
                  $("#lista_notificaciones").find(".modal-body").attr("id",data.emisor_id);
                  $("#lista_notificaciones").find(".modal-footer").attr("id",data.id);
                  $("#lista_notificaciones").find(".modal-title").text("Notificación emitida por "+ data.emisor+" ("+data.categoria_emisor+")");
                  $("#lista_notificaciones").find(".modal-body").text(data.texto);
                  $('#lista_notificaciones').modal('show');
                  valor=parseInt($(".span_cant_notificaciones").text());
                  notificacion_li=$(".dropdown_notificaciones").find("#"+id_notificacion);
                  if(notificacion_li.hasClass("notificacion_sin_revisar") == true){
                      notificacion_li.removeClass("notificacion_sin_revisar");
                      if(valor > 1) {
                      valor-=1;
                      $(".span_cant_notificaciones").text(valor);
                  }
                  else if(valor == 1) {
                      $(".span_cant_notificaciones").remove();
                  }
                  }

              }
          });
}


function responder_notificacion() {
    $('#lista_notificaciones').modal('hide');
    emisor=$("#lista_notificaciones").find(".modal-body").attr("id");
    $("#select_usuarios_notificaciones option[value="+emisor+"]").prop("selected",true).trigger("change");
    $('#enviar_notificacion').find(".modal-title").text("Responder Notificación");
    $('#enviar_notificacion').modal('show');
}



function eliminar_notificacion() {
    id_notificacion=$("#lista_notificaciones").find(".modal-footer").attr("id");
    $('#lista_notificaciones').modal('hide');
    $.ajax(
          {
              url: "/eliminar_notificacion/"+id_notificacion+"",
              type: "get",
              success:function(data)
              {
                  $(".dropdown_notificaciones").find("#"+id_notificacion).remove();
              }
          });
}


/*Gestion de Usuarios---------------------------------------------------------------------------------------------------*/
/**Controlar los modals*/

function modificar_usuario(id){
        $("#modal_modificar_user").find("a").attr('href',"/usuarios/"+ id+"/modificar");
}

function eliminar_usuario(id){
        $("#modal_eliminar_user").find("a").attr('href',"/usuarios/"+ id+"/eliminar");
}

function cambiar_contrasenna(id){
        $("#modal_contrasenna_user").find("a").attr('href',"/usuarios/"+ id+"/cambiar_contrasenna");
}

/*Gestion de Organismos---------------------------------------------------------------------------------------------------*/
/**Controlar los modals*/

function modificar_organismo(id){
        $("#modal_modificar_org").find("a").attr('href',"/organismos/"+ id+"/modificar");
}

function eliminar_organismo(id){
        $("#modal_eliminar_org").find("a").attr('href',"/organismos/"+ id+"/eliminar");
}
//----gesion de ubicaciones---------------------------------------------------------------------------------------------

function confirmar_no_presentacion(id){
    $("#modal_confirmar_no_presentacion_ubicado").find("#id_graduado_no_presentacion").val(id);
}

function eliminar_ubicacion(id){
        $("#modal_eliminar_ubicacion").find("a").attr('href',"/ubicados/"+ id+"/eliminar");
}

function eliminar_disponibilidad(id){
        $("#modal_eliminar_disponibilidad").find("a").attr('href',"/disponibles/"+ id+"/eliminar");
}


function buscar_ci_disponible(){
    ci=$("#ci_disponible").val();
    if (isNaN(ci)==false){
         if(ci != ""){
           window.location.href = "/disponibles/ci/"+ci+"";
         }
    }

}


function buscar_ci_ubicado(){
    ci=$("#ci_ubicado").val();
    if (isNaN(ci)==false){
         if(ci != ""){
           window.location.href = "/ubicados/ci/"+ci+"";
         }
    }

}



function buscar_ficha_graduado(){
     ci=$("#ci_ficha_graduado").val();
    if (isNaN(ci)==false){
         if(ci != ""){
           window.location.href = "/graduado/ci/"+ci+"";
         }
    }
}

/*Gestion de Direcciones---------------------------------------------------------------------------------------------------*/
/**Controlar los modals*/

function modificar_direccion(id){
        $("#modal_modificar_dir").find("a").attr('href',"/direcciones_trabajo/"+ id+"/modificar");
}


/*Gestion de Causales---------------------------------------------------------------------------------------------------*/
/**Controlar los modals*/

function modificar_causal(id){
        $("#modal_modificar_causal").find("a").attr('href',"/causales/"+ id+"/modificar");
}

function eliminar_causal(id){
        $("#modal_eliminar_causal").find("a").attr('href',"/causales/"+ id+"/eliminar");
}
/*Gestion de Expedientes---------------------------------------------------------------------------------------------------*/
/**Controlar los modals*/

function click_btn_mod_exp(id){

    $("div[id='modal_modificar_exp']").find("a").attr('href',"/gestion_expedientes/"+id+"/modificar");
}


function click_btn_eli_exp(id){
        $("div[id='modal_eliminar_exp']").find("a").attr('href',"/gestion_expedientes/"+ id+"/eliminar");
}


/*Gestion de Movimientos Internos---------------------------------------------------------------------------------------------------*/
/**Controlar los modals*/
function click_btn_mod_exp_int(id){

    $("div[id='modal_modificar_exp_int']").find("a").attr('href',"/movimientos_internos/"+id+"/modificar");
}

function click_btn_eli_exp_int(id){
        $("div[id='modal_eliminar_exp_int']").find("a").attr('href',"/movimientos_internos/"+ id+"/eliminar");
}





function export_to_pdf(){
    $('#tabla_gestion').tableExport({
        type:'excel',
        tableName:'Totales de expedientes aprobados por Organismos',
        separator: ',',
        pdfFontSize:8,
        escape:'false',
        htmlContent:'false',
        consoleLog:'false'


    });
}


function rep_org_carr_keup(dato){
      nombre_organismo=$('#buscar_org').val();

    if (dato == "aprobado"){
        anno=$("#select_rep_org_carrera option:selected").text();
        url="/reportes/reporte_exp_org_carrera/";
    }
    else{
        anno=$("#noselect_rep_org_carrera option:selected").text();
        url="/reportes/reporte_noexp_org_carrera/";
    }

      if (nombre_organismo != ""){
          $.ajax(
          {
              url:url ,
              data:{
                  'anno':anno,
                  'nombre_organismo':nombre_organismo

              },
              type: "get",
              dataType:'html',
              success:function(data)
              {
                  $("body").html(data);
                  $('#buscar_org').val(nombre_organismo);
                  if (dato == "aprobado"){
                  $('#select_rep_org_carrera option').filter(function() {
                      return ($(this).text() == anno);
                       }).prop('selected', true);}
                  else{
                      $('#noselect_rep_org_carrera option').filter(function() {
                      return ($(this).text() == anno);
                       }).prop('selected', true);
                  }



              }
          });
      }
      else{
          cambio_anno_rep_org_carrera(dato);
      }
}





function cambio_anno_rep_org(dato){

      if (dato == "aprobado"){
          url="/reportes/reporte_exp_organismos/";
          anno=$("#select_rep_org option:selected").text();
      }
      else{

           url="/reportes/reporte_noexp_organismos/";
           anno=$("#noselect_rep_org option:selected").text();
      }

      $.ajax(
          {
              url: url,
              data:{
                  'anno':anno
              },
              type: "get",
              dataType:'html',
              success:function(data)
              {
                  $("body").html(data);
                   if (dato == "aprobado"){
                        $('#select_rep_org option').filter(function() {
                      return ($(this).text() == anno);
                       }).prop('selected', true);
                   }
                  else{
                       $('#noselect_rep_org option').filter(function() {
                      return ($(this).text() == anno);
                       }).prop('selected', true);
                   }


              }
          });
}


function cambio_anno_rep_org_carrera(dato){
       nombre_organismo=$('#buscar_org').val();

      if(dato == "aprobado"){
          url="/reportes/reporte_exp_org_carrera/";
          anno=$("#select_rep_org_carrera option:selected").text();

      }
      else{
          url="/reportes/reporte_noexp_org_carrera/";
          anno=$("#noselect_rep_org_carrera option:selected").text();

      }

      $.ajax(
          {
              url: url,
              data:{
                  'anno':anno,
                  'nombre_organismo':nombre_organismo
              },
              type: "get",
              dataType:'html',
              success:function(data)
              {
                  $("body").html(data);
                  $('#buscar_org').val(nombre_organismo);
                  if(dato == 'aprobado'){
                       $('#select_rep_org_carrera option').filter(function() {
                      return ($(this).text() == anno);
                       }).prop('selected', true);
                  }
                  else{
                       $('#noselect_rep_org_carrera option').filter(function() {
                      return ($(this).text() == anno);
                       }).prop('selected', true);
                  }


              }
          });
}


function cambio_anno_rep_org_provincia(dato){

      if (dato == 'aprobado'){
          url="/reportes/reporte_exp_org_provincia/";
          anno=$("#select_rep_org_provincia option:selected").text();
     }
     else{
          url="/reportes/reporte_noexp_org_provincia/";
          anno=$("#noselect_rep_org_provincia option:selected").text();
     }

      $.ajax(
          {
              url: url,
              data:{
                  'anno':anno
              },
              type: "get",
              dataType:'html',
              success:function(data)
              {
                  $("body").html(data);
                  if (dato == "aprobado"){
                      $('#select_rep_org_provincia option').filter(function() {
                      return ($(this).text() == anno);
                       }).prop('selected', true);
                  }
                  else{
                       $('#noselect_rep_org_provincia option').filter(function() {
                      return ($(this).text() == anno);
                       }).prop('selected', true);
                  }


              }
          });
}


function cambio_anno_rep_mov_int(){
      anno=$("#select_rep_mov_int option:selected").text();
      $.ajax(
          {
              url: "/reportes/reporte_mov_int_organismos/",
              data:{
                  'anno':anno
              },
              type: "get",
              dataType:'html',
              success:function(data)
              {
                  $("body").html(data);
                  $('#select_rep_mov_int option').filter(function() {
                      return ($(this).text() == anno);
                       }).prop('selected', true);

              }
          });
}

function totales_provincias(){

  var nColumnas = 19;

  var campos=[];

    for(var i=0; i<nColumnas-1;i++){
      campos[i]=0;
    }

    $("#tabla_gestion tbody tr").each(function (index) {

             $(this).children("td").each(function (index2)
            {
                 if (index2!=0){
                     campos[index2-1]+=parseInt($(this).text());
                     }
            });


    });

    $('#fila_totales').append('<td><strong>Total</strong></td>');
    for(var i=0;i<campos.length-2;i++){
        $('#fila_totales').append('<td><strong>'+campos[i]+'</strong></td>');
    }


}


function cambiar_estado_ubicacion(){
    if($('#id_estado_ubicacion option').filter(':selected').val() != "graduado"){
       $('.codigo_boleta_fade').prop({'disabled':true,'required':false}).val("");

    }
    else {
        $('.codigo_boleta_fade').prop({'disabled':false,'required':true})
    }



}





$(document).on('ready',function(){





    $("button[name='btn_aprobar_exp']").on('click',function(){
         $('#aceptar_exp_aprobado').attr('name',$(this).attr('id'));

    });

    $("button[name='btn_rechazar_exp']").on('click',function(){
         $('#aceptar_exp_rechazado').attr('name',$(this).attr('id'));

    });

    $("button[name='btn_no_aprobar_exp']").on('click',function(){
         $('#aceptar_exp_no_aprobado').attr('name',$(this).attr('id'));
    });

    $("button[name='btn_exportar_exp']").on('click',function(){
         $('#aceptar_exp_exportado').attr('name',$(this).attr('id'));

    });


    $('#modal_aprobar_exp').on('hidden.bs.modal', function(){
            $(this).removeData('bs.modal');
            $('#id_registro_entrada').val("");
            $('#id_registro_salida').val("");
            $('#id_fecha_aprobado').val("");
            $('#id_informe_expediente').val("");
            $('#aprobar_epxediente').bootstrapValidator('resetForm', true);
        });

    $('#modal_no_aprobar_exp').on('hidden.bs.modal', function(){
            $('#id_causa_rechazo').val("");

        });


    $('#modal_rechazar_exp').on('hidden.bs.modal', function(){
            $('#id_causa_no_aprobado').val("");
        });


    $("button[name='btn_pasar_pend_exp']").on('click',function(){
        $("div[id='modal_pasar_pend_exp']").find("a").attr('href',"/pasar_a_pendientes/"+ $(this).attr('id')+"");
    });

    $("button[name='btn_pasar_a_pend_exp_re']").on('click',function(){
        $("div[id='modal_pasar_pend_exp']").find("a").attr('href',"/pasar_a_pendientes_de_rechazo/"+ $(this).attr('id')+"");
    });

     $("button[name='btn_pasar_a_pend_exp_no']").on('click',function(){
        $("div[id='modal_pasar_pend_exp']").find("a").attr('href',"/pasar_a_pendientes_de_no_aprobado/"+ $(this).attr('id')+"");
    });


});