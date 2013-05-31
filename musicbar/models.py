'''
Created on Sept 10, 2011

@author: par
'''
from django.db import models

  


class Artist(models.Model):
    name = models.CharField(max_length=255)
    twitter = models.CharField(max_length=255, null=True)
    created = models.DateTimeField(auto_now_add=True)
        
class Ticket(models.Model):
    name = models.CharField(max_length=512)
    url = models.CharField(max_length=512)
    created = models.DateTimeField(auto_now_add=True)
    
class Tag(models.Model):
    name = models.CharField(max_length=255)        
    created = models.DateTimeField(auto_now_add=True)

class Country(models.Model):    
    name = models.CharField(max_length=255)
    short_name = models.CharField(max_length=40)
    

class City(models.Model):    
    name = models.CharField(max_length=255)
    slug = models.CharField(max_length=255)
    country = models.ForeignKey(Country)
    created = models.DateTimeField(auto_now_add=True)
    

class EventSource(models.Model):
    name = models.CharField(max_length=256)
    url = models.CharField(max_length=1024, blank=True)    
    active = models.BooleanField(default=True)    
    proxy = models.CharField(max_length='127', blank=True)
    category = models.CharField(max_length='100', blank=True)
    created = models.DateTimeField(auto_now_add=True)
    
class Venue(models.Model):
    external_id = models.CharField(max_length=100, blank=True)
    name = models.CharField(max_length=1024)
    city = models.ForeignKey(City)
    country =  models.CharField(max_length=100, blank=True)
    street = models.CharField(max_length=512, blank=True)
    zip = models.CharField(max_length=25, blank=True)
    lat = models.DecimalField(max_digits=11, decimal_places=7, null=True)
    long = models.DecimalField(max_digits=11, decimal_places=7, null=True)
    external_url = models.CharField(max_length=1024, blank=True)
    url = models.CharField(max_length=1024, blank=True)
    phone_number = models.CharField(max_length=100, blank=True)
    image_size_sm = models.CharField(max_length=255, blank=True)
    image_size_med = models.CharField(max_length=255, blank=True)
    image_size_lg = models.CharField(max_length=255, blank=True)
    image_size_xl = models.CharField(max_length=255, blank=True)
    image_size_mega = models.CharField(max_length=255, blank=True)
    source = models.ForeignKey(EventSource)
    created = models.DateTimeField(auto_now_add=True)
        
class Event(models.Model):
    external_id = models.CharField(max_length=100, blank=True)
    name = models.CharField(max_length=512, blank=True)
    venue = models.ForeignKey(Venue, null=True)
    artists = models.ManyToManyField(Artist, null=True, related_name="event_artists_join")
    headliners = models.ManyToManyField(Artist, null=True, related_name="event_headliners_join")
    start_time = models.DateTimeField(null=True)
    end_time = models.DateTimeField(null=True)
    description = models.TextField(blank=True)
    image_size_sm = models.CharField(max_length=255, blank=True)
    image_size_med = models.CharField(max_length=255, blank=True)
    image_size_lg = models.CharField(max_length=255, blank=True)
    image_size_xl = models.CharField(max_length=255, blank=True)
    external_url = models.CharField(max_length=1024, blank=True)
    url = models.CharField(max_length=1024, blank=True)        
    tickets = models.ManyToManyField(Ticket, null=True)
    tags = models.ManyToManyField(Tag, null=True)
    cancelled = models.BooleanField(default=False)
    category = models.CharField(max_length='100', blank=True)
    source = models.ForeignKey(EventSource, null=True)
    featured = models.BooleanField(default=False)
    deleted = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    tweeted = models.DateTimeField(null=True)

    
    