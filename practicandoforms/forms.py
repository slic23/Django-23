from  django import    forms 

class tiposForms(forms.Form):
    texto_simple = forms.CharField(
          label= "texto simple  (charfield)",
          help_text= "esto es un texto simple"
     )

    text_area = forms.CharField(
          label = "texto largo  (textarea)",
          widget= forms.Textarea(attrs={"rows": 3, "placeholder":"escribe  aqui"})

     )

    pasword = forms.CharField(
          
          label = "contraseña",
          widget= forms.PasswordInput

     )

    email = forms.EmailField(label="Correo ELECTRONICO")
    URL = forms.URLField(label="sitio web ",required=False)

    #### seccion numeros 

    entero = forms.IntegerField(
        label="Numero entero",
        min_value=0,
        max_value=100
    )

    decimal = forms.DecimalField(
        label = "moneda",

        max_digits= 5, 
        decimal_places=2
    )

    # fechas 

    fecha = forms.DateField(
        widget=forms.DateInput(attrs={"type": "date"})
    )


    fecha_hora = forms.DateTimeField(
        widget= forms.DateTimeInput(attrs= {"type":"datetime-local"})
    )


    ##### seleciones

    ejemplo_colores = [("rojo","Rojo"),
                       ("azul","Azul"),
                       ("verde","Verde")]
    
    selection_simple = forms.ChoiceField(label="lista desplegable",
                                         choices=ejemplo_colores)
    
    select_ratio = forms.ChoiceField(
        label = "botones de radio",
        choices=ejemplo_colores,
        widget=forms.RadioSelect
    )

    seleccion_multiple = forms.MultipleChoiceField(
        label = "seleccion multiple ",
        choices= ejemplo_colores
    )


    selection_m_choices = forms.MultipleChoiceField(
        label= "checkboxes multiple",
        choices = ejemplo_colores,
        widget=forms.CheckboxSelectMultiple
    )


    booleano = forms.BooleanField(
        label= "aceptas los acuerdos",
        required=False
    )


# modelsFORMS 

