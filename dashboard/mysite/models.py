from django.db import models


class Member(models.Model):
    GENDER_CHOICES = [
        ("ยังไม่ได้ดำเนินการ", "In plan"),
        ("ส่ง สจล.", "Submit Project"),
        ("ดำเนินการแล้ว", "Project finish"),
    ]

    projectName = models.CharField(max_length=255)
    agency = models.CharField(max_length=255)
    status = models.CharField(max_length=20, choices=GENDER_CHOICES, null=True)
    total = models.DecimalField(max_digits=15, decimal_places=2, null=True)
    withdraw = models.DecimalField(max_digits=15, decimal_places=2, null=True)

    def __str__(self):
        return f"{self.projectName} {self.agency}"
