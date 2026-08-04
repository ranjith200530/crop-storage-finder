from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from accounts.models import State

def crop_listing(request):
    return render(request, "farmer/crop_listing.html", {
        "states": State.objects.all()
    })