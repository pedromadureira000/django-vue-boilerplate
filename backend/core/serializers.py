from django.utils.timezone import now
from rest_framework import serializers
from core.models import User
from rolepermissions.roles import get_user_roles

class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def save(self):
        user = User(
            first_name=self.validated_data.get('first_name', ''),
            last_name=self.validated_data.get('last_name', '' ),
            email=self.validated_data['email'],
        )
        password = self.validated_data['password']
        user.set_password(password)
        user.save()
        return user


class UserSerializer(serializers.ModelSerializer):
    modules = serializers.SerializerMethodField() # will call get_<field_name> by default
    email = serializers.EmailField(read_only=True)

    class Meta:
        ref_name = "User Serializer" # fixes name collision with djoser when fetching urls with swagger
        model = User
        fields = ['first_name', 'last_name', 'email', 'modules']


    def get_modules(self, user):
        modules = []
        user_roles = get_user_roles(user) 
        for role in user_roles:
            modules.append(role.get_name())
        return modules


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField(write_only=True)
    password = serializers.CharField(write_only=True)
 
    #  class Meta:
        #  model = User
        #  fields = ['email', 'password']

class ProfilePasswordSerializer(serializers.Serializer):
    password = serializers.CharField(write_only=True)
    current_password = serializers.CharField(write_only=True)
 

