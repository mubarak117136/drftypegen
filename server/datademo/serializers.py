from .models import *
from rest_framework import serializers
from django.contrib.auth import get_user_model

USER_MODEL = get_user_model()

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = "__all__"

class PersonBookRelationSerializer(serializers.ModelSerializer):


    class Meta:
        model = PersonBookRelation
        fields = "__all__"

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = USER_MODEL
        fields = ('username', 'first_name', 'last_name')

class PersonSerializer(serializers.ModelSerializer):
    books = BookSerializer(read_only=True, many=True)
    users = UserSerializer(many=True, read_only=True)
    class Meta:
        model = Person
        fields = '__all__'