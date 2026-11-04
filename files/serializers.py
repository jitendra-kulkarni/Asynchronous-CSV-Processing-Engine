from rest_framework import serializers
from .models import File


class FileUploadSerializer(serializers.ModelSerializer):

    class Meta:

        model = File
        fields = ["file"]

    def validate_file(self, value):

        allowed_extensions = [".csv"]
        extension = value.name.lower().rsplit(".",1)[-1]

        if f".{extension}" not in allowed_extensions:
            raise serializers.ValidationError(
                "Only .CSV Files are Allowed."
            )

        if value.size > 10 * 1024 * 1024:
            raise serializers.ValidationError(
                "File size must not exceed 10 MB."
            )

        return value