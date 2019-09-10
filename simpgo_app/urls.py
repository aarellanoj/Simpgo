from django.urls import path

from . import views

urlpatterns = [
	path('',views.index,name='index'),
	path('login/', views.user_login, name='user_login'),
	path('register/',views.register,name='register'),
	path('create-ticket/', views.create_ticket,name='create_ticket'),
]