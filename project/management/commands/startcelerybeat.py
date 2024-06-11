#  {
#     'x': ['1/1/2016', '3/1/2016', '6/1/2016', '7/1/2016', '10/1/2019', '11/1/2019', '2/1/2020'], 
#     'y': [70.0, 50.0, 70.0, 80.0, 70.0, 70.0, 320.0], 
#     'z': {
#        '1/1/2016': {'Health and beauty': 1}, 
#        '3/1/2016': {'Electronic accessories': 1}, 
#        '6/1/2016': {'Home and lifestyle': 1}, 
#        '7/1/2016': {'Health and beauty': 1}, 
#        '10/1/2019': {'Sports and travel': 1}, 
#        '11/1/2019': {'Electronic accessories': 1}, 
#        '2/1/2020': {'Electronic accessories': 2, 'Sports and travel': 1}
#        }
# }

from django.core.management.base import BaseCommand
from subprocess import Popen
import os

class Command(BaseCommand):
    help = 'Start Celery Beat scheduler'

    def handle(self, *args, **options):
        cwd = os.getcwd()
        celery_cmd = f'celery -A {cwd}.celery beat'
        Popen(celery_cmd, shell=True)
        self.stdout.write(self.style.SUCCESS('Celery Beat scheduler started successfully.'))