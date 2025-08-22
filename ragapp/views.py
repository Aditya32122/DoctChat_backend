from django.shortcuts import render
from .serializers import DocumentSerializer,QuerySerializer,AnswerSerializer,VectorStoreSerializer,UserSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Document, Query, Answer, VectorStore
from .embedding import get_embedding
from .qdrant_client import add_vector, initialize_qdrant_collection
from .rag import generate_answer
from rest_framework import status, permissions
from django.contrib.auth.models import User 
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
import os
import fitz  # PyMuPDF
from rest_framework.parsers import MultiPartParser, FormParser



import uuid

initialize_qdrant_collection()

class RegisterView(APIView):
    def post(self,request):
        username = request.data.get("username")
        password = request.data.get("password")
        email = request.data.get("email")

        if not username or not password or not email:
            return Response({"msg":"provide all the details"},status=400)
        
        if User.objects.filter(username=username).exists():
            return Response({"msg":"Username already exists"},status=400)
        
        user = User.objects.create_user(username=username,password=password,email=email)
        return Response({'message':"user register successfully"})
    
class LoginView(APIView):
    def post(self,request):
            username = request.data.get("username")
            password = request.data.get("password")

            user = authenticate(username=username,password=password)

            
            if user is not None:
                refresh = RefreshToken.for_user(user)
                return Response({
                    'refresh':str(refresh),
                    'access':str(refresh.access_token)
                })
            else:
                return Response({'error':'invalid credetials'})



class DocumentUploadView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]  # 👈 THIS is required


    def post(self, request):
        serializer = DocumentSerializer(data=request.data)

        if serializer.is_valid():
            document = serializer.save(user=request.user)

            file_obj = document.file
            ext = os.path.splitext(file_obj.name)[-1].lower()
            file_obj.seek(0)

            try:
                if ext == ".pdf":
                    with fitz.open(stream=file_obj.read(), filetype="pdf") as doc:
                        text = "\n".join(page.get_text() for page in doc)
                else:
                    text = file_obj.read().decode("utf-8")
            except Exception as e:
                return Response({"error": f"Unsupported or corrupted file: {str(e)}"}, status=400)

            embedding = get_embedding(text)
            qdrant_id = str(uuid.uuid4())
            metadata = {
                "document_id": document.id,
                "title": document.title,
                "text": text[:5000],
            }
            add_vector(id=qdrant_id, vector=embedding, metadata=metadata)

            VectorStore.objects.create(
                document=document,
                qdrant_point_id=qdrant_id,
                embedding_model="gemini-embedding-001",
            )

            return Response({"msg": "Document uploaded and embedded"}, status=201)

        return Response(serializer.errors, status=400)

class QueryAnswerView(APIView):

    permission_classes = [permissions.IsAuthenticated]

    def post(self,request):
        serializer = QuerySerializer(data = request.data)
        if serializer.is_valid():
            query = serializer.save(user= request.user)

            result= generate_answer(query.query_text)

            answer = Answer.objects.create(
                query=query,
                answer_text=result["answer"],
                confidence=1.0,  # placeholder, Gemini doesn't return score
                source="\n\n".join(result["context"]),
            )

            answer_serializer = AnswerSerializer(answer)
            return Response(answer_serializer.data, status=200)

        return Response(serializer.errors, status=400)

class DocumentListView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        documents = Document.objects.filter(user=request.user).order_by('-uploaded_at')
        serializer = DocumentSerializer(documents, many=True)
        return Response(serializer.data)


