from django.contrib import admin

# Register your models here.
from blog.models import Post, Comment


class PostAdmin(admin.ModelAdmin):
    list_per_page = 30


admin.site.register(Post, PostAdmin)
admin.site.register(Comment)