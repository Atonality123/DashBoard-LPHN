from django.db import models


class Member(models.Model):
    def __str__(self):
        return f"{self.projectName} {self.agency}"

    @classmethod
    def search(cls, query):
        return cls.objects.filter(projectName__contains=query).values()

    CHOICES = [
        ("ยังไม่ได้ดำเนินการ", "ยังไม่ได้ดำเนินการ"),
        ("ขอเสนอโครงการภายใน รพ.", "ขอเสนอโครงการภายใน รพ."),
        ("ไม่ผ่านการพิจารณาอนุมัติ", "ไม่ผ่านการพิจารณาอนุมัติ"),
        (
            "พิจารณาอนุมัติและดำเนินการจัดส่ง สสจ.ลำพูน",
            "พิจารณาอนุมัติและดำเนินการจัดส่ง สสจ.ลำพูน",
        ),
        ("โครงการมีการแก้ไขจาก สสจ.ลำพูน", "โครงการมีการแก้ไขจาก สสจ.ลำพูน"),
        ("พิจารณาอนุมัติจาก นพ.สสจ.ลำพูน แล้ว", "พิจารณาอนุมัติจาก นพ.สสจ.ลำพูน แล้ว"),
        ("ขออนุมัติจัดโครงการ", "ขออนุมัติจัดโครงการ"),
        ("เสนอพิจารณาอนุมัติจัดโครงการ", "เสนอพิจารณาอนุมัติจัดโครงการ"),
        ("อนุมัติจัดโครงการ", "อนุมัติจัดโครงการ"),
        ("ขออนุมัติเบิกค่าใช้จ่าย", "ขออนุมัติเบิกค่าใช้จ่าย"),
        (
            "ตรวจสอบความถูกต้องขออนุมัติเบิกค่าใช้จ่าย",
            "ตรวจสอบความถูกต้องขออนุมัติเบิกค่าใช้จ่าย",
        ),
        (
            "เสนอพิจารณาอนุมัติเบิกค่าใช้จ่ายโครงการ",
            "เสนอพิจารณาอนุมัติเบิกค่าใช้จ่ายโครงการ",
        ),
    ]

    choices = [
        ("ยังไม่ได้ดำเนินการ", "ยังไม่ได้ดำเนินการ"),
        ("ขอเสนออนุมัติ", "ขอเสนออนุมัติ"),
        ("ระหว่างดำเนินงาน", "ระหว่างดำเนินงาน"),
        ("ดำเนินงานเสร็จแล้ว", "ดำเนินงานเสร็จแล้ว"),
    ]

    code = models.CharField(max_length=255)
    projectName = models.CharField(max_length=255)
    agency = models.CharField(max_length=255)
    status = models.CharField(max_length=50, choices=CHOICES, null=True)
    detail = models.CharField(max_length=20, choices=choices, null=True)
    total = models.FloatField(null=True)
    withdraw = models.FloatField(null=True)
    note = models.CharField(max_length=255, null=True, blank=True)
