from django.contrib import admin
from .models import *
from django_summernote.admin import SummernoteModelAdmin


class blogadmin(SummernoteModelAdmin):
    list_display = ('role', 'title', 'created_at', )
    list_filter = ('role', 'title', 'created_at', )
    search_fields = ['role', 'title', 'author', 'created_at', ]
    summernote_fields = ('text', )


admin.site.register(Post, blogadmin)
admin.site.register(Role)
admin.site.register(Replies)
