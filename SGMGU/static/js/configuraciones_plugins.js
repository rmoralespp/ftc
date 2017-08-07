$(document).on('ready',function(){


     $('input[type="radio"]').iCheck({
                checkboxClass: 'icheckbox_square-red',
                radioClass: 'iradio_square-red'
            })

    .on('ifChanged', function(e) {
                // Get the field name
                var field = $(this).attr('name');
                $('#exportar_expediente')
                    // Mark the field as not validated
                    .bootstrapValidator('updateStatus', field, 'NOT_VALIDATED')
                    // Validate field
                    .bootstrapValidator('validateField', field);
            });

    //Configuracion del select2
    $("select").select2();


    //Configuracion del datetimepicker
    $(function() {
            $('#id_fecha_aprobado, #id_fecha_inicio, #id_fecha_fin').datetimepicker({
                pick12HourFormat: false,
                autoclose: true,
                todayBtn: true,
                clearBtn:true,
                pickerPosition: "bottom-left"

            });

        });


    //Configuracion del dataTable
    $('#tabla_gestion').DataTable({
        "lengthMenu": [ [10, 25, 50, 100,-1], [10, 25, 50, 100,"Todos"] ],
        language: {
            "decimal":        "",
            "emptyTable":     "No hay datos disponibles en la tabla",
            "info":           "Mostrando _START_ de _END_ de _TOTAL_ registros",
            "infoEmpty":      "Mostrando 0 de 0 de 0 registros",
            "infoFiltered":   "(filtrado de _MAX_ registros)",
            "infoPostFix":    "",
            "thousands":      ",",
            "lengthMenu":     "Mostrando _MENU_  registros",
            "loadingRecords": "Cargando...",
            "processing":     "Procesando...",
            "search":         "Buscar:",
            "zeroRecords":    "No se encontraron registros coincidentes",
            "paginate": {
                "first":      "Primero",
                "last":       "Último",
                "next":       "Próximo",
                "previous":   "Anterior"
            },
            "aria": {
                "sortAscending":  ": activar para ordenar la columna ascendentemente",
                "sortDescending": ": activar para ordenar la columna descendentemente"
            }
        }
    });

    $('.gestion_exp').DataTable({
        "lengthMenu": [ [10, 25, 50, 100,-1], [10, 25, 50, 100,"Todos"] ],
        order: [[ 4, 'desc' ], [ 0, 'asc' ]],
        language: {
            "decimal":        "",
            "emptyTable":     "No hay datos disponibles en la tabla",
            "info":           "Mostrando _START_ de _END_ de _TOTAL_ registros",
            "infoEmpty":      "Mostrando 0 de 0 de 0 registros",
            "infoFiltered":   "(filtrado de _MAX_ registros)",
            "infoPostFix":    "",
            "thousands":      ",",
            "lengthMenu":     "Mostrando _MENU_  registros",
            "loadingRecords": "Cargando...",
            "processing":     "Procesando...",
            "search":         "Buscar:",
            "zeroRecords":    "No se encontraron registros coincidentes",
            "paginate": {
                "first":      "Primero",
                "last":       "Último",
                "next":       "Próximo",
                "previous":   "Anterior"
            },
            "aria": {
                "sortAscending":  ": activar para ordenar la columna ascendentemente",
                "sortDescending": ": activar para ordenar la columna descendentemente"
            }
        }
    });

    $('.tabla_exp').DataTable({
        "lengthMenu": [ [10, 25, 50, 100,-1], [10, 25, 50, 100,"Todos"] ],
        order: [[ 5, 'desc' ], [ 1, 'asc' ]],
        language: {
            "decimal":        "",
            "emptyTable":     "No hay datos disponibles en la tabla",
            "info":           "Mostrando _START_ de _END_ de _TOTAL_ registros",
            "infoEmpty":      "Mostrando 0 de 0 de 0 registros",
            "infoFiltered":   "(filtrado de _MAX_ registros)",
            "infoPostFix":    "",
            "thousands":      ",",
            "lengthMenu":     "Mostrando _MENU_  registros",
            "loadingRecords": "Cargando...",
            "processing":     "Procesando...",
            "search":         "Buscar:",
            "zeroRecords":    "No se encontraron registros coincidentes",
            "paginate": {
                "first":      "Primero",
                "last":       "Último",
                "next":       "Próximo",
                "previous":   "Anterior"
            },
            "aria": {
                "sortAscending":  ": activar para ordenar la columna ascendentemente",
                "sortDescending": ": activar para ordenar la columna descendentemente"
            }
        }
    });




    $('.usar_DataTable_2').DataTable({
        searching:false,
        paging: false,
        language: {
            "decimal":        "",
            "emptyTable":     "No hay datos disponibles en la tabla",
            "info":           "Mostrando _START_ de _END_ de _TOTAL_ registros",
            "infoEmpty":      "Mostrando 0 de 0 de 0 registros",
            "infoFiltered":   "(filtrado de _MAX_ registros)",
            "infoPostFix":    "",
            "thousands":      ",",
            "lengthMenu":     "Mostrando _MENU_  registros",
            "loadingRecords": "Cargando...",
            "processing":     "Procesando...",
            "search":         "Buscar:",
            "zeroRecords":    "No se encontraron registros coincidentes",
            "paginate": {
                "first":      "Primero",
                "last":       "Último",
                "next":       "Próximo",
                "previous":   "Anterior"
            },
            "aria": {
                "sortAscending":  ": activar para ordenar la columna ascendentemente",
                "sortDescending": ": activar para ordenar la columna descendentemente"
            }
        }
    });
    $('.usar_DataTable_3').DataTable({
        ordering:false,
        searching:false,
        paging: false,
        language: {
            "decimal":        "",
            "emptyTable":     "No hay datos disponibles en la tabla",
            "info":           "Mostrando _START_ de _END_ de _TOTAL_ registros",
            "infoEmpty":      "Mostrando 0 de 0 de 0 registros",
            "infoFiltered":   "(filtrado de _MAX_ registros)",
            "infoPostFix":    "",
            "thousands":      ",",
            "lengthMenu":     "Mostrando _MENU_  registros",
            "loadingRecords": "Cargando...",
            "processing":     "Procesando...",
            "search":         "Buscar:",
            "zeroRecords":    "No se encontraron registros coincidentes",
            "paginate": {
                "first":      "Primero",
                "last":       "Último",
                "next":       "Próximo",
                "previous":   "Anterior"
            },
            "aria": {
                "sortAscending":  ": activar para ordenar la columna ascendentemente",
                "sortDescending": ": activar para ordenar la columna descendentemente"
            }
        }
    });

});