from django.contrib import admin
from .models import ToDo


admin.site.site_header = "ToDo Admin Paneli"
admin.site.site_title = "ToDo Admin Paneli"
admin.site.index_title = "ToDo Boshqaruv Paneliga Xush Kelibsiz!"


@admin.register(ToDo)
class ToDoAdmin(admin.ModelAdmin):
    ordering = ('-id',)
    list_display = (
        'id',
        'title',
        'sub_title',
        'priority',
        'deadline',
        'image',
        'video',
        'is_done',
        'is_active',
        'created_at',
        'updated_at',
    )
    prepopulated_fields = {
        'slug': ('title',),
    }
    readonly_fields = (
        'id',
        'created_at',
        'updated_at',
    )
    list_filter = (
        'is_active',
        'is_done',
        'priority',
    )
    search_fields = (
        'title',
        'sub_title',
        'priority',
    )