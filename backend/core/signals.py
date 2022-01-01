from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
#  from settings import settings  ?any difference?
from django.conf import settings
from rolepermissions.roles import assign_role
from django.contrib.auth import user_logged_in, user_logged_out
from .models import LoggedInUser
from datetime import datetime

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)  # every time a user was created, a token will be generated fo that user.

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def assign_default_roles(sender, instance=None, created=False, **kwargs):
    if created:
        assign_role(instance, 'reports')

# Signals that fires when a user logs in and logs out. And send 'user' as positional argument

@receiver(user_logged_in)
def on_user_logged_in(sender, request, **kwargs):
    print('on_user_logged_in: ', datetime.now())
    obj, created = LoggedInUser.objects.get_or_create(user=kwargs.get('user'))   #get_or_create returns a tuple( created is a boolean )
    obj.session_key = request.session.session_key
    obj.save()


@receiver(user_logged_out)
def on_user_logged_out(sender, **kwargs):
    print('on_user_logged_out')
    LoggedInUser.objects.filter(user=kwargs.get('user')).delete()
