from django.http import HttpResponse
from django.template import loader
from .models import Member


def coutMember(mymembers):
    percents = [0, 0, 0, 0]

    for member in mymembers:
        if member["status"] == "ยังไม่ได้ดำเนินการ":
            percents[0] += 1
        elif member["status"] == "ขอเสนออนุมัติ":
            percents[1] += 1
        elif member["status"] == "ระหว่างดำเนินงาน":
            percents[2] += 1
        elif member["status"] == "ดำเนินงานเสร็จแล้ว":
            percents[3] += 1

    total = len(mymembers)
    percents = [int((x / total) * 100) for x in percents]

    return percents


def home(request):
    mymembers = Member.objects.all().values()
    percent = coutMember(mymembers)
    template = loader.get_template("home.html")
    context = {"mymembers": mymembers, "percents": percent}
    return HttpResponse(template.render(context, request))
