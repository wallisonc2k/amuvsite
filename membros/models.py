# membros/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser

class Membro(AbstractUser):
    telefone = models.CharField(max_length=20, blank=True)
    cpf = models.CharField(max_length=14, blank=True)
    foto = models.ImageField(upload_to='fotos_perfil/', null=True, blank=True)
    data_nascimento = models.DateField(null=True, blank=True)
    is_ativo = models.BooleanField(default=True)
    
    # Para o endereço, podemos continuar com um campo de texto ou criar campos específicos
    cep = models.CharField(max_length=9, blank=True)
    logradouro = models.CharField(max_length=100, blank=True)
    numero = models.CharField(max_length=10, blank=True)
    complemento = models.CharField(max_length=100, blank=True)
    bairro = models.CharField(max_length=100, blank=True)
    cidade = models.CharField(max_length=100, blank=True)
    estado = models.CharField(max_length=2, blank=True)
    
    # Preferências
    interesses = models.JSONField(default=list, blank=True, null=True)
    receber_notificacoes = models.BooleanField(default=True)
    disponivel_voluntario = models.BooleanField(default=False)

    def __str__(self):
        return self.get_full_name() or self.username

class Pagamento(models.Model):
    membro = models.ForeignKey(Membro, on_delete=models.CASCADE)
    valor = models.DecimalField(max_digits=8, decimal_places=2)
    data_pagamento = models.DateField()
    referencia_mes = models.CharField(max_length=20)  # ex: 'Abril 2025'
    confirmado = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.membro} - {self.referencia_mes} - R$ {self.valor}"
