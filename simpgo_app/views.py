from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

# Create your views here.
def index(request):
	return HttpResponse("<h1>Primera Prueba</h1>")
