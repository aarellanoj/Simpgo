import django_filters as df
from django import forms

from .models import Ticket, Profile, Department

class TicketFilter(df.FilterSet):
    title = df.CharFilter(lookup_expr='icontains')
    workers = Profile.objects.filter(rank__in=[3,4])
    assigned_to = df.ModelChoiceFilter(queryset=workers)
    created_by__user__username = df.CharFilter(lookup_expr='exact',label="Nombre del Creador")
    departments = Department.objects.all()
    created_by__department = df.ModelChoiceFilter(queryset=departments)
    description__department = df.ModelChoiceFilter(queryset=departments)
    status = df.MultipleChoiceFilter(choices=Ticket.TICKET_STATUS,widget=forms.CheckboxSelectMultiple)
    deleted = df.ChoiceFilter(choices=((False,'No'),(True,'Si')))
    class Meta:
        model = Ticket
        fields = ['id', 'title', 'assigned_to', 'status', 'deleted','description']

