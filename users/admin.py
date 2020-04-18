from django.contrib import admin

from .models import Post,Comment


class PostAdmin(admin.ModelAdmin):
    list_display = ["post_title", "date_published"]


class CommentAdmin(admin.ModelAdmin):
    list_display = ["user", "post_title", "comment"]


admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)

