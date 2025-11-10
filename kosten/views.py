from django.shortcuts import render , redirect
from django.http import HttpResponse
from datetime import datetime
from .models import Kosten, Kosten_Summe, Einnahmen, Einnahmen_Summe, Restwert
from decimal import Decimal, InvalidOperation
from django.contrib import messages
from django.db.models import Sum


def kosten_view(request):

    #Zugriff auf die Datenbakobjekte
    kosten_summe = Kosten_Summe.objects.first()
    einnahmen_summe = Einnahmen_Summe.objects.first()

    #Zugriff auf die Werte der Datenbankfelder
    kosten_wert = kosten_summe.kosten_gesamt if kosten_summe else Decimal('0')
    einnahmen_wert = einnahmen_summe.einnahmen_gesamt if einnahmen_summe else Decimal('0')
    
    # Jetzt kannst du rechnen
    Restbetrag = einnahmen_wert - kosten_wert

    # Speichern in der Datenbank
    Restwert.objects.update_or_create(
        id=1,
        defaults={'restwert': Restbetrag}
    )

    # ✅ RICHTIG: Restwert.objects (nicht Restbetrag.objects)
    Bugtest = Restwert.objects.first()
    print("Berechneter Restbetrag:", Restbetrag)
    print("Gespeicherter Restwert:", Bugtest.restwert if Bugtest else "Keine Daten")

    summen_context = {
        "Summe_kosten": kosten_wert,
        "Summe_einnahmen": einnahmen_wert,
        "Restbetrag": Restbetrag,
    }

    return render(request, 'kosten/kosten.html', summen_context)


#Einnahmen Hinzufügen
def einnahmen_add(request):
    if request.method != 'POST':
        return HttpResponse("Nur POST erlaubt", status=405)
    
    einnahmen_kategorie = request.POST.get('einnahmen_kategorie')
    einnahmen_name = request.POST.get("einnahmen_name")
    einnahmen_höhe = request.POST.get('einnahmen_höhe')

    # Validierung
    if not all([einnahmen_kategorie, einnahmen_name, einnahmen_höhe]):
        return HttpResponse("""
            <div class="error-message" style="color: red; padding: 10px; margin: 10px 0; background: #f8d7da; border-radius: 5px;">
                ⚠️ Bitte fülle alle Felder aus!
            </div>
        """)

    try:
        einnahmen_höhe = Decimal(einnahmen_höhe)
    except (InvalidOperation, TypeError):
        return HttpResponse("""
            <div class="error-message" style="color: red; padding: 10px; margin: 10px 0; background: #f8d7da; border-radius: 5px;">
                ⚠️ Bitte gib eine gültige Zahl für die Kostenhöhe ein!
            </div>
        """)

    try:
        einnahmen = Einnahmen.objects.create(
            einnahmen_kategorie=einnahmen_kategorie,
            einnahmen_name=einnahmen_name,
            einnahmen_höhe=einnahmen_höhe,
        )
        return HttpResponse(f"""
            <div class="success-message" style="color: green; padding: 10px; margin: 10px 0; background: #d4edda; border-radius: 5px;">
                ✅ {einnahmen.einnahmen_name} in Höhe von {einnahmen.einnahmen_höhe}€ gespeichert!
            </div>
        """)
    except Exception as e:
        return HttpResponse(f"""
            <div class="error-message" style="color: red; padding: 10px; margin: 10px 0; background: #f8d7da; border-radius: 5px;">
                ❌ Fehler beim Speichern: {str(e)}
            </div>
        """)






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
    <div class="alert alert-success alert-dismissible fade show" role="alert">
        <i class="bi bi-check-circle-fill"></i>
        <strong>Erfolgreich!</strong> {kosten.kosten_name} in Höhe von {kosten.kosten_höhe}€ gespeichert!
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    </div>
    <script>
        document.querySelector('form[hx-post*="kosten_add"]').reset();
    </script>
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
    einnahmen_summe = Einnahmen_Summe.objects.first()
    
    # Restbetrag berechnen und speichern
    einnahmen_wert = einnahmen_summe.einnahmen_gesamt if einnahmen_summe else Decimal('0')
    kosten_wert = summe.kosten_gesamt if summe else Decimal('0')
    Restbetrag = einnahmen_wert - kosten_wert
    
    # ✅ IN DATENBANK SPEICHERN
    Restwert.objects.update_or_create(
        id=1,
        defaults={'restwert': Restbetrag}
    )
    
    context = {
        'alle_kosten': alle_kosten,
        'Summe_kosten': kosten_wert,
        'Summe_einnahmen': einnahmen_wert,
        'Restbetrag': Restbetrag
    }
    
    return render(request, 'kosten/kosten.html', context)






def einnahmen_view(request):
    
    # Summe berechnen
    einnahmen_gesamt = Einnahmen.objects.aggregate(
        total=Sum('einnahmen_höhe')
    )['total'] or 0
    
    # Aktualisieren
    Einnahmen_Summe.objects.update_or_create(
        id=1,
        defaults={'einnahmen_gesamt': einnahmen_gesamt}
    )
    
    # Alle Einnahmen laden
    alle_einnahmen = Einnahmen.objects.all()
    summe = Einnahmen_Summe.objects.first()
    kosten_summe = Kosten_Summe.objects.first()
    
    # Restbetrag berechnen und speichern
    einnahmen_wert = summe.einnahmen_gesamt if summe else Decimal('0')
    kosten_wert = kosten_summe.kosten_gesamt if kosten_summe else Decimal('0')
    Restbetrag = einnahmen_wert - kosten_wert
    
    # ✅ IN DATENBANK SPEICHERN
    Restwert.objects.update_or_create(
        id=1,
        defaults={'restwert': Restbetrag}
    )
    
    context = {
        'alle_einnahmen': alle_einnahmen,
        'Summe_einnahmen': einnahmen_wert,
        'Summe_kosten': kosten_wert,
        'Restbetrag': Restbetrag
    }
    
    return render(request, 'kosten/kosten.html', context)