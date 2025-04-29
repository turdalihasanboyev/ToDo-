from django.contrib import admin
from .models import ToDo, CustomUser
from django.contrib.auth.admin import UserAdmin


admin.site.site_header = "ToDo Admin Paneli"
admin.site.site_title = "ToDo Admin Paneli"
admin.site.index_title = "ToDo Boshqaruv Paneliga Xush Kelibsiz!"


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    ordering = ('email',)
    search_fields = ('email',)
    list_display = (
        'id',
        'email',
        'is_active',
        'is_superuser',
        'is_staff',
        'last_login',
        'date_joined',
    )
    readonly_fields = (
        'id',
        'last_login',
        'date_joined',
    )
    list_filter = (
        'is_active',
        'is_superuser',
        'is_staff',
    )
    fieldsets = (
        ('Login', {
            'fields': ('email', 'password',),
            'classes': ('wide',),
        }),
        ("Permissions", {
            'fields': ('is_superuser', 'is_staff', 'is_active',),
            'classes': ('wide',),
        }),
        ("Important Dates", {
            'fields': ('date_joined', 'last_login',),
            'classes': ('wide',),
        }),
    )
    add_fieldsets = (
        ('Create Super User', {
            'fields': ('email', 'password1', 'password2',),
            'classes': ('wide',),
        }),
        ("Permissions", {
            'fields': ('is_superuser', 'is_staff',),
            'classes': ('wide',),
        }),
    )


@admin.register(ToDo)
class ToDoAdmin(admin.ModelAdmin):
    model = ToDo
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
    prepopulated_fields = {'slug': ('title',),}
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
    fieldsets = (
        ("Basic Information", {
            "fields": ("title", "sub_title", "slug", "description",),
            'classes': ('wide',),
        }),
        ("Media", {
            "fields": ("image", "video",),
            'classes': ('wide',),
        }),
        ("Status & Priority", {
            "fields": ("priority", "is_done", "is_active",),
            'classes': ('wide',),
        }),
        ("Deadline", {
            "fields": ("deadline",),
            'classes': ('wide',),
        }),
        ("Timestamps", {
            "fields": ("created_at", "updated_at",),
            'classes': ('wide',),
        }),
        ("ID", {
            "fields": ("id",),
            'classes': ('wide',),
        }),
    )