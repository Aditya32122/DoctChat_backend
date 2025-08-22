from django.contrib import admin
from .models import Document,Query,VectorStore,Answer
# Register your models here.

admin.site.register(Document)
admin.site.register(Query)
admin.site.register(Answer)
admin.site.register(VectorStore)

