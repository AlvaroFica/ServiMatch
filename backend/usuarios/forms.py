from django import forms
from .models import Servicio, PlanServicioTrabajador

class CrearPlanServicioTrabajadorForm(forms.ModelForm):
    servicio = forms.ModelChoiceField(
        queryset=Servicio.objects.all(),
        empty_label="Selecciona un servicio",
        widget=forms.Select(attrs={'id': 'servicio-select'}) # ID para JavaScript
    )
    nombre_plan = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={'placeholder': 'Ej: Plan Básico de Reparación'})
    )
    descripcion_plan = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3, 'placeholder': 'Describe los detalles de este plan'})
    )
    precio_ofrecido = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        widget=forms.NumberInput(attrs={'placeholder': 'Ej: 25000'})
    )
    duracion_estimada = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={'placeholder': 'Ej: 1 hora, 3 días'})
    )

    class Meta:
        model = PlanServicioTrabajador
        fields = ['servicio', 'nombre_plan', 'descripcion_plan', 'precio_ofrecido', 'duracion_estimada']