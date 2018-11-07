from celery import shared_task
from django.conf import settings
from mail_templated import EmailMessage


@shared_task
def rejected_certificate_email(certificate_title, issuer_name, send_to):
    from_email = settings.DEFAULT_FROM_EMAIL
    message = EmailMessage(
        'mail/certificate_rejected.tpl',
        {
            'issuer_name': issuer_name,
            'certificate_title': certificate_title,
            'unsubscribe_link': 'https://dapp.os.university/#/settings',
        },
        from_email,
        to=[send_to])
    message.send()


@shared_task
def verified_certificate_email(certificate_title, issuer_name, send_to):
    from_email = settings.DEFAULT_FROM_EMAIL
    message = EmailMessage(
        'mail/certificate_verified.tpl',
        {
            'issuer_name': issuer_name,
            'certificate_title': certificate_title,
            'unsubscribe_link': 'https://dapp.os.university/#/settings',
        },
        from_email,
        to=[send_to])
    message.send()


@shared_task
def certificate_upload_email(certificate_title, issuer_name, send_to):
    from_email = settings.DEFAULT_FROM_EMAIL
    message = EmailMessage(
        'mail/certificate_uploaded.tpl',
        {
            'issuer_name': issuer_name,
            'certificate_title': certificate_title,
            'unsubscribe_link': 'https://dapp.os.university/#/settings',
        },
        from_email,
        to=[send_to])
    message.send()


@shared_task
def approved_job_application_email(job_title, issuer_name, send_to):
    from_email = settings.DEFAULT_FROM_EMAIL
    message = EmailMessage(
        'mail/job_application_approved.tpl',
        {
            'issuer_name': issuer_name,
            'job_title': job_title,
            'unsubscribe_link': 'https://dapp.os.university/#/settings',
        },
        from_email,
        to=[send_to])
    message.send()


@shared_task
def inviting_email(connection, unsubscribe_link, owner_name):
    from_email = settings.DEFAULT_FROM_EMAIL
    message = EmailMessage(
        'mail/linkedin_connection.tpl',
        {
            'full_name': connection['full_name'],
            'unsubscribe_link': unsubscribe_link,
            'owner_name': owner_name,
        },
        from_email,
        to=[connection['email']])
    message.send()


@shared_task
def verification_email(verification_link, send_to):
    from_email = settings.DEFAULT_FROM_EMAIL
    message = EmailMessage(
        'mail/account_created.tpl',
        {
            'verification_link': verification_link,
            'unsubscribe_link': 'https://dapp.os.university/#/settings',
        },
        from_email,
        to=[send_to])
    message.send()


@shared_task
def not_created_email(unsubscribe_link, send_to):
    from_email = settings.DEFAULT_FROM_EMAIL
    message = EmailMessage(
        'mail/account_not_created.tpl',
        {
            'unsubscribe_link': unsubscribe_link,
        },
        from_email,
        to=[send_to])
    message.send()


@shared_task
def profile_created_email(profile_type, send_to):
    from_email = settings.DEFAULT_FROM_EMAIL
    message = EmailMessage(
        'mail/profile_created.tpl',
        {
            'profile_type': profile_type,
            'unsubscribe_link': 'https://dapp.os.university/#/settings',
        },
        from_email,
        to=[send_to])
    message.send()
