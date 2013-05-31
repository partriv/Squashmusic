'''
Created on Sept 10, 2011

@author: par
'''

from django.db.models.query_utils import Q
from musicbar.models import Event, EventSource
from musicbar.proxy.news import RssProxy
from xml.dom import minidom
import datetime
import logging
import urllib2




def update_event_data():
    
    # clear out old shizen
    now = datetime.datetime.now()
    events = Event.objects.filter(end_time__lte=now)
    for e in events:
        e.delete()
    
    for s in EventSource.objects.all():
        if not s.active:
            logging.info("Skipping %s, it is not active" % s.name)
            continue
        if s.proxy == '':
            print "NO PROXY FOR EVENT SOURCE: " + s.name
            continue
        
        logging.info(s.name + " using: " + s.proxy)
        pkg = s.proxy[:s.proxy.rfind('.')]
        clazz = s.proxy[s.proxy.rfind('.')+1:]
        event_mod = __import__(pkg, globals(), locals(), clazz)
        event_proxy = getattr(event_mod, clazz)(s)
        
        if s.url != '' and isinstance(event_proxy, RssProxy):
            # got an RssProxy just do rss stuff
            rssStr = urllib2.urlopen(s.url).read()
            xmlDoc = minidom.parseString(rssStr)
            rssNode = xmlDoc.documentElement
            for item in rssNode.getElementsByTagName(event_proxy.ITEM_TAG):            
                event_proxy.set_item(item)
                eid = event_proxy.get_external_id()
                eventDb, created = Event.objects.get_or_create(external_id=eid)
                eventDb.name = event_proxy.get_title() 
                eventDb.start_time = event_proxy.get_start_date()
                eventDb.end_time = event_proxy.get_end_date()
                eventDb.url = event_proxy.get_url()
                eventDb.external_url = event_proxy.get_url()
                eventDb.description = event_proxy.get_description()
                eventDb.category = s.category
                eventDb.source = s
                eventDb.venue = event_proxy.get_venue()
                eventDb.image_size_med = event_proxy.get_image()
                eventDb.save()
        else:
            # not an RssProxy so try an update method
            event_proxy.update()

def get_music_events(city, start=0, end=20, venue_id=None, artist=None):
    events = Event.objects.exclude(start_time=None).filter(deleted=False, venue__city=city).order_by('start_time')

    if artist:
        events = events.filter(artists__name__icontains=artist)
    if venue_id:
        events = events.filter(venue=venue_id)
    
    events = events[start:end]
    for e in events:
        edescAr = e.description.split(',')        
        if len(e.description) < 35 and len(edescAr) == 3 and len(edescAr[1].strip().split(' ')) == 2:
            midEdescAr = edescAr[1].strip().split(' ')
            try:
                # OH SHIT FUZZY LOGIC DETERMINED U R PROBABLY SOMETHING LIKE THIS
                # Mon., January 10, 7:00pm
                int(midEdescAr[1])
                e.description = ''
            except ValueError:    
                # , valid descgood to go
                pass
    return events
    