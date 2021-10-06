from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from .validation import validate_year


class MyAccountManager(BaseUserManager):
    def create_user(self, email, username, surname, first_name, patronymic, password):
        if not email:
            raise ValueError("Users must have an email address")
        if not username:
            raise ValueError("Users must have an username")

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            surname=surname,
            first_name=first_name,
            patronymic=patronymic,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password):
        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
            username=username,
            surname='surname',
            first_name='first_name',
            patronymic='patronymic',
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class Account(AbstractBaseUser):
    email = models.EmailField(max_length=30, unique=True, verbose_name='email')
    username = models.CharField(max_length=30, unique=True, verbose_name='Логин')
    first_name = models.CharField(max_length=30, verbose_name='Имя', default='Имя')
    surname = models.CharField(max_length=30, verbose_name='Фамилия', default='Фамилия')
    patronymic = models.CharField(max_length=30, verbose_name='Отчество', default='Отчество')
    data_joined = models.DateTimeField(auto_now_add=True, verbose_name='Дата регистрации')
    last_login = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    objects = MyAccountManager()

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True


class Division(models.Model):
    name = models.CharField(max_length=20, null=True, verbose_name='Название')

    def __str__(self):
        return self.name


class ClubsLib(models.Model):
    name = models.CharField(max_length=20, null=True, verbose_name='Название')
    division = models.ForeignKey(Division, on_delete=models.CASCADE, verbose_name='Дивизион')

    def __str__(self):
        return self.name


class ClubsTable(models.Model):
    name = models.OneToOneField(ClubsLib, on_delete=models.CASCADE, verbose_name='Название')
    fio = models.CharField(max_length=50, null=True, verbose_name='ФИО тренера')
    year = models.IntegerField(validators=[validate_year], null=True, verbose_name='Год основания')
    photo = models.ImageField(upload_to='images/', null=True, blank=True, verbose_name='Фото')

    def __str__(self):
        return self.fio


class ForwardsTable(models.Model):
    last_name = models.CharField(max_length=50, null=True, verbose_name='Фамилия', unique=True)
    club = models.ForeignKey(ClubsLib, on_delete=models.CASCADE, verbose_name='Клуб')
    pucks = models.PositiveIntegerField(null=True, verbose_name='Число заброшенных шайб')
    setups = models.PositiveIntegerField(null=True, verbose_name='Количество голевых передач')
    penalty = models.DurationField(null=True, verbose_name='Штрафное время')

    def __str__(self):
        return self.last_name


class Partner(models.Model):
    class Meta:
        # делает уникальным направление обмена
        unique_together = ("last_name", "partner")
    last_name = models.ForeignKey(ForwardsTable, on_delete=models.CASCADE, verbose_name='Фамилия', related_name='forward')
    partner = models.ForeignKey(ForwardsTable, on_delete=models.CASCADE, verbose_name='Партнёр', related_name='partner')
