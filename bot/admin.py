from django.contrib import admin
from django.utils.safestring import mark_safe

from bot.models import Shoes, SizeQuantity, UserTG, OrderTG


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
	list_display = ('date', 'user_id', 'user_instagram', 'shoes_model', 'balance', 'invoice')
	fields = ('user_id', 'user_instagram', 'shoes_model', 'shoes_size', 'client_name', 'client_phone', 'data', 'postpayment', 'screen_payment', 'balance', 'invoice')
	search_fields = ('client_name', 'invoice', 'data')
	ordering = ('date', )

	def get_list_display(self, request):
		list_display = super().get_list_display(request)
		user_id = list_display.index('user_id')
		user_instagram = list_display.index('user_instagram')
		if request.user:
			list_display = tuple(i for i in list_display if list_display.index(i) != user_id)
		else:
			list_display = tuple(i for i in list_display if list_display.index(i) != user_instagram)
		return list_display

	def get_fields(self, request, obj=None):
		fields = super().get_fields(request)
		user_id = fields.index('user_id')
		user_instagram = fields.index('user_instagram')
		screen_payment = fields.index('screen_payment')
		shoes_size = fields.index('shoes_size')
		if request.user:
			fields = tuple(i for i in fields if fields.index(i) not in [user_id, screen_payment])
		else:
			fields = tuple(i for i in fields if fields.index(i) != [user_instagram, shoes_size])
		return fields
