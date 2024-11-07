from django.db import models
from django.contrib.auth.models import User

class Country(models.Model):
    CONTINENT_CHOICES = [
        ("Africa", "Africa"),
        ("Asia", "Asia"),
        ("Europe", "Europe"),
        ("North America", "North America"),
        ("South America", "South America"),
        ("Antarctica", "Antarctica"),
        ("Australia", "Australia"),
    ]
    name = models.CharField(max_length=255, verbose_name="Country Name")
    continent = models.CharField(max_length=20, choices=CONTINENT_CHOICES, verbose_name="Continent")
    code = models.CharField(max_length=10, verbose_name="Country Code", unique=True)


    class Meta:
        verbose_name = "Country"
        verbose_name_plural = "Countries"

    def __str__(self):
        return self.name


class Material(models.Model):
    name = models.CharField(max_length=255, verbose_name="Material Name")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Material Price")

    class Meta:
        verbose_name = "Material"
        verbose_name_plural = "Materials"

    def __str__(self):
        return self.name


class Coin(models.Model):
    name = models.CharField(max_length=255, verbose_name="Coin Name")
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, blank=True, null=True,
                                verbose_name="Country of Origin")
    year = models.IntegerField(verbose_name="Year of Issue", null=True, blank=True)
    material = models.ManyToManyField(Material, verbose_name="Coin Material", null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Coin Price")
    imageObverse = models.ImageField(upload_to="coins/", verbose_name="Coin Obverse Image", blank=True, null=True)
    imageReverse = models.ImageField(upload_to="coins/", verbose_name="Coin Reverse Image", blank=True, null=True)
    shop = models.ForeignKey('Shop', on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Shop",
                             related_name="coins")

    class Meta:
        verbose_name = "Coin"
        verbose_name_plural = "Coins"

    def __str__(self):
        return f"{self.name} ({self.year})"


class Shop(models.Model):
    name = models.CharField(max_length=255, verbose_name="Shop Name")
    location = models.CharField(max_length=255, verbose_name="Shop Location")
    contact_info = models.CharField(max_length=255, verbose_name="Contact Info", default="No Info")

    class Meta:
        verbose_name = "Shop"
        verbose_name_plural = "Shops"

    def __str__(self):
        return self.name

class CoinCollection(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    coin = models.ForeignKey(Coin, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'coin')

    def __str__(self):
        return f"{self.user.username}'s collection of {self.coin.name}"