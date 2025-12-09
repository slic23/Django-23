from django.shortcuts import render,redirect
from django.views import generic 
from django.http import HttpResponse
from .models import *
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect 
from django.urls  import reverse 
import  datetime 
from .forms import evento
from .forms import *
from django.contrib import messages
# Create your views here.

def index(request):
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()
    bookInstance_av = BookInstance.objects.filter(status__exact = "a").count()
    num_authors = Author.objects.all().count()
    num_genres = Genre.objects.all().count()

    numero_visitas = request.session.get("numeroVisitas",0)

    numero_visitas+= 1
    request.session["numeroVisitas"] = numero_visitas
    #buscarPalabra = ""
    context = {
            "num_books": num_books,
            "num_instances": num_instances,
            "bookInstance_av": bookInstance_av,
            "num_authors": num_authors,
            "numero_visitas": numero_visitas,


            "num_genres":num_genres,
            }


    return render (request,"index.html",context)
class ListaLibros(generic.ListView):
    model = Book

class ListarAutores(generic.ListView):
    model = Author
class DetalleLibro(generic.DetailView):
    model = Book
class DetalleAutor(generic.DetailView):
    model = Author
class listaPrestados(generic.ListView):
    model = BookInstance
    def get_queryset(self):
        return super().get_queryset().filter(status__exact = "o")
def ampliarFecha(request,pk):
    book_inst = get_object_or_404(BookInstance, pk = pk )
    if request.method == "POST":
        print('esto es el post dentro que es realmente ', request.POST)

        form  = RenewBookForm(request.POST)
        if form.is_valid():
            book_inst.due_back = form.cleaned_data["renewel_date"]
            book_inst.save()



            return HttpResponseRedirect(reverse("prestados"))

    else:

        fecha_propuesta = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookForm(initial = {"renewel_date": fecha_propuesta})

    return render(request, "fecha_ampliada.html", {"form":form, "bookins": book_inst})

def crearEvento(request):
        form = evento()
        if request.method == "POST":
            form = evento(request.POST)
            if form.is_valid():
                form.save()
                return redirect("eventos")
                

        return render(request,"crearEvento.html",{"form":form})
    

class eventos(generic.ListView):
    model = Evento
    def get_queryset(self):
        return super().get_queryset().filter(qpersonas__usuario=self.request.user)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Mis Eventos"
        #context['ocultar_boton'] = True # Bandera para ocultar botón
        return context

class EventosDisponibles(generic.ListView):
    model = Evento
    template_name = 'catalog/evento_list.html'
    
    def get_queryset(self):
        # Excluir eventos donde el usuario ya está inscrito
        return Evento.objects.exclude(qpersonas__usuario=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Eventos Disponibles"
        return context
    
def asistir(request,pk):
    evento = get_object_or_404(Evento, pk = pk)
   
    """
    esta es la funcion que se encarga de registrar la asistencia de un usuario a un evento
    aqui meto algunas validaciones para que no se pueda registrar un usuario a un evento que ya esta inscrito, entre otras validaciones 
    como que el usuario no pueda inscribirse a mas de 5 eventos y que el evento no sea el mismo dia que otro evento
    """
    fecha = evento.fecha_evento
   
    evento_mismo_dia = Persona.objects.filter(usuario=request.user, eventos__fecha_evento__exact = fecha) 
    
    ids_eventos_usuario = Persona.objects.filter(nombre__exact = request.user.username).values_list("eventos__id", flat=True)
    
    if evento and evento.id not in ids_eventos_usuario and len(ids_eventos_usuario) < 5 and not evento_mismo_dia.exists() and evento.aforoMaximo:

        objeto_us = Persona.objects.filter(nombre__exact = request.user.username)[0]



            
        evento.personas.add(objeto_us, through_defaults={ "fecha":datetime.date.today()
       
    } )
        
        messages.success(request, 'Tu asisntencia se ha registrado')
        return redirect("eventos")
    else: 
        messages.success(request, "tu asistencia no se ha podido registrar")
        return redirect("eventos")



"""ESTA ES LA FUNCION QUE SE ENCARGA DE REGISTRAR UN USUARIO """
def registroUsuario(request):
    form = registroform()
    if request.method == 'POST':
        form = registroform(request.POST)
        if form.is_valid():
            
            usuario = User.objects.create_user(username=form.cleaned_data["nombre"], password = form.cleaned_data["password"])
            persona = Persona(nombre = form.cleaned_data["nombre"], socio_codigo =  form.cleaned_data["numero_socio"], apellido = form.cleaned_data["apellidos"],usuario = usuario)
            
            persona.save()

            return redirect("index")

    return render(request, "registro.html", {"form":form})





    


    