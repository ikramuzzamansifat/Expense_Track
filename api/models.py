from django.db import models
from datetime import date

# Create your models here.


class Expense(models.Model):
    CATEGORY_CHOICES = (
        ("food", "Food"),
        ("transportation", "Transportation"),
        ("housing", "Housing"),
        ("education", "Education"),
        ("shopping", "Shopping"),
        ("travel", "Travel"),
        ("others", "Others"),
    )

    date = models.DateField(default=date.today)
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    category = models.CharField(max_length=100, choices=CATEGORY_CHOICES)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.date} - {self.amount} - {self.category}"