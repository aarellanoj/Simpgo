from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from simpgo_app.forms import UserForm, ProfileForm,TicketForm

# Create your views here.
def index(request):
	return render(request,'simpgo_app/index.html')

def user_login(request):
	if request.method == 'POST':
		username = request.POST.get('username')
		password = request.POST.get('password')
		user = authenticate(username=username,password=password)
		if user:
			if user.is_active:
				login(request,user)
				return HttpResponseRedirect(reverse('index'))
			else:
				return HttpResponse("Su Cuenta Fue Desactivada.")
		else:
			return HttpResponse("¡Usuario o Clave Invalida!")
	else:
		return render(request, 'simpgo_app/login.html', {})

def register(request):
    registered = False
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = ProfileForm(data=request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            registered = True
        else:
            print(user_form.errors,profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = ProfileForm()
    return render(request,'simpgo_app/registration.html',
                          {'user_form':user_form,
                           'profile_form':profile_form,
                           'registered':registered})

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

@login_required
def create_ticket(request):
    if request.method == 'POST':
        print(request.user.id)
        type(request.user.id)
        ticket_form = TicketForm(data=request.POST)
        if ticket_form.is_valid():
            ticket = ticket_form.save(commit=False)
            ticket.created_by = request.user
            ticket.save()
    else:
        ticket_form = TicketForm()
    
    return render(request,'simpgo_app/create_ticket.html',{'ticket_form':ticket_form})