from django.db import models

# Create your models here.
from django.db import models

class Expediente(models.Model):
    ESTADOS = [
        ('borrador', 'Borrador'),
        ('revision', 'En Revisión'),
        ('publicado', 'Publicado'),
    ]

    titulo = models.CharField(max_length=200)
    resumen = models.TextField()
    prioridad = models.IntegerField()
    fecha_limite = models.DateField()
    estado = models.CharField(max_length=20, choices=ESTADOS, default='borrador')
    es_urgente = models.BooleanField(default=False)

    def __str__(self):
        return self.titulo
    


