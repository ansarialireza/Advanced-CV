from django.contrib import admin
from website.models import Contact,Newsletter


# @admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'budget', 'created_date')
    search_fields = ('name', 'email', 'subject', 'budget', 'created_date')
    list_filter = ('created_date',)


admin.site.register(Contact, ContactAdmin)
admin.site.register(Newsletter)
# Register your models here.
