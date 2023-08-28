from django.contrib import admin
from django.utils.safestring import mark_safe

from bot.models import Shoes, SizeQuantity, UserTG, OrderTG, OrderInstagram


class SizeInline(admin.TabularInline):
	model = SizeQuantity
	extra = 0


@admin.register(Shoes)
class ShoesAdmin(admin.ModelAdmin):
	inlines = (SizeInline,)

	list_display = ('article', 'price_opt', 'price_outlet', 'get_html_photo')
	prepopulated_fields = {'slug': ('article',)}
	ordering = ('article',)
	search_fields = ('article',)
	fields = ('article', 'slug', 'description', 'image', 'get_html_photo', 'price_opt', 'price_outlet')
	readonly_fields = ('get_html_photo', )

	def get_html_photo(self, object):
		if object.image:
			return mark_safe(f"<img src='{object.image.url}' width=100>")

	get_html_photo.short_description = 'Фото моделі'


@admin.register(UserTG)
class UserTGAdmin(admin.ModelAdmin):
	list_display = ('name', 'username', 'balance')
	fields = ('tg_id', 'name', 'username', 'phone', 'bank_card', 'balance')
	readonly_fields = ('tg_id', )
	search_fields = ('name', 'username', 'phone')
	ordering = ('name', )


@admin.register(OrderTG)
class OrderTGAdmin(admin.ModelAdmin):
	list_display = ('user_id', 'date', 'shoes_model', 'balance', 'invoice', 'issued')
	search_fields = ('client_name', 'invoice', 'other_data', 'user_id__name', 'shoes_model__article')
	fields = ('user_id', 'shoes_model', 'shoes_size', 'client_name', 'client_phone', 'other_data', 'get_html_photo', 'balance_pay', 'postpayment', 'balance', 'issued', 'invoice')
	readonly_fields = ('get_html_photo', 'user_id')
	ordering = ('-date', 'user_id', 'shoes_model')

	def get_html_photo(self, object):
		if object.screen_payment:
			return mark_safe(f"<img src='{object.screen_payment}' width=100>")
		return 'Немає'

	get_html_photo.short_description = 'Скрін оплати'


@admin.register(OrderInstagram)
class OrderInstagramAdmin(admin.ModelAdmin):
	list_display = ('user_instagram', 'date', 'shoes_model', 'invoice', 'issued')
	fields = ('user_instagram', 'shoes_model', 'shoes_size', 'client_name', 'client_phone', 'other_data', 'advance', 'postpayment', 'issued', 'invoice')
	search_fields = ('client_name', 'invoice', 'other_data', 'user_instagram', 'shoes_model__article')
	ordering = ('date', 'user_instagram', 'shoes_model')
