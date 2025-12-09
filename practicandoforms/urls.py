from django.urls import path
from . import views
urlpatterns = [
    path("mostrar/",views.mostrar , name = "mostrar"),
    path("listaExpendientes/",views.listaExpendiente.as_view(),name = "expendientes")
]