from rest_framework import serializers
from .models import Payment, Receipt

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'

class ReceiptSerializer(serializers.ModelSerializer):
    class Meta:
        model = Receipt
        fields = '__all__'
        read_only_fields = ['status', 'issued_date']

    def create(self, validated_data):
        return Receipt.objects.create(**validated_data)
