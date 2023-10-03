from django.shortcuts import render

from django.http import HttpResponse

# here we write the code that is going to serve HTTP requests

# Create your views here.
from .models import HousingListing

def listings_view(request):
    all_listings = HousingListing.objects.all()
    return render(request, 'main/listings.html', {'listings': all_listings})


def index(response):
    return HttpResponse("<h1>Welcome to Houser.io</h1>")
    #the <h1> encasing is optional but allows for subheadings

def login_view(response):
    return HttpResponse("<h1>This is where muhfuckas login from YES</h1>")
    #the <h1> encasing is optional but allows for subheadings
    
def main_page(request):
    context = {
        'page_title': 'My Fancy Website',
        'main_text': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.',
        'background_color': '#f1f1f1',
    }
    return render(request, 'main_page.html', context)

def home(request):
    context = {'message': 'Hello, Django!'}
    return render(request, 'home.html', context)

