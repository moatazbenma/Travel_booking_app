from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from .models import Booking


from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(
        label="Email Address",
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Email'
        })
    )
    username = forms.CharField(
        label="Username",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Username'
        })
    )
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Password'
        })
    )
    password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirm Password'
        })
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already registered")
        return email

            


class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Username'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Password'
    }))


class UpdateProfile(forms.ModelForm):
    class Meta:
        model = User
        fields = ["username", "email"]


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['number_of_seats']
        labels = {'number_of_seats': 'Number of Seats'}
        widgets = {
            'number_of_seats': forms.NumberInput(
                attrs={'class': 'form-control form-control-lg', 'min': '1'}
            ),
        }

    def __init__(self, *args, **kwargs):
        self.travel_option = kwargs.pop('travel_option', None)  # Pass in from view
        super().__init__(*args, **kwargs)
        if self.travel_option:
            self.fields['number_of_seats'].widget.attrs['max'] = self.travel_option.available_seats

    def clean_number_of_seats(self):
        seats_requested = self.cleaned_data['number_of_seats']
        if self.travel_option and seats_requested > self.travel_option.available_seats:
            raise forms.ValidationError(f"Only {self.travel_option.available_seats} seats available.")
        return seats_requested