from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import *
from django.contrib.auth.password_validation import validate_password

class CustomerUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerUser
        fields = '__all__'


class LoginSerializer(serializers.Serializer):
    user_name = serializers.CharField(max_length=150)
    password = serializers.CharField(write_only=True)
    
    def validate(self, data):
        user = authenticate(username=data['user_name'], password=data['password'])
        if user:
           return user
        raise serializers.ValidationError('Invalid username or password')


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password_two = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = CustomerUser
        fields = '__all__'


    def validate(self, data):
        if data['password'] != data['password_two']:
            raise serializers.ValidationError('Passwords must match')
        return data
            
    def create(self, validated_data):
        user = CustomerUser.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user


class AccountUpdateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password_two = serializers.CharField(write_only=True, required=True)
    
    class Meta:
        model = CustomerUser
        fields = '__all__'


    def validate(self, data):
        if data['password'] != data['password_two']:
            raise serializers.ValidationError('Passwords must match')
        return data
        
    def update(self, actual, validated_data):
        actual.username = validated_data.get('username', actual.username)
        actual.email = validated_data.get('email', actual.email)
        actual.bio = validated_data.get('bio', actual.bio)
        actual.avatar = validated_data.get('avatar', actual.avatar)

        if 'password' in validated_data:
            actual.set_password(validated_data['password'])  
            actual.save()
        return actual


