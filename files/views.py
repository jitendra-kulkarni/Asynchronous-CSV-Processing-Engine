from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import FileUploadSerializer
from .models import File
from rest_framework import status
from .tasks import process_file
from rest_framework.parsers import MultiPartParser, FormParser
from drf_spectacular.utils import extend_schema


# Create your views here.

class FileUploadView(APIView):

    parser_classes=[MultiPartParser, FormParser]

    @extend_schema(
            request=FileUploadSerializer,
            responses={201: None}
    )

    def post(self, request):
        serializer = FileUploadSerializer(data=request.data)

        if serializer.is_valid():
            uploaded_file=serializer.save(
                original_name=serializer.validated_data["file"].name
            )

            process_file.delay(uploaded_file.id)

            return Response(
                {"status": "Uploaded"},

                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class FileStatusView(APIView):
    def get(self, request, file_id):
        try:
            uploaded_file=File.objects.get(id=file_id)

        except File.DoesNotExist:
            return Response(
                {"Error":"File Not Found"},
                status=status.HTTP_404_NOT_FOUND
            )

        return Response({
            "id": uploaded_file.id,
            "filename": uploaded_file.original_name,
            "status": uploaded_file.status,
            "processed_row": uploaded_file.processed_row,
            "uploaded_at": uploaded_file.uploaded_at,
            "processed_at": uploaded_file.processed_at,
        },status=status.HTTP_200_OK)


class FileResultView(APIView):
    def get(self, request, file_id):
        try:
            uploaded_file=File.objects.get(id=file_id)

        except File.DoesNotExist:
            return Response({
                "Error":"File Not Found"
            }, status=status.HTTP_404_NOT_FOUND)

        return Response({
            "id": uploaded_file.id,
            "filename": uploaded_file.original_name,
            "status": uploaded_file.status,
            "processed_row": uploaded_file.processed_row,
        }, status=status.HTTP_200_OK)


def dashboard(request):

    message = None
    errors = None

    if request.method == "POST":

        serializer = FileUploadSerializer(data=request.FILES)

        if serializer.is_valid():

            uploaded_file = serializer.save(
                original_name=serializer.validated_data["file"].name
            )

            process_file.delay(uploaded_file.id)

            message = "File uploaded successfully!"

        else:
            errors = serializer.errors

    uploaded_files = File.objects.order_by("-uploaded_at")

    return render(request, "files/dashboard.html", {
        "message": message,
        "errors": errors,
        "files": uploaded_files
    })
