import csv
import logging
import zipfile
import codecs
import time
from celery import shared_task
from .models import Connection, FileUpload
from bdn.profiles.models import Profile
from django.core.mail import BadHeaderError, send_mass_mail
from django.http import HttpResponse


logger = logging.getLogger(__name__)


@shared_task
def import_connection(connection_file_id):
    file_upload = FileUpload.objects.get(id=connection_file_id)
    with zipfile.ZipFile(file_upload.datafile) as connection_zip:
        with connection_zip.open('Connections.csv', 'r') as connection_file:
            connection_file = codecs.iterdecode(connection_file, 'utf-8')
            reader = csv.reader(connection_file, delimiter=',', quotechar='"')
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
        user_id=handle_onboarding(email)
    )
    connection.save()


@shared_task
def handle_onboarding(email):
    if len(email) > 0:
        onboarded_users = Profile.objects.filter(learner_email=email)
        if onboarded_users:
            return onboarded_users[0].user.id
    return None


@shared_task
def inviting_emails(connection_file_id):
    subject = 'Test Subject {name}'
    message = 'This is a test message ... {name}'
    from_email = 'project@os.university'
    all_emails = []
    chunk_size = 500
    if subject and message and from_email:
        file_upload = FileUpload.objects.get(id=connection_file_id)
        if file_upload:
            # profile = Profile.objects.get(user=file_upload.owner)
            connections = Connection.objects.filter(
                owner_id=file_upload.owner.id, user_id=None)
            for connection in connections:
                all_emails.append(
                    (subject.format(name='test name'),
                     message.format(name='test name'),
                     from_email, [connection.email]))
            if all_emails:
                all_emails = [all_emails[i:i+chunk_size] for i in range(
                    0, len(all_emails), chunk_size)]
                for item in all_emails:
                    send_chunk_of_emails(tuple(item))
        else:
            return HttpResponse('Archive not found!')


@shared_task
def send_chunk_of_emails(messages):
    try:
        send_mass_mail((messages,), fail_silently=False)
    except BadHeaderError:
        return HttpResponse('Invalid header found.')
    return True
