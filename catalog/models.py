from django.db import models
import uuid 
# Es requerido para las instancias de bookInstanc
from django.urls import reverse
from django.contrib.auth.models import User
# Create your models here. 
class Book(models.Model):
    """
        Modelo que representa el libro de la biblioteca

    """
    title = models.CharField(max_length = 100)
    author = models.ForeignKey("Author",on_delete = models.RESTRICT,null = True)
    summary = models.TextField(max_length = 1300,help_text = "Introduce una descripcion del libro")
    genre = models.ManyToManyField("Genre",help_text = "Introduce un genero")
    isbn = models.CharField('ISBN',max_length=13  , help_text =  'Character <a href="https://www.isbn-international.org/content/what-isbn">ISBN number</a>')
    def __str__(self):
        """
        sobrescribir metodo str
        """
        return self.title
    def get_absolute_url(self):
                
        return  reverse("detalle-libro",args=[str(self.id)])



class Genre(models.Model):
    name = models.CharField(max_length = 100, unique = True, help_text = "Añade un genero")
    def __str__(self):
        return self.name
    
   
    def get_absolute_url(self):
                
        return  reverse("detalle-genero",args = [str(self.id)])

class BookInstance(models.Model):
   id = models.UUIDField(primary_key=True,default=uuid.uuid4,help_text = "ID unico para un ejemplar en toda la biblioteca") 
   book = models.ForeignKey(Book,on_delete = models.RESTRICT,null = True)
   imprint = models.CharField(max_length = 100)    
   due_back = models.DateField(null = True ,blank=True)
   LOAN_STATUS = (
           ("m","Maintenance"),
           ("o","On loan"),
           ("a","Available"),
           ("r","Reserved"),
           )
   language = models.ForeignKey("Language",on_delete = models.SET_NULL,null = True)
   status = models.CharField(max_length = 1, choices = LOAN_STATUS, blank = True, default = 'm' ,help_text = "Disponibilidad del ejemplar")
   class Meta:
       ordering = ["due_back"]
   def __str__(self):
       return f"{self.id} {self.book.title}"
class Author(models.Model):
    first_name = models.CharField(max_length = 200)
    last_name = models.CharField(max_length = 200)
    date_of_birth = models.DateField(null=True,blank = True) 
    date_of_death = models.DateField(null=True,blank=True)
    def get_absolute_url(self):
                
        return  reverse("detalle-author",args = [str(self.id)])
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
class Language(models.Model):
    lenguaje = models.CharField(max_length = 50)
    def __str__(self):
        return self.lenguaje

"""
ESTA ES LA TABLA QUE SE ENCARGA DE CREAR LOS EVENTOS
"""
class Evento(models.Model):
    nombre = models.CharField(max_length = 100 )
    detalle = models.TextField(max_length = 500)

    aforo_max = models.IntegerField(help_text = "Numero maximo que puede asistir al evento")
    fecha_evento = models.DateTimeField(null=True) 
    def __str__(self):
        return self.nombre
    @property
    def evento_caducado(self):
        if self.fecha_evento < datetime.datetime.now():
            return True
        return False
    @property
    def aforoMaximo(self):
       
        return self.personas.count() < self.aforo_max



    @property
    def eventoTiempoRestante(self):
        tiempo = self.fecha_evento - datetime.datetime.now()
        return f"Quedan {tiempo.days} dias"
class Persona(models.Model):
    nombre = models.CharField(max_length=100)
    socio_codigo = models.CharField(max_length=9, null=True, unique=True )
    apellido = models.CharField(max_length=100)
    eventos = models.ManyToManyField(Evento, related_name="personas", related_query_name="qpersonas", through="Asistencia")
    usuario = models.OneToOneField(User,on_delete=models.CASCADE ,null=True)
    
    def __str__(self):
        return self.nombre

"""
este es la tabla que se encarga de la asistencia de las personas a los eventos 


"""
class Asistencia(models.Model):
    persona = models.ForeignKey(Persona,on_delete=models.CASCADE)
    evento = models.ForeignKey(Evento, on_delete = models.CASCADE)
    fecha = models.DateField(null=True, blank=True)
    asistido = models.BooleanField(default=False)

    def __str__(self):
        return   f"{self.persona.nombre} asiste al {self.evento.nombre}"
    
    
    

    
    

    

    


