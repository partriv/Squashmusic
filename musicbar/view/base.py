'''
Created on Sept 10, 2011
@author: par
'''
from django.http import HttpResponse
from django.shortcuts import render_to_response
from musicbar.models import City, Event, Country
from musicbar.service.lastfm_service import LastFmService
import datetime
import logging
import random

def init(request):
    
    
    fm = LastFmService(source='homeinit')
    fm.set_locations_from_api()
    return HttpResponse("DONE!")
    
    
def get_right_col(baseVars):
    #events = eventful_service.get_events()
    #logging.log(logging.DEBUG, 'promoted events')
    events  = Event.objects.filter(featured=True, deleted=False).exclude(start_time=None).order_by('start_time')
    #logging.log(logging.DEBUG, 'promoted events')
    baseVars["music_events"] = events
     

def get_left_col(baseVars, photos=True, etsy=True):
    pass    

def render(request, template, vars, admin=False):    
    baseVars = {}
    baseVars.update(vars)
    return render_to_response(template, baseVars)