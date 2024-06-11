import shutil
from celery import shared_task
from datetime import datetime, timedelta
from project.models import Working
import os

STORAGE_PATH = "Storage/Visitor_Storage"

@shared_task
def delete_old_files():
    two_days_ago = datetime.now() - timedelta(days=7)
    old_files = Working.objects.filter(date__lt=two_days_ago)

    for file_record in old_files:
        time_str = file_record.date.strftime("%H-%M-%S")
        print(f"Time of record: {time_str}")
        file_path = os.path.join(STORAGE_PATH, file_record.filename)
        if os.path.exists(file_path):
            print(file_path)
            os.remove(file_path)
            print(f"Deleted file: {file_path}")
        else:
            print(f"File not found: {file_path}")
        file_record.delete()
        print(f"Deleted record: {file_record.filename}")
    print("Cleanup complete.")




@shared_task
def print_hello():
    print("hello fawad")