from django.conf import settings
from django.contrib.auth.models import User
from rest_framework import exceptions
from rest_framework.authentication import BasicAuthentication


class RelayAuthentication(BasicAuthentication):
    """
    Override BasicAuthentication to avoid using a database.
    """

    def authenticate_credentials(self, userid, password, request=None):
        """
        Authenticate the userid and password against username and password
        from the settings file, to authenticate relay.
        with optional request for context.
        """
        if userid == settings.RELAY_CREDENTIALS['username'] \
            and password == settings.RELAY_CREDENTIALS['password']:
            return User(), None # Return a 'empty' user to allow access
        else:
            msg = 'Invalid username/password.'
            raise exceptions.AuthenticationFailed(msg)
