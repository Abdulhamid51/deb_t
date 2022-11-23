from django.db import models
from django.contrib.auth.models import User

class Client(models.Model):
    owner = models.ForeignKey(User, related_name="client", on_delete=models.CASCADE)
    name = models.CharField(max_length=150)
    debt_mount = models.FloatField(default=0)

    def __str__(self):
        return self.name

class Debt(models.Model):
    client = models.ForeignKey(Client, related_name="debts", on_delete=models.CASCADE)
    date = models.DateField()
    mount = models.FloatField()

    def __str__(self):
        return str(self.mount)