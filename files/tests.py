from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework import status


class FileUploadTests(TestCase):

    def test_csv_upload_returns_created(self):
        csv_file = SimpleUploadedFile(
            "test_data.csv",
            b"name,age\nAlice,25\nBob,30\n",
            content_type="text/csv",
        )

        response = self.client.post(
            "/api/upload/",
            {"file": csv_file},
            format="multipart",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )
    
    def test_pdf_upload_is_rejected(self):
        pdf_file = SimpleUploadedFile(
            "resume.pdf",
            b"%PDF-1.4 test content",
            content_type="application/pdf",
        )

        response = self.client.post(
            "/api/upload/",
            {"file": pdf_file},
            format="multipart",
        )

        self.assertEqual(response.status_code, 400)

    
    def test_oversized_csv_is_rejected(self):
        large_file = SimpleUploadedFile(
            "large.csv",
            b"a" * (10 * 1024 * 1024 + 1),
            content_type="text/csv",
        )

        response = self.client.post(
            "/api/upload/",
            {"file": large_file},
            format="multipart",
        )

        self.assertEqual(response.status_code, 400)
