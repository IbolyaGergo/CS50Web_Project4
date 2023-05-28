from django.contrib import admin
from .models import User, Post


class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username')

class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'body', 'timestamp')

# Register your models here.
admin.site.register(Post, PostAdmin)
admin.site.register(User, UserAdmin)
