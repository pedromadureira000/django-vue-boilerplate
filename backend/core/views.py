from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth import authenticate, login, logout
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect, ensure_csrf_cookie
from rest_framework import status, viewsets, permissions
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.views import APIView
from core.serializers import RegistrationSerializer, UserSerializer
from rest_framework.authtoken.models import Token
from core.models import User


def index(request):
    return render(request, 'index.html')


@api_view(['POST', 'GET', 'DELETE', 'HEAD', 'PUT', 'CONNECT', 'OPTIONS', 'TRACE', 'PATCH', 'COPY', 'LINK', 'UNLINK', 'PURGE', 'LOCK','UNLOCK','PROPFIND', 'VIEW'])
@permission_classes([AllowAny])
def apiNotFound(request):
    return Response({"status":"api not found"}, status=status.HTTP_404_NOT_FOUND)


@method_decorator(ensure_csrf_cookie, name='dispatch')
class GetCSRFToken(APIView):
    permission_classes = (permissions.AllowAny,)

    def get(self, request, format=None):
        return Response({"sucess": "csrf cookie set"})


#  @method_decorator(csrf_protect, name='dispatch')
#  class SignupView(APIView):
    #  permission_classes = (permissions.AllowAny,)

    #  def post(self, request, format=None):
        #  email = request.data.get('email')
        #  password = request.data.get('password')
        #  if not email:
            #  return Response({'error': "'email' field is missing."})
        #  if not password:
            #  return Response({'error': "'password' field is missing."})
        #  if User.objects.filter(email=email).exists():
            #  return Response({'error': 'That email was already been registered.'})
        #  else:
            #  user = User.objects.create_user(email=email, password=password)
            #  user.save()
            #  return Response({"success": "user created successfully"})


#  @method_decorator(csrf_protect, name='dispatch')
class SignupView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        data = request.data
        serializer =  RegistrationSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class LoginView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        if request.user.is_authenticated:
            return Response({"status": "already_authenticated."})
        email = request.data.get('email')
        password = request.data.get('password')
        if not email:
            return Response({'error': "'email' field is missing."})

        if not password:
            return Response({'error': "'password' field is missing."})

        user = authenticate(username=email, password=password, request=request)
        if user is not None:
            login(request, user)
            # 'auth.login' will add user session in request, and in some way this session will be sent in Response
            # I think that APIView is doing this automatically.
            return Response({'first_name': request.user.first_name, 'last_name': request.user.last_name, 
                'email': request.user.email, 'modules': [{"title": "reports", "icon":"mdi-clipboard-list-outline", "to": "/reports"}]})
        else:
            return Response({"status": "login_failed"}, status=status.HTTP_401_UNAUTHORIZED)


# if user is already logged with sessionAuthentication, the views will be CSRF protected. You just need to use the CSRF
# decorator if you use 'permission.AllowAny'

#  @method_decorator(csrf_protect, name='dispatch')
class LogoutView(APIView):
    def post(self, request, format=None):
        try:
            logout(request)
            return Response({'success': 'Loggout out'})
        except:
            return Response({'error': 'Something went wrong when logging out.'})


#  class UserView(APIView):
    #  def get(self, request):
        #  user = request.user
        #  data = UserSerializer(user).data
        #  return Response(data)


#  class DeleteAccountView(APIView):
    #  def delete(self, request, format=None):
        #  request.user.delete()
        #  return Response({"success": "User deleted successfully."})



class ProfileInfoView(APIView):
    def put(self, request):
        user = request.user
        serializer = UserSerializer(user, data=request.data, partial=True) # (partial=True)we dont want to update every field
        serializer.is_valid(raise_exception=True)
        serializer.save()
        print(serializer.data)
        return Response(serializer.data)


class ProfilePasswordView(APIView):
    def put(self, request):
        user = request.user
        data = request.data
        if not data.get('password'):
            return Response({"status": "Password field not sent."}, status=status.HTTP_400_BAD_REQUEST)

        if not data.get('current_password'):
            return Response({"status": "Current Password field not sent."},status=status.HTTP_400_BAD_REQUEST)

        if user.check_password(data.get('current_password')):
            user.set_password(data['password'])
            user.save()
            #  return Response(UserSerializer(user).data)
            return Response({"status": "Password updated"})
        return Response({"status": "passwords don't match"},status=status.HTTP_400_BAD_REQUEST)


#  @method_decorator(csrf_protect, name='dispatch')
#  class ProfileInfoView(APIView):
    #  def post(self, request):
        #  return Response({"oi":"oi"})


class CheckAuthenticatedView(APIView):
    def get(self, request, format=None):
        try:
            return Response({'first_name': request.user.first_name, 'last_name': request.user.last_name, 'email': request.user.email, 'modules': [{"title": "reports", "icon":"mdi-clipboard-list-outline", "to": "/reports"}]}, status=status.HTTP_200_OK)
        except:
            return Response({'status': 'error', 'description': 'Something went wrong when checking authentication status.'}, 
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR)


#  class PasswordResetView(APIView):
    #  permission_classes = (permissions.AllowAny,)

    #  def get(self, request, format=None):
        #  return Response({"status": "email has been sent."})
