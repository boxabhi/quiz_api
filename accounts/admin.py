from django.contrib import admin
from .models import User,ForgetPassword , Test

admin.site.register(Test)

admin.site.register(User)
admin.site.register(ForgetPassword)