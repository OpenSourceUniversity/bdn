import csv
import logging
import zipfile
import codecs
from celery import shared_task
from .models import Connection, FileUpload


logger = logging.getLogger(__name__)


@shared_task
def import_connections(connections_file_id):
    file_upload = FileUpload.objects.get(id=connections_file_id)
    with zipfile.ZipFile(file_upload.datafile) as connections_zip:
        with connections_zip.open('Connections.csv', 'r') as connections_file:
            connections_file = codecs.iterdecode(connections_file, 'utf-8')
            reader = csv.reader(connections_file, delimiter=',', quotechar='"')
            for row in reader:
                first_name = row[0]
                last_name = row[1]
                email = row[2]
                company = row[3]
                position = row[4]
                # connected_on = row[5]
                connection = Connection(
                    owner=file_upload.owner,
                    first_name=first_name,
                    last_name=last_name,
                    email=email,
                    company_name=company,
                    position_title=position,
                    user=None  # TODO: user might already be on the platform
                )
                connection.save()
