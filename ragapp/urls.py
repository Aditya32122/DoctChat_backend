from django.urls import path
from .views import (
    RegisterView,
    LoginView,
    DocumentUploadView,
    QueryAnswerView,
    DocumentListView
)


urlpatterns = [
    path("register/",RegisterView.as_view(),name="register"),
    path("login/",LoginView.as_view(),name="login"),
    path("upload-document/",DocumentUploadView.as_view(),name = "upload-document"),
    path("query/",QueryAnswerView.as_view(),name="query"),
    path("documents/", DocumentListView.as_view(), name="document-list"),   
]