from django.shortcuts import render , redirect
from django.http import HttpResponse
from datetime import datetime
from .models import Kosten, Kosten_Summe
from decimal import Decimal, InvalidOperation
from django.contrib import messages
from django.db.models import Sum



def kosten_view(request):
    context = {}  # ✅ Leeres Dictionary
    # ODER
    context = {
        'titel': 'Kostenübersicht',
        'daten': 'irgendwas'
    }
    
    return render(request, 'kosten/kosten.html', context)





def kosten_add(request):
    if request.method != 'POST':
        return HttpResponse("Nur POST erlaubt", status=405)
    
    kosten_kategorie = request.POST.get('kosten_kategorie')
    kosten_name = request.POST.get("kosten_name")
    kosten_höhe = request.POST.get('kosten_höhe')

    # Validierung
    if not all([kosten_kategorie, kosten_name, kosten_höhe]):
        return HttpResponse("""
            <div class="error-message" style="color: red; padding: 10px; margin: 10px 0; background: #f8d7da; border-radius: 5px;">
                ⚠️ Bitte fülle alle Felder aus!
            </div>
        """)

    try:
        kosten_höhe = Decimal(kosten_höhe)
    except (InvalidOperation, TypeError):
        return HttpResponse("""
            <div class="error-message" style="color: red; padding: 10px; margin: 10px 0; background: #f8d7da; border-radius: 5px;">
                ⚠️ Bitte gib eine gültige Zahl für die Kostenhöhe ein!
            </div>
        """)

    try:
        kosten = Kosten.objects.create(
            kosten_kategorie=kosten_kategorie,
            kosten_name=kosten_name,
            kosten_höhe=kosten_höhe,
        )
        return HttpResponse(f"""
            <div class="success-message" style="color: green; padding: 10px; margin: 10px 0; background: #d4edda; border-radius: 5px;">
                ✅ {kosten.kosten_name} in Höhe von {kosten.kosten_höhe}€ gespeichert!
            </div>
        """)
    except Exception as e:
        return HttpResponse(f"""
            <div class="error-message" style="color: red; padding: 10px; margin: 10px 0; background: #f8d7da; border-radius: 5px;">
                ❌ Fehler beim Speichern: {str(e)}
            </div>
        """)




def gesamtkosten_view(request):
    
    # Summe berechnen
    kosten_gesamt = Kosten.objects.aggregate(
        total=Sum('kosten_höhe')
    )['total'] or 0
    
    # Aktualisieren
    Kosten_Summe.objects.update_or_create(
        id=1,
        defaults={'kosten_gesamt': kosten_gesamt}
    )
    
    # Alle Kosten laden
    alle_kosten = Kosten.objects.all()
    summe = Kosten_Summe.objects.first()
    
    context = {
        'alle_kosten': alle_kosten,
        'kosten_gesamt': summe.kosten_gesamt if summe else 0
    }
    
    return render(request, 'kosten/kosten.html', context)
"""    
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




def add_profit(request): 
    if request.method == 'POST':
        kosten_kategorie = request.POST.get('kosten_kategorie')
        kosten_name = request.POST.get("kosten_name")
        kosten_höhe = request.POST.get('kosten_höhe')
        einnahme_datum = request.POST.get()
        
        
        try:
            ausgabe = Ausgabe.objects.create(
                ausgaben_höhe=ausgaben_höhe,
                ausgaben_kategorie=ausgaben_kategorie,

            )
            
            
    return HttpResponse("Nur POST erlaubt")
"""