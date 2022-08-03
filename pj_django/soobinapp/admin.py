from django.contrib import admin
from .models import Address, Board
from .models import Book, Author, Publisher


admin.site.register(Address)
admin.site.register(Board)
admin.site.register(Book)
admin.site.register(Author)
admin.site.register(Publisher)