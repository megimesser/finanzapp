from django.shortcuts import render
from django.http import HttpResponse
from .models import Ausgabe, Kapital
from datetime import datetime
from django.db.models import Sum
import json
from kosten.models import Einnahmen_Summe, Kosten_Summe, Restwert
from decimal import Decimal


#Ausgaben hinzufügen
def add_cost(request):
    if request.method == 'POST':
        ausgaben_kategorie = request.POST.get('ausgaben_kategorie')
        ausgaben_höhe = request.POST.get('ausgaben_höhe')
        
        try:
            ausgabe = Ausgabe.objects.create(
                ausgaben_höhe=ausgaben_höhe,
                ausgaben_kategorie=ausgaben_kategorie,
            )
            
            return HttpResponse(f"""
                <div class="success-message" style="color: green; padding: 10px; margin: 10px 0; background: #d4edda; border-radius: 5px;">
                    ✅ {ausgabe.ausgaben_kategorie} - {ausgabe.ausgaben_höhe}€ gespeichert!
                </div>
            """)
        except Exception as e:
            return HttpResponse(f"""
                <div class="error-message" style="color: red; padding: 10px; margin: 10px 0; background: #f8d7da; border-radius: 5px;">
                    ❌ Fehler beim Speichern: {str(e)}
                </div>
            """)
    
    return HttpResponse("Nur POST erlaubt")


# Berechnung für Variablen Restbetrag
# In den Mainview implementieren 
# Restbetrag wird innerhalb der Kosten.App berechnet 
"""

heute = datetime.now()
monat = heute.month
jahr = heute.year
    

ausgaben_gesamt = Ausgabe.objects.all()
ausgaben_wert_gesamt = ausgaben_gesamt.ausgaben if ausgaben_gesamt else Decumal('0')

   
ausgaben_monatlich_furberechnung = Ausgabe.objects.filter(
        zeitpunkt_ausgabe__month=monat,
    )

for ausgabe in 




for ausgaben_einzeln in ausgaben_gesamt:
    if 



restbetrag_objekt = Restwert.objects.first()
restbetrag_wert = restbetrag_objekt.restwert if restbetrag_objekt else Decimal('0')




restbetrag_variabel = resbetrag_variabel.objects.update_or_create(
        zeitpunkt_ausgabe__month=monat,
        zeitpunkt_ausgabe__year=jahr
    )




"""





#Anzeige von Ausgaben
def main_view(request):
    # Aktueller Monat und Jahr
    heute = datetime.now()
    monat = heute.month
    jahr = heute.year
    
    monate = ['Januar', 'Februar', 'März', 'April', 'Mai', 'Juni', 
              'Juli', 'August', 'September', 'Oktober', 'November', 'Dezember']
    monat_name = monate[monat - 1]
    
    # Nur Ausgaben des aktuellen Monats
    ausgaben_monatlich = Ausgabe.objects.filter(
        zeitpunkt_ausgabe__month=monat,
        zeitpunkt_ausgabe__year=jahr
    ).order_by('-zeitpunkt_ausgabe')

    # Gesamtsumme berechnen
    gesamt_summe = 0
    for ausgabe in ausgaben_monatlich: 
        print(f"Kategorie: {ausgabe.ausgaben_kategorie} - Höhe: {ausgabe.ausgaben_höhe}€")
        gesamt_summe += ausgabe.ausgaben_höhe

    print(f"Gesamtsumme für {monat}/{jahr}: {gesamt_summe}€")
    
    # Chart-Daten vorbereiten (nur für aktuellen Monat)
    kategorien_daten = ausgaben_monatlich.values('ausgaben_kategorie').annotate(
        summe=Sum('ausgaben_höhe')
    ).order_by('-summe')
    
    chart_labels = [item['ausgaben_kategorie'] for item in kategorien_daten]
    chart_data = [float(item['summe']) for item in kategorien_daten]
    
    chart_labels_json = json.dumps(chart_labels)
    chart_data_json = json.dumps(chart_data)
    # Restbetrag hinzufügen
    restbetrag_objekt = Restwert.objects.first()
    restbetrag_wert = restbetrag_objekt.restwert if restbetrag_objekt else Decimal('0')

    #Das noch frei zur Verfügung stehende Kapital 
    kapital = restbetrag_wert - gesamt_summe

    Kapital.objects.create(
        kapital = kapital,
        datum = heute,

    )

    
    context = {
        'kapital': kapital,
        'ausgaben': ausgaben_monatlich,
        'gesamt_summe': gesamt_summe,
        'monat': monat,
        'monat_name': monat_name,
        'jahr': jahr,
        'chart_labels': chart_labels_json,
        'chart_data': chart_data_json,
        'restbetrag': restbetrag_wert,  # ← NEU!
    }
    return render(request, 'home/main.html', context)

def show_cost(request):
    # Diese Funktion können Sie löschen oder für eine separate Seite verwenden
    heute = datetime.now()
    monat = heute.month
    jahr = heute.year
    
    ausgaben_monatlich = Ausgabe.objects.filter(
        zeitpunkt_ausgabe__month=monat,
        zeitpunkt_ausgabe__year=jahr
    )

    gesamt_summe = 0
    for ausgabe in ausgaben_monatlich: 
        print(f"Kategorie: {ausgabe.ausgaben_kategorie} - Höhe: {ausgabe.ausgaben_höhe}€")
        gesamt_summe += ausgabe.ausgaben_höhe
    
    print(f"Gesamtsumme für {monat}/{jahr}: {gesamt_summe}€")

    cost_context = {
        'ausgaben': ausgaben_monatlich,
        'gesamt_summe': gesamt_summe,
        'monat': monat,
        'jahr': jahr
    }
    
    return render(request, 'home/ausgaben.html', cost_context)




def dateien_nach_monat(request):
    monat_nummer = int(request.GET.get('monat', datetime.now().month))
    
    monate = ['Januar', 'Februar', 'März', 'April', 'Mai', 'Juni', 
              'Juli', 'August', 'September', 'Oktober', 'November', 'Dezember']
    
    monat_name = monate[monat_nummer - 1]

    context = {
        'monat': monat_nummer,
        'monat_name': monat_name,
    }
    return render(request, 'home/main.html', context)



