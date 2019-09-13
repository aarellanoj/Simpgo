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
            'username': forms.TextInput(attrs={'class':'input'}),
            'first_name': forms.TextInput(attrs={'class':'input'}),
            'last_name': forms.TextInput(attrs={'class':'input'}),
            'password': forms.PasswordInput(attrs={'class':'input'}),
            'email': forms.EmailInput(attrs={'class':'input'}),
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
            'department': forms.Select(),
            'job_title': forms.Select(),
            'rank': forms.Select(),
         }

class TicketForm(forms.ModelForm):
    class Meta():
        model = Ticket
        fields = ('title','content','priority', 'image_file')

        widgets = {
            'title':forms.TextInput(attrs={'class':'input','placeholder':'Asunto del Ticket'}),
            'content': forms.Textarea(attrs={'class':'textarea','placeholder':'Contenido del Ticket'}),
            'priority': forms.Select(),
            'image_file': forms.FileInput(attrs={'class':'file-input'}),
        }