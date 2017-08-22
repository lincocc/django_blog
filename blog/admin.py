from django.contrib import admin

# Register your models here.
from blog.models import Post, Comment, Tag


class PostAdmin(admin.ModelAdmin):
    list_per_page = 30


admin.site.register(Post, PostAdmin)
admin.site.register(Comment)
admin.site.register(Tag)
