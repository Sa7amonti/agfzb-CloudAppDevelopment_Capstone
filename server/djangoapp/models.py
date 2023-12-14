from django.db import models
from django.utils.timezone import now
import datetime
from django.core.validators import MaxValueValidator, MinValueValidator

def current_year():
    return datetime.date.today().year


def max_value_current_year(value):
    return MaxValueValidator(current_year())(value)

BUILD_CHOICES = (
    ("1", "Sedan"),
    ("2", "SUV"),
    ("3", "WAGON"),
    ("4", "NONE"),
)
# Create your models here.

# <HINT> Create a Car Make model `class CarMake(models.Model)`:
# - Name
# - Description
# - Any other fields you would like to include in car make model
# - __str__ method to print a car make object
class CarMake(models.Model):
    name = models.CharField(null=False, max_length=30)
    description = models.CharField(null=False, max_length=30)
    year = models.PositiveIntegerField(default=current_year(), validators=[MinValueValidator(1927), max_value_current_year])

    def __str__(self):
        return self.name + " (" + str(self.year) + ") : " + self.description 

# <HINT> Create a Car Model model `class CarModel(models.Model):`:
# - Many-To-One relationship to Car Make model (One Car Make has many Car Models, using ForeignKey field)
# - Name
# - Dealer id, used to refer a dealer created in cloudant database
# - Type (CharField with a choices argument to provide limited choices such as Sedan, SUV, WAGON, etc.)
# - Year (DateField)
# - Any other fields you would like to include in car model
# - __str__ method to print a car make object
class CarModel(models.Model):
    CarMakes = models.ForeignKey(CarMake, null=True, on_delete=models.CASCADE)
    dealer_id = models.IntegerField()
    name = models.CharField(null=False, max_length=30)
    type = models.CharField(max_length=32, choices=BUILD_CHOICES, default='4')
    year = models.PositiveIntegerField(default=current_year(), validators=[MinValueValidator(1927), max_value_current_year])

    def __str__(self):
        return self.name + " : " + self.type + ", " + str(self.year)

# <HINT> Create a plain Python class `CarDealer` to hold dealer data


# <HINT> Create a plain Python class `DealerReview` to hold review data
