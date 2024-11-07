from django.db import models

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
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, blank=True,null=True, verbose_name="Country of Origin")
    year = models.IntegerField(verbose_name="Year of Issue")
    material = models.ManyToManyField(Material, verbose_name="Coin Material")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Coin Price")
    imageObverse = models.ImageField(upload_to="coins/", verbose_name="Coin Obverse Image", blank=True, null=True)
    imageReverse = models.ImageField(upload_to="coins/", verbose_name="Coin Reverse Image", blank=True, null=True)
    shop = models.ForeignKey('Shop', on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Shop", related_name="coins")

    class Meta:
        verbose_name = "Coin"
        verbose_name_plural = "Coins"

    def __str__(self):
        return f"{self.name} ({self.year})"

class Collector(models.Model):
    first_name = models.CharField(max_length=255, verbose_name="First Name")
    last_name = models.CharField(max_length=255, verbose_name="Last Name")
    email = models.EmailField(unique=True, verbose_name="Email")
    phone = models.CharField(max_length=20, blank=True, verbose_name="Phone Number")
    coins = models.ManyToManyField(Coin, verbose_name="Collected Coins", blank=True)

    class Meta:
        verbose_name = "Collector"
        verbose_name_plural = "Collectors"

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Shop(models.Model):
    name = models.CharField(max_length=255, verbose_name="Shop Name")
    location = models.CharField(max_length=255, verbose_name="Shop Location")
    contact_info = models.CharField(max_length=255, verbose_name="Contact Info", default="No Info")

    class Meta:
        verbose_name = "Shop"
        verbose_name_plural = "Shops"

    def __str__(self):
        return self.name
