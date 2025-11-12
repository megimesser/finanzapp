from django.shortcuts import render
from django.http import HttpResponse
from .models import Ausgabe, Kapital
from datetime import datetime
from django.db.models import Sum
import json
from kosten.models import Einnahmen_Summe, Kosten_Summe, Restwert, Einnahmen, Kosten
from decimal import Decimal





#Ausgaben hinzufügen
#Ausgaben hinzufügen
def add_cost(request):
    if request.method == 'POST':
        ausgaben_kategorie = request.POST.get('ausgaben_kategorie')
        ausgaben_höhe = request.POST.get('ausgaben_höhe')
        ausgaben_eigen = request.POST.get('ausgaben_eigen')
        ausgaben_kommentar = request.POST.get('ausgaben_kommentar')
        
        # Wenn ausgaben_höhe leer ist, nutze ausgaben_eigen
        if not ausgaben_höhe or ausgaben_höhe.strip() == '':
            ausgaben_höhe = ausgaben_eigen
        
        # Wenn ausgaben_kommentar leer ist, setze Default
        if not ausgaben_kommentar or ausgaben_kommentar.strip() == '':
            ausgaben_kommentar = "kein Kommentar"
        
        # Validierung: Mindestens eine Ausgabenhöhe muss vorhanden sein
        if not ausgaben_höhe or ausgaben_höhe.strip() == '':
            return HttpResponse(f"""
                <div class="error-message" style="color: red; padding: 10px; margin: 10px 0; background: #f8d7da; border-radius: 5px;">
                    ❌ Bitte gib eine Ausgabenhöhe an!
                </div>
            """)
        
        try:
            ausgabe = Ausgabe.objects.create(
                ausgaben_höhe=ausgaben_höhe,
                ausgaben_kategorie=ausgaben_kategorie,
                ausgaben_kommentar=ausgaben_kommentar,  # Hinzugefügt
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
def kosten_view(request):
    import json
    from django.db.models import Sum
    
    # Bestehender Code...
    kosten_summe = Kosten_Summe.objects.first()
    
    # NEU: Chart-Daten
    kategorien_daten = Kosten.objects.values('kosten_kategorie').annotate(
        summe=Sum('kosten_höhe')
    ).order_by('-summe')
    
    chart_labels = [item['kosten_kategorie'] for item in kategorien_daten]
    chart_data = [float(item['summe']) for item in kategorien_daten]
    
    context = {
        "Summe_kosten": kosten_summe.kosten_gesamt if kosten_summe else 0,
        "chart_labels": json.dumps(chart_labels),  # NEU
        "chart_data": json.dumps(chart_data),      # NEU
    }
    
    return render(request, 'kosten/kosten.html', context)


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



def index(request):
    heute = datetime.now()
    monat_name = heute.strftime("%B %Y")
    
    # Ausgaben des aktuellen Monats
    ausgaben = Ausgabe.objects.filter(
        zeitpunkt_ausgabe__month=heute.month,
        zeitpunkt_ausgabe__year=heute.year
    ).order_by('-zeitpunkt_ausgabe')
    
    # Gesamtsumme der Ausgaben
    gesamt_summe = ausgaben.aggregate(
        total=Sum('ausgaben_höhe')
    )['total'] or 0
    
    # Startkapital aus Restwert holen
    restbetrag_objekt = Restwert.objects.first()
    startkapital = restbetrag_objekt.restwert if restbetrag_objekt else Decimal('2000')
    
    # Konvertiere zu float für Berechnungen
    startkapital = float(startkapital)
    gesamt_summe = float(gesamt_summe)
    
    # Verfügbares Kapital
    kapital = startkapital - gesamt_summe
    
    # Prozentsätze berechnen
    if startkapital > 0:
        prozent_verbraucht = round((gesamt_summe / startkapital) * 100, 1)
        prozent_verfuegbar = round(100 - prozent_verbraucht, 1)
    else:
        prozent_verbraucht = 0
        prozent_verfuegbar = 100
    
    # Farbe für den Balken basierend auf Verbrauch
    if prozent_verbraucht < 50:
        bar_color = "#28a745"  # Grün
    elif prozent_verbraucht < 75:
        bar_color = "#ffc107"  # Gelb
    elif prozent_verbraucht < 90:
        bar_color = "#fd7e14"  # Orange
    else:
        bar_color = "#dc3545"  # Rot
    
    # Chart-Daten für Kategorien
    kategorien_summen = ausgaben.values('ausgaben_kategorie').annotate(
        summe=Sum('ausgaben_höhe')
    ).order_by('-summe')
    
    chart_labels = json.dumps([k['ausgaben_kategorie'] for k in kategorien_summen])
    chart_data = json.dumps([float(k['summe']) for k in kategorien_summen])
    
    context = {
        'ausgaben': ausgaben,
        'gesamt_summe': gesamt_summe,
        'monat_name': monat_name,
        'kapital': kapital,
        'startkapital': startkapital,
        'prozent_verbraucht': prozent_verbraucht,
        'prozent_verfuegbar': prozent_verfuegbar,
        'bar_color': bar_color,
        'chart_labels': chart_labels,
        'chart_data': chart_data,
    }
    
    return render(request, 'home/index.html', context)
