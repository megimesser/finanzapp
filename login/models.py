from django.db import models
from django.utils import timezone

# Singular ist besser für Models!
class Logs(models.Model):
    Username = models.CharField(max_length=100)
    zeitpunkt_ausgabe = models.DateTimeField(auto_now_add=True)  # Automatisch setzen!
       
    def __str__(self):
        return f"{self.Username} - {self.zeitpunkt_ausgabe}€"
    
   