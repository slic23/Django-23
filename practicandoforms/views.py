from django.shortcuts import render
from  .forms  import tiposForms

from django.views import generic
import datetime
from .models import Expediente
# Create your views here.


def mostrar(request):
    form = tiposForms()
    if request.method == "POST":

        if form.is_valid():
            pass
    
    return render(request,"mostrar.html",{"form":form})



class listaExpendiente(generic.ListView):
    model = Expediente

    def get_context_data(self, **kwargs):
        dic = super().get_context_data(**kwargs)
        dic["fecha_hoy"] = datetime.datetime.now().strftime("%Y-%m-%d %H-%M")
        return dic 
    

   




