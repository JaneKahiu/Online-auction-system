from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
    
class AuctioningListing(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    starting_bid = models.DecimalField(max_digits=10, decimal_places=2)
    current_bid = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    end_date = models.DateTimeField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    image = models.ImageField(upload_to='auction_images/', null=True, blank=True)

    def __str__(self): 
        return self.title
    
    def save(self, *args, **kwargs):
      if not self.current_bid:
          self.current_bid = self.starting_bid
          super().save(*args, **kwargs)

    
    def is_active(self):
        return timezone.now()
    
class Bid(models.Model):
    auction = models.ForeignKey(AuctioningListing, on_delete=models.CASCADE)
    bidder = models.ForeignKey(User, on_delete=models.CASCADE)
    bid_amount = models.DecimalField(max_digits=10, decimal_places=2)
    bid_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.bidder.username} - {self.bid_amount} on {self.auction.title}"
    




    

 























































