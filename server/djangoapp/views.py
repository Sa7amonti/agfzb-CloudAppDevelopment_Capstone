from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
# from .models import related models
from .models import *
# from .restapis import related methods
from .restapis import *
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
# ...
def about(request):
    if request.method == "GET":
        return render(request, 'djangoapp/about.html')


# Create a `contact` view to return a static contact page
# def contact(request):
def contact(request):
    if request.method == "GET":
        return render(request, 'djangoapp/contact.html')

# Create a `login_request` view to handle sign in request
# def login_request(request):
# ...


def login_request(request):
    # Handles POST request
    if request.method == "POST":
        # Get username and password from request.POST dictionary
        username = request.POST['username']
        password = request.POST['psw']
        # Try to check if provide credential can be authenticated
        user = authenticate(username=username, password=password)
        if user is not None:
            # If user is valid, call login method to login current user
            login(request, user)
            return redirect('djangoapp:index')
        else:
            # If not, return to login page again
            return render(request, 'djangoapp/user_login.html')
    else:
        return render(request, 'djangoapp/user_login.html')

# Create a `logout_request` view to handle sign out request
# def logout_request(request):
# ...


def logout_request(request):
    print("Log out the user `{}`".format(request.user.username))
    # Logout user in the request
    logout(request)
    return redirect('djangoapp:index')

# Create a `registration_request` view to handle sign up request
# def registration_request(request):
# ...


def registration_request(request):
    context = {}
    # If it is a GET request, just render the registration page
    if request.method == 'GET':
        return render(request, 'djangoapp/registration.html', context)
    # If it is a POST request
    elif request.method == 'POST':
        # Get user information from request.POST
        username = request.POST['username']
        password = request.POST['psw']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        user_exist = False
        try:
            # Check if user already exists
            User.objects.get(username=username)
            user_exist = True
        except:
            # If not, simply log this is a new user
            logger.debug("{} is new user".format(username))
        # If it is a new user
        if not user_exist:
            # Create user in auth_user table
            user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name,
                                            password=password)
            # Login the user and redirect to main page
            login(request, user)
            return redirect("djangoapp:index")
        else:
            return render(request, 'djangoapp/registration.html', context)

# Update the `get_dealerships` view to render the index page with a list of dealerships


def get_dealerships(request):
    context = {}
    if request.method == "GET":
        url = "http://127.0.0.1:3000/dealerships/get"
        # Get dealers from the URL
        dealerships = get_dealers_from_cf(url)
        context = {"dealership_list": dealerships}
        return render(request, 'djangoapp/index.html', context)
        # Concat all dealer's short name
        # dealer_names = ' '.join([dealer.short_name for dealer in dealerships])
        # # Return a list of dealer short name
        # return HttpResponse(dealer_names)


# Create a `get_dealer_details` view to render the reviews of a dealer
# def get_dealer_details(request, dealer_id):
# ...
def get_dealer_details(request, id):
    context = {}
    if request.method == "GET":
        dealer_url = "http://127.0.0.1:3000/dealerships/get"
        dealer = get_dealer_by_id_from_cf(dealer_url, id = id)
        context['dealer'] = dealer

        review_url = "http://127.0.0.1:5000/api/get_reviews"
        reviews = get_dealer_reviews_from_cf(review_url, id = id)
        for review in reviews:
            print("SENTIMENT", review.sentiment)
        context["reviews"] = reviews

        return render(request, 'djangoapp/dealer_details.html', context)


# Create a `add_review` view to submit a review
# def add_review(request, dealer_id):
# ...
def add_review(request, id):
    context = {}
    url = "http://127.0.0.1:3000/dealerships/get"
    dealer = get_dealer_by_id_from_cf(url, id=id)
    context["dealer"] = dealer

    if request.method == 'GET':
        cars = CarModel.objects.all()
        context["cars"] = cars
        return render(request, 'djangoapp/add_review.html', context)
    
    if request.method == 'POST':
        if request.user.is_authentocated:
            username = request.user.username
            payload = dict()
            car_id = request.POST["car"]
            car = CarModel.objects.get(pk=car_id)
            payload["time"] = datetime.utcnow.isoformat()
            payload["name"] = username
            payload["dealership"] = id
            payload["id"] = id
            payload["review"] = request.POST["content"]
            payload["purchase"] = False
            if "purchasecheck" in request.POST:
                if request.POST["purchasecheck"] == 'on':
                    payload["purchase"] = True
            payload["purchase_date"] = request.POST["purchasedate"]
            payload["car_make"] = car.carmake.name
            payload["car_model"] = car.name
            payload["car_year"] = int(car.year.strftime("%Y"))
            new_payload = {}
            new_payload["review"] = payload
            review_post_url = "http://127.0.0.1:5000/api/post_review"
            review = {
                "id": id,
                "time": datetime.utcnow().isoformat(),
                "dealership": id,
                "review": request.POST["content"],
                "purchase": True,
                "purchase_date": request.POST["purchasedate"],
                "car_make": car.carmake.name,
                "car_model": car.name,
                "car_year": int(car.year.strftime("%Y")),
            }
            review = json.dumps(review, default=str)
            new_payload_updated = {}
            new_payload_updated["review"] = review
            post_request(review_post_url, review, id=id)
        return redirect("djangoapp:dealer_details", id=id)
