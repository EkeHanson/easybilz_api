from rest_framework import serializers
from .models import CustomUser



class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()
    

class CustomUserSerializer(serializers.ModelSerializer):
    user_type = serializers.CharField(default='customer')
    password = serializers.CharField(min_length=8, write_only=True)

    class Meta:
        model = CustomUser
        fields = '__all__'

    def create(self, validated_data):
        password = validated_data.pop("password")

        user = super().create(validated_data)
        user.set_password(password)

        user.save()

        return user

