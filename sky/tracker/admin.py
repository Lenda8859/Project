from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from django.urls import path
from django.utils.html import format_html
from django.shortcuts import redirect
from django.contrib import messages

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'is_active', 'is_staff', 'action_buttons')

    # Добавление кнопок для активации/деактивации пользователей
    def action_buttons(self, obj):
        if obj.is_active:
            return format_html(
                '<a class="button" href="{}">Деактивировать</a>',
                f'/admin/deactivate_user/{obj.id}/'
            )
        else:
            return format_html(
                '<a class="button" href="{}">Активировать</a>',
                f'/admin/activate_user/{obj.id}/'
            )
    action_buttons.short_description = 'Действия'
    action_buttons.allow_tags = True

    # Методы для активации/деактивации пользователя
    def activate_user(self, request, user_id):
        user = User.objects.get(pk=user_id)
        user.is_active = True
        user.save()
        self.message_user(request, f'Пользователь {user.username} активирован.')
        return redirect('/admin/auth/user/')

    def deactivate_user(self, request, user_id):
        user = User.objects.get(pk=user_id)
        user.is_active = False
        user.save()
        self.message_user(request, f'Пользователь {user.username} деактивирован.')
        return redirect('/admin/auth/user/')

    # Регистрация URL для активации/деактивации
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('activate_user/<int:user_id>/', self.admin_site.admin_view(self.activate_user)),
            path('deactivate_user/<int:user_id>/', self.admin_site.admin_view(self.deactivate_user)),
        ]
        return custom_urls + urls

# Регистрация модели пользователя с кастомным админом
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
