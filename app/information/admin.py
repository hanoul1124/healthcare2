from django.contrib import admin

# Register your models here.


# Multi DB admin settings #1
from information.models import *


class OpenAPIDBModelAdmin(admin.ModelAdmin):
    using = 'open_api_db'

    def save_model(self, request, obj, form, change):
        # Tell Django to save objects to the 'other' database.
        obj.save(using=self.using)

    def delete_model(self, request, obj):
        # Tell Django to delete objects from the 'other' database
        obj.delete(using=self.using)

    def get_queryset(self, request):
        # Tell Django to look for objects on the 'other' database.
        return super().get_queryset(request).using(self.using)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        # Tell Django to populate ForeignKey widgets using a query
        # on the 'other' database.
        return super().formfield_for_foreignkey(db_field, request, using=self.using, **kwargs)

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        # Tell Django to populate ManyToMany widgets using a query
        # on the 'other' database.
        return super().formfield_for_manytomany(db_field, request, using=self.using, **kwargs)


# Multi DB admin settings #1
class OpenAPIDBTabularInline(admin.TabularInline):
    using = 'other'

    def get_queryset(self, request):
        # Tell Django to look for inline objects on the 'other' database.
        return super().get_queryset(request).using(self.using)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        # Tell Django to populate ForeignKey widgets using a query
        # on the 'other' database.
        return super().formfield_for_foreignkey(db_field, request, using=self.using, **kwargs)

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        # Tell Django to populate ManyToMany widgets using a query
        # on the 'other' database.
        return super().formfield_for_manytomany(db_field, request, using=self.using, **kwargs)


# FNI model admin
class FNIAdmin(OpenAPIDBModelAdmin):
    list_display = ['food_name', 'pk']


class HFIAdmin(OpenAPIDBModelAdmin):
    list_display = ['material_name', 'pk']


class HFCAdmin(OpenAPIDBModelAdmin):
    list_display = ['material_name', 'pk']


class HFAAdmin(OpenAPIDBModelAdmin):
    list_display = ['material_name', 'pk']

admin.site.register(FNI, FNIAdmin)
admin.site.register(HFI, HFIAdmin)
admin.site.register(HFC, HFCAdmin)
admin.site.register(HFA, HFAAdmin)