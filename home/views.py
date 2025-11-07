from django.shortcuts import render
from django.http import HttpResponse
from .models import Ausgabe

def add_cost(request):
    if request.method == 'POST':
        # Daten aus dem Formular holen
        ausgaben_kategorie = request.POST.get('ausgaben_kategorie')
        ausgaben_höhe = request.POST.get('ausgaben_höhe')
        
        # Debugging (optional)
        print(f"Kategorie: {ausgaben_kategorie}")
        print(f"Höhe: {ausgaben_höhe}")
        
        try:
            # In Datenbank speichern
            ausgabe = Ausgabe.objects.create(
                ausgaben_höhe=ausgaben_höhe,
                ausgaben_kategorie=ausgaben_kategorie,
            )
            
            # HTMX Response zurückgeben (mit KORREKTEN Variablen!)
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