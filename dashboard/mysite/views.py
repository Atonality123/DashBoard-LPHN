from django.http import HttpResponse
from django.template import loader
from .models import Member


def coutMember(mymembers):
    percents = [0, 0, 0, 0]
    total = len(mymembers)

    if total == 0:
        return percents

    for member in mymembers:
        if member["status"] == "ยังไม่ได้ดำเนินการ":
            percents[0] += 1
        elif member["status"] == "ขอเสนออนุมัติ":
            percents[1] += 1
        elif member["status"] == "ระหว่างดำเนินงาน":
            percents[2] += 1
        elif member["status"] == "ดำเนินงานเสร็จแล้ว":
            percents[3] += 1

    percents = [int((x / total) * 100) for x in percents]
    return percents


def getColor(mymembers):
    for member in mymembers:
        if member["status"] == "ยังไม่ได้ดำเนินการ":
            member["color"] = "🔴"
        elif member["status"] == "ขอเสนออนุมัติ":
            member["color"] = "🟠"
        elif member["status"] == "ระหว่างดำเนินงาน":
            member["color"] = "🟡"
        elif member["status"] == "ดำเนินงานเสร็จแล้ว":
            member["color"] = "🟢"

    return mymembers


def home(request):
    mymembers = Member.objects.all().values()
    mymembers = [{"remain": x["total"] - x["withdraw"], **x} for x in mymembers]
    mymembers = getColor(mymembers)
    percent = coutMember(mymembers)
    template = loader.get_template("home.html")
    context = {"mymembers": mymembers, "percents": percent}
    return HttpResponse(template.render(context, request))
