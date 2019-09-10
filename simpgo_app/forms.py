from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

from .models import Profile, Ticket

#Class Forms
class UserForm(forms.ModelForm):
    class Meta():
        model = User
        fields = ('username','first_name','last_name','password','email')

        widgets = {
            'username': forms.TextInput(attrs={'class':'form-control'}),
            'first_name': forms.TextInput(attrs={'class':'form-control'}),
            'last_name': forms.TextInput(attrs={'class':'form-control'}),
            'password': forms.PasswordInput(attrs={'class':'form-control'}),
            'email': forms.EmailInput(attrs={'class':'form-control'}),
        }

        labels = {
            'username': 'Nombre de Usuario',
            'first_name': 'Nombre',
            'last_name': 'Apellido',
            'password': 'Contraseña',
            'email': 'Email',
        }

class ProfileForm(forms.ModelForm):
     class Meta():
         model = Profile
         fields = ('department','job_title','rank')

         widgets = {
            'department': forms.Select(attrs={'class':'form-control'}),
            'job_title': forms.Select(attrs={'class':'form-control'}),
            'rank': forms.Select(attrs={'class':'form-control'}),
         }

class TicketForm(forms.ModelForm):
    class Meta():
        model = Ticket
        fields = ('title','content','priority', 'image_file')

        widgets = {
            'title':forms.TextInput(attrs={'class':'form-control'}),
            'content': forms.Textarea(attrs={'class':'form-control'}),
            'priority': forms.Select(attrs={'class':'form-control'}),
        }