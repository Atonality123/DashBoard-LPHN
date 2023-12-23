from django.http import HttpResponse
from django.template import loader
from .models import Member


def home(request):
    mymembers = Member.objects.all().values()
    template = loader.get_template("home.html")
    context = {"mymembers": mymembers}
    return HttpResponse(template.render(context, request))
