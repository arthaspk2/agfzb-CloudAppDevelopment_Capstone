from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
# from .models import related models
# from .restapis import related methods
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.


# Create an `about` view to render a static about page
# def about(request):
def about(request):
    if request.method == "GET":
        return render(request, 'djangoapp/about.html')


# Create a `contact` view to return a static contact page
#def contact(request):

def contact(request):
    if request.method == "GET":
        return render(request, 'djangoapp/contact.html')

# Create a `login_request` view to handle sign in request
# def login_request(request):
def login_request(request): 
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['psw']
        user = authenticate(username=username, password=password) 
        if user is not None:
            login(request, user)
            return render(request, 'djangoapp/index.html')
        else:
            return render(request, 'djangoapp/index.html')
    else:
        return render(request, 'djangoapp/index.html')

# Create a `logout_request` view to handle sign out request
# def logout_request(request):
def logout_request(request):
    logout(request)
    print("Log out the user `{}`".format(request.user.username))
    return render(request, 'djangoapp/index.html')

# Create a `registration_request` view to handle sign up request
# def registration_request(request):
def registration_request(request):
    if request.method == 'GET':
        return render(request, 'djangoapp/registration.html')
    elif request.method == 'POST':
        username = request.POST['username']
        password = request.POST['psw']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        user_exist = False
        try:
            User.objects.get(username=username)
            user_exist = True
        except:
            print(f'{username} has registered')
        if not user_exist:
            user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name, password=password)
            login(request, user)
            return render(request, 'djangoapp/index.html')
        else:
            return render(request, 'djangoapp/index.html')

# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/index.html', context)


# Create a `get_dealer_details` view to render the reviews of a dealer
# def get_dealer_details(request, dealer_id):
def get_dealer_details(request, dealer_id):
    if request.method == "GET":
        return render(request, 'djangoapp/dealer_details.html', context={ "reviews": get_dealer_reviews_from_cf(dealer_id) })


# Create a `add_review` view to submit a review
# def add_review(request, dealer_id):
def add_review(request, dealer_id: int):
    if request.method == "GET":
        context = {
            "cars": CarModel.objects.all(),
            "dealer": get_dealers_from_cf(dealer_id)[0],
        }
        return render(request, 'djangoapp/add_review.html', context)
    elif request.method == "POST":
        form = request.POST
        review = {
            "name": f"{request.user.first_name} {request.user.last_name}",
            "dealership": dealer_id,
            "review": form["content"],
            "purchase": "true" if form.get("purchase_check") == 'on' else "false",
        }
        if form.get("purchase_check"):
            car = CarModel.objects.get(pk=form["car"])
            review["purchase_date"] = datetime.strptime(form.get("purchase_date"), "%m/%d/%Y").isoformat() 
            review["car_make"] = car.car_make.name
            review["car_model"] = car.name
            review["car_year"] = car.year.strftime("%Y")
          
        print(post_request(POST_DEALERSHIP_REVIEW_URL, review));
    
    return redirect("djangoapp:dealer_details", dealer_id=dealer_id)

