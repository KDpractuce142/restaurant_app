from django.db import models
from django.contrib.auth.models import User

class Food(models.Model):
    name = models.CharField(max_length=255, verbose_name='Назва страви')
    weight = models.IntegerField(blank=True, verbose_name='Вага')
    description = models.TextField(blank=True, verbose_name='Опис страви')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Ціна')
    image = models.ImageField(upload_to='media/', blank=True, null=True, verbose_name='Зображення страви')
    STATUS_CHOICES = [('other', 'Інше'),
        ('hot_dishe', 'Гарячі страви'),
        ('non_alc_drink', 'Без акогольні напої'),
        ('long_alc_drink', 'Лонги'),
        ('short_alc_drink', 'Шоти'),
        ('salat', 'Салати'),
        ('side_dish', 'Гарніри')]
    
    category = models.CharField(choices=STATUS_CHOICES, max_length=255, default = 'other', verbose_name='Категорія')

    class Meta:
        verbose_name = 'Страва'
        verbose_name_plural = 'Страви'

    def __str__(self):
        return self.name


class Basket(models.Model):
    food = models.ForeignKey(Food, on_delete=models.CASCADE, verbose_name='Страви')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Володар')
    def __str__(self):
        return self.user.username


class Order(models.Model):
    basket = models.ForeignKey(Basket, on_delete=models.CASCADE, verbose_name='Кошик')
    deliver_time = models.DateTimeField(verbose_name='Доставити до')
    adress = models.CharField(max_length=255, verbose_name='Адреса')
    def __str__(self):
        return self.deliver_time + self.basket.user.username
    

