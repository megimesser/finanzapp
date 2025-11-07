from django.db import models
from django.utils import timezone

# Singular ist besser für Models!
class Ausgabe(models.Model):
    ausgaben_höhe = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    ausgaben_kategorie = models.CharField(max_length=100)
    zeitpunkt_ausgabe = models.DateTimeField(auto_now_add=True)  # Automatisch setzen!
    
    def __str__(self):
        return f"{self.ausgaben_kategorie} - {self.ausgaben_höhe}€"
    
    class Meta:
        verbose_name = "Ausgabe"
        verbose_name_plural = "Ausgaben"  # Plural nur für Admin-Anzeige