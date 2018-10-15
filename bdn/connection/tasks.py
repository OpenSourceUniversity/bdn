import logging
import time
from celery import shared_task
from bdn.auth.models import User
from mail_templated import EmailMessage
from .models import Connection
from django.conf import settings
# from .serializers import ConnectionSerializer


logger = logging.getLogger(__name__)


@shared_task
def handle_onboarding(email):
    if email:
        onboarded_user = User.objects.filter(email=email).first()
        if onboarded_user:
            return onboarded_user.id
    return None


@shared_task
def handle_connection_row(owner, row):
    full_name = '{} {}'.format(row[0], row[1])
    email = row[2].lower()
    company = row[3]
    position = row[4]
    connected_on = time.strptime(row[5].strip(), "%m/%d/%y, %I:%M %p")
    onboarded_user = handle_onboarding(email)
    connection, created = Connection.objects.get_or_create(
        owner_id=owner,
        full_name=full_name,
        email=email,
        company_name=company,
        position_title=position,
        connected_on=time.strftime("%Y-%m-%d %H:%M", connected_on),
        user_id=onboarded_user
    )
    if created:
        connection.save()
        # if not onboarded_user:
        #     inviting_emails.delay(ConnectionSerializer(connection).data)


@shared_task
def inviting_emails(connection):
    from_email = settings.DEFAULT_FROM_EMAIL
    message = EmailMessage(
        'mail/sec1.tpl',
        {
            'full_name': connection['full_name'],
        },
        from_email,
        to=[connection['email']])
    message.send()
