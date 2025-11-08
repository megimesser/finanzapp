from django.db import models

class Kosten(models.Model):
    kosten_kategorie = models.CharField(max_length=100)
    kosten_name = models.CharField(max_length=100)  # war CharfField
    kosten_höhe = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.kosten_höhe} - {self.kosten_name}"


class Kosten_Summe(models.Model):
    kosten_gesamt = models.DecimalField(max_digits=10, decimal_places=2, default=0)


