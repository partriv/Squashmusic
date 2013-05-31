'''
Created on Sept 10, 2011
@author: par
'''

from django.shortcuts import render_to_response
from musicbar.models import City, Event
from musicbar.service import event_service
from musicbar.view.index import MUSIC_EVENTS_SIZE

def get_event(request):
    eventid = request.GET.get('eid')
    vars = {}
    event = Event.objects.get(id=eventid)
    vars['event'] = event
    vars['city'] = event.venue.city
    return render_to_response("ajax/event_info.html", vars)
    

def find_events(request):
    vars= {}
    vid = request.GET.get('vid', None)
    cid = request.GET['cid']    
    artist = request.GET.get('txt', None)
    if artist == 'Artist Search': artist = None
    if vid == '0': vid = None 
        
    start = request.GET.get('start', None)    
    end = int(request.GET.get('end', MUSIC_EVENTS_SIZE))
    if start == None: start = end - MUSIC_EVENTS_SIZE
    
    city = City.objects.get(id=cid)
    vars['city'] = city
    events = event_service.get_music_events(city, start, end, vid, artist)
    vars['events'] = events

    return render_to_response("ajax/find_events.html", vars)
