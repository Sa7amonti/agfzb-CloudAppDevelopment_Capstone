from django.db import models
from django.utils.timezone import now


class CarMake(models.Model):
    name = models.CharField(null=False, max_length=100, default="Make")
    description = models.CharField(max_length=500)

    def __str__(self):
        return "Name: " + self.name + ", Description: " + self.description


SEDAN = "Sedan"
SUV = "SUV"
WAGON = "Wagon"
MINIVAN = "Minivan"

CAR_TYPES = [("Sedan", SEDAN), ("SUV", SUV),
             ("Wagon", WAGON), ("Minivan", MINIVAN)]


class CarModel(models.Model):
    make = models.ForeignKey(CarMake, on_delete=models.CASCADE)
    name = models.CharField(null=False, max_length=100)
    dealer_id = models.IntegerField()
    type = models.CharField(null=False, max_length=50, choices=CAR_TYPES,
                            default=SEDAN
                            )
    year = models.DateField()

    def __str__(self):
        return "Name: " + self.name + ", Type: " + self.type + ", Year: " + str(self.year)

class CarDealer:

    def __init__(self, address, city, full_name, id, lat, long, short_name, st, zip):
        self.address = address
        self.city = city
        self.full_name = full_name
        self.id = id
        self.lat = lat
        self.long = long
        self.short_name = short_name
        self.st = st
        self.zip = zip

    def __str__(self):
        return "Dealer name: " + self.full_name

class DealerReview:
    def __init__(self, dealership, name, purchase, review):
        self.dealership = dealership
        self.name = name
        self.purchase = purchase
        self.review = review
        self.purchase_date = ""
        self.purchase_make = ""
        self.purchase_model = ""
        self.purchase_year = ""
        self.sentiment = ""
        self.id = ""

    def __str__(self):
        return "Review: " + self.review + ", Sentiment: " + self.sentiment + ", Dealership: " + self.dealership + ", Purchase: " + self.purchase
