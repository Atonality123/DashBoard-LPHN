from django.db import models


class Member(models.Model):
    def __str__(self):
        return f"{self.projectName} {self.agency}"

    CHOICES = [
        ("ยังไม่ได้ดำเนินการ", "ยังไม่ได้ดำเนินการ"),
        ("ขอเสนออนุมัติ", "ขอเสนออนุมัติ"),
        ("ระหว่างดำเนินงาน", "ระหว่างดำเนินงาน"),
        ("ดำเนินงานเสร็จแล้ว", "ดำเนินงานเสร็จแล้ว"),
    ]

    code = models.DecimalField(max_digits=20, decimal_places=0, null=True)
    projectName = models.CharField(max_length=255)
    agency = models.CharField(max_length=255)
    status = models.CharField(max_length=20, choices=CHOICES, null=True)
    total = models.DecimalField(max_digits=15, decimal_places=2, null=True)
    withdraw = models.DecimalField(max_digits=15, decimal_places=2, null=True)
    note = models.CharField(max_length=255, null=True, blank=True)
