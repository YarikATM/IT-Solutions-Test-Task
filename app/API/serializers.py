from rest_framework import serializers
from API.models import Car, Comment
from django.contrib.auth import get_user_model
User=get_user_model()



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'is_active', 'is_staff', 'is_superuser')



class CarSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = Car
        fields = ('id', 'make', 'model', 'year', 'description', 'created_at', 'updated_at', 'user')




class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    car = CarSerializer(read_only=True)
    class Meta:
        model = Comment
        fields = ('id', 'content', 'created_at', 'car', 'user')