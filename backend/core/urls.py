from django.urls import path
from django.urls.conf import include
#  from rest_framework.authtoken.views import obtain_auth_token
from core.views import (
    CheckAuthenticatedView, DeleteAccountView, GetUsers, ProfileInfoView, ProfilePasswordView, CreateUserView, LoginView, LogoutView, GetCSRFToken
)

urlpatterns = [
    path('createuser', CreateUserView.as_view()),
    path('login', LoginView.as_view()),
    path('logout', LogoutView.as_view()),
    path('getcsrf', GetCSRFToken.as_view()),
    path('checkauth', CheckAuthenticatedView.as_view()),
    path('profile', ProfileInfoView.as_view()),
    path('profilepassword', ProfilePasswordView.as_view()),
    path('passwordreset/', include('djoser.urls')),
    #  path('delete', DeleteAccountView.as_view(), name='deleteAccount'),
    path('delete/<str:email>', DeleteAccountView.as_view(), name='deleteAccount'),
    path('getusers', GetUsers.as_view(), name='deleteAccount'),
    #  path('tokenauth/', include('djoser.urls.authtoken')),
    #  path('gettoken', obtain_auth_token, name='gettoken'),
]
