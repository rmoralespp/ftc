/**
 * Created by Rolando.Morales on 12/05/2016.
 */

$(document).on('ready',function(){



     $('#aprobar_expediente').bootstrapValidator({
             message: 'Este valor no es valido',
             excluded: [':disabled',':hidden', ':not(:visible)'],
             submitButton: '$input[id="aceptar_exp_aprobado"]',

         /*
             submitHandler: function(validator, form, submitButton) {
             $.ajax(
                     {
                         enctype: "multipart/form-data",
                         url: "/aprobar_expediente_pendiente/"+$('#aceptar_exp_aprobado').attr('name')+"",
                         data:{
                             'csrfmiddlewaretoken' : $("input[name='csrfmiddlewaretoken']").val(),
                             'registro_entrada':$('#id_registro_entrada').val(),
                             'registro_salida':$('#id_registro_salida').val(),
                             'informe_expediente': $('#id_informe_expediente').val(),
                             'fecha_aprobado': $('#id_fecha_aprobado').val(),
                             'notificar_dir':$('#id_notificar_dir').prop('checked')

                         },
                         type: "POST",
                         dataType:'json',
                         success:function(data)
                         {    

                              window.location.href = data['redirect'];
                         },
                         error: function(jqXHR, textStatus, errorThrown)
                         {
                             alert(errorThrown);
                         }
                     });
                 return false;
             },
             */

             feedbackIcons: {
                 valid: 'glyphicon glyphicon-ok',
                 invalid: 'glyphicon glyphicon-remove',
                 validating: 'glyphicon glyphicon-refresh'
             },
             fields: {
                 registro_entrada: {
                     validators: {
                         notEmpty: {
                             message: 'El registro de entrada es requerido'
                         }
                     }
                 },
                 registro_salida: {
                     validators: {
                         notEmpty: {
                             message: 'El registro de salida es requerido'
                         }
                     }
                 }


             }
     });


     $('#exportar_expediente').bootstrapValidator({
             message: 'Este valor no es valido',
             excluded: [':disabled',':hidden', ':not(:visible)'],
             submitButton: '$input[id="aceptar_exp_exportado"]',

             feedbackIcons: {
                 valid: 'glyphicon glyphicon-ok',
                 invalid: 'glyphicon glyphicon-remove',
                 validating: 'glyphicon glyphicon-refresh'
             },
             fields: {

                 registro_salida: {
                     validators: {
                         notEmpty: {
                             message: 'El registro de salida es requerido'
                         }
                     }
                 },


                 nombre_anno: {
                     validators: {
                         notEmpty: {
                             message: 'El nombre del año es requerido'
                         }
                     }
                 }
             }
     });


     $('#aprobar_expediente_rech').bootstrapValidator({
             message: 'Este valor no es valido',
             excluded: [':disabled',':hidden', ':not(:visible)'],
             submitButton: '$input[id="aceptar_exp_aprobado"]',

             feedbackIcons: {
                 valid: 'glyphicon glyphicon-ok',
                 invalid: 'glyphicon glyphicon-remove',
                 validating: 'glyphicon glyphicon-refresh'
             },
             fields: {
                 registro_entrada: {
                     validators: {
                         notEmpty: {
                             message: 'El registro de entrada es requerido'
                         }
                     }
                 },
                 registro_salida: {
                     validators: {
                         notEmpty: {
                             message: 'El registro de salida es requerido'
                         }
                     }
                 }
             }
     });


    $('#aprobar_expediente_no_aprob').bootstrapValidator({
             message: 'Este valor no es valido',
             excluded: [':disabled',':hidden', ':not(:visible)'],
             submitButton: '$input[id="aceptar_exp_aprobado"]',


             feedbackIcons: {
                 valid: 'glyphicon glyphicon-ok',
                 invalid: 'glyphicon glyphicon-remove',
                 validating: 'glyphicon glyphicon-refresh'
             },
             fields: {
                 registro_entrada: {
                     validators: {
                         notEmpty: {
                             message: 'El registro de entrada es requerido'
                         }
                     }
                 },
                 registro_salida: {
                     validators: {
                         notEmpty: {
                             message: 'El registro de salida es requerido'
                         }
                     }
                 }
             }
     });



     $('#rechazar_expediente').bootstrapValidator({
             message: 'Este valor no es valido',
             excluded: [':disabled',':hidden', ':not(:visible)'],
             submitButton: '$input[id="aceptar_exp_rechazado"]',
             submitHandler: function(validator, form, submitButton) {
             $.ajax(
                     {
                         url: "/rechazar_expediente_pendiente/"+$('#aceptar_exp_rechazado').attr('name')+"",
                         data:{
                             'csrfmiddlewaretoken' : $("input[name='csrfmiddlewaretoken']").val(),
                             'causa_rechazo':$('#id_causa_rechazo').val()

                         },
                         type: "POST",
                         dataType:'json',
                         success:function(data)
                         {

                              window.location.href = data['redirect'];
                         },
                         error: function(jqXHR, textStatus, errorThrown)
                         {
                             alert(errorThrown);
                         }
                     });
                 return false;
             },
             feedbackIcons: {
                 valid: 'glyphicon glyphicon-ok',
                 invalid: 'glyphicon glyphicon-remove',
                 validating: 'glyphicon glyphicon-refresh'
             },
             fields: {
                 causa_rechazo: {
                     validators: {
                         notEmpty: {
                             message: 'La causa es requerida'
                         }
                     }
                 }

             }
     });



     $('#rechazar_expediente_aprob').bootstrapValidator({
             message: 'Este valor no es valido',
             excluded: [':disabled',':hidden', ':not(:visible)'],
             submitButton: '$input[id="aceptar_exp_rechazado"]',
             submitHandler: function(validator, form, submitButton) {
             $.ajax(
                     {
                         url: "/rechazar_expediente_aprobado/"+$('#aceptar_exp_rechazado').attr('name')+"",
                         data:{
                             'csrfmiddlewaretoken' : $("input[name='csrfmiddlewaretoken']").val(),
                             'causa_rechazo':$('#id_causa_rechazo').val()

                         },
                         type: "POST",
                         dataType:'json',
                         success:function(data)
                         {

                              window.location.href = data['redirect'];
                         },
                         error: function(jqXHR, textStatus, errorThrown)
                         {
                             alert(errorThrown);
                         }
                     });
                 return false;
             },
             feedbackIcons: {
                 valid: 'glyphicon glyphicon-ok',
                 invalid: 'glyphicon glyphicon-remove',
                 validating: 'glyphicon glyphicon-refresh'
             },
             fields: {
                 causa_rechazo: {
                     validators: {
                         notEmpty: {
                             message: 'La causa es requerida'
                         }
                     }
                 }

             }
     });



    $('#rechazar_expediente_no_aprob').bootstrapValidator({
             message: 'Este valor no es valido',
             excluded: [':disabled',':hidden', ':not(:visible)'],
             submitButton: '$input[id="aceptar_exp_rechazado"]',
             submitHandler: function(validator, form, submitButton) {
             $.ajax(
                     {
                         url: "/rechazar_expediente_no_aprobado/"+$('#aceptar_exp_rechazado').attr('name')+"",
                         data:{
                             'csrfmiddlewaretoken' : $("input[name='csrfmiddlewaretoken']").val(),
                             'causa_rechazo':$('#id_causa_rechazo').val()

                         },
                         type: "POST",
                         dataType:'json',
                         success:function(data)
                         {

                              window.location.href = data['redirect'];
                         },
                         error: function(jqXHR, textStatus, errorThrown)
                         {
                             alert(errorThrown);
                         }
                     });
                 return false;
             },
             feedbackIcons: {
                 valid: 'glyphicon glyphicon-ok',
                 invalid: 'glyphicon glyphicon-remove',
                 validating: 'glyphicon glyphicon-refresh'
             },
             fields: {
                 causa_rechazo: {
                     validators: {
                         notEmpty: {
                             message: 'La causa es requerida'
                         }
                     }
                 }

             }
     });









     $('#no_aprobar_expediente').bootstrapValidator({
             message: 'Este valor no es valido',
             excluded: [':disabled',':hidden', ':not(:visible)'],
             submitButton: '$input[id="aceptar_exp_no_aprobado"]',
             submitHandler: function(validator, form, submitButton) {
             $.ajax(
                     {
                         url: "/no_aprobar_expediente_pendiente/"+$('#aceptar_exp_no_aprobado').attr('name')+"",
                         data:{
                             'csrfmiddlewaretoken' : $("input[name='csrfmiddlewaretoken']").val(),
                             'causa_no_aprobado':$('#id_causa_no_aprobado').val()

                         },
                         type: "POST",
                         dataType:'json',
                         success:function(data)
                         {

                              window.location.href = data['redirect'];
                         },
                         error: function(jqXHR, textStatus, errorThrown)
                         {
                             alert(errorThrown);
                         }
                     });
                 return false;
             },
             feedbackIcons: {
                 valid: 'glyphicon glyphicon-ok',
                 invalid: 'glyphicon glyphicon-remove',
                 validating: 'glyphicon glyphicon-refresh'
             },
             fields: {
                 causa_no_aprobado: {
                     validators: {
                         notEmpty: {
                             message: 'La causa es requerida'
                         }
                     }
                 }

             }
     });


    $('#no_aprobar_expediente_rech').bootstrapValidator({
             message: 'Este valor no es valido',
             excluded: [':disabled',':hidden', ':not(:visible)'],
             submitButton: '$input[id="aceptar_exp_no_aprobado"]',
             submitHandler: function(validator, form, submitButton) {
             $.ajax(
                     {
                         url: "/no_aprobar_expediente_rechazado/"+$('#aceptar_exp_no_aprobado').attr('name')+"",
                         data:{
                             'csrfmiddlewaretoken' : $("input[name='csrfmiddlewaretoken']").val(),
                             'causa_no_aprobado':$('#id_causa_no_aprobado').val()

                         },
                         type: "POST",
                         dataType:'json',
                         success:function(data)
                         {

                              window.location.href = data['redirect'];
                         },
                         error: function(jqXHR, textStatus, errorThrown)
                         {
                             alert(errorThrown);
                         }
                     });
                 return false;
             },
             feedbackIcons: {
                 valid: 'glyphicon glyphicon-ok',
                 invalid: 'glyphicon glyphicon-remove',
                 validating: 'glyphicon glyphicon-refresh'
             },
             fields: {
                 causa_no_aprobado: {
                     validators: {
                         notEmpty: {
                             message: 'La causa es requerida'
                         }
                     }
                 }

             }
     });


        $('#no_aprobar_expediente_aprob').bootstrapValidator({
             message: 'Este valor no es valido',
             excluded: [':disabled',':hidden', ':not(:visible)'],
             submitButton: '$input[id="aceptar_exp_no_aprobado"]',
             submitHandler: function(validator, form, submitButton) {
             $.ajax(
                     {
                         url: "/no_aprobar_expediente_aprobado/"+$('#aceptar_exp_no_aprobado').attr('name')+"",
                         data:{
                             'csrfmiddlewaretoken' : $("input[name='csrfmiddlewaretoken']").val(),
                             'causa_no_aprobado':$('#id_causa_no_aprobado').val()

                         },
                         type: "POST",
                         dataType:'json',
                         success:function(data)
                         {

                              window.location.href = data['redirect'];
                         },
                         error: function(jqXHR, textStatus, errorThrown)
                         {
                             alert(errorThrown);
                         }
                     });
                 return false;
             },
             feedbackIcons: {
                 valid: 'glyphicon glyphicon-ok',
                 invalid: 'glyphicon glyphicon-remove',
                 validating: 'glyphicon glyphicon-refresh'
             },
             fields: {
                 causa_no_aprobado: {
                     validators: {
                         notEmpty: {
                             message: 'La causa es requerida'
                         }
                     }
                 }

             }
     });


    // validacion del formulario Registrar causal
    $('#registrar_causal').bootstrapValidator({
    	 message: 'Este valor no es valido',
    	 feedbackIcons: {
    		 valid: 'glyphicon glyphicon-ok',
    		 invalid: 'glyphicon glyphicon-remove',
    		 validating: 'glyphicon glyphicon-refresh'
    	 },
    	 fields: {
    		 nombre: {
    			 validators: {
    				 notEmpty: {
    					 message: 'El nombre de la causal es requerida'
    				 }
    			 }
    		 }
    	 }
    });


     $('#registrar_direccion').bootstrapValidator({
    	 message: 'Este valor no es valido',
    	 feedbackIcons: {
    		 valid: 'glyphicon glyphicon-ok',
    		 invalid: 'glyphicon glyphicon-remove',
    		 validating: 'glyphicon glyphicon-refresh'
    	 },
    	 fields: {
    		 provincia: {
    			 validators: {
    				 notEmpty: {
    					 message: 'La provincia es requerida'
    				 }
    			 }
    		 }
    	 }
    });


    // validacion del formulario Registrar usuario
    $('#registrar_usuario').bootstrapValidator({
    	 message: 'Este valor no es valido',
    	 feedbackIcons: {
    		 valid: 'glyphicon glyphicon-ok',
    		 invalid: 'glyphicon glyphicon-remove',
    		 validating: 'glyphicon glyphicon-refresh'
    	 },
    	 fields: {

    		 username: {
    			 validators: {
    				 notEmpty: {
    					 message: 'El nombre de usuario es requerido'
    				 },
                     stringLength: {
					 min: 5,
					 message: 'El nombre de usuario debe contener al menos 5 carácteres'
                     }
    			 }
    		 },

    		 password: {
    			 validators: {
    				 notEmpty: {
    					 message: 'La contraseña es requerida'
    				 },

                     stringLength: {
					 min: 5,
					 message: 'La contraseña debe contener al menos 5 carácteres'
                     }




    			 }
    		 },

             password2: {
    			 validators: {
    				 notEmpty: {
    					 message: 'La confirmación de la contraseña es requerida'
    				 },
                      identical: {
                         field: 'password',
                         message:'La contraseña y la confirmacion de ella deben ser iguales'
                     },
                     stringLength: {
					 min: 5,
					 message: 'La contraseña debe contener al menos 5 carácteres'
                     }

    			 }
    		 },

             organismo: {
    			 validators: {
    				 notEmpty: {
    					 message: 'El organismo es requerido'
    				 }

    			 }
    		 },

             categoria: {
                 validators: {
                     notEmpty: {
                         message: 'La categoria es requerida'
                     }
                 }
             },
             provincia: {
    			 validators: {
    				 notEmpty: {
    					 message: 'La provincia es requerida'
    				 }

    			 }
    		 }
    	 }
    });

    // validacion del formulario Registrar organismo
    $('#registrar_organismo').bootstrapValidator({
    	 message: 'Este valor no es valido',
    	 feedbackIcons: {
    		 valid: 'glyphicon glyphicon-ok',
    		 invalid: 'glyphicon glyphicon-remove',
    		 validating: 'glyphicon glyphicon-refresh'
    	 },
    	 fields: {

    		 nombre: {
    			 validators: {
    				 notEmpty: {
    					 message: 'El nombre del organismo es requerido'
    				 }

    			 }
    		 },

             siglas: {
    			 validators: {
    				 notEmpty: {
    					 message: 'Las siglas del organismos son requeridas'
    				 }

    			 }
    		 }





    	 }
    });

    // validacion del formulario Registrar entidad
    $('#registrar_entidad').bootstrapValidator({
    	 message: 'Este valor no es valido',
    	 feedbackIcons: {
    		 valid: 'glyphicon glyphicon-ok',
    		 invalid: 'glyphicon glyphicon-remove',
    		 validating: 'glyphicon glyphicon-refresh'
    	 },
    	 fields: {
    		 nombre: {
    			 validators: {
    				 notEmpty: {
    					 message: 'El nombre de la entidad es requerida'
    				 }

    			 }
    		 },

             organismo: {
    			 validators: {
    				 notEmpty: {
    					 message: 'El organismo es requerido'
    				 }

    			 }
    		 },
             provincia: {
    			 validators: {
    				 notEmpty: {
    					 message: 'La provincia es requerida'
    				 }

    			 }
    		 }






    	 }
    });


    // validacion del formulario cambiar contrasenna
    $('#cambiar_contrasenna').bootstrapValidator({
    	 message: 'Este valor no es valido',
    	 feedbackIcons: {
    		 valid: 'glyphicon glyphicon-ok',
    		 invalid: 'glyphicon glyphicon-remove',
    		 validating: 'glyphicon glyphicon-refresh'
    	 },
    	 fields: {

    		 password: {
    			 validators: {
    				 notEmpty: {
    					 message: 'La contraseña es requerida'
    				 },

                     stringLength: {
					 min: 5,
					 message: 'La contraseña debe contener al menos 5 carácteres'
                     }




    			 }
    		 },

             password2: {
    			 validators: {
    				 notEmpty: {
    					 message: 'La confirmación de la contraseña es requerida'
    				 },
                      identical: {
                         field: 'password',
                         message:'La contraseña y la confirmacion de ella deben ser iguales'
                     },
                     stringLength: {
					 min: 5,
					 message: 'La contraseña debe contener al menos 5 carácteres'
                     }


    			 }

    		 }


    	 }
    });





    // validacion del formulario modificar usuario
    $('#modificar_usuario').bootstrapValidator({
    	 message: 'Este valor no es válido',
    	 feedbackIcons: {
    		 valid: 'glyphicon glyphicon-ok',
    		 invalid: 'glyphicon glyphicon-remove',
    		 validating: 'glyphicon glyphicon-refresh'
    	 },
    	 fields: {

    		 username: {
    			 validators: {
    				 notEmpty: {
    					 message: 'El nombre de usuario es requerido'
    				 },
                     stringLength: {
					 min: 5,
					 message: 'El nombre de usuario debe contener al menos 5 carácteres'
                     }
    			 }
    		 },
             categoria: {
                 validators: {
                     notEmpty: {
                         message: 'La categoria es requerida'
                     }
                 }
             },
             provincia: {
    			 validators: {
    				 notEmpty: {
    					 message: 'La provincia es requerida'
    				 }

    			 }
    		 }


    	 }
    });

    $('#registrar_movimiento_interno').bootstrapValidator({
    	 message: 'Este valor no es valido',
         submitButton: 'input[id="button_registrar_mov_int"]',
    	 feedbackIcons: {
    		 valid: 'glyphicon glyphicon-ok',
    		 invalid: 'glyphicon glyphicon-remove',
    		 validating: 'glyphicon glyphicon-refresh'
    	 },
    	 fields: {

    		 nombre_graduado: {
    			 validators: {
    				 notEmpty: {
    					 message: 'El nombre del graduado es requerido'
                     }
                 }
             },

    		 apellidos_graduado: {
    			 validators: {
    				 notEmpty: {
                         message: 'Los apellidos del graduado son requeridos'
                     }
                 }
             },

             carrera_graduado: {
    			 validators: {
    				 notEmpty: {
                         message: 'La carrera del graduado es requerida'
                     }
    			 }
    		 },

             centro_estudio: {
    			 validators: {
    				 notEmpty: {
                         message: 'El centro de estudio del graduado es requerido'
                     }
    			 }
    		 },

             causal_movimiento: {
    			 validators: {
    				 notEmpty: {
                         message: 'La causa del movimiento es requerida'
                     }
    			 }
    		 },

             anno_graduacion: {
    			 validators: {
    				 notEmpty: {
                         message: 'El año de graduado es requerido'
                     },
                     digits: {
                         message: 'El año de graduado debe ser un numero'
                     },

                     stringLength: {
                         max: 4,
                         min: 4,
                         message: 'El año de graduado debe contener 4 carácteres'
                     }

    			 }
    		 },

             municipio_entidad_liberacion: {
    			 validators: {
    				 notEmpty: {
                         message: 'El municipio de la entidad que lo libera es requerido'
                     }
    			 }
    		 },

             municipio_entidad_aceptacion: {
    			 validators: {
    				 notEmpty: {
                         message: 'El municipio de la entidad que lo acepta es requerido'
                     }
    			 }
    		 },

             entidad_liberacion: {
    			 validators: {
    				 notEmpty: {
                         message: 'La entidad que lo libera es requerida'
                     }
    			 }
    		 },

             entidad_aceptacion: {
    			 validators: {
    				 notEmpty: {
                          message: 'La entidad que lo acepta es requerida'
                     }
    			 }
    		 },

             codigo_boleta: {
    			 validators: {
    				 notEmpty: {
                          message: 'El código de la boleta es requerido'
                     }
    			 }
    		 },

             ci: {
    			 validators: {
    				 notEmpty: {
                          message: 'El carnet de identidad es requerido'
                     }
    			 }
    		 },


             municipio_residencia: {
    			 validators: {
    				 notEmpty: {
                          message: 'El municipio de residencia es requerido'
                     }
    			 }
    		 },

             aprobado: {
    			 validators: {
    				 notEmpty: {
                         message: 'La persona que aprueba el caso es requerida'
                     }
    			 }
    		 }

    	 }
    });

    $('#registrar_expediente').bootstrapValidator({
    	 message: 'Este valor no es valido',
    	 feedbackIcons: {
    		 valid: 'glyphicon glyphicon-ok',
    		 invalid: 'glyphicon glyphicon-remove',
    		 validating: 'glyphicon glyphicon-refresh'
    	 },
    	 fields: {

    		 nombre_graduado: {
    			 validators: {
    				 notEmpty: {
    					 message: 'El nombre y los apellidos del graduado son requeridos'
                     }
                 }
             },
/*
    		 apellidos_graduado: {
    			 validators: {
    				 notEmpty: {
                         message: 'Los apellidos del graduado son requeridos'
                     }
                 }
             },
*/
             carrera_graduado: {
    			 validators: {
    				 notEmpty: {
                         message: 'La carrera del graduado es requerida'
                     }
    			 }
    		 },


             centro_estudio: {
    			 validators: {
    				 notEmpty: {
                         message: 'El centro de estudio del graduado es requerido'
                     }
    			 }
    		 },

             causal_movimiento: {
    			 validators: {
    				 notEmpty: {
                         message: 'La causa del movimiento es requerida'
                     }
    			 }
    		 },

             anno_graduacion: {
    			 validators: {
    				 notEmpty: {
                         message: 'El año de graduado es requerido'
                     },
                     digits: {
                         message: 'El año de graduado debe ser un numero'
                     },

                     stringLength: {
                         max: 4,
                         min: 4,
                         message: 'El año de graduado debe contener 4 carácteres'
                     }
    			 }
    		 },

             municipio_entidad_liberacion: {
    			 validators: {
    				 notEmpty: {
                         message: 'El municipio de la entidad que lo libera es requerido'
                     }
    			 }
    		 },

             municipio_entidad_aceptacion: {
    			 validators: {
    				 notEmpty: {
                         message: 'El municipio de la entidad que lo acepta es requerido'
                     }
    			 }
    		 },

             entidad_liberacion: {
    			 validators: {
    				 notEmpty: {
                         message: 'La entidad que lo libera es requerida'
                     }
    			 }
    		 },

             entidad_aceptacion: {
    			 validators: {
    				 notEmpty: {
                          message: 'La entidad que lo acepta es requerida'
                     }
    			 }
    		 },

             organismo_liberacion: {
    			 validators: {
    				 notEmpty: {
                         message: 'El organismo que lo libera es requerido'
                     }
    			 }
    		 },

             organismo_aceptacion: {
    			 validators: {
    				 notEmpty: {
                          message: 'El organismo que lo acepta es requerido'
                     }
    			 }
    		 },

             codigo_boleta: {
    			 validators: {
    				 notEmpty: {
                          message: 'El código de la boleta es requerido'
                     }
    			 }
    		 },

             ci: {
    			 validators: {
    				 notEmpty: {
                          message: 'El carnet de identidad es requerido'
                     }
    			 }
    		 },



             municipio_residencia: {
    			 validators: {
    				 notEmpty: {
                          message: 'El municipio de residencia es requerido'
                     }
    			 }
    		 },

             facultado_liberacion: {
    			 validators: {
    				 notEmpty: {
                         message: 'El facultado que lo libera es requerido'
                     }
    			 }
    		 },

             facultado_aceptacion: {
    			 validators: {
    				 notEmpty: {
                          message: 'El facultado que lo acepta es requerido'
                     }
    			 }
    		 }



    	 }
    });






























    // validacion del formulario login
    $('#login').bootstrapValidator({
        message: 'Este valor no es valido',

        feedbackIcons: {
    		 valid: 'glyphicon glyphicon-ok',
    		 invalid: 'glyphicon glyphicon-remove',
    		 validating: 'glyphicon glyphicon-refresh'
    	 },
        fields:{
            username:{
                validators:{
                    notEmpty:{
                        message:'El nombre de usuario es requerido'
                    }
                }
            },
            password:{
                 validators:{
                    notEmpty:{
                        message:'La contraseña es requerida'
                    }
            }
        }

    }});












});



