from django.db import models

# Create your models here.
class Product(models.Model):
    title       = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    price       = models.DecimalField(decimal_places=2, max_digits=10000)
    summary     = models.TextField()
    featured    = models.BooleanField(default=True) #Since I am adding something without deleting the database I will need to state it's initial value, so that Django will know what to put inside the old products that didn't have the value in principle.
                                        # null=True or default=True (default= ObjType of the model)