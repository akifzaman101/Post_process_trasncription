from django.urls import path
from .views import UploadChunkView

urlpatterns = [
    path("upload-chunk/", UploadChunkView.as_view(), name="upload-chunk"),
]