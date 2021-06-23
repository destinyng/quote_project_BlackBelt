from django.urls import path
from . import views

urlpatterns=[
    path('', views.index),
    path('users/register', views.register),
    path('users/login', views.login),
    path('quotes', views.quotes),
    path('quotes/delete/<int:quoteid>', views.delete),
    path('quotes/create', views.create),
    path('quotes/like/<int:quoteid>', views.like),
    path('users/<int:userid>', views.profile),
    path('users/update/<int:userid>', views.update),
    path('editmyaccount/<int:userid>', views.editmyaccount),
    path('logout', views.logout)
    
    
]




























