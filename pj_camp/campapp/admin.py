from django.contrib import admin
from .models import Member, Notice, Board, Board_Comment
# Register your models here.
admin.site.register(Member)
admin.site.register(Notice)
admin.site.register(Board)
admin.site.register(Board_Comment)