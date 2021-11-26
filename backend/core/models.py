from django.contrib import auth
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django_cpf_cnpj.fields import CPFField, CNPJField
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from settings import settings


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """
        Create and save a user with the given email, and password.
        """
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_admin_agent', True)
        extra_fields.setdefault('all_api_permissions', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)

    def with_perm(self, perm, is_active=True, include_superusers=True, backend=None, obj=None):
        if backend is None:
            backends = auth._get_backends(return_tuples=True)
            if len(backends) == 1:
                backend, _ = backends[0]
            else:
                raise ValueError(
                    'You have multiple authentication backends configured and '
                    'therefore must provide the `backend` argument.'
                )
        elif not isinstance(backend, str):
            raise TypeError(
                'backend must be a dotted import path string (got %r).'
                % backend
            )
        else:
            backend = auth.load_backend(backend)
        if hasattr(backend, 'with_perm'):
            return backend.with_perm(
                perm,
                is_active=is_active,
                include_superusers=include_superusers,
                obj=obj,
            )
        return self.none()


class User(AbstractBaseUser, PermissionsMixin):
    """
    App User 'User Class'

    Email and password are required. Other fields are optional.
    """

    first_name = models.CharField(_('first name'), max_length=150, blank=True)
    last_name = models.CharField(_('last name'), max_length=150, blank=True)
    email = models.EmailField(_('email address'), unique=True)
    cpf = CPFField(masked=True, blank=True, verbose_name="CPF")
    company = models.ForeignKey('Company', blank=True, on_delete=models.PROTECT, null=True, verbose_name="Empresa")
    is_admin_agent = models.BooleanField(default=False)
    all_api_permissions = models.BooleanField(default=False)
    modules = [{"title": "reports", "icon":"mdi-clipboard-list-outline", "to": "/reports"}]

    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    objects = UserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    # REQUIRED_FIELDS must contain all required fields on your user model, but should not contain the USERNAME_FIELD or
    # password as these fields will always be prompted for.

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """Return the short name for the user."""
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)


class Company(models.Model):
    type_choices = (
        ("D", "Distribuidora"),
        ("L", "Lojista"),
        ("O", "Outros")
    )
    status_choices = (
        ("A", "Ativado"),
        ("D", "Desativado"),
        ("B", "Bloqueado"),
    )
    #  price_table = models.ForeignKey('orders.PriceTable', blank=True, null=True, on_delete=models.DO_NOTHING, verbose_name="Tabela preço")
    name = models.CharField(max_length=60, verbose_name="Nome")
    cnpj = CNPJField(masked=True, blank=True, verbose_name="CNPJ")
    client_code = models.CharField(blank=True, max_length=9, verbose_name="Código do cliente")
    vendor_code = models.CharField(blank=True, max_length=9, verbose_name="Código do vendedor")
    status = models.CharField(max_length=1, choices=status_choices)
    type = models.CharField(max_length=1, choices=type_choices)

    def __str__(self):
        return f'Empresa: {self.name}'


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)  # every time a user was created, a token will be generated fo that user.

