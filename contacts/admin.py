from django.contrib import admin
from .models import Category, Contact

class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'midname', 'phone', 'email', 'createdate', 'category', 'id', 'active')
    list_display_links = ('name', 'midname')
    # list_filter = ('name', 'midname')
    list_per_page = 15
    search_fields = ('name', 'midname', 'phone')
    list_editable = ('active',)

admin.site.register(Category)
admin.site.register(Contact, ContactAdmin)
