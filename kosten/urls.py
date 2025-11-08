from django.urls import path 
from . import views

app_name = 'kosten'
urlpatterns = [
    path('', views.kosten_view, name='kosten_view'),  # ← main_view verwenden!
    path("kosten_add/", views.kosten_add, name="kosten_add"),
    path("gesamtkosten_view/", views.gesamtkosten_view, name="gesamtkosten_view"),
]


