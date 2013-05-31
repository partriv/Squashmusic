'''
Created on Sept 10, 2011

@author: par
'''
from django.core.exceptions import MultipleObjectsReturned
from django.template.defaultfilters import slugify
from musicbar import settings_local as settings
from musicbar import util
from musicbar.const import datetime_formats
from musicbar.models import Event, Artist, Venue, Ticket, Tag, Country, City
from xml.dom import minidom
import datetime
import httplib
import logging
import time
import urllib
import urllib2
from django.utils.encoding import smart_str
from musicbar.util import exception_util





class LastFmService():
    
    def __init__(self, source):
        self.source = source
    
    def call(self, params):
        api_key = "&api_key=" + settings.LAST_FM_API_KEY
        method = urllib.urlencode(params)
        url = settings.LAST_FM_API + method + api_key
        logging.info(url)
        try:
            f = urllib2.urlopen(url)
        except httplib.BadStatusLine:
            logging.error("Bad status line, skipping")
            return None
        xml = f.read()
        return minidom.parseString(xml)
        
    def get_events(self, start_index=0, end_index=100, title_filter=None):
        events = Event.objects.filter()
        if title_filter != None:
            events = events.filter(artists__name__istartswith=title_filter)
        return events[start_index:end_index]

    def set_locations_from_api(self):    
        params = {"method":"geo.getmetros"}
        
        xmlevents = self.call(params)
        root = xmlevents.documentElement
        metros = root.getElementsByTagName('metros')[0]
        for m in metros.getElementsByTagName('metro'):
            city_name = util.getNodeText(m.getElementsByTagName('name')[0].childNodes)
            country_name =  util.getNodeText(m.getElementsByTagName('country')[0].childNodes)            
            try:
                dbcountry, created = Country.objects.get_or_create(name=country_name, short_name=slugify(country_name))
                City.objects.get_or_create(name=city_name, slug=slugify(city_name), country=dbcountry)
            except:
                print 'FAILED ON', city_name, country_name
    

    
    def update_events_from_api(self, location="new york"):    
        params = {"method":"geo.getevents",
                      "location":location,
                      "page":'1'}
        
        logging.debug("Updated Last.FM events for " + location)
        
        xmlevents = self.call(params)
        root = xmlevents.documentElement
        events = root.getElementsByTagName('events')[0]
        max_limit = int(events.getAttribute("totalPages"))
        #max_limit = 10
        for i in range(1, max_limit+1):
            if events == None:
                params["page"] = str(i)
                xmlevents = self.call(params)
                if xmlevents == None:
                    continue
                root = xmlevents.documentElement
                events = root.getElementsByTagName('events')[0]
        
            eventNodes = events.getElementsByTagName('event')
    
            for e in eventNodes:
                self.save_event_to_db(e, location)
                        
            logging.info(str(i) + " / " + str(max_limit))
            events = None
    
        return root
            
    def save_event_to_db(self, eventNode, loc):        
        artists = []
        headliners = []
        
        # load up artists
        
        artistsNodes = eventNode.getElementsByTagName('artists')[0]
        for a in artistsNodes.getElementsByTagName('artist'):
            try:
                artist = util.getNodeText(a.childNodes)
                a = Artist.objects.get_or_create(name=artist)[0]
                artists.append(a)
            except: print exception_util.get_exception_str()
        for h in artistsNodes.getElementsByTagName('headliner'):
            try:
                headliner = util.getNodeText(h.childNodes)
                h = Artist.objects.get_or_create(name=headliner)[0]
                headliners.append(h)
            except: print exception_util.get_exception_str()         
        
        # venue stuff
        
        vNode = eventNode.getElementsByTagName('venue')[0]
        vId = util.getNodeText(vNode.getElementsByTagName('id')[0].childNodes)
        vName = util.getNodeText(vNode.getElementsByTagName('name')[0].childNodes)
        vExternalUrl = util.getNodeText(vNode.getElementsByTagName('url')[0].childNodes)
        vUrl = util.getNodeText(vNode.getElementsByTagName('website')[0].childNodes)
        vPhone = util.getNodeText(vNode.getElementsByTagName('phonenumber')[0].childNodes)
        imgNodes = vNode.getElementsByTagName('image')
        vImgSm = ""
        vImgMed = ""
        vImgLg = ""
        vImgXLg = ""
        vImgMega = ""
        for iNode in imgNodes:
            if iNode.hasChildNodes(): 
                if iNode.getAttribute('size') == "small":
                    vImgSm = util.getNodeText(iNode.childNodes)
                elif iNode.getAttribute('size') == "medium":
                    vImgMed = util.getNodeText(iNode.childNodes)
                elif iNode.getAttribute('size') == "large":
                    vImgLg = util.getNodeText(iNode.childNodes)
                elif iNode.getAttribute('size') == "extralarge":
                    vImgXLg = util.getNodeText(iNode.childNodes)
                elif iNode.getAttribute('size') == "mega":
                    vImgMega = util.getNodeText(iNode.childNodes)                    
        locNode = vNode.getElementsByTagName('location')[0]
        #vCity = util.getNodeText(locNode.getElementsByTagName('city')[0].childNodes)
        vCountry = util.getNodeText(locNode.getElementsByTagName('country')[0].childNodes)
        vStreet= util.getNodeText(locNode.getElementsByTagName('street')[0].childNodes)
        vZip = util.getNodeText(locNode.getElementsByTagName('postalcode')[0].childNodes)
        geoNode = locNode.getElementsByTagName('geo:point')[0]
        vLat = util.getNodeText(geoNode.getElementsByTagName('geo:lat')[0].childNodes)
        vLong = util.getNodeText(geoNode.getElementsByTagName('geo:long')[0].childNodes)
        city = City.objects.get(name=loc)
        v = None
        try:
            v = Venue.objects.get_or_create(external_id=vId, name=vName, city=city, country=vCountry, source=self.source)[0]
            v.street=vStreet
            v.zip=vZip
            v.lat=vLat
            v.long=vLong
            v.external_url=vExternalUrl
            v.url=vUrl
            v.phone_number=vPhone
            v.image_size_sm=vImgSm
            v.image_size_med=vImgMed
            v.image_size_lg=vImgLg
            v.image_size_xl=vImgXLg
            v.image_size_mega=vImgMega
            v.save()
        except:
            print "VENUE PROB", exception_util.get_exception_str()
        
        # Ticket stuff
        tickets = []
        ticketsNode = eventNode.getElementsByTagName('tickets')
        if len(ticketsNode) != 0:
            ticketsNode = ticketsNode[0]
            for tNode in ticketsNode.getElementsByTagName('ticket'):
                supplier = tNode.getAttribute('supplier')
                tixUrl = util.getNodeText(tNode.childNodes)
                ticket = Ticket.objects.get_or_create(name=supplier, url=tixUrl)[0]
                tickets.append(ticket)
        
        # Tags stuff
        tags = []
        tagsNode = eventNode.getElementsByTagName('tags')
        if len(tagsNode) != 0:
            tagsNode = tagsNode[0]
            for tNode in tagsNode.getElementsByTagName('tag'):
                tagTxt = util.getNodeText(tNode.childNodes)
                tag = Tag.objects.get_or_create(name=tagTxt)[0]
                tags.append(tag)
                                        
                                        
        # Event stuff                                    
        lastfm_id = util.getNodeText(eventNode.getElementsByTagName('id')[0].childNodes)
        lastfm_id = 'lfm' + lastfm_id
        title = util.getNodeText(eventNode.getElementsByTagName('title')[0].childNodes)
        startDate = util.getNodeText(eventNode.getElementsByTagName('startDate')[0].childNodes)
        
        start_date = datetime.datetime.fromtimestamp(time.mktime(time.strptime(startDate, datetime_formats.LAST_FM_FORMAT)))
        startDate = start_date.strftime(datetime_formats.MYSQL_FORMAT)
        
        
        description = util.getNodeText(eventNode.getElementsByTagName('description')[0].childNodes) #TODO get text???
        external_url = ""
        url = ""
        for urlNode in eventNode.getElementsByTagName('url'):
            if urlNode.parentNode == eventNode:
                external_url = util.getNodeText(urlNode.childNodes)
        for urlNode in eventNode.getElementsByTagName('website'):
            if urlNode.parentNode == eventNode:
                url = util.getNodeText(urlNode.childNodes)            
        cancelled = util.getNodeText(eventNode.getElementsByTagName('cancelled')[0].childNodes)
        if cancelled == '':
            cancelled = 0
        else:
            cancelled = int(cancelled)
        imgSm = ""
        imgMed = ""
        imgLg = ""
        imgXLg = ""
        imgNodes = eventNode.getElementsByTagName('image')
        for iNode in imgNodes:
            if iNode.parentNode == eventNode:
                if iNode.getAttribute('size') == "small":
                    imgSm = util.getNodeText(iNode.childNodes)
                elif iNode.getAttribute('size') == "medium":
                    imgMed = util.getNodeText(iNode.childNodes)
                elif iNode.getAttribute('size') == "large":
                    imgLg = util.getNodeText(iNode.childNodes)
                elif iNode.getAttribute('size') == "extralarge":
                    imgXLg = util.getNodeText(iNode.childNodes)
        
        
        if v != None:
            event, created = Event.objects.get_or_create(external_id=lastfm_id)
            event.name = title
            event.start_time=start_date
            # default all last.fm events to end at 6
            event.end_time = start_date + datetime.timedelta(hours=6)
            event.description=description
            event.image_size_sm=imgSm
            event.image_size_med=imgMed
            event.image_size_lg=imgLg
            event.image_size_xl=imgXLg
            event.cancelled=cancelled
            event.venue=v    
            event.category = self.source.category
            event.source = self.source
            event.external_url = external_url
            event.url = url                                          
            for a in artists:
                event.artists.add(a)
            for h in headliners:
                event.headliners.add(h)
            for t in tags:
                event.tags.add(t)        
            for t in tickets:
                event.tickets.add(t)    
            try:
                event.save()
            except:
                print "EVENT ERR", exception_util.get_exception_str()        
        
        
        

