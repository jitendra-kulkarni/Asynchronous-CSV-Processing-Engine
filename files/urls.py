from .views import FileUploadView, FileStatusView, FileResultView
from django.urls import path

urlpatterns=[
    path("upload/", FileUploadView.as_view(), name="File_upload"),
    path("files/<int:file_id>/status/",FileStatusView.as_view(),name="file_status"),
    path("files/<int:file_id>/result/", FileResultView.as_view(), name="file_result")
]


