from django.urls import path

from . import views

urlpatterns = [
	path('',views.index,name='index'),
	path('login/', views.user_login, name='user_login'),
	path('register/',views.register,name='register'),
	path('my-tickets/', views.my_tickets, name='my_tickets'),
	path('all-tickets/', views.all_tickets, name='all_tickets'),
	path('create-ticket/', views.create_ticket,name='create_ticket'),
	path('ticket-view/<int:ticket_id>/', views.ticket_view, name='ticket_view'),
]