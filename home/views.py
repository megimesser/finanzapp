from django.shortcuts import render
from django.http import HttpResponse
from .models import Ausgabe
from datetime import datetime
from django.db.models import Sum
import json

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

    context = {
        'ausgaben': ausgaben_monatlich,
        'gesamt_summe': gesamt_summe,
        'monat': monat,
        'monat_name': monat_name,
        'jahr': jahr,
        'chart_labels': chart_labels_json,
        'chart_data': chart_data_json,
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