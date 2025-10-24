from django.contrib import admin
from django.utils.html import format_html
from adminsortable2.admin import SortableTabularInline, SortableAdminBase
from .models import Place, Image


class ImageInline(SortableTabularInline):
    model = Image
    extra = 0
    sortable_field_name = "sort_order"

    exclude = ('sort_order',)

    fields = ('image', 'preview',)
    readonly_fields = ('preview',)

    def preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 200px; max-width: 200px;" />', obj.image.url)
        return 'Нет фото'


@admin.register(Place)
class PlaceAdmin(SortableAdminBase, admin.ModelAdmin):
    list_display = ('title',)
    inlines = [
        ImageInline,
    ]
