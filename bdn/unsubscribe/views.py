from django.http import HttpResponseRedirect
from django.core.exceptions import ValidationError
from .models import Unsubscribe


def unsubscribe(request, email_id, token):
    try:
        anonymous_unsubscribe = Unsubscribe.objects.all().filter(
            id=email_id,
            unsubscribe_token=token).first()
    except ValidationError:
        return HttpResponseRedirect('/deny/')
    if anonymous_unsubscribe:
        anonymous_unsubscribe.subscribed = False
        anonymous_unsubscribe.save()
        return HttpResponseRedirect('/unsubscribed/')
    else:
        return HttpResponseRedirect('/deny/')
