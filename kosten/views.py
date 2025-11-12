from django.shortcuts import render , redirect
from django.http import HttpResponse
from datetime import datetime
from .models import Kosten, Kosten_Summe, Einnahmen, Einnahmen_Summe, Restwert
from decimal import Decimal, InvalidOperation
from django.contrib import messages
from django.db.models import Sum
from django.views import View


#CBV für Löschen und Erstellen und Ändenr von neuen Kosten 
class UbersichtView(View):
    
    def get(self, request):
        # Alle Kosten (Liste)
        kosten = Kosten.objects.all()
        
        # Ein einzelnes Objekt (das letzte)
        kosten_einzeln = Kosten.objects.last()
        
        # ✅ RICHTIG: Felder vom EINZELNEN Objekt
        if kosten_einzeln:  # ✅ KORRIGIERT: kosten_einzeln statt kosten prüfen!
            kosten_höhe = kosten_einzeln.kosten_höhe
            kosten_kategorie = kosten_einzeln.kosten_kategorie
            kosten_name = kosten_einzeln.kosten_name
        else:
            kosten_höhe = 0
            kosten_kategorie = ""
            kosten_name = ""
        
        return render(request, 'ubersicht/ubersicht.html', {
            'kosten': kosten,                        # Alle Kosten (Liste)
            'kosten_höhe': kosten_höhe,              # Höhe vom letzten
            'kosten_kategorie': kosten_kategorie,    # Kategorie vom letzten
            'kosten_name': kosten_name,              # Name vom letzten
        })

    def post(self, request):
        # Zeile 1: Holt den Wert des 'action' Feldes aus dem POST-Request
        # Das ist ein verstecktes Feld im HTML-Formular: <input name="action" value="eintrag_loschen">
        action = request.POST.get('action')

        # Zeile 2: Prüft, ob die action "eintrag_loschen" ist
        # Wenn ja, wird der Code im if-Block ausgeführt
        if action == "eintrag_loschen":
            
            # Zeile 3: Holt die Primary Key (ID) des zu löschenden Eintrags
            # Das kommt aus einem versteckten Feld: <input name="pk" value="5">
            pk = request.POST.get('pk')
            
            # Zeile 4: Sucht das Kosten-Objekt mit dieser ID und löscht es
            # filter(pk=pk) findet alle Objekte mit dieser ID (normalerweise nur eins)
            # .delete() löscht sie aus der Datenbank
            Kosten.objects.filter(pk=pk).delete()
            
            # Zeile 5: Leitet den User zurück zur Übersicht
            # PROBLEM: 'kosten:uberblick' existiert nicht in deinen URLs!
            # ✅ KORRIGIERT zu 'kosten:ubersicht'
            return redirect('kosten:ubersicht')
        
        # Zeile 6: Falls keine Action matched, zeige die GET-Seite nochmal
        # Besser: Rufe einfach self.get() auf
        return self.get(request)

    

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