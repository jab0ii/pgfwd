from django.contrib import admin
from users.models import UserData, ContactMethodData

admin.site.register(UserData)
admin.site.register(ContactMethodData)