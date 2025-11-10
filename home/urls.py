from django.urls import path 
from . import views

app_name = 'home'
urlpatterns = [
    path('', views.main_view, name='main'),  # ← main_view verwenden!
    path('add-cost/', views.add_cost, name='add_cost'),
    path('dateien/', views.dateien_nach_monat, name='dateien_nach_monat'),
    path('show_cost/', views.show_cost, name='show_cost'),

]