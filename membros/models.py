# membros/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser

class Membro(AbstractUser):
    telefone = models.CharField(max_length=20, blank=True)
    endereco = models.TextField(blank=True)
    data_nascimento = models.DateField(null=True, blank=True)
    is_ativo = models.BooleanField(default=True)

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
