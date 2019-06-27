import uuid

from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)

from django.utils.translation import gettext as _
from tinymce.models import HTMLField


def uploaded_filename(instance, filename):
    """
    Scramble / uglify the filename of the uploaded file, but keep the files extension (e.g., .jpg or .png)
    :param instance:
    :param filename:
    :return:
    """
    extension = filename.split(".")[-1]
    return "{}/{}.{}".format(instance.pk, uuid.uuid4(), extension)


class UserManager(BaseUserManager):

    def create_user(self, email, password=None):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError(_('Users must have an email address'))

        user = self.model(
            email=self.normalize_email(email)
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(
            email,
            password=password
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name=_('Email адрес'),
        max_length=255,
        unique=True,
    )
    name = models.CharField(max_length=1024, blank=True, default="")
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    CLIENT = "Клиент"
    ADMINISTRATOR = "Администратор"

    TYPE_CHOICES = (
        (CLIENT, _('Клиент')),
        (ADMINISTRATOR, _('Администратор')),
    )

    type = models.CharField(choices=TYPE_CHOICES, default=ADMINISTRATOR, max_length=100, db_index=True, verbose_name=_("Тип пользователя"))

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _("Пользователь")
        verbose_name_plural = _("Пользователи")

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin


class Application(models.Model):
    user = models.ForeignKey(User, blank=False, null=False, on_delete=models.CASCADE, related_name='users', verbose_name=_('ФИО заявителя'))
    money = models.IntegerField(default=0, blank=False, null=False, db_index=True, verbose_name=_('Запрашиваемая сумма'))
    timestamp = models.DateTimeField(blank=False, null=False, auto_now_add=True, verbose_name=_('Дата заявки'))
    approved = models.BooleanField(default=False, verbose_name=_('Одобрено администратором'))

    class Meta:
        verbose_name = _("Заявка")
        verbose_name_plural = _("Заявки")
