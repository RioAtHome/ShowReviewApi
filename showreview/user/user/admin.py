from django.contrib import admin
from django.contrib.auth.models import User
from .models import ApiUser
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

# Register your models here.

class ApiUserInLine(admin.StackedInline):
	model = ApiUser
	can_delete = False
	verbose_name = 'Api User'

class UserAdmin(BaseUserAdmin):
	inlines = (ApiUserInLine, )

admin.site.unregister(User)
admin.site.register(User, UserAdmin)