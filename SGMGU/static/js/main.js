Objeto = {

    __init__: function(id, modelo, ventana_id) {
        Objeto.id = id;
        Objeto.modelo = modelo;
        Objeto.ventana_id = ventana_id;
        Objeto.url_base = "/" + modelo + "/" + id;
        return this
    },

    no_presentar_ubicado: function() {
        $("#" + Objeto.ventana_id).find("#id_graduado_no_presentacion").val(Objeto.id);
    },

    eliminar: function() {
        $("#" + Objeto.ventana_id).find("a").attr('href', Objeto.url_base + "/eliminar");
    },

    modificar: function() {
        $("#" + Objeto.ventana_id).find("a").attr('href', Objeto.url_base + "/modificar");
    },

    buscar: function(termino_busqueda) {

        digitos_valor = $("#" + Objeto.ventana_id).val();
        Objeto.url_base = "/" + Objeto.modelo + "/" + termino_busqueda + "/" + digitos_valor + "";
        if (isNaN(digitos_valor) == false) {
            if (digitos_valor != "") {
                window.location.href = Objeto.url_base;
            }
        }
    },

    cambiar_contrasenna: function() {
        $("#" + Objeto.ventana_id).find("a").attr('href', Objeto.url_base + "/cambiar_contrasenna");
    },

    revisar_notificacion: function() {
        $.ajax({
            url: Objeto.url_base,
            type: "get",
            success: function(data) {
                $("#lista_notificaciones").find(".modal-body").attr("id", data.emisor_id);
                $("#lista_notificaciones").find(".modal-footer").attr("id", data.id);
                $("#lista_notificaciones").find(".modal-title").text("Notificación emitida por " + data.emisor + " (" + data.categoria_emisor + ")");
                $("#lista_notificaciones").find(".modal-body").text(data.texto);
                $('#lista_notificaciones').modal('show');
                valor = parseInt($(".span_cant_notificaciones").text());
                notificacion_li = $(".dropdown_notificaciones").find("#" + Objeto.id);
                if (notificacion_li.hasClass("notificacion_sin_revisar") == true) {
                    notificacion_li.removeClass("notificacion_sin_revisar");
                    if (valor > 1) {
                        valor -= 1;
                        $(".span_cant_notificaciones").text(valor);
                    } else if (valor == 1) {
                        $(".span_cant_notificaciones").remove();
                    }
                }

            }
        });
    },

    responder_notificacion: function() {
        $('#lista_notificaciones').modal('hide');
        emisor = $("#lista_notificaciones").find(".modal-body").attr("id");
        $("#select_usuarios_notificaciones option[value=" + emisor + "]").prop("selected", true).trigger("change");
        $('#enviar_notificacion').find(".modal-title").text("Responder Notificación");
        $('#enviar_notificacion').modal('show');
    },

    eliminar_notificacion: function() {
        id_notificacion = $("#lista_notificaciones").find(".modal-footer").attr("id");
        $('#lista_notificaciones').modal('hide');
        $.ajax({
            url: "/eliminar_notificacion/" + id_notificacion + "",
            type: "get",
            success: function(data) {
                $(".dropdown_notificaciones").find("#" + id_notificacion).remove();
            }
        });
    },

    cambiar_estado_ubicacion: function() {
        if ($('#id_estado_ubicacion option').filter(':selected').val() != "graduado") {
            $('.codigo_boleta_fade').prop({ 'disabled': true, 'required': false }).val("");
        } else {
            $('.codigo_boleta_fade').prop({ 'disabled': false, 'required': true })
        }
    },

    cambiar_estado_inhabilitacion: function() {
        if ($('#id_proceso option').filter(':selected').val() == "s") {
            $('.causal_inhabilitacion').prop({ 'disabled': true, 'required': false }).val("-1").trigger("change");
        } else {
            $('.causal_inhabilitacion').prop({ 'disabled': false, 'required': true })
        }
    }
};


$(document).on('ready', function() {


    $("button[name='btn_aprobar_exp']").on('click', function() {
        $('#aceptar_exp_aprobado').attr('name', $(this).attr('id'));

    });

    $("button[name='btn_rechazar_exp']").on('click', function() {
        $('#aceptar_exp_rechazado').attr('name', $(this).attr('id'));

    });

    $("button[name='btn_no_aprobar_exp']").on('click', function() {
        $('#aceptar_exp_no_aprobado').attr('name', $(this).attr('id'));
    });

    $("button[name='btn_exportar_exp']").on('click', function() {
        $('#aceptar_exp_exportado').attr('name', $(this).attr('id'));

    });


    $('#modal_aprobar_exp').on('hidden.bs.modal', function() {
        $(this).removeData('bs.modal');
        $('#id_registro_entrada').val("");
        $('#id_registro_salida').val("");
        $('#id_fecha_aprobado').val("");
        $('#id_informe_expediente').val("");
        $('#aprobar_epxediente').bootstrapValidator('resetForm', true);
    });

    $('#modal_no_aprobar_exp').on('hidden.bs.modal', function() {
        $('#id_causa_rechazo').val("");

    });


    $('#modal_rechazar_exp').on('hidden.bs.modal', function() {
        $('#id_causa_no_aprobado').val("");
    });


    $("button[name='btn_pasar_pend_exp']").on('click', function() {
        $("div[id='modal_pasar_pend_exp']").find("a").attr('href', "/pasar_a_pendientes/" + $(this).attr('id') + "");
    });

    $("button[name='btn_pasar_a_pend_exp_re']").on('click', function() {
        $("div[id='modal_pasar_pend_exp']").find("a").attr('href', "/pasar_a_pendientes_de_rechazo/" + $(this).attr('id') + "");
    });

    $("button[name='btn_pasar_a_pend_exp_no']").on('click', function() {
        $("div[id='modal_pasar_pend_exp']").find("a").attr('href', "/pasar_a_pendientes_de_no_aprobado/" + $(this).attr('id') + "");
    });


});