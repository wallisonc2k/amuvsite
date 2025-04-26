from django import forms
from .models import Noticia

class NoticiaForm(forms.ModelForm):
    class Meta:
        model = Noticia
        fields = ['titulo', 'subtitulo', 'conteudo', 'imagem_capa']
        widgets = {
            'titulo': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border rounded-xl',
                'placeholder': 'Digite o título da notícia'
            }),
            'subtitulo': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border rounded-xl',
                'placeholder': 'Digite o subtítulo (opcional)'
            }),
            'conteudo': forms.Textarea(attrs={
                'class': 'w-full px-4 py-2 border rounded-xl h-40',
                'placeholder': 'Escreva o conteúdo da notícia aqui...'
            }),
            'imagem_capa': forms.ClearableFileInput(attrs={
                'class': 'w-full px-4 py-2'
            }),
        }

    def clean_titulo(self):
        titulo = self.cleaned_data.get('titulo')
        if "spam" in titulo.lower():
            raise forms.ValidationError("O título não pode conter a palavra 'spam'.")
        return titulo
