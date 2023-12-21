import requests
import json
from requests.auth import HTTPBasicAuth
from .models import CarMake, CarModel, CarDealer, DealerReview
import logging
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_watson.natural_language_understanding_v1 import Features, SentimentOptions
import time

logger = logging.getLogger(__name__)

def get_request(url, **kwargs):
    api_key = kwargs.get("api_key")
    print("GET from {} ".format(url))
    response = None
    try:
        if api_key:
            params = dict()
            params["text"] = kwargs["text"]
            params["version"] = kwargs["version"]
            params["features"] = kwargs["features"]
            params["return_analyzed_text"] = kwargs["return_analyzed_text"]
            response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
                                    auth=HTTPBasicAuth('apikey', api_key))
        else:
            response = requests.get(url, headers={'Content-Type': 'application/json'},
                                    params=kwargs)
    except:
        print("Network exception occurred")

    if response is not None:
        status_code = response.status_code
        print("With status {} ".format(status_code))
        json_data = json.loads(response.text)
        return json_data
    else:
        print("Error: No response")
        return None


def post_request(url, payload, **kwargs):
    print(kwargs)
    print("POST to {} ".format(url))
    print(payload)
    response = requests.post(url, params=kwargs, json=payload, headers={'Content-Type': 'application/json'})
    status_code = response.status_code
    print("With status {} ".format(status_code))
    try:
        json_data = response.json()
        return json_data
    except json.JSONDecodeError:
        print("Error reading JSON")
        return None

def get_dealers_from_cf(url, **kwargs):
    results = []
    response = requests.get(url)

    if response.status_code == 200:
        try:
            dealers = response.json()
            for dealer in dealers:
                logger.info(type(dealer))
                dealer_doc = dealer
                dealer_obj = CarDealer(id=dealer_doc["id"],
                                       city=dealer_doc["city"],
                                       # state=dealer_doc["state"],
                                       st=dealer_doc["st"],
                                       address=dealer_doc["address"],
                                       zip=dealer_doc["zip"],
                                       lat=dealer_doc["lat"],
                                       long=dealer_doc["long"],
                                       short_name=dealer_doc["short_name"],
                                       full_name=dealer_doc["full_name"])
                results.append(dealer_obj)
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")

    return results

def get_dealer_by_id_from_cf(url, dealer_id):
    json_result = get_request(url, id=dealer_id)

    if json_result:
        dealers = json_result
        dealer_doc = dealers[0]
        dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"],
                               id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"], full_name=dealer_doc["full_name"],
                               st=dealer_doc["st"], zip=dealer_doc["zip"], short_name=dealer_doc["short_name"])
    return dealer_obj


def get_dealer_reviews_from_cf(url, dealer_id):
    results = []
    if id:
        json_result = get_request(url, id=dealer_id)
    else:
        json_result = get_request(url)
    
    print(json_result)
    if json_result:
        reviews = json_result
        for dealer_review in reviews:
            review_obj = DealerReview(dealership=dealer_review["dealership"],
                                      name=dealer_review["name"],
                                      purchase=dealer_review["purchase"],
                                      review=dealer_review["review"])
            if "id" in dealer_review:
                review_obj.id = dealer_review["id"]
            if "purchase_date" in dealer_review:
                review_obj.purchase_date = dealer_review["purchase_date"]
            if "car_make" in dealer_review:
                review_obj.car_make = dealer_review["car_make"]
            if "car_model" in dealer_review:
                review_obj.car_model = dealer_review["car_model"]
            if "car_year" in dealer_review:
                review_obj.car_year = dealer_review["car_year"]

            sentiment = analyze_review_sentiments(review_obj.review)
            print(sentiment)
            review_obj.sentiment = sentiment
            results.append(review_obj)

    return results


def analyze_review_sentiments(text):
    url = "https://api.eu-gb.natural-language-understanding.watson.cloud.ibm.com/instances/cfcb245e-a7f3-4875-bcbb-82de55aa6455"
    api_key = "HJIQPjEmaVnMH0LDw8xZsWCuhjFZeczyGUiJv1cOx5Bt"
    authenticator = IAMAuthenticator(api_key)
    natural_language_understanding = NaturalLanguageUnderstandingV1(
        version='2022-04-07', authenticator=authenticator)
    natural_language_understanding.set_service_url(url)
    response = natural_language_understanding.analyze(text=text+"hellohellohello", features=Features(
        sentiment=SentimentOptions(targets=[text+"hellohellohello"]))).get_result()
    label = json.dumps(response, indent=2)
    label = response['sentiment']['document']['label']

    return (label)