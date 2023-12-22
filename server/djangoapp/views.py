from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from .models import CarModel
from .restapis import get_dealers_from_cf, get_dealer_reviews_from_cf, get_dealer_by_id_from_cf, post_request
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json
from django.db import models
from django.core import serializers
from django.utils.timezone import now
import uuid

# Get an instance of a logger
logger = logging.getLogger(__name__)

def about(request):
    if request.method == "GET":
        return render(request, 'djangoapp/about.html')


def contact(request):
    if request.method == "GET":
        return render(request, 'djangoapp/contact.html')


def login_request(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['psw']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Login successfully!")
            return redirect('djangoapp:index')
        else:
            messages.warning(request, "Invalid username or password.")
            return redirect("djangoapp:index")
    return redirect("djangoapp:index")


def logout_request(request):
    logger.info(f"Logout the user: {request.user.username}")
    logout(request)
    messages.success(request, "Logout successful!")
    return redirect("djangoapp:index")


def registration_request(request):
    context = {}
    if request.method == 'GET':
        return render(request, 'djangoapp/registration.html', context)
    elif request.method == 'POST':
        # Check if user exists
        username = request.POST['username']
        password = request.POST['password']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        user_exist = False
        try:
            User.objects.get(username=username)
            user_exist = True
        except:
            logger.error("New user registered successfully")
        if not user_exist:
            user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name,
                                            password=password)
            user.is_superuser = True
            user.is_staff = True
            user.save()
            login(request, user)
            messages.success(request, "User registered successfully!")
            return redirect("djangoapp:index")
        else:
            messages.warning(request, "The user already exists.")
            return redirect("djangoapp:register")


def get_dealerships(request):
    if request.method == "GET":
        # local lab
        # url = "http://127.0.0.1:3000/dealerships/get"
        # online lab
        url = "https://igabi-3000.theiadockernext-0-labs-prod-theiak8s-4-tor01.proxy.cognitiveclass.ai/dealerships/get"
        dealerships = get_dealers_from_cf(url)

        context = {}
        # context["dealerships"] = dealerships
        context = {"dealership_list": dealerships}
        return render(request, 'djangoapp/index.html', context)


def get_dealer_details(request, dealer_id):
    if request.method == "GET":
        context = {}
        # local lab
        # dealer_url = "http://127.0.0.1:3000/dealerships/get"
        # online lab
        dealer_url = "https://igabi-3000.theiadockernext-0-labs-prod-theiak8s-4-tor01.proxy.cognitiveclass.ai/dealerships/get"
        dealer = get_dealer_by_id_from_cf(dealer_url, dealer_id)
        context['dealer'] = dealer
        # context = {"dealer": dealer}

        # local lab
        review_url = "http://127.0.0.1:5000/api/get_reviews"
        # online-lab
        review_url = "https://igabi-5000.theiadockernext-0-labs-prod-theiak8s-4-tor01.proxy.cognitiveclass.ai/api/get_reviews"
        reviews = get_dealer_reviews_from_cf(review_url, dealer_id)
        for review in reviews:
            print("sentiment", review.sentiment)
        print("REVIEWS:", reviews)
        context['reviews'] = reviews
        # context = {"reviews": reviews}

        logger.info('Dealer ID: ' + str(dealer.id))
        return render(request, 'djangoapp/dealer_details.html', context)

def add_review(request, dealer_id):
    context = {}
    # local lab
    # url = "http://127.0.0.1:3000/dealerships/get"
    # online lab
    url = "https://igabi-3000.theiadockernext-0-labs-prod-theiak8s-4-tor01.proxy.cognitiveclass.ai/dealerships/get"
    dealer = get_dealer_by_id_from_cf(url, dealer_id)
    context["dealer"] = dealer

    if request.method == 'GET':
        cars = CarModel.objects.all()
        print(cars)
        context["cars"] = cars
        return render(request, 'djangoapp/add_review.html', context)

    elif request.method == 'POST':
        if request.user.is_authenticated:
            username = request.user.username
            print(request.POST)
            payload = dict()
            car_id = request.POST["car"]
            car = CarModel.objects.get(pk=car_id)
            payload["time"] = datetime.utcnow().isoformat()
            payload["name"] = username
            payload["dealership"] = dealer_id
            payload["id"] = dealer_id
            payload["review"] = request.POST["content"]
            payload["purchase"] = False
            if "purchasecheck" in request.POST:
                if request.POST["purchasecheck"] == 'on':
                    payload["purchase"] = True
            payload["purchase_date"] = request.POST["purchasedate"]
            payload["car_make"] = car.make.name
            payload["car_model"] = car.name
            payload["car_year"] = int(car.year.strftime("%Y"))
            new_payload = {}
            new_payload["review"] = payload
            # local lab
            # review_post_url = "http://127.0.0.1:5000/api/post_review"
            # online lab
            review_post_url = "https://igabi-5000.theiadockernext-0-labs-prod-theiak8s-4-tor01.proxy.cognitiveclass.ai/api/post_review"
            review = {
                "id": dealer_id,
                "time": datetime.utcnow().isoformat(),
                "name": request.user.username,
                "dealership": dealer_id,
                "review": request.POST["content"],
                "purchase": True, 
                "purchase_date": request.POST["purchasedate"],
                "car_make": car.make.name,
                "car_model": car.name,
                "car_year": int(car.year.strftime("%Y")),
            }
            review = json.dumps(review, default=str)
            new_payload1 = {}
            new_payload1["review"] = review
            print("\nREVIEW:", review)
            post_request(review_post_url, review, dealer_id=dealer_id)
        return redirect("djangoapp:dealer_details", dealer_id=dealer_id)