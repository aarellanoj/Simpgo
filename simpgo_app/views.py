from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.urls import reverse
from django.core.exceptions import PermissionDenied

from simpgo_app.forms import UserForm, ProfileForm, TicketForm, ResponseForm

from simpgo_app.models import Ticket, Response

#Others Functions

def is_myticket(user,ticket):
    if user.is_superuser or user.is_staff or user.id == ticket.created_by.id:
        return True
    else:
        return False

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
        ticket_form = TicketForm(data=request.POST)
        if ticket_form.is_valid():
            ticket = ticket_form.save(commit=False)
            ticket.created_by = request.user
            ticket.save()
            return HttpResponseRedirect('/ticket-view/' + str(ticket.id))
    else:
        ticket_form = TicketForm()
    
    return render(request,'simpgo_app/create_ticket.html',{'ticket_form':ticket_form,})

@login_required
def ticket_view(request, ticket_id):
    ticket = get_object_or_404(Ticket, pk=ticket_id)
    responses = list(Response.objects.filter(ticket=ticket))
    if not is_myticket(request.user, ticket):
        raise PermissionDenied()

    #Verificamos el Formulario de Respuesta
    if request.method == 'POST':
        response_form = ResponseForm(data=request.POST)
        if response_form.is_valid():
            response = response_form.save(commit=False)
            response.user = request.user
            response.ticket = ticket

            response.save()
            response_form = ResponseForm() #Guardamos la Respuesta
            return HttpResponseRedirect('./') #Limpiamos el Formulario
    else:
        response_form = ResponseForm()

    return render(request, 'simpgo_app/ticket_view.html',
                            {'ticket':ticket,
                            'responses': responses,
                            'response_form':response_form,})
    
@login_required
def my_tickets(request):
    tickets = list(Ticket.objects.filter(created_by=request.user.id))
    return render(request, 'simpgo_app/my_tickets.html', {'tickets':tickets})

