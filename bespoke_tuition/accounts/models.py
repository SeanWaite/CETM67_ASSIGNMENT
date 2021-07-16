from django.db import models
from django.utils import timezone
from django.utils.timezone import now
from django.core.validators import RegexValidator, validate_email
from django.contrib.auth.models import User

letters_only = RegexValidator(r'^[a-zA-Z]*$', 'Only letters are allowed.')
numbers_only = RegexValidator(r'^[0-9]*$', 'Only numbers are allowed.')

# Main client table, this is linked to the django users table for when customers
# register.
class Client(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.SET_NULL)
    forename = models.CharField(max_length=100, validators=[letters_only])
    surname = models.CharField(max_length=100, validators=[letters_only])
    date_inserted = models.DateTimeField(default=now)
    active = models.BooleanField(default=True)
    contract_signed = models.BooleanField(default=False)

    def __str__(self):
        return str(self.forename + ' ' + self.surname)

# Address table to populate client addresses and future new address which is why
# the effective from a to dates are there. The invoice can then retrieve the address
# at the time the invoice was created. Linked to client table
class Address(models.Model):
    client = models.ForeignKey(Client, related_name='address', on_delete=models.CASCADE)
    line_one = models.CharField('Address Line One', max_length=100)
    line_two = models.CharField('Address Line Two', max_length=100, null=True, blank=True)
    line_three = models.CharField('Address Line Three', max_length=100, null=True, blank=True)
    town = models.CharField('Town/City', max_length=100)
    postcode = models.CharField(max_length=10)
    effective_from_date = models.DateField(default=now)
    effective_to_date = models.DateField(null=True, blank=True)
    date_inserted = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Address Details'
        verbose_name_plural = 'Address Details'

    def __str__(self):
        return str(self.client)

# Contacts table. The email address is unique to stop multiple users registering with the same.
# Linked to client table
class ContactDetails(models.Model):
    client = models.ForeignKey(Client, related_name='contacts', on_delete=models.CASCADE)
    contact_number = models.CharField(max_length=15, validators=[numbers_only])
    email_address = models.CharField(max_length=100, validators=[validate_email], unique=True)

    class Meta:
        verbose_name = 'Contact Details'
        verbose_name_plural = 'Contact Details'

    def __str__(self):
        return str(self.client)

# Student table to hold basic student details. Many to many field for the parents as children
# can have multiple parents if they want to split the costs. And parents can have multiple children
# being taught
class Student(models.Model):
    YEAR_1 = 1
    YEAR_2 = 2
    YEAR_3 = 3
    YEAR_4 = 4
    YEAR_5 = 5
    YEAR_6 = 6
    YEAR_7 = 7
    YEAR_8 = 8
    YEAR_9 = 9
    YEAR_10 = 10
    YEAR_11 = 11
    NO_SCHOOL = 0
    SCHOOL_YEAR_CHOICES = (
        (YEAR_1, 'Year 1'),
        (YEAR_2, 'Year 2'),
        (YEAR_3, 'Year 3'),
        (YEAR_4, 'Year 4'),
        (YEAR_5, 'Year 5'),
        (YEAR_6, 'Year 6'),
        (YEAR_7, 'Year 7'),
        (YEAR_8, 'Year 8'),
        (YEAR_9, 'Year 9'),
        (YEAR_10, 'Year 10'),
        (YEAR_11, 'Year 11'),
        (NO_SCHOOL, 'No longer in school'),
    )
    parent = models.ManyToManyField(Client)
    forename = models.CharField(max_length=100, validators=[letters_only])
    surname = models.CharField(max_length=100, null=True, blank=True, validators=[letters_only])
    date_of_birth = models.DateField(null=True, blank=True)
    school_year = models.IntegerField(choices=SCHOOL_YEAR_CHOICES, default=1)
    date_inserted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.forename + ' ' + self.surname)

# Tuition address table. This doesn't actually need a effective from and too like the client address
# as we dont need to keep a record of this one. linked to student
class TuitionAddress(models.Model):
    student = models.ForeignKey(Student, related_name='address_student', on_delete=models.CASCADE)
    line_one = models.CharField('Address Line One', max_length=100)
    line_two = models.CharField('Address Line Two', max_length=100, null=True, blank=True)
    line_three = models.CharField('Address Line Three', max_length=100, null=True, blank=True)
    town = models.CharField('Town/City', max_length=100)
    postcode = models.CharField(max_length=10)
    effective_from_date = models.DateField(default=now)
    effective_to_date = models.DateField(null=True, blank=True)
    date_inserted = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Student Address'
        verbose_name_plural = 'Student Address'

    def __str__(self):
        return str(self.student)

# Products table to add new products. Important for creating bespoke products for splitting bills with 
# multiple parents.
class Products(models.Model):
    product_name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    effective_from_date = models.DateField(default=now)
    effective_to_date = models.DateField(null=True, blank=True)
    date_inserted = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'

    def __str__(self):
        return str(self.product_name)

# Term table to match the school term as tuition is only offered in term time
class Term(models.Model):
    term_name = models.CharField(max_length=100)
    term_start_date = models.DateField()
    term_end_date = models.DateField()
    half_term_start_date = models.DateField()
    half_term_end_date = models.DateField()

    def __str__(self):
        return str(self.term_name)

# Invoice table to show, total, amount paid and outstanding with status.
# Linked to client
class Invoices(models.Model):
    DRAFT = 1
    ISSUED = 2
    UNPAID = 3
    PART_PAID = 4
    PAID = 5
    STATUS_CHOICES = (
        (DRAFT,'Draft'),
        (ISSUED,'Issued'),
        (UNPAID,'Unpaid'),
        (PART_PAID,'Part paid'),
        (PAID, 'Paid'),
    )
    invoice_number = models.CharField(max_length=20, unique=True)
    client = models.ForeignKey(Client, related_name='invoices', on_delete=models.CASCADE)
    status = models.IntegerField(choices=STATUS_CHOICES, default=1)
    total_amount = models.DecimalField(max_digits=8, decimal_places=2)
    amount_paid = models.DecimalField(max_digits=8, decimal_places=2)
    amount_outstanding = models.DecimalField(max_digits=8, decimal_places=2)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.invoice_number)

# The main table that drives most functionality. Lessons need to be linked to students to show
# when the lesson will take place. Linked to products to show cost of the lesson. Linked to term
# to ensure the lesson is within that term and linked to invoice to be included in the invoice produced.
class Lesson(models.Model):
    student = models.ForeignKey(Student, null=True, related_name='lesson_student', on_delete=models.SET_NULL)
    lesson_type = models.ForeignKey(Products, related_name='lesson_link', on_delete=models.PROTECT)
    term = models.ForeignKey(Term, null=True, related_name='term', on_delete=models.SET_NULL)
    lesson_start = models.DateTimeField()
    lesson_end = models.DateTimeField()
    invoiced = models.BooleanField(default=False)
    invoice_number = models.ForeignKey(Invoices, null=True, blank=True, related_name='invoice_no', on_delete=models.SET_NULL)

    def __str__(self):
        return str(self.lesson_type)
