from django.contrib import admin
from django.utils.safestring import mark_safe

from bot.models import Shoes, Size, SizeQuantity


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


# admin.site.register(Size)

# @admin.register(Size)
# class SizeAdmin(admin.ModelAdmin):
# 	ordering = ('size', )







