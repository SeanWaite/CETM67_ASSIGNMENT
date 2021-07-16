from django.contrib import admin

from .models import Client, Address, ContactDetails, Student, TuitionAddress, Products, Lesson, Invoices, Term

class AddressInline(admin.StackedInline):
    model = Address
    extra = 1

class ContactDetailsInline(admin.StackedInline):
    model = ContactDetails
    extra = 1

class ClientAdmin(admin.ModelAdmin):
    inlines = [ContactDetailsInline, AddressInline]

class TuitionAddressInline(admin.StackedInline):
    model = TuitionAddress
    extra = 1

class StudentAdmin(admin.ModelAdmin):
    inlines = [TuitionAddressInline]

admin.site.register(Client, ClientAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(Products)
admin.site.register(Lesson)
admin.site.register(Invoices)
admin.site.register(Term)