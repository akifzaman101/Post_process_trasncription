from django.urls import path
from .views import UploadChunkView
from .views import MergeChunksView

urlpatterns = [
    path("upload-chunk/", UploadChunkView.as_view(), name="upload-chunk"),
    path("merge-chunks/", MergeChunksView.as_view(), name="merge-chunks"),
]