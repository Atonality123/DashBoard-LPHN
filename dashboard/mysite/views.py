from django.http import HttpResponse
from django.http import JsonResponse
from django.template import loader
from .models import Member
from .utility import coutMember, getColor, fetch_data, updateDB


def finance_data(request, member_id):
    try:
        member = Member.objects.get(id=member_id)
        remain = member.total - member.withdraw

        data = {
            "total": f"{member.total:,.2f}",
            "withdraw": member.withdraw,
            "remain": remain,
        }

        response = JsonResponse(data)
        response["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response["Pragma"] = "no-cache"
        response["Expires"] = "0"

        return response

    except Member.DoesNotExist:
        return HttpResponse(status=404)


def home(request):
    (
        code_list,
        name_list,
        agency_list,
        status_list,
        total_list,
        withdraw_list,
    ) = fetch_data()

    updateDB(code_list, name_list, agency_list, status_list, total_list, withdraw_list)

    mymembers = Member.objects.all().values()
    mymembers = getColor(mymembers)
    percent = coutMember(mymembers)

    template = loader.get_template("home.html")
    context = {"mymembers": mymembers, "percents": percent}
    return HttpResponse(template.render(context, request))
