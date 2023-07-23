from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models



class UserTG(models.Model):
    tg_id = models.IntegerField(verbose_name='id', unique=True)
    name = models.CharField(max_length=12, verbose_name="Ім'я дроппера")
    username = models.CharField(max_length=32, verbose_name="Нік в телеграмі")
    phone = models.IntegerField(verbose_name="Телефон дроппера")
    bank_card = models.CharField(max_length=16, verbose_name='Картка для виплат')


# class OrderTG(models.Model):
#     date = models.DateField(auto_now_add=True, verbose_name='Дата замовлення')
#     payment = models.CharField(max_length=12, verbose_name='')
#     client_name = models.CharField(max_length=64)
#     data = models.TextField()  # Данные заказа
#     postpayment = models.CharField(max_length=5)
#     model = models.CharField(max_length=12)
#     manufacturer = models.CharField(max_length=32)
#     invoice = models.IntegerField()
#     user_id = models.ForeignKey(UserTG, on_delete=models.CASCADE)


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
        max_digits=4,
        decimal_places=2,
        verbose_name='Ціна ОПТ'
    )
    price_outlet = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        verbose_name='Ціна РОЗ'
    )
    image = models.ImageField(
        upload_to=f'shoes_images',
        verbose_name='Фото'
    )

    class Meta:
        verbose_name = 'модель'
        verbose_name_plural = 'Моделі взуття'


    def __str__(self):
        return f"Модель {self.article}"


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

    class Meta:
        verbose_name_plural = 'Розміри та їх наявність'

    def __str__(self):
        return f"{str(self.size)} - {str(self.quantity)}"
