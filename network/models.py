from django.db import models
from django.core.validators import MinValueValidator
# from django.contrib.auth.models import User
from django.conf import settings
from django.db import models

class Contact(models.Model):
    email = models.EmailField(verbose_name='Email')
    country = models.CharField(max_length=100, verbose_name='Страна')
    city = models.CharField(max_length=100, verbose_name='Город')
    street = models.CharField(max_length=100, verbose_name='Улица')
    house_number = models.CharField(max_length=10, verbose_name='Номер дома')

    class Meta:
        verbose_name = 'Контакт'
        verbose_name_plural = 'Контакты'

    def __str__(self):
        return f"{self.country}, {self.city}, {self.street}, {self.house_number}"

class Product(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название')
    model = models.CharField(max_length=100, verbose_name='Модель')
    release_date = models.DateField(verbose_name='Дата выхода на рынок')

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'

    def __str__(self):
        return f"{self.name} {self.model}"

class NetworkNode(models.Model):
    LEVEL_CHOICES = [
        (0, 'Завод'),
        (1, 'Розничная сеть'),
        (2, 'Индивидуальный предприниматель'),
    ]

    name = models.CharField(max_length=100, verbose_name='Название')
    level = models.IntegerField(choices=LEVEL_CHOICES, verbose_name='Уровень сети')
    contact = models.OneToOneField(Contact, on_delete=models.CASCADE, verbose_name='Контакты')
    products = models.ManyToManyField(Product, verbose_name='Продукты')
    supplier = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True,
                               verbose_name='Поставщик')
    debt = models.DecimalField(max_digits=10, decimal_places=2, default=0,
                              validators=[MinValueValidator(0)],
                              verbose_name='Задолженность перед поставщиком')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')
    # employees = models.ManyToManyField(User, verbose_name='Сотрудники')
    employees = models.ManyToManyField(settings.AUTH_USER_MODEL, verbose_name='employees')

    class Meta:
        verbose_name = 'Звено сети'
        verbose_name_plural = 'Звенья сети'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.get_level_display()}: {self.name}"
