from django.contrib import admin
from .models import (Ticket, Department, Management, Ticket_Actions,
Job_Titles, Profile, Subscribe, Response, Description)

# Register your models here.
admin.site.register(Ticket)
admin.site.register(Management)
admin.site.register(Department)
admin.site.register(Profile)
admin.site.register(Ticket_Actions)
admin.site.register(Job_Titles)
admin.site.register(Subscribe)
admin.site.register(Response)
admin.site.register(Description)