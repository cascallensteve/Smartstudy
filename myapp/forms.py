from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from .models import PlannerTask

User = get_user_model()

# Login form using email and password
class LoginForm(forms.Form):
    email = forms.EmailField(
        max_length=100,
        widget=forms.EmailInput(attrs={
            'class': 'w-full px-4 py-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-400',
            'placeholder': 'Enter your email',
        })
    )
    password = forms.CharField(
        max_length=100,
        widget=forms.PasswordInput(attrs={
            'class': 'w-full px-4 py-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-400',
            'placeholder': 'Enter your password',
        })
    )
   


# Alternative login form using phone number only
class PhoneLoginForm(forms.Form):
    phone = forms.CharField(
        max_length=15,
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'Enter your phone number',
            'type': 'tel'  # optional but recommended for phone inputs
        }),
        label='Phone Number'
    )


# User registration form extending built-in UserCreationForm with phone number
class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={
        'class': 'w-full px-4 py-2 border rounded',
        'placeholder': 'Enter your email'
    }))
    phone = forms.CharField(required=True, max_length=15, widget=forms.TextInput(attrs={
        'class': 'w-full px-4 py-2 border rounded',
        'placeholder': 'Enter your phone number',
        'type': 'tel'
    }), label='Phone Number')
    
    class Meta:
        model = User
        fields = ['username', 'email', 'phone', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': 'w-full px-4 py-2 border rounded',
            'placeholder': 'Enter your username'
        })
        self.fields['phone'].widget.attrs.update({
            'class': 'w-full px-4 py-2 border rounded',
            'placeholder': 'Enter your phone number',
            'type': 'tel'
        })
        self.fields['password1'].widget.attrs.update({
            'class': 'w-full px-4 py-2 border rounded',
            'placeholder': 'Enter password'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'w-full px-4 py-2 border rounded',
            'placeholder': 'Confirm password'
        })


# Form for pasting notes
class NoteForm(forms.Form):
    notes = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'w-full px-4 py-2 border rounded',
            'placeholder': 'Paste your notes here'
        }),
        label="Paste your notes"
    )


# Model form for PlannerTask model
class PlannerTaskForm(forms.ModelForm):
    class Meta:
        model = PlannerTask
        fields = ['title', 'description', 'date', 'is_completed']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border rounded',
                'placeholder': 'Task title'
            }),
            'description': forms.Textarea(attrs={
                'class': 'w-full px-4 py-2 border rounded',
                'placeholder': 'Task description'
            }),
            'date': forms.DateInput(attrs={
                'class': 'w-full px-4 py-2 border rounded',
                'type': 'date'
            }),
            'is_completed': forms.CheckboxInput(attrs={
                'class': 'form-checkbox'
            }),
        }



class NotesForm(forms.Form):
    notes = forms.CharField(widget=forms.Textarea(attrs={'rows':6, 'cols':60}), label="Enter your notes")  #class notes 