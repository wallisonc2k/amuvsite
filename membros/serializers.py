from rest_framework import serializers
from .models import Membro, Pagamento

class MembroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Membro
        exclude = ['password', 'user_permissions', 'groups']

class PagamentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pagamento
        fields = '__all__'
