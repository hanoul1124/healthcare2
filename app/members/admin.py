from django.contrib import admin

# Register your models here.
from .models import *


class UserAdmin(admin.ModelAdmin):
    model = User
    list_display = ['username']

    def save_model(self, request, obj, form, change):
        super(UserAdmin, self).save_model(request, obj, form, change)
        obj.set_password(request.POST.get('password'))
        obj.save()


admin.site.register(User, UserAdmin)
admin.site.register(Profile)