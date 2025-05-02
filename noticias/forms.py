from django import forms
from .models import Noticia

class NoticiaForm(forms.ModelForm):
    class Meta:
        model = Noticia
        fields = ['titulo', 'subtitulo', 'resumo', 'conteudo', 'imagem_capa', 'categoria', 'data_evento', 'local_evento']
        widgets = {
            'titulo': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border rounded-xl',
                'placeholder': 'Digite o título da notícia'
            }),
            'subtitulo': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border rounded-xl',
                'placeholder': 'Digite o subtítulo (opcional)'
            }),
            'resumo': forms.Textarea(attrs={
                'class': 'w-full px-4 py-2 border rounded-xl h-24',
                'placeholder': 'Digite um resumo curto da notícia...',
                'maxlength': '300',  # Limite visual no form
            }),
            'conteudo': forms.CharField(),  # O CKEditor será aplicado automaticamente
            'imagem_capa': forms.ClearableFileInput(attrs={
                'class': 'w-full px-4 py-2'
            }),
            'data_evento': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Tornar campos de evento condicionais
        self.fields['data_evento'].required = False
        self.fields['local_evento'].required = False

    def clean_titulo(self):
        titulo = self.cleaned_data.get('titulo')
        if "spam" in titulo.lower():
            raise forms.ValidationError("O título não pode conter a palavra 'spam'.")
        return titulo

    def clean_resumo(self):
        resumo = self.cleaned_data.get('resumo')
        if len(resumo) > 300:
            raise forms.ValidationError("O resumo deve ter no máximo 300 caracteres.")
        return resumo
