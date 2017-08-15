# -*- coding: utf-8 -*-
__author__ = 'Rolando.Morales'

from django import forms
from .models import *



class EnviarCorreoForm(forms.Form):

    para = forms.CharField(
        label="Para",
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Escriba el remitente del correo'
            }))


    asunto = forms.CharField(
        label="Asunto",
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Escriba el asunto del correo'
            }))

    texto = forms.CharField(
        label="Texto",
        required=True,
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
                'placeholder': 'Escriba el texto del correo',
                'rows':5
            }))





class RegistroUserForm(forms.Form):

    username = forms.CharField(
        label="Usuario",
        required=True,
        min_length=5,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Escriba su nombre de usuario'

            }))

    first_name = forms.CharField(
         label="Nombre",
            required=False,
         widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Escriba su nombre (opcional)'
            }))


    last_name = forms.CharField(
        label="Apellidos",
           required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Escriba sus apellidos (opcional)'
            }))


    email = forms.EmailField(
        label="Correo",
        required=False,
        widget=forms.EmailInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Escriba su correo electrónico'
            }))

    password = forms.CharField(
        label="Contraseña",
        required=True,
        min_length=5,
        widget=forms.PasswordInput(
            attrs={'class': 'form-control',
                   'placeholder': 'Escriba su contraseña'

                   }
        ))

    password2 = forms.CharField(
        label="Confirmar Contraseña",
        min_length=5,
        required=True,
        widget=forms.PasswordInput(
            attrs={ 'class': 'form-control',
                    'placeholder': 'Confirme su contraseña'
                   }))

    telefono = forms.CharField(
        label="Teléfono",
        required=False,
        widget=forms.TextInput(
            attrs={ 'class': 'form-control',
                    'placeholder': 'Escriba el teléfono (opcional)'
                   }))

    organismo = forms.ModelChoiceField(
        queryset=Organismo.objects.all().order_by("nombre"),
        required=True,
        widget=forms.Select(
            attrs={ 'class': 'form-control'

                   }))


    categoria = forms.ModelChoiceField(
        queryset=Categoria_usuario.objects.all().order_by("nombre"),
        required=True,
        widget=forms.Select(
            attrs={ 'class': 'form-control'
                   }))


    provincia = forms.ModelChoiceField(
        queryset=Provincia.objects.all().order_by("nombre"),
        required=True,
        widget=forms.Select(
            attrs={ 'class': 'form-control',
                    'style':'visibility:hidden',
                   }))

    foto = forms.ImageField(required=False)


    def clean_username(self):
        """Comprueba que no exista un username igual en la db"""
        username = self.cleaned_data['username']
        if User.objects.filter(username=username):
            raise forms.ValidationError('Nombre de usuario ya registrado.')
        return username



    def clean_password2(self):
        """Comprueba que password y password2 sean iguales."""
        password = self.cleaned_data['password']
        password2 = self.cleaned_data['password2']
        if password != password2:
            raise forms.ValidationError('Las contraseñas no coinciden.')
        return password2

#Modificar datos del usuario-----------------------------------------------------------------------------

class ModificarUserPerfilForm(forms.ModelForm):

      telefono = forms.CharField(
        label="Télefono",
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Escriba su télefono (opcional)'
            }))

      class Meta:
        model=Perfil_usuario
        fields=["organismo","telefono","foto","categoria","provincia"]
        widgets = {
            "organismo": forms.Select(attrs={"class" : "form-control"}),
            "categoria": forms.Select(attrs={"class" : "form-control"}),
            "provincia": forms.Select(attrs={"class" : "form-control"})
        }


class ModificarUserForm(forms.ModelForm):

    class Meta:
        model=User
        fields=["username","email","first_name","last_name"]

    username = forms.CharField(
        label="Usuario",
        required=True,
        min_length=5,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Escriba su nombre de usuario'

            }))

    first_name = forms.CharField(
         label="Nombre",
            required=False,
         widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Escriba su nombre'
            }))


    last_name = forms.CharField(
        label="Apellidos",
           required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Escriba sus apellidos'
            }))


    email = forms.EmailField(
        label="Correo",
        required=False,
        widget=forms.EmailInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Escriba su correo electrónico'
            }))


    def clean_username(self):
        """Comprueba que no exista un username igual en la db"""
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exclude(username=username):
            raise forms.ValidationError('Nombre de usuario ya registrado.')
        return username


# Usuario Actual------------------------------------------------------------------------------------------------

class ModificarUserPerfilFormActual(forms.ModelForm):

      telefono = forms.CharField(
        label="Télefono",
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Escriba su télefono (opcional)'
            }))

      class Meta:
        model=Perfil_usuario
        fields=["telefono","foto"]


class ModificarUserFormActual(forms.ModelForm):

    class Meta:
        model=User
        fields=["email","first_name","last_name"]


    first_name = forms.CharField(
         label="Nombre",
            required=False,
         widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Escriba su nombre'
            }))


    last_name = forms.CharField(
        label="Apellidos",
           required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Escriba sus apellidos'
            }))


    email = forms.EmailField(
        label="Correo",
        required=False,
        widget=forms.EmailInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Escriba su correo electrónico'
            }))

#----Mario David------------------------------------------------------------------------

class RegistrarCarreraForm(forms.ModelForm):
    
        class Meta:
           model=Carrera
           fields=["codigo_mes","nombre","tipo"]
           widgets={
               'tipo':forms.Select(
                     attrs={
                'class': 'form-control'
               
            })
           }


        codigo_mes = forms.CharField(
        label="Código Mes",
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Escriba el código de la carrera'
            }))

        nombre = forms.CharField(
        label="Nombre",
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Escriba el nombre de la carrera'
            }))
    
class RegistrarCentroEstudioForm(forms.ModelForm):
    
        class Meta:
           model=Centro_estudio
           fields=["codigo_mes","nombre","siglas","provincia"]
           widgets={
               'provincia':forms.Select(
                     attrs={
                'class': 'form-control'
               
            })
           }


        codigo_mes = forms.CharField(
        label="Código Mes",
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Escriba el código del centro de estudios'
            }))

        nombre = forms.CharField(
        label="Nombre",
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Escriba el nombre del centro de estudios'
            }))
        
        siglas = forms.CharField(
        label="Siglas",
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Escriba el nombre de la carrera'
            }))

#---------------------------------------------------------------------------------------

#-----------------------------------------------------------------------------
class ModificarContrasennaUserForm(forms.Form):
    password = forms.CharField(
        label="Contraseña",
        required=True,
        min_length=5,
        widget=forms.PasswordInput(
            attrs={'class': 'form-control',
                   'placeholder': 'Escriba su nueva contraseña'

                   }
        ))

    password2 = forms.CharField(
        label="Confirmar Contraseña",
        min_length=5,
        required=True,
        widget=forms.PasswordInput(
            attrs={ 'class': 'form-control',
                    'placeholder': 'Confirme su nueva contraseña'
                   }))

    def clean_password2(self):
        """Comprueba que password y password2 sean iguales."""
        password = self.cleaned_data['password']
        password2 = self.cleaned_data['password2']
        if password != password2:
            raise forms.ValidationError('Las contraseñas no coinciden.')
        return password2
#----------------------------------------------------------------------------------------------------
from django.core.validators import RegexValidator
class RegistroExpedienteForm(forms.Form):

      nombre_graduado = forms.CharField(
        label="Nombre del graduado",
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Escriba el nombre y apellidos del graduado '
            }))


      centro_estudio = forms.ModelChoiceField(
        label="Centro de estudio",
        queryset=Centro_estudio.objects.all(),
        required=True,
        widget=forms.Select(
            attrs={
                'class': 'form-control',

            }))

      carrera_graduado = forms.ModelChoiceField(
        label="Carrera del graduado",
        queryset=Carrera.objects.filter(tipo='ns'),
        required=True,

        widget=forms.Select(
            attrs={
                'class': 'form-control',
                'placeholder': 'Seleccione la carrera del graduado'
            }))

      anno_graduacion = forms.CharField(
        label="Año de graduado",
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Escriba el año de graduación del graduado'
            }))

      causal_movimiento = forms.ModelChoiceField(
        queryset=Causal_movimiento.objects.filter(activo=True,tipo='ml'),
        label="Causa del movimiento",
        required=True,
        widget=forms.Select(
            attrs={
                'class': 'form-control'

            }))

      sintesis_causal_movimiento = forms.CharField(
        label="Síntesis de la causa del movimiento",
        required=False,
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
                'placeholder': 'Escriba una síntesis de la causa del movimiento',
                'rows':2
            }))

      codigo_boleta = forms.CharField(
        label="Código de la boleta",
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Escriba el código de la boleta'
            }))

      imagen_boleta=forms.ImageField(label="Imagen de la boleta",required=False)

      ci= forms.CharField(
      validators= [RegexValidator(
                regex='^[0-9]{2}(0[1-9]|1[0-2])(31|30|(0[1-9]|[1-2][0-9]))[0-9]{5}$',
                message='Carnet de identidad incorrecto',
            )],
        label="Carnet de identidad del graduado",
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Escriba el carnet de identidad del graduado '
            }))




      detalle_direccion_residencia = forms.CharField(
        label="Dirección de residencia",
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Escriba la dirección de residencia del graduado'
            }))



      municipio_residencia = forms.ModelChoiceField(
        label="Municipio de residencia",
        queryset=Municipio.objects.all(),
        required=False,
        widget=forms.Select(
            attrs={
                'class': 'form-control',
            }))


      organismo_liberacion = forms.ModelChoiceField(
        label="Organismo que libera",
        queryset=Organismo.objects.all(),
        required=True,
        widget=forms.Select(
            attrs={
                'class': 'form-control'

            }))


      entidad_liberacion = forms.CharField(
        label="Entidad que lo libera",
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Escriba el nombre de la entidad que lo libera',
            }))



      municipio_entidad_liberacion = forms.ModelChoiceField(
        label="Mun. Entidad que libera",
        queryset=Municipio.objects.all(),
        required=True,
        widget=forms.Select(
            attrs={
                'class': 'form-control',
            }))

      facultado_liberacion = forms.CharField(
        label="Facultado de liberación",
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Escriba nombre y apellidos del facultado que lo libera',
            }))


      organismo_aceptacion = forms.ModelChoiceField(
        label="Organismo que acepta",
        queryset=Organismo.objects.all(),
        required=True,
        widget=forms.Select(
            attrs={
                'class': 'form-control'

            }))


      entidad_aceptacion = forms.CharField(
        label="Entidad que lo acepta",
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                 'placeholder': 'Escriba el nombre de la entidad que lo acepta',
            }))



      municipio_entidad_aceptacion = forms.ModelChoiceField(
        label="Mun. Entidad que acepta",
        queryset=Municipio.objects.all(),
        required=True,
        widget=forms.Select(
            attrs={
                'class': 'form-control'
            }))

      facultado_aceptacion = forms.CharField(
        label="Facultado de aceptación",
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Escriba nombre y apellidos del facultado que lo acepta',
            }))

      comprimido = forms.FileField(
        label="Comprimido (Documentos)",
        required=False
       )





#Registrar Movimiento interno


class RegistroMovimientoInternoForm(forms.Form):

      nombre_graduado = forms.CharField(
        label="Nombre del graduado",
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Escriba el nombre y apellidos del graduado '
            }))


      centro_estudio = forms.ModelChoiceField(
        label="Centro de estudio",
        queryset=Centro_estudio.objects.all(),
        required=True,
        widget=forms.Select(
            attrs={
                'class': 'form-control',

            }))

      carrera_graduado = forms.ModelChoiceField(
        label="Carrera del graduado",
        queryset=Carrera.objects.filter(tipo='ns'),
        required=True,

        widget=forms.Select(
            attrs={
                'class': 'form-control',
                'placeholder': 'Seleccione la carrera del graduado'
            }))

      anno_graduacion = forms.CharField(
        label="Año de graduado",
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Escriba el año de graduación del graduado'
            }))

      causal_movimiento = forms.ModelChoiceField(
        queryset=Causal_movimiento.objects.filter(activo=True,tipo='ml'),
        label="Causa del movimiento",
        required=True,
        widget=forms.Select(
            attrs={
                'class': 'form-control'

            }))

      sintesis_causal_movimiento = forms.CharField(
        label="Síntesis de la causa del movimiento",
        required=False,
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
                'placeholder': 'Escriba una síntesis de la causa del movimiento',
                'rows':2


            }))

      codigo_boleta = forms.CharField(
        label="Código de la boleta",
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Escriba el código de la boleta'
            }))

      imagen_boleta=forms.ImageField(label="Imagen de la boleta",required=False)

      ci= forms.CharField(
        label="Carnet de identidad del graduado",
        required=False,
        validators=[RegexValidator(regex='^[0-9]{2}(0[1-9]|1[0-2])(31|30|(0[1-9]|[1-2][0-9]))[0-9]{5}$',message='CI incorrecto',)],
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Escriba el carnet de identidad del graduado '
            }))




      detalle_direccion_residencia = forms.CharField(
        label="Dirección de residencia",
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Escriba la dirección de residencia del graduado'
            }))



      municipio_residencia = forms.ModelChoiceField(
        label="Municipio de residencia",
        queryset=Municipio.objects.all(),
        required=False,
        widget=forms.Select(
            attrs={
                'class': 'form-control',
            }))




      entidad_liberacion = forms.CharField(
        label="Entidad que lo libera",
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Escriba el nombre de la entidad que lo libera',
            }))



      municipio_entidad_liberacion = forms.ModelChoiceField(
        label="Mun. Entidad que libera",
        queryset=Municipio.objects.all(),
        required=True,
        widget=forms.Select(
            attrs={
                'class': 'form-control',
            }))



      entidad_aceptacion = forms.CharField(
        label="Entidad que lo acepta",
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                 'placeholder': 'Escriba el nombre de la entidad que lo acepta',
            }))



      municipio_entidad_aceptacion = forms.ModelChoiceField(
        label="Mun. Entidad que acepta",
        queryset=Municipio.objects.all(),
        required=True,
        widget=forms.Select(
            attrs={
                'class': 'form-control'
            }))



      aprobado = forms.CharField(
        label="Aprobado por",
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Escriba nombre y apellidos del facultado que lo aprueba',
            }))



#------------------------------------------------------------------------------

class RegistrarOrganismoForm(forms.ModelForm):

        class Meta:
           model=Organismo
           fields=["nombre","siglas","hijode"]



        nombre = forms.CharField(
        label="Nombre",
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Escriba el nombre del organismo'
            }))

        siglas = forms.CharField(
        label="Siglas",
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Escriba las siglas del organismo'
            }))


        hijode = forms.ModelChoiceField(
        label="Org. Superior",
        queryset=Organismo.objects.filter(activo=True).order_by("nombre"),
        required=False,
        widget=forms.Select(
            attrs={ 'class': 'form-control'}))


class RegistrarCausalForm(forms.ModelForm):

        class Meta:
           model=Causal_movimiento
           fields=["nombre","tipo"]
           widgets={
               'nombre':forms.TextInput(attrs={ 'class': 'form-control'}),
               'tipo':forms.Select(attrs={ 'class': 'form-control'})
           }





class ModificarDireccionTrabajo(forms.ModelForm):
        class Meta:
           model=Direccion_trabajo
           exclude=["activo"]


        director = forms.CharField(
        label="Director",
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Escriba el nombre del director'
            }))


        sexo_director = forms.ChoiceField(
        label="Sexo director",
        required=False,
        choices=(("F","Femenino"),("M","Masculino"),),
        widget=forms.Select(

            attrs={
                'class': 'form-control',
                'placeholder': 'Seleccione el sexo del director'
            }))


        correo_director = forms.CharField(
        label="Correo Director",
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Escriba el correo del director'
            }))

        especialista = forms.CharField(
        label="Especialista",
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Escriba el nombre del especialista'
            }))

        correo_especialista = forms.CharField(
        label="Correo Especialista",
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Escriba el correo del especialista'
            }))


        provincia = forms.ModelChoiceField(
        queryset=Provincia.objects.all().order_by("nombre"),
        required=True,
        widget=forms.Select(
            attrs={ 'class': 'form-control'}))



class Expedientes_segun_carrera_form(forms.Form):
        anno = forms.CharField(
        label="anno",
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Escriba el año',
                'type':'number'
            }))


        carrera = forms.ModelChoiceField(
        queryset=Carrera.objects.filter(activo=True,tipo='ns').order_by("nombre"),
        required=True,
        widget=forms.Select(
            attrs={ 'class': 'form-control'}))



class Expedientes_segun_causal_form(forms.Form):
        anno = forms.CharField(
        label="anno",
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Escriba el año',
                'type':'number'
            }))


        causal = forms.ModelChoiceField(
        queryset=Causal_movimiento.objects.filter(activo=True,tipo='ml').order_by("nombre"),
        required=True,
        widget=forms.Select(
            attrs={'class': 'form-control'}))


class UbicadoForm(forms.ModelForm):
    class Meta:
        model=UbicacionLaboral
        fields=["nombre_apellidos","boleta","centro_estudio","carrera","ci","cumple_servicio_social","organismo","entidad","municipio_residencia","provincia_ubicacion","sexo","direccion_particular","estado_ubicacion"]
        widgets = {
                "nombre_apellidos":forms.TextInput(attrs={"class" : "form-control"}),
                "boleta": forms.TextInput(attrs={"class" : "form-control codigo_boleta_fade"}),
                "centro_estudio": forms.Select(attrs={"class" : "form-control"}),
                "carrera": forms.Select(attrs={"class" : "form-control"}),
                "ci": forms.TextInput(attrs={"class" : "form-control"}),
                "cumple_servicio_social": forms.Select(attrs={"class" : "form-control"}),
                "organismo": forms.Select(attrs={"class" : "form-control"}),
                "entidad": forms.TextInput(attrs={"class" : "form-control"}),
                "municipio_residencia": forms.Select(attrs={"class" : "form-control"}),
                "provincia_ubicacion": forms.Select(attrs={"class" : "form-control"}),
                "direccion_particular": forms.TextInput(attrs={"class" : "form-control"}),
                "estado_ubicacion": forms.Select(attrs={"class" : "form-control", 'onchange':'Objeto.cambiar_estado_ubicacion()'}),
              }
    cumple_servicio_social= forms.ChoiceField(choices=((True,"Si"),(False,"No"),),widget=forms.Select(attrs={"class" : "form-control"}))
    sexo= forms.ChoiceField(choices=(("F","Femenino"),("M","Masculino"),),widget=forms.Select(attrs={"class" : "form-control"}))





class DisponibleForm(forms.ModelForm):
    class Meta:
        model=DisponibilidadGraduados
        fields=["nombre_apellidos","centro_estudio","carrera","ci","municipio_residencia","sexo","direccion_particular",'cumple_servicio_social']
        widgets = {
                "nombre_apellidos":forms.TextInput(attrs={"class" : "form-control"}),
                "centro_estudio": forms.Select(attrs={"class" : "form-control"}),
                "carrera": forms.Select(attrs={"class" : "form-control"}),
                "ci": forms.TextInput(attrs={"class" : "form-control"}),
                "municipio_residencia": forms.Select(attrs={"class" : "form-control"}),
                "direccion_particular": forms.TextInput(attrs={"class" : "form-control"}),
                    }

    sexo= forms.ChoiceField(choices=(("F","Femenino"),("M","Masculino"),),widget=forms.Select(attrs={"class" : "form-control"}))
    cumple_servicio_social= forms.ChoiceField(choices=((True,"Si"),(False,"No"),),widget=forms.Select(attrs={"class" : "form-control"}))


class ExportarUbicadosProvinciaForm(forms.Form):
        anno = forms.CharField(
            label="anno",
            required=True,
            widget=forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Escriba el año',
                    'type':'number'
                }))

        provincia = forms.ModelChoiceField(
        queryset=Provincia.objects.all(),
        required=True,
        widget=forms.Select(
            attrs={'class': 'form-control'}))

class ExportarUbicadosOrganismoForm(forms.Form):
        anno = forms.CharField(
            label="anno",
            required=True,
            widget=forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Escriba el año',
                    'type':'number'
                }))

        organismo = forms.ModelChoiceField(
        queryset=Organismo.objects.filter(activo=True),
        required=True,
        widget=forms.Select(
            attrs={'class': 'form-control'}))



















class FormBuscarUbicadosCI(forms.Form):
        ci=forms.CharField(label="ci",required=True,widget=forms.TextInput(
             attrs={ 'class': 'form-control', 'placeholder': 'Escriba el ci', 'type':'number'}))

class FormBuscarUbicadosBoleta(forms.Form):
        boleta=forms.CharField(label="código boleta",required=True,
             widget=forms.TextInput(attrs={ 'class': 'form-control', 'placeholder': 'Escriba el código de la boleta'}))

class FormBuscarUbicadosOrganismo(forms.Form):
      organismo=forms.ModelChoiceField(queryset=Organismo.objects.filter(activo=True),required=True,
             widget=forms.Select( attrs={'class': 'form-control'}))

class FormBuscarUbicadosCarrera(forms.Form):
       carrera=forms.ModelChoiceField(queryset=Carrera.objects.filter(activo=True).order_by("nombre"), required=True,
              widget=forms.Select(attrs={'class': 'form-control'}))

class FormBuscarUbicadosMunicipioResidencia(forms.Form):
       municipio_residencia=forms.ModelChoiceField(queryset=Municipio.objects.all(), required=True,
              widget=forms.Select(attrs={ 'class': 'form-control'}))

class FormBuscarUbicadosProvinciaUbicacion(forms.Form):
       provincia_ubicacion=forms.ModelChoiceField(queryset=Provincia.objects.all(), required=True,
              widget=forms.Select(attrs={ 'class': 'form-control'}))

class FormBuscarUbicadosProvinciaResidencia(forms.Form):
       provincia_residencia=forms.ModelChoiceField(queryset=Provincia.objects.all(), required=True,
              widget=forms.Select(attrs={ 'class': 'form-control'}))

class FormBuscarUbicadosCentroEstudio(forms.Form):
       centro_estudio=forms.ModelChoiceField(queryset=Centro_estudio.objects.all(), required=True,
              widget=forms.Select(attrs={ 'class': 'form-control'}))

class FormFactory:
    @staticmethod
    def build(opcion):
        if opcion == "organismo":
           form=FormBuscarUbicadosOrganismo

        if opcion == "boleta":
           form=FormBuscarUbicadosBoleta

        elif opcion == "carrera":
           form=FormBuscarUbicadosCarrera

        elif opcion == "provincia_ubicacion":
           form=FormBuscarUbicadosProvinciaUbicacion

        elif opcion == "municipio_residencia":
           form=FormBuscarUbicadosMunicipioResidencia

        elif opcion == "provincia_residencia":
           form=FormBuscarUbicadosProvinciaResidencia

        elif opcion == "centro_estudio":
           form=FormBuscarUbicadosCentroEstudio

        return form



class ProcesoInhabilitacionForm(forms.ModelForm):
    numero_resolucion=forms.CharField(label="Número resolución",required=True,widget=forms.TextInput(
             attrs={ 'class': 'form-control', 'type':'number'}))

    causal = forms.ModelChoiceField(
        label="Causal",
        required=False,
        queryset=Causal_movimiento.objects.filter(activo=True,tipo='i'),
        widget=forms.Select(

            attrs={
                'class': 'form-control causal_inhabilitacion',
            }))

    proceso = forms.ChoiceField(
        label="Proceso",
        required=True,
        choices=[
            ('i', 'Inhabilitación'),
            ('s', 'Suspensión de la Inhabilitación'),
        ],
    widget=forms.Select(

            attrs={
                'class': 'form-control',
                'onchange':'Objeto.cambiar_estado_inhabilitacion()'
            }))


    class Meta:
        model=GraduadoInhabilitacion
        fields=["nombre_apellidos","ci","carrera","nivel_educacional","provincia",'cumple_servicio_social','organismo']
        widgets = {
                "numero_resolucion":forms.TextInput(attrs={"class" : "form-control"}),
                "nombre_apellidos":forms.TextInput(attrs={"class" : "form-control"}),
                "ci": forms.TextInput(attrs={"class" : "form-control"}),
                "nivel_educacional": forms.Select(attrs={"class" : "form-control"}),
                "carrera": forms.Select(attrs={"class" : "form-control"}),
                "provincia": forms.Select(attrs={"class" : "form-control"}),
                "cumple_servicio_social": forms.Select(attrs={"class" : "form-control"}),
                "organismo": forms.Select(attrs={"class" : "form-control"})
                    }




