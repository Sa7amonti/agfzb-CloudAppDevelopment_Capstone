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
    # defining car choices
    make = models.ForeignKey(CarMake, on_delete=models.CASCADE)
    name = models.CharField(null=False, max_length=100)
    dealer_id = models.IntegerField()
    type = models.CharField(null=False, max_length=50, choices=CAR_TYPES,
                            default=SEDAN
                            )
    year = models.DateField()

    def __str__(self):
        return "Name: " + self.name + ", Type: " + self.type + ", Year: " + str(self.year)


# <HINT> Create a plain Python class `CarDealer` to hold dealer data
class CarDealer:

    def __init__(self, address, city, full_name, id, lat, long, short_name, st, zip):
        # Dealer address
        self.address = address
        # Dealer city
        self.city = city
        # Dealer Full Name
        self.full_name = full_name
        # Dealer id
        self.id = id
        # Location lat
        self.lat = lat
        # Location long
        self.long = long
        # Dealer short name
        self.short_name = short_name
        # Dealer state
        self.st = st
        # Dealer zip
        self.zip = zip

    def __str__(self):
        return "Dealer name: " + self.full_name


# <HINT> Create a plain Python class `DealerReview` to hold review data
class DealerReview:
    def __init__(self, dealership, name, purchase, review):
        # Required attributes
        self.dealership = dealership
        self.name = name
        self.purchase = purchase
        self.review = review
        # Optional attributes
        self.purchase_date = ""
        self.purchase_make = ""
        self.purchase_model = ""
        self.purchase_year = ""
        self.sentiment = ""
        self.id = ""

    def __str__(self):
        return "Review: " + self.review + ", Sentiment: " + self.sentiment + ", Dealership: " + self.dealership + ", Purchase: " + self.purchase
