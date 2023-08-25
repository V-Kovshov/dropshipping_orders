from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


class UserTG(models.Model):
    tg_id = models.IntegerField(verbose_name='id')
    name = models.CharField(max_length=12, verbose_name="Ім'я дроппера")
    username = models.CharField(max_length=32, verbose_name="Нік в телеграмі")
    phone = models.CharField(max_length=13, verbose_name="Телефон дроппера")
    bank_card = models.CharField(max_length=20, verbose_name='Картка для виплат')
    balance = models.FloatField(verbose_name='Баланс', default=0)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'дропер'
        verbose_name_plural = 'Усі дропери'


class OrderTG(models.Model):
    SIZES_LIST = [
        ('34', 34),
        ('35', 35),
        ('36', 36),
        ('37', 37),
        ('38', 38),
        ('39', 39),
        ('40', 40),
        ('41', 41),
    ]

    user_id = models.ForeignKey(UserTG, on_delete=models.DO_NOTHING, verbose_name='Здав замовлення', null=True, blank=True)
    shoes_model = models.ForeignKey(to='Shoes', on_delete=models.DO_NOTHING, verbose_name='Модель замовлення')
    shoes_size = models.CharField(max_length=2, choices=SIZES_LIST, verbose_name='Розмір', null=True, blank=True)
    date = models.DateField(auto_now_add=True, verbose_name='Дата замовлення')
    client_name = models.CharField(max_length=64, verbose_name='ПІБ клієнта')
    client_phone = models.CharField(max_length=13, verbose_name='Телефон клієнта')
    other_data = models.TextField(verbose_name='Інші дані для відправки')
    postpayment = models.IntegerField(verbose_name='Накладний платіж', default=0)
    balance_pay = models.IntegerField(verbose_name='Аванс с балансу', default=0)
    screen_payment = models.ImageField(upload_to=f'screen_payment/{user_id}', verbose_name='Скрін оплати', null=True, blank=True)
    balance = models.FloatField(verbose_name='Баланс с замовлення', default=0.0)
    invoice = models.CharField(max_length=14, verbose_name='ТТН', null=True, blank=True)
    issued = models.BooleanField(verbose_name='Замовлення видане', default=False)

    def __str__(self):
        return f"Замовлення від {self.user_id}"

    class Meta:
        verbose_name = 'замовлення з ТГ'
        verbose_name_plural = 'Усі замовлення з ТГ'


class OrderInstagram(models.Model):
    SIZES_LIST = [
        ('34', 34),
        ('35', 35),
        ('36', 36),
        ('37', 37),
        ('38', 38),
        ('39', 39),
        ('40', 40),
        ('41', 41),
    ]

    user_instagram = models.CharField(max_length=64, verbose_name='Нік в інстаграмі')
    shoes_model = models.ForeignKey(to='Shoes', on_delete=models.DO_NOTHING, verbose_name='Модель замовлення')
    shoes_size = models.CharField(max_length=2, choices=SIZES_LIST, verbose_name='Розмір')
    date = models.DateField(auto_now_add=True, verbose_name='Дата замовлення')
    client_name = models.CharField(max_length=64, verbose_name='ПІБ клієнта')
    client_phone = models.CharField(max_length=13, verbose_name='Телефон клієнта')
    other_data = models.TextField(verbose_name='Інші дані для відправки')
    advance = models.IntegerField(verbose_name='Аванс', default=0)
    postpayment = models.IntegerField(verbose_name='Накладний платіж', default=0)
    invoice = models.CharField(max_length=14, verbose_name='ТТН', null=True, blank=True)
    issued = models.BooleanField(verbose_name='Замовлення видане', default=False)

    def __str__(self):
        return f"Замовлення від {self.user_instagram}"

    class Meta:
        verbose_name = 'замовлення з Instagram'
        verbose_name_plural = 'Усі замовлення з Instagram'


class Shoes(models.Model):
    article = models.CharField(
        max_length=70,
        verbose_name='Модель'
    )
    slug = models.SlugField(
        max_length=255,
        unique=True,
        db_index=True,
        verbose_name='URL фото'
    )
    description = models.TextField(
        verbose_name='Опис взуття'
    )
    price_opt = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        verbose_name='Ціна ОПТ'
    )
    price_outlet = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        verbose_name='Ціна РОЗДРІБ'
    )
    image = models.ImageField(
        upload_to='shoes_images',
        verbose_name='Фото',
    )

    class Meta:
        verbose_name = 'модель'
        verbose_name_plural = 'Моделі взуття'


    def __str__(self):
        return self.article


class SizeQuantity(models.Model):
    size = models.PositiveIntegerField(
        verbose_name='Розмір взуття',
        validators=[
            MinValueValidator(34),
            MaxValueValidator(41)
        ],
        default=34,
        help_text='Можна обрати розміри з 34 по 41 (включно)'
    )
    shoes = models.ForeignKey(to=Shoes, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(
        verbose_name='Наявність',
        default=0,
    )
    centimeters = models.CharField(max_length=10, verbose_name='Заміри')

    class Meta:
        verbose_name_plural = 'Розміри та їх наявність'

    def __str__(self):
        return f"{str(self.size)}({str(self.centimeters)}) - {str(self.quantity)}"
