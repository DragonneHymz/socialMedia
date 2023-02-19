from django.contrib import admin
from .models import follower, profile, post, like
# Register your models here.
admin.site.register(profile)
admin.site.register(post)
admin.site.register(like)
admin.site.register(follower)