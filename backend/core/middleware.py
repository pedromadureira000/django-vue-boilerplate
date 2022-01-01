from django.http import HttpResponseForbidden
from rest_framework import exceptions, status
from django.contrib.sessions.models import Session
from datetime import datetime

class OneSessionPerUserMiddleware:
    # Called only once when the web server starts
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        print('inside onesession middleware: ', datetime.now())
        if request.user.is_authenticated:
            path = request.get_full_path()
            stored_session_key = request.user.logged_in_user.session_key
            if path == '/api/user/checkauth':
                request.user.logged_in_user.session_key = request.session.session_key
                request.user.logged_in_user.save()
                response = self.get_response(request)
                return response

            if stored_session_key and stored_session_key != request.session.session_key:
                return HttpResponseForbidden("Session already open.")
              #  raise exceptions.APIException("There was a problem!", 403)

            response = self.get_response(request)
            return response
        response = self.get_response(request)
        return response
