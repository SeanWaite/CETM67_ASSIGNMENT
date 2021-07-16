from django import forms
from django.forms import ModelForm, CheckboxSelectMultiple, EmailInput
from django.forms.models import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from datetime import datetime
from django.core.exceptions import ValidationError

# Imported all models as all required
from .models import *

# Class to display calendar for datetime fields
class DateTimeInput(forms.DateTimeInput):
    input_type = 'datetime-local'

# Class to display calendar for date fields
class DateInput(forms.DateInput):
    input_type = 'date'

# Class to add new clients, excluded fields not required at point on client creation
class AddClientForm(ModelForm):
    class Meta:
        model = Client
        exclude = ('date_inserted', 'active', 'contract_signed', 'user')

# Both inline forsets allow the forms to be displayed on the same page and linked via
# the foreign key. This meant I didn't need 3 pages to populate the customers information
AddAddressSet = inlineformset_factory(Client, Address, exclude=('effective_from_date','effective_to_date'), extra=1, can_delete=False)
AddContactSet = inlineformset_factory(Client, ContactDetails, exclude=(), extra=1, can_delete=False, widgets={'email_address': EmailInput})

# Class to add new students
class AddStudentForm(ModelForm):
    class Meta:
        model = Student
        exclude = ()
        widgets = {'parent': CheckboxSelectMultiple(),
                   'date_of_birth': DateInput()}
    
    # Validation required to not select more than 2 parents. Error returned the page if they are.
    def clean(self):
        cleaned_data = super().clean()
        parents = cleaned_data.get("parent")
        errors={}

        # if more that 2 check boxes are selected
        if len(parents) > 2:
            errors['parent'] = ValidationError("Should not select more that 2 parents")

        if errors:
            raise ValidationError(errors)

# Inline forsets allow the forms to be displayed on the same page and linked via
# the foreign key. This meant I didn't need 2 pages to populate the students information
AddStudentAddressSet = inlineformset_factory(Student, TuitionAddress, exclude=('effective_from_date','effective_to_date'), extra=1, can_delete=False)

# Class to add lessons for the students, at this point not invoice is generated so these
# fields could be hidden using HiddenInput(). Also used DateTimeInput to bring up calendar
class AddLessonForm(ModelForm):
    class Meta:
        model = Lesson
        exclude = ()
        widgets = {'lesson_start': DateTimeInput(), 
                   'lesson_end':DateTimeInput(),
                   'invoiced': forms.HiddenInput(), 
                   'invoice_number': forms.HiddenInput(),
                   'student': forms.HiddenInput()}

    # Validation required to start can't be after end datetime. Also need to ensure lesson is within
    # the selected term and that start and end dates are the same. Alot of datetime conversion 
    # required due to error below (temp work around until a better way is found):
    # "TypeError: can't compare offset-naive and offset-aware datetimes"
    def clean(self):
        cleaned_data = super().clean()
        lesson_start_str = datetime.strftime(cleaned_data.get("lesson_start"),"%Y-%m-%d %H:%M:%S")
        lesson_start_day = datetime.strftime(cleaned_data.get("lesson_start"),"%d")
        lesson_start_date = datetime.strptime(lesson_start_str,"%Y-%m-%d %H:%M:%S")
        lesson_end_str = datetime.strftime(cleaned_data.get("lesson_end"),"%Y-%m-%d %H:%M:%S")
        lesson_end_day = datetime.strftime(cleaned_data.get("lesson_end"),"%d")
        lesson_end_date = datetime.strptime(lesson_end_str,"%Y-%m-%d %H:%M:%S")

        form_term = cleaned_data.get("term")
        term = Term.objects.get(pk=form_term.pk)

        term_start_str = datetime.strftime(term.term_start_date, "%Y-%m-%d %H:%M:%S")
        term_start_mes = datetime.strftime(term.term_start_date, "%d/%m/%Y")
        term_start_date = datetime.strptime(term_start_str, "%Y-%m-%d %H:%M:%S")
        term_end_str = datetime.strftime(term.term_end_date, "%Y-%m-%d %H:%M:%S")
        term_end_mes = datetime.strftime(term.term_end_date, "%d/%m/%Y")
        term_end_date = datetime.strptime(term_end_str, "%Y-%m-%d %H:%M:%S")
        
        errors={}

        if lesson_start_date > lesson_end_date:
            errors['lesson_start'] = ValidationError("The lesson start should be before the lesson end")

        if lesson_start_day != lesson_end_day:
            errors['lesson_start'] = ValidationError("The lesson start should be same day as lesson end")

        if lesson_start_date < term_start_date:
            errors['lesson_start'] = ValidationError("The lesson start should on or after term start " +
                                                     term_start_mes)

        if lesson_end_date > term_end_date:
            errors['lesson_end'] = ValidationError("The lesson start should on or before term end " +
                                                     term_end_mes)

        if errors:
            raise ValidationError(errors)

# Class to update the lesson form is needs be
# Validation required to start can't be after end datetime
class UpdateLessonForm(ModelForm):
    class Meta:
        model = Lesson
        exclude = ()
        widgets = {'student': forms.HiddenInput()}

    # Validation required to start can't be after end datetime    
    def clean(self):
        cleaned_data = super().clean()
        lesson_start = cleaned_data.get("lesson_start")
        lesson_end = cleaned_data.get("lesson_end")
        errors={}

        if lesson_start > lesson_end:
            errors['lesson_start'] = ValidationError("The lesson start should be before the lesson end")

        if errors:
            raise ValidationError(errors)

# Class to add new products. Validation required to start can't be after end datetime
class AddProductForm(ModelForm):
    class Meta:
        model = Products
        exclude = ()
        widgets = {'effective_from_date': DateInput(),
                   'effective_to_date': DateInput()}

    # Validation required to start can't be after end datetime
    def clean(self):
        cleaned_data = super().clean()
        eff_from_date = cleaned_data.get("effective_from_date")
        eff_to_date = cleaned_data.get("effective_to_date")
        errors={}

        if eff_from_date > eff_to_date:
            errors['effective_from_date'] = ValidationError("Effective from date should be before effective to date")

        if errors:
            raise ValidationError(errors)

# Class to update products. Validation required to start can't be after end datetime
class UpdateProductForm(ModelForm):
    class Meta:
        model = Products
        exclude = ()
        widgets = {}

    # Validation required to start can't be after end datetime
    def clean(self):
        cleaned_data = super().clean()
        eff_from_date = cleaned_data.get("effective_from_date")
        eff_to_date = cleaned_data.get("effective_to_date")
        errors={}

        if eff_from_date > eff_to_date:
            errors['effective_from_date'] = ValidationError("Effective from date should be before effective to date")

        if errors:
            raise ValidationError(errors)

# Class to add new terms. Alot of Validation required on dates here
class AddTermForm(ModelForm):
    class Meta:
        model = Term
        exclude = ()
        widgets = {'term_start_date': DateInput(),
                   'term_end_date': DateInput(),
                   'half_term_start_date': DateInput(),
                   'half_term_end_date': DateInput(),}
    
    # Validation required to start can't be after end datetime on the 4 seperate date fields
    def clean(self):
        cleaned_data = super().clean()
        term_start = cleaned_data.get("term_start_date")
        term_end = cleaned_data.get("term_end_date")
        half_term_start = cleaned_data.get("half_term_start_date")
        half_term_end = cleaned_data.get("half_term_end_date")
        errors={}

        if term_start > term_end:
            errors['term_start_date'] = ValidationError("Start date should be before end date")
        
        if half_term_start > half_term_end:
            errors['half_term_start_date'] = ValidationError("Half term start date should be before half term end date")
        
        if half_term_end > term_end:
            errors['half_term_end_date'] = ValidationError("Half term end date should be before term end date")

        if term_start > half_term_start:
            errors['term_start_date'] = ValidationError("Start date should be before half term start date")

        if errors:
            raise ValidationError(errors)

# Class to update terms. Alot of Validation required on dates here
class UpdateTermForm(ModelForm):
    class Meta:
        model = Term
        exclude = ()
        widgets = {}
    
    # Validation required to start can't be after end datetime on the 4 seperate date fields
    def clean(self):
        cleaned_data = super().clean()
        term_start = cleaned_data.get("term_start_date")
        term_end = cleaned_data.get("term_end_date")
        half_term_start = cleaned_data.get("half_term_start_date")
        half_term_end = cleaned_data.get("half_term_end_date")
        errors={}

        if term_start > term_end:
            errors['term_start_date'] = ValidationError("Start date should be before end date")
        
        if half_term_start > half_term_end:
            errors['half_term_start_date'] = ValidationError("Half term start date should be before half term end date")
        
        if half_term_end > term_end:
            errors['half_term_end_date'] = ValidationError("Half term end date should be before term end date")

        if term_start > half_term_start:
            errors['term_start_date'] = ValidationError("Start date should be before half term start date")

        if errors:
            raise ValidationError(errors)

# Class to create new invoices
class CreateInvoiceForm(ModelForm):
    class Meta:
        model = Invoices
        exclude = ()
        widgets = {'client': forms.HiddenInput(),
                   'amount_paid': forms.HiddenInput(),
                   'amount_outstanding': forms.HiddenInput()}
    
    # Validation required to check the total amount greater than 0
    def clean(self):
        cleaned_data = super().clean()
        total_amount = cleaned_data.get("total_amount")
        errors={}

        if total_amount <= 0:
            errors['total_amount'] = ValidationError("Invoice total amount needs to be greater than 0")

        if errors:
            raise ValidationError(errors)

# Class to create new users. Here we wanted to be sure the user already add an email inserted by
# admin to be able to create an account. This way it should be more secure.
class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
    
    # Validation to check the email provided exists on the DB already. Also validation to ensure
    # the same email address cannot be registered twice.
    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get("email")
        check_reg_email = ContactDetails.objects.filter(email_address=email).exists()

        check_user_email = User.objects.filter(email=email).exists()

        errors={}

        if check_reg_email is False:
            errors['email'] = ValidationError("That email is not linked to a current client. " 
                                              "Please contact us if the email is correct")

        if check_user_email is True:
            errors['email'] = ValidationError("That email is already registered. "
                                              "Please contact us if you have forgotten your password")

        if errors:
            raise ValidationError(errors)

# Class to update the invoices to add status updates and amounts paid.
# Some fields set to read only so they cannot be edited such as total and invoice number
class UpdateInvoiceForm(ModelForm):
    class Meta:
        model = Invoices
        exclude = ()
        widgets = {'invoice_number': forms.TextInput(attrs={'readonly':'readonly'}),
                   'total_amount': forms.NumberInput(attrs={'readonly':'readonly'}),
                   'client': forms.HiddenInput(),
                   'amount_outstanding': forms.HiddenInput()}

    # Validation to ensure the status will match the amount being paid. The amount should also
    # be greater than 0 but less than or equal to the total amount
    def clean(self):
        cleaned_data = super().clean()
        status = cleaned_data.get("status")
        total_amount = cleaned_data.get("total_amount")
        amount_paid = cleaned_data.get("amount_paid")

        errors={}

        if amount_paid <= 0:
            errors['amount_paid'] = ValidationError("Amount paid needs to be greater than 0")

        if total_amount != amount_paid and status != 4 and amount_paid > 0 and amount_paid < total_amount:
            errors['status'] = ValidationError("Full amount not paid, status should be part paid")

        if total_amount == amount_paid and status != 5:
            errors['status'] = ValidationError("Full amount paid, status should be paid")

        if amount_paid > total_amount:
            errors['amount_paid'] = ValidationError("Amount paid should not be greater than total amount")

        if errors:
            raise ValidationError(errors)
