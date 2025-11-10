from django.db import models

class Kosten(models.Model):
    kosten_kategorie = models.CharField(max_length=100)
    kosten_name = models.CharField(max_length=100)  # war CharfField
    kosten_höhe = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.kosten_höhe} - {self.kosten_name}"

class Einnahmen(models.Model):
    einnahmen_kategorie = models.CharField(max_length=100)
    einnahmen_name = models.CharField(max_length=100)  # war CharfField
    einnahmen_höhe = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.einnahmen_höhe} - {self.einnahmen_name}"

class Kosten_Summe(models.Model):
    kosten_gesamt = models.DecimalField(max_digits=10, decimal_places=2, default=0)


class Einnahmen_Summe(models.Model):
    einnahmen_gesamt = models.DecimalField(max_digits=10, decimal_places=2, default=0)


class Restwert(models.Model):
    restwert  = models.DecimalField(max_digits=10, decimal_places=2, default=0)