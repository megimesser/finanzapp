from django.urls import path 
from . import views

app_name = 'kosten'
urlpatterns = [
    # Kosten
    path('', views.kosten_view, name='kosten_view'),
    path('kosten_add/', views.kosten_add, name='kosten_add'),
    path('gesamtkosten_view/', views.gesamtkosten_view, name='gesamtkosten_view'),
    
    # Einnahmen
    path('einnahmen/', views.einnahmen_view, name='einnahmen_view'),  # ✅ NEU
    path('einnahmen_add/', views.einnahmen_add, name='einnahmen_add'),
]