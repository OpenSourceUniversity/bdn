import uuid
from django.db import models as m


class Unsubscribe(m.Model):
    id = m.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = m.EmailField(max_length=100)
    unsubscribe_token = m.UUIDField(default=uuid.uuid4, editable=False)
    subscribed = m.BooleanField(default=True)

    def __str__(self):
        return self.email

    @property
    def unsubscribe_link(self):
        return 'https://bdn.os.university/unsubscribe/{}/{}/'.format(
            self.id, self.unsubscribe_token)
