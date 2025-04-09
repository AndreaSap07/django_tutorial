from django.db import models

# Create your models here.
class PassItem(models.Model):
    satellite = models.CharField(max_length=4)
    antenna = models.CharField(max_length=100)
    orbit_num = models.IntegerField(default=0)
    utc_start_time = models.DateTimeField(auto_now_add=True)
    source_file = models.CharField(max_length=255)  # To trace origin
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.satellite