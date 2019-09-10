from django.contrib import admin
from .models import Ticket, Department, Management, Ticket_Actions, Job_Titles, Rank, Profile, Subscribe

# Register your models here.
admin.site.register(Ticket)
admin.site.register(Management)
admin.site.register(Department)
admin.site.register(Profile)
admin.site.register(Ticket_Actions)
admin.site.register(Job_Titles)
admin.site.register(Rank)
admin.site.register(Subscribe)