from django.urls import path

from . import views

urlpatterns = [
	path('',views.index,name='index'),
	path('login/', views.user_login, name='user_login'),
	path('register/',views.register,name='register'),
	path('my-tickets/', views.my_tickets, name='my_tickets'),
	path('my-tickets/processed/', views.my_tickets_pro, name='my_tickets_pro'),
	path('my-tickets/history/', views.my_tickets_history, name='my_tickets_history'),
	path('all-tickets/', views.all_tickets, name='all_tickets'),
	path('create-ticket/', views.create_ticket,name='create_ticket'),
	path('users/', views.users,name='users'),
	path('departments/', views.departments,name='departments'),
	path('account/<int:user_id>/', views.account, name='account'),
	path('ticket-view/<int:ticket_id>/', views.ticket_view, name='ticket_view'),
]