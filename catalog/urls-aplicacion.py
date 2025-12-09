from django.urls import path
from  . import views

urlpatterns = [ path("",views.index,name="index")
               ,path("Libros/",views.ListaLibros.as_view(),name = "listarLibros"),
               path("Autores/",views.ListarAutores.as_view(),name = "listarAutores"),
               path("Libros/<int:pk>",views.DetalleLibro.as_view(),name = 'detalle-libro'),
               path("listaPrestados/", views.listaPrestados.as_view(),name= "prestados"),
               path("ampliar/<uuid:pk>/fecha", views.ampliarFecha, name="ampliar"),
               path("eventos/",views.eventos.as_view(),name="eventos"),
               path("eventos-disponibles/",views.EventosDisponibles.as_view(),name="eventos_disponibles"),
               path("asistir/<int:pk>",views.asistir, name = "asistir"),
               path("registrar/", views.registroUsuario, name="registro")]

urlpatterns += [path("registrarEvento/",views.crearEvento, name = "crearevento")]
