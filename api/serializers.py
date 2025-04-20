from .models import Person,Color

from rest_framework import serializers
from django.contrib.auth.models import User

class ColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Color
        fields = "__all__"

class PersonSerializer(serializers.ModelSerializer):
    color = ColorSerializer()
    country = serializers.SerializerMethodField()


    class Meta:
        model = Person
        fields = '__all__'
        # depth = 1

    def get_country(self,obj):
        return "Spain"

    def validate(self, data):
        if data['age']<18:
            raise serializers.ValidationError('age must be 18+')

        return data
    def validate_name(self,value):
        special_char = '! @ # $ % ^ & * ( ) - _ = + \ | { } ; : / ? . >'
        if any(c in special_char for c in value):
            raise serializers.ValidationError('No ! @ # $ % ^ & * ( ) - _ = + \ | { } ; : / ? . > in ur name')
        return value
    
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()


class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField()
    email =serializers.EmailField()
    password = serializers.CharField()

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Username already exists.")
        return value

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already in use.")
        return value

    def validate_password(self, value):
        # Add more custom password validation rules if needed
        if len(value) < 8:
            raise serializers.ValidationError("Password must be at least 8 characters long.")
        return value
    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
        )
        return user 
    
