from django import forms
from .models import Etiqueta

class EtiquetasForm(forms.Form):
    etiquetas = forms.ModelMultipleChoiceField(
        queryset=Etiqueta.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        help_text="Selecciona hasta 3 etiquetas",
        label="Selecciona etiquetas"
    )

    valoracion = forms.ChoiceField(
        choices=[(i, f"{i} estrella{'s' if i != '1' else ''}") for i in ['1','2','3','4','5']],
        required=False,
        widget=forms.RadioSelect,
        label="Valoración (opcional)"
    )

    def clean_etiquetas(self):
        etiquetas = self.cleaned_data.get('etiquetas')
        if etiquetas and len(etiquetas) > 3:
            raise forms.ValidationError("Máximo 3 etiquetas.")
        return etiquetas
