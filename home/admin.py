from django.contrib import admin
from .models import Ausgabe 
from kosten.models import Einnahmen, Einnahmen_Summe, Kosten, Kosten_Summe, Restwert
# Model registrieren
admin.site.register(Ausgabe)
admin.site.register(Kosten)
admin.site.register(Kosten_Summe)
admin.site.register(Einnahmen_Summe)
admin.site.register(Einnahmen)
admin.site.register(Restwert)
# Register your models here.
