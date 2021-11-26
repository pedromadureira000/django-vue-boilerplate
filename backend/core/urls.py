from django.urls import path
from django.urls.conf import include
#  from rest_framework.authtoken.views import obtain_auth_token
from core.views import (
    CheckAuthenticatedView, ProfileInfoView, ProfilePasswordView, SignupView, LoginView, LogoutView, GetCSRFToken
)

urlpatterns = [
    path('signup', SignupView.as_view()),
    path('login', LoginView.as_view()),
    path('logout', LogoutView.as_view()),
    path('getcsrf', GetCSRFToken.as_view()),
    path('checkauth', CheckAuthenticatedView.as_view()),
    path('profile', ProfileInfoView.as_view()),
    path('profilepassword', ProfilePasswordView.as_view()),
    path('passwordreset/', include('djoser.urls')),
    #  path('tokenauth/', include('djoser.urls.authtoken')),
    #  path('gettoken', obtain_auth_token, name='gettoken'),
    #  path('delete', DeleteAccountView.as_view(), name='deleteAccount'),
]
