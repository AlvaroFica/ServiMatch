from django import forms
from .models import Servicio, Trabajador

class ServiciosTrabajadorForm(forms.ModelForm):
    servicios = forms.ModelMultipleChoiceField(
        queryset=Servicio.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        label="Servicios que ofreces",
        required=True
    )

    class Meta:
        model = Trabajador
        fields = ['servicios']
