from rest_framework import serializers
from .models import *

class ClientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Client
        fields = '__all__'


class DebtSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Debt
        fields = '__all__'