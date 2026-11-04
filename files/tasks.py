import csv
import logging
from celery import shared_task
from django.utils import timezone
from .models import File


logger = logging.getLogger(__name__)


@shared_task
def process_file(file_id):
    try:
        uploaded_file = File.objects.get(id=file_id)

        uploaded_file.status = "PROCESSING"
        uploaded_file.processed_row = None
        uploaded_file.processed_at = None

        uploaded_file.save(
            update_fields=[
                "status",
                "processed_row",
                "processed_at",
            ]
        )

        if not uploaded_file.file.name.lower().endswith(".csv"):
            uploaded_file.status = "FAILED"
            uploaded_file.save(update_fields=["status"])

            logger.warning(
                "File %s has an unsupported file type.",
                file_id,
            )

            return {
                "file_id": file_id,
                "status": "FAILED",
                "reason": "Unsupported file type",
            }

        with uploaded_file.file.open("r") as file:
            reader = csv.reader(file)
            next(reader, None)
            row_count = sum(1 for row in reader)

       
        uploaded_file.processed_row = row_count
        uploaded_file.status = "COMPLETED"
        uploaded_file.processed_at = timezone.now()

        uploaded_file.save(
            update_fields=[
                "processed_row",
                "status",
                "processed_row",
                "processed_at",
            ]
        )

        logger.info(
            "File %s processed successfully. Rows: %s",
            file_id,
            row_count,
        )

        return {
            "file_id": file_id,
            "status": "COMPLETED",
            "processed_row": row_count,
        }

    except File.DoesNotExist:
        logger.error(
            "File record with ID %s does not exist.",
            file_id,
        )
        raise

    except Exception:
        File.objects.filter(id=file_id).update(status="FAILED")
        logger.exception(
            "Processing failed for file ID %s.",
            file_id,
        )
        raise
