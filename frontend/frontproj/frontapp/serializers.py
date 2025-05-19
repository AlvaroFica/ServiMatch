from rest_framework import serializers
from .models import Servicio, CalificacionEtiqueta

class ServicioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Servicio
        fields = '__all__'

class CalificacionEtiquetaSerializer(serializers.ModelSerializer):
    class Meta:
        model = CalificacionEtiqueta
        fields = '__all__'
