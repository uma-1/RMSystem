from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import PasswordResetForm
from .models import NewsletterUser, Newsletter
from upload_validator import FileTypeValidator


class VacancyForm(forms.Form):
    name = forms.CharField(required=True,
                           widget=forms.TextInput(
                               attrs={'class': 'form-control', 'placeholder': 'Enter Your Full Name'}))
    email = forms.EmailField(required=True,
                             widget=forms.EmailInput(
                                 attrs={'class': 'form-control', 'placeholder': 'Enter Your Email',
                                        'pattern': '^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
                                        }))
    phone = forms.IntegerField(required=True,
                               widget=forms.TextInput(
                                   attrs={'class': 'form-control', 'placeholder': 'Enter Your Contact Number'}))
    cv = forms.FileField(required=True,
                         validators=[FileTypeValidator(allowed_types=['application/pdf', 'application/docx'])])
    photo = forms.ImageField(required=True, help_text="Formats accepted: JPEG dnd PNG",
                             validators=[FileTypeValidator(allowed_types=['image/jpeg', 'image/png'])])

    def clean_name(self):
        cleaned_data = super(VacancyForm, self).clean()
        name = cleaned_data.get('name')
        if len(name) < 6:
            raise forms.ValidationError('Name is too short')

    def clean_phone(self):
        cleaned_data = super(VacancyForm, self).clean()
        phone = cleaned_data.get('phone')
        if len(str(phone)) < 10:
            raise forms.ValidationError('Please enter 10 digit phone number')

    def clean_photo(self):
        cleaned_data = super(VacancyForm, self).clean()
        photo = cleaned_data.get('photo')
        file_size = photo.size
        if file_size > 1048576:
            raise forms.ValidationError('Size of photo must be less than 1 mb')

    def clean_cv(self):
        cleaned_data = super(VacancyForm, self).clean()
        cv = cleaned_data.get('cv')
        file_size = cv.size
        if file_size > 1048576:
            raise forms.ValidationError('Size of file must be less than 1 mb')


class UserRegister(UserCreationForm):
    email = forms.EmailField()
    first_name = forms.CharField(max_length=255)
    last_name = forms.CharField(max_length=255)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super(UserRegister, self).__init__(*args, **kwargs)

        for fieldname in ['username', 'password1', 'password2']:
            self.fields[fieldname].help_text = None


class EmailValidationOnForgotPassword(PasswordResetForm):
    def clean_email(self):
        email = self.cleaned_data['email']
        if not User.objects.filter(email__iexact=email, is_active=True).exists():
            msg = "There is no user registered with the specified E-Mail address."
            self.add_error('email', msg)
        return email


class DestinationForm(forms.Form):
    name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Your Full Name'}))
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter Your Email',
                                       'pattern': '^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
                                       }))
    contact = forms.IntegerField(
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter Contact Number'}))
    depature = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control', 'placeholder': 'Date'}))
    person = forms.IntegerField(
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Number of person'}))
    message = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Message'}))


class Contact_Form(forms.Form):
    name = forms.CharField(required=True,
                           widget=forms.TextInput(
                               attrs={'class': 'form-control', 'placeholder': 'Enter Your Full Name'}))
    email = forms.EmailField(required=True,
                             widget=forms.EmailInput(
                                 attrs={'class': 'form-control',
                                        'placeholder': 'Enter Your Email',
                                        'pattern': '^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'}))
    phoneno = forms.CharField(required=True,
                              widget=forms.TextInput(
                                  attrs={'class': 'form-control', 'placeholder': 'Enter Your Contact'}))
    message = forms.CharField(required=True,
                              widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Message'}))



class NewsletterSignUpForm(forms.ModelForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(
        attrs={'class': 'form-control', 'placeholder': 'Enter Your Email Address',
               'pattern': '^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
               }))

    class Meta:
        model = NewsletterUser
        fields = ['email']

        def clean_email(self):
            email = self.cleaned_data.get('email')

            return email


class NewsletterCreationForm(forms.ModelForm):
    class Meta:
        model = Newsletter
        fields = ['subject', 'body', 'email', 'image', 'status']
