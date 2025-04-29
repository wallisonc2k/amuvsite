from django import forms
from .models import Membro

class MembroForm(forms.ModelForm):
    # Campos adicionais para facilitar o processamento
    interesses_choices = [
        ('cultural', 'Eventos Culturais'),
        ('religioso', 'Eventos Religiosos'),
        ('esporte', 'Esportes'),
        ('educacao', 'Educação'),
        ('saude', 'Saúde'),
        ('social', 'Ação Social')
    ]
    
    # Campos criados explicitamente para os checkboxes
    interesses = forms.MultipleChoiceField(
        choices=interesses_choices,
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    
    class Meta:
        model = Membro
        fields = [
            'first_name', 'last_name', 'email', 'telefone', 'cpf', 'data_nascimento', 'foto',
            'cep', 'logradouro', 'numero', 'complemento', 'bairro', 'cidade', 'estado',
            'interesses', 'receber_notificacoes', 'disponivel_voluntario'
        ]
        widgets = {
            'data_nascimento': forms.DateInput(attrs={'type': 'date'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Aplica classes CSS aos campos
        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.CheckboxInput) or isinstance(field.widget, forms.CheckboxSelectMultiple):
                continue
            field.widget.attrs.update({
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-red-500 focus:border-red-500'
            })
            
        # Se o usuário já tem interesses, pré-selecione-os
        if self.instance.pk and self.instance.interesses:
            self.initial['interesses'] = self.instance.interesses