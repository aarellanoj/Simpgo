from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.urls import reverse
from django.core.exceptions import PermissionDenied
from django.contrib.auth.models import User

from simpgo_app.forms import UserForm, ProfileForm, TicketForm, ResponseForm

from simpgo_app.models import Ticket, Response, Profile, Department, Job_Titles, Rank

#Others Functions
def is_myticket(user,ticket):
    if user.is_superuser or user.is_staff or user.id == ticket.created_by.id:
        return True
    else:
        return False

def user_was_created():
    user_without_profile = [x for x in User.objects.all() if(not hasattr(x,'profile'))]

# Create your views here.
def index(request):
    users_w = [x for x in User.objects.all() if(not hasattr(x,'profile'))]
    return render(request,'simpgo_app/index.html',{'users_w':users_w})

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username,password=password)
        if user:
            if user.is_active:
                if hasattr(user,'profile'):
                    login(request,user)
                    return HttpResponseRedirect(reverse('index'))
                else:
                    return HttpResponse("Su Perfil Aun no ha sido creado.")
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
        if user_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            registered = True
        else:
            print(user_form.errors)
    else:
        user_form = UserForm()
    return render(request,'simpgo_app/registration.html',
                          {'user_form':user_form,
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
            ticket._assign_priority()
            ticket._assign_ticket()
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

        if request.POST.get('response') is not None:
            response_form = ResponseForm(data=request.POST)
            if response_form.is_valid():
                response = response_form.save(commit=False)
                response.user = request.user
                response.ticket = ticket
                response.save() #Guardamos la Respuesta
                response_form = ResponseForm(use_required_attribute=False) #Limpiamos el Formulario

        if request.POST.get('comment/close') is not None:
            ticket._change_status_to(3)

        if request.POST.get('change') is not None:
            value = int(request.POST.get('status'))
            if value in [1,2,3,4]:
                ticket._change_status_to(value)

        return HttpResponseRedirect('./')

    else:
        response_form = ResponseForm(use_required_attribute=False)

    return render(request, 'simpgo_app/ticket_view.html',
                            {'ticket':ticket,
                            'responses': responses,
                            'response_form':response_form,})
    
@login_required
def my_tickets(request):

    tickets = list(Ticket.objects.filter(created_by=request.user.id,status__in=[1],deleted=0))
    tickets_pro = list(Ticket.objects.filter(created_by=request.user.id,status__in=[3],deleted=0))

    if request.method == 'POST':

        if request.POST.get('seeall') is not None:
            all_tickets = list(Ticket.objects.filter(created_by=request.user.id))
            return render(request, 'simpgo_app/my_tickets.html', {'all_tickets':all_tickets,})

        if request.POST.get('ticket_id') is not None:
            for ids in request.POST.getlist('ticket_id'):
                Ticket.objects.get(id=ids)._remove()
        else:
            for ids in request.POST.getlist('ticket_id2'):
                Ticket.objects.get(id=ids)._remove()

        return HttpResponseRedirect('./')

    return render(request, 'simpgo_app/my_tickets.html', {'tickets':tickets, 'tickets_pro':tickets_pro})

@login_required
def account(request,user_id):
    account = get_object_or_404(User,pk=user_id)

    if request.method == 'POST':
        print(request.POST)

        verify = account.check_password(request.POST['password'])
        if request.user == account and verify:
            if request.POST.get('email') is not None:
                account.email = request.POST.get('email')
                account.save()
        elif request.user.is_staff:
            if request.POST.get('email') is not None:
                account.email = request.POST.get('email')
                account.save()

        if not hasattr(account,'profile'):
            profile_form = ProfileForm(data=request.POST)
            if profile_form.is_valid():
                profile = profile_form.save(commit=False)
                profile.user = account
                profile.save()
        else:
            if request.POST.get('department') is not None:
                account.profile.department = get_object_or_404(Department,
                                            pk=request.POST.get('department'))
                account.profile.save()

            if request.POST.get('job_title') is not None:
                account.profile.job_title = get_object_or_404(Job_Titles,
                                            pk=request.POST.get('job_title'))
                account.profile.save()

            if request.POST.get('rank') is not None:
                account.profile.rank = get_object_or_404(Rank,
                                        pk=request.POST.get('rank'))
                account.profile.save()

    if request.user == account or request.user.is_staff:
        user_form = UserForm(instance=account)
        if request.user.is_staff:
            print('Es Staff')
            user_form = UserForm(use_required_attribute=False,instance=account)

        if hasattr(account,'profile'):
            profile_form = ProfileForm(instance=account.profile)
        else:
            profile_form = ProfileForm()
    else:
        raise PermissionDenied()

    return render(request, 'simpgo_app/account.html', {'account':account,
                                                        'user_form':user_form,
                                                        'profile_form':profile_form })

@staff_member_required
def users(request):
    users = [x for x in User.objects.all() if(hasattr(x,'profile'))]
    user_without_profile = [x for x in User.objects.all() if(not hasattr(x,'profile'))]

    if request.method == 'POST':
        if request.POST.get('seeall') is not None:
             return render(request,'simpgo_app/users.html',{'users':user_without_profile})

    return render(request,'simpgo_app/users.html',{'users':users,
                                                   'users_w':user_without_profile})

@staff_member_required
def departments(request):
    management = Management.objects.all()
    department = Department.objects.all()
    args = {'management':management,'department':department}
    return render(request,'simpgo_app/department.html', args)
    
@staff_member_required
def all_tickets(request):
    tickets = list(Ticket.objects.filter(deleted=0))
    if request.method == 'POST':

        if request.POST.get('seeall') is not None:
            tickets = list(Ticket.objects.all())
            return render(request, 'simpgo_app/all_tickets.html', {'tickets':tickets,})

        if request.POST.get('ticket_id') is not None:

            if request.POST.get('cancel') is not None:
                for ids in request.POST.getlist('ticket_id'):
                    Ticket.objects.get(id=ids)._remove()

            if request.POST.get('change') is not None:
                value = int(request.POST.get('status'))
                if value in [1,2,3,4]:
                    for ids in request.POST.getlist('ticket_id'):
                        Ticket.objects.get(id=ids)._change_status_to(value)

        else:
            pass

        return HttpResponseRedirect('./') 

    return render(request, 'simpgo_app/all_tickets.html', {'tickets':tickets,})

