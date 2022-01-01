from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth import authenticate, login, logout
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect, ensure_csrf_cookie, requires_csrf_token
from rest_framework import status, viewsets, permissions
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.views import APIView
from core.serializers import RegistrationSerializer, UserSerializer, UserLoginSerializer, ProfilePasswordSerializer
#  from rest_framework.authtoken.models import Token
from core.models import User
from rolepermissions.checkers import has_permission, has_role
from django.db import transaction
import jwt
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

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


class CreateUserView(APIView):
    @swagger_auto_schema(request_body=RegistrationSerializer) 
    @transaction.atomic  # if there is some error, it will be roolback all transaction
    def post(self, request):
        try:
            if has_permission(request.user, 'create_user'):
                data = request.data
                serializer =  RegistrationSerializer(data=data)
                serializer.is_valid(raise_exception=True)
                serializer.save()
                return Response(serializer.data)
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        except Exception:
            transaction.rollback()


class LoginView(APIView):
    permission_classes = (permissions.AllowAny,)

    #  csrftoken = openapi.Parameter(
        #  'email', in_=openapi.IN_HEADER, description='User email',type=openapi.TYPE_STRING    <<<< how to use custom header/query param
    #  )
    #  sessionid = openapi.Parameter(
        #  'password', in_=openapi.IN_HEADER, description='User password',type=openapi.TYPE_STRING
    #  )
    #  @swagger_auto_schema(request_body=UserLoginSerializer, manual_parameters=[csrftoken, sessionid]) 

    @swagger_auto_schema(request_body=UserLoginSerializer) 
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
            # 'auth.login' will add user session in request, and in some way the sessionid cookie will be sent in the Response
            # I think that APIView is doing this automatically.

            #  payload = {
                #  'id': user.id,
                #  "username": user.first_name
            #  }

            #  token = jwt.encode(payload, 'secret', algorithm='HS256').decode('utf-8')

            #  response = Response()

            #  response.set_cookie(key='jwt', value=token, httponly=True)
            
            return Response(UserSerializer(user).data)
        else:
            return Response({"status": "login_failed"}, status=status.HTTP_401_UNAUTHORIZED)

#  @method_decorator(csrf_protect, name='dispatch')
class LogoutView(APIView):
    def post(self, request, format=None):
        try:
            logout(request)
            return Response({'success': 'Loggout out'})
        except Exception as error:
            print(error)
            return Response({'error': 'Something went wrong when logging out.'})


class GetUsers(APIView):
    def get(self, request):
        user = request.user
        if has_permission(user, 'get_all_users'):
            users = User.objects.all()
            data = UserSerializer(users, many=True).data
            return Response(data)

        return Response({'error': "You don't have permission to access this resource."},status=status.HTTP_401_UNAUTHORIZED)


class DeleteAccountView(APIView):
    @transaction.atomic  
    def delete(self, request, email, format=None):
        if has_permission(request.user, 'delete_users'):
            try: 
              user = User.objects.get(email=email)

              if user.is_superuser or has_role(user, 'admin'):
                return Response({'error': "You don't have permission to delete this user."},status=status.HTTP_401_UNAUTHORIZED)

              user.delete()
              return Response({"success": "User deleted successfully."})

            except User.DoesNotExist:
              return Response(status=status.HTTP_404_NOT_FOUND) 

            except Exception as error:
                print(error)
                transaction.rollback()

        return Response({'error': "You don't have permission to access this resource."},status=status.HTTP_401_UNAUTHORIZED)


#  class DeleteAccountView(APIView):
    #  def delete(self, request, format=None):
        #  if has_permission(user, 'get_all_users'):
        #  request.user.delete()
        #  return Response({"success": "User deleted successfully."})


class ProfileInfoView(APIView):
    @swagger_auto_schema(request_body=UserSerializer) 
    def put(self, request):
        user = request.user
        serializer = UserSerializer(user, data=request.data, partial=True) # (partial=True)we dont want to update every field
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class ProfilePasswordView(APIView):
    #  @swagger_auto_schema(request_body=openapi.Schema(title="Password", description='Description', type=openapi.TYPE_STRING))
    @swagger_auto_schema(request_body=ProfilePasswordSerializer) 
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


@method_decorator( ensure_csrf_cookie, name='dispatch')
class CheckAuthenticatedView(APIView):
    def get(self, request, format=None):
        try:
            data = UserSerializer(request.user).data
            return Response(data)
        except Exception as error:
            return Response({'status': 'error', 'description': 'Something went wrong when checking authentication status.'}, 
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR)


#  class PasswordResetView(APIView):
    #  permission_classes = (permissions.AllowAny,)

    #  def get(self, request, format=None):
        #  return Response({"status": "email has been sent."})
