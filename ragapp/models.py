from django.db import models
from django.contrib.auth.models import User

class Document(models.Model):
    """Model to store uploaded documents."""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True,null=True)
    file = models.FileField(upload_to='documents/')
    file_type = models.CharField(max_length=50, blank=True, null=True)  
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
class Query(models.Model):
    """Model to store user queries."""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    document = models.ForeignKey(Document, on_delete=models.SET_NULL, null=True, blank=True) 
    status = models.CharField(max_length=20, default="pending")
    query_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Query by {self.user.username}: {self.query_text[:50]}"
    
class Answer(models.Model):
    """Model to store answers to user queries."""
    query = models.ForeignKey(Query, on_delete=models.CASCADE, related_name='answers')
    answer_text = models.TextField()
    confidence = models.FloatField(default=0.0)  # Added
    source = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"Answer to {self.query.query_text[:50]}: {self.answer_text[:50]}"
    
class VectorStore(models.Model):
    """Model to store metadata and references for Qdrant vector representations."""
    document = models.ForeignKey(Document, on_delete=models.CASCADE)
    qdrant_point_id = models.CharField(max_length=100, unique=True)  # Reference to Qdrant point
    embedding_model = models.CharField(max_length=100, default="unknown")  # Track model used
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Qdrant Vector for {self.document.title} (ID: {self.qdrant_point_id})"
    
