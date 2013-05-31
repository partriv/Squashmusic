'''
Created on Sept 10, 2011
@author: par
'''
from django.db import connection
from django.db.models.query_utils import Q
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.shortcuts import render_to_response
from musicbar.const import const
from musicbar.models import Event, Venue, City
from musicbar.service import event_service
from musicbar.view import base
import datetime

LATEST_NEWS_SIZE = 8
OTHER_NEWS_SIZE = 8
MUSIC_EVENTS_SIZE = 56

def city_slug_handler(request, city_slug=None):
    if city_slug == None:
        city_slug = request.COOKIES.get('city_slug', 'new-york')
        return HttpResponseRedirect("/%s/" % city_slug)
    
    vars = {}
    try:
        city = City.objects.get(slug=city_slug)
    except City.DoesNotExist: raise Http404
    vars['city'] = city
    
    events = event_service.get_music_events(city, 0, MUSIC_EVENTS_SIZE)
    vars["events"] =  events
    vars['cities'] = City.objects.filter(Q(country=const.LFM_COUNTRY_ID_USA) | Q(id=const.LFM_LONDON_CID)).order_by('name')
    
    vids = [o['venue_id'] for o in events.values('venue_id')]
    vars['venues'] = Venue.objects.filter(city=city, id__in=vids).order_by('name')
    vars['MUSIC_EVENTS_SIZE'] = MUSIC_EVENTS_SIZE
    
    resp =  base.render(request, "music_events.html", vars)
    resp.set_cookie('city_slug', city_slug, max_age=315569260)
    
    return resp




def sitemap(request):
    vars = {}
    venues = Venue.objects.all()
    vars['venues'] = venues
    d = datetime.datetime.now()
    vars['date'] = d.strftime('%Y-%m-%d')
    resp = render_to_response("sitemap.xml", vars)    
    resp.content_type = "text/xml"
    resp = HttpResponse(content=resp.content, content_type="text/xml")
    return resp
    
    
    