from django.db import models

class User(models.Model):
	energy_credit_amount = models.IntegerField()
	water_credit_amount = models.IntegerField()

