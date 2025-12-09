from  django import    forms 
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _ 
from .models import *
import datetime 
class RenewBookForm(forms.Form):
    renewel_date = forms.DateField(help_text = "introduce una fecha entre ahora y 4 semanas ")


    def clean_renewel_date(self):
        data = self.cleaned_data['renewel_date']

        if data < datetime.date.today():
            raise ValidationError(_("Fecha invalida -esta metiendo una fecha del pasado "))
        if data > datetime.date.today()  + datetime.timedelta(weeks = 4):
            raise ValidationError(_("fecha invalida - esta pasando las 4 semanas propuestas "))

        return data 
"""
class Autor():
    nombre = forms.DateField(help_text = "introduce un nombre ")
    apellido = forms.DateField(help_text = "introduce un apellido ")
    fecha_namcimiento = forms.DateField(help_text = "Introduce la fecha de nacimiento ")
    fecha_de_muerte = forms.DateField(help_text = "introduce la fecha de la muerte", required =False)"""

"""
inscribirse al evento, este formulario sirve para pasar los datos y controlar el aforo, sobreescribiendo el metodo del formulario
se usa sessions porque estos datos son efimeros 
"""
class InscribirseEvento(forms.Form):
    nombre = forms.CharField( help_text = "Introduce tu nombre")
    apellido = forms.CharField(help_text = "Introduce tu apellido")

"""
Aqui esta el modelForm EVENTO que hereda de forms.ModelFor establezco 
una validacion para que la fecha del evento no sea en el pasado   

"""
class evento(forms.ModelForm):
    class Meta:
        model = Evento
        fields = "__all__"
        widgets = {

            "fecha_evento":forms.DateTimeInput( attrs=
                        {
                            "type": "datetime-local",

                        })
        }


    def clean_fecha_evento(self):
        dato = self.cleaned_data["fecha_evento"]
        
        from django.utils import timezone
        if dato < timezone.now():
             raise  ValidationError(_("La fecha no puede estar en el pasado"))

        return dato 




    """Aqui esta el registro form que hereda de forms.Form
    establezco validaciones para que el numero de socio sea de 9 digitos y
     que el nombre no sea igual a la contraseña y las contraseñas coincidan
     """

class  registroform(forms.Form):

    nombre = forms.CharField(help_text="introduce tu nombre")
    numero_socio = forms.CharField(
        max_length=9, 
        min_length=9,
        help_text="Introduce tu número de socio (9 dígitos)",
        widget=forms.TextInput(attrs={'type': 'number'}) 
    )
    apellidos = forms.CharField(help_text = "introduce tus apellidos")
    password = forms.CharField(widget = forms.PasswordInput)
    password2 = forms.CharField(widget = forms.PasswordInput)
    
    """
    validaciones 
    """
    def clean_numero_socio(self):
        dato = self.cleaned_data.get("numero_socio")
        if not dato.isdigit():
            raise ValidationError(_("El NUMERO NO SON LETRAS"))
        
        return dato 
        

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password2 = cleaned_data.get("password2")
        nombre = cleaned_data.get("nombre") # Usar .get() es más seguro

        if password != password2:
            raise ValidationError("Las contraseñas no coinciden")
        
        elif nombre == password:
            raise ValidationError("El nombre no debe ser igual a la contraseña")
        return cleaned_data
    


    
    
    
    