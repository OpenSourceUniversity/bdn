import logging
import time
from celery import shared_task
from bdn.auth.models import User
from .models import Connection
from bdn.utils.send_email_tasks import inviting_email
from bdn.unsubscribe.models import Unsubscribe
from .serializers import ConnectionSerializer


logger = logging.getLogger(__name__)


@shared_task
def handle_onboarding(email):
    if email:
        onboarded_user = User.objects.filter(email=email).first()
        if onboarded_user:
            return onboarded_user.id
    return None


@shared_task
def handle_connection_row(owner_id, row):
    full_name = '{} {}'.format(row[0], row[1])
    email = row[2].lower()
    company = row[3]
    position = row[4]
    connected_on = time.strptime(row[5].strip(), "%m/%d/%y, %I:%M %p")
    onboarded_user = handle_onboarding(email)
    connection, created = Connection.objects.get_or_create(
        owner_id=owner_id,
        full_name=full_name,
        email=email,
        company_name=company,
        position_title=position,
        connected_on=time.strftime("%Y-%m-%d %H:%M", connected_on),
        user_id=onboarded_user
    )
    if created:
        connection.save()
        if not onboarded_user:
            unsubscribe, _ = Unsubscribe.objects.get_or_create(
                email=email)
            if unsubscribe.subscribed:
                owner = User.objects.get(id=owner_id)
                owner_name = owner.profile.full_name
                inviting_email.delay(
                    ConnectionSerializer(
                        connection).data,
                    unsubscribe.unsubscribe_link,
                    str(owner_name))
