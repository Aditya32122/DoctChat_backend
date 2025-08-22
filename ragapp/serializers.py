from rest_framework import serializers
from .models import Document, Query, Answer, VectorStore
from django.contrib.auth.models import User

class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = '__all__'
        read_only_fields = ['user',"uploaded_at"]

class QuerySerializer(serializers.ModelSerializer):
    class Meta:
        model = Query
        fields = ['id', 'document', 'query_text', 'status', 'created_at']
        read_only_fields = ['status', 'created_at']

class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = '__all__'

class VectorStoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = VectorStore
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'id', 'email']