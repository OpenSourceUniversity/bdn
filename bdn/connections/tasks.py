import csv
import logging
import zipfile
import codecs
import time
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
                handle_connection_row.delay(str(file_upload.owner.id), row)


@shared_task
def handle_connection_row(owner, row):
    first_name = row[0]
    last_name = row[1]
    email = row[2]
    company = row[3]
    position = row[4]
    connected_on = time.strptime(row[5].strip(), "%m/%d/%y, %I:%M %p")
    connection = Connection(
        owner_id=owner,
        first_name=first_name,
        last_name=last_name,
        email=email,
        company_name=company,
        position_title=position,
        connected_on=time.strftime("%Y-%m-%d %H:%M", connected_on),
        user=None  # TODO: user might already be on the platform
    )
    connection.save()
