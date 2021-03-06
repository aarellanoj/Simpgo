from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

from .models import Profile, Ticket, Response, Management, Department


#Class Forms
class UserForm(forms.ModelForm):    
    class Meta():
        model = User
        fields = ('username','first_name','last_name','password','email')

        widgets = {
            'username': forms.TextInput(attrs={'class':'input','required':'True','oninput':'let p = this.selectionStart; this.value = this.value.toLowerCase();this.setSelectionRange(p, p);'}),
            'first_name': forms.TextInput(attrs={'class':'input','required':'True', 'oninput':'let p = this.selectionStart; this.value = this.value.toUpperCase();this.setSelectionRange(p, p);'}),
            'last_name': forms.TextInput(attrs={'class':'input','required':'True', 'oninput':'let p = this.selectionStart; this.value = this.value.toUpperCase();this.setSelectionRange(p, p);'}),
            'password': forms.PasswordInput(attrs={'class':'input','pattern':'(?=.*\d)(?=.*[a-z]).{6,}'}),
            'email': forms.EmailInput(attrs={'class':'input','required':'True'}),
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
        fields = ('title','content','description','image_file')

        widgets = {
            'title':forms.TextInput(attrs={'class':'input','placeholder':'Asunto del Ticket'}),
            'content': forms.Textarea(attrs={'class':'textarea','placeholder':'Contenido del Ticket'}),
            'description': forms.Select(),
            'image_file': forms.FileInput(attrs={'class':'file-input'}),
        }

class ResponseForm(forms.ModelForm):
    class Meta():
        model = Response
        fields = ('response','image_file')

        widgets = {
            'response': forms.Textarea(attrs={'class':'textarea','placeholder':'Respuesta',
                                              'rows':'4'}),
            'image_file': forms.FileInput(attrs={'class':'file-input'}),
        }
        
class ManagementForm(forms.ModelForm):
    class Meta():
        model = Management
        fields = ('name',)
        
        widgets = {
            'name': forms.TextInput(attrs={'class':'input','placeholder':'Nombre de la Dirección'}),
        }
        
class DepartmentForm(forms.ModelForm):
    class Meta():
        model = Department
        fields = '__all__'
        
        widgets = {
            'name': forms.TextInput(attrs={'class':'input','placeholder':'Nombre del Departamento'}),
            'management' : forms.Select(),
            'department_chief' : forms.Select(),
        }