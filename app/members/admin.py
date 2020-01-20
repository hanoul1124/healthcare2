from django.contrib import admin

# Register your models here.
from .models import *


class UserAdmin(admin.ModelAdmin):
    model = User
    change_list_template = 'admin/members/User/change_list.html'
    fields = [
        'username', 'password', 'name', 'phone_number', 'email',
        'gender', 'height', 'weight', 'renal_disease', 'hospital', 'attending_physician',
        'date_joined', 'last_login', 'is_active', 'is_superuser', 'is_staff'
    ]
    list_display = ['username']
    search_fields = ['username', 'name', 'email', 'phone_number']

    def save_model(self, request, obj, form, change):
        super(UserAdmin, self).save_model(request, obj, form, change)
        obj.set_password(request.POST.get('password'))
        obj.save()


admin.site.register(User, UserAdmin)