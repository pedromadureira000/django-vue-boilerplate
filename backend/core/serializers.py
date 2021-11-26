from django.utils.timezone import now
from rest_framework import serializers
from core.models import User


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
            #  last_name=self.validated_data['last_name'],
            email=self.validated_data['email'],
        )
        password = self.validated_data['password']
        user.set_password(password)
        user.save()
        return user


class UserSerializer(serializers.ModelSerializer):
    #  days_since_joined = serializers.SerializerMethodField()
    email = serializers.EmailField(read_only=True)
    modules = [{"title": "reports", "icon":"mdi-clipboard-list-outline", "to": "/reports"}]

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'modules']

    #  def get_days_since_joined(self, obj):
        #  return (now() - obj.date_joined).days
