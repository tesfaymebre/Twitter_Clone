from django.contrib import admin
from django.contrib.auth.models import Group,User
from .models import Profile, Tweets

admin.site.unregister(Group)

class ProfileInline(admin.StackedInline):
    model= Profile

class UserAdmin(admin.ModelAdmin):
    modal = User
    
    fields = ["username"]
    inlines = [ProfileInline]

admin.site.unregister(User)

admin.site.register(User, UserAdmin)
admin.site.register(Tweets)
# admin.site.register(Profile)


# Register your models here.
