from django.views.generic import TemplateView
from django.urls import path 
from . import views

app_name = 'home'
urlpatterns  = [
    path('', TemplateView.as_view(template_name='home/main.html')),
    path('add-cost/', views.add_cost, name='add_cost'),

]
