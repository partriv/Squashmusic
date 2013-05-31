'''
Created on Sept 10, 2011

@author: par
'''


from django.utils import simplejson
from musicbar import settings
from musicbar.const import datetime_formats
from musicbar.models import Event, Venue
import datetime
import urllib
import urllib2



class EventfulService():
    
    def __init__(self, source):
        self.source = source
        
    def update_events(self):
        url = settings.EVENTFUL_API + 'events/search'
        params = {}
        params['location'] = 'new york'
        params['date'] = 'Future'
        params['app_key'] = settings.EVENTFUL_API_KEY
        params['page_size'] = 100
        for k in ('movies', 'clothing', 'fashion', 'books', 'art', 'museum', 'food'):
            #keywords=movies&location=new+york&date=Future&app_key=9FpQkTSvTh32PHcx
            #http://api.eventful.com/rest/events/search?keywords=clothing&location=new+york&date=Future&app_key=9FpQkTSvTh32PHcx
            params['keywords'] = k
            
            paramStr = urllib.urlencode(params)
            pg1url = url + "?" + paramStr
            print pg1url
            event_json = simplejson.loads(urllib2.urlopen(pg1url).read())
            #print event_json
            page_size = event_json['page_size']
            
            for i in range(1, 2):
                if i != 1:
                    params['page_number'] = i
                    paramStr = urllib.urlencode(params)
                    nurl = url + "?" + paramStr
                    print nurl
                    event_json = simplejson.loads(urllib2.urlopen(nurl).read())
                for e in event_json['events']['event']:
                    
                    event = e#['event']
                    id = event['id']                    
                    dbEvent, create = Event.objects.get_or_create(external_id=id)
                    #print "doing event " + id
                    if k == 'clothing':
                        dbEvent.category = 'Fashion'
                    elif k == 'museum':
                        dbEvent.category = 'Art'
                    else:
                        dbEvent.category = k.title()
                    
                    dbEvent.name = event['title']
                    dbEvent.url = event['url']
                    dbEvent.description = event['description'] if event['description'] else ''
                    st = event['start_time']
                    st_dt = datetime.datetime.strptime(st, datetime_formats.MYSQL_FORMAT)
                    dbEvent.start_time = st_dt
                    stopTimeStr = event['stop_time']
                    if stopTimeStr != None and stopTimeStr != '': 
                        stopTime = datetime.datetime.strptime(stopTimeStr, datetime_formats.MYSQL_FORMAT)
                        dbEvent.end_time = stopTime
                    else:
                        dbEvent.end_time = st_dt + datetime.timedelta(hours=6)
                    
                    if event['image']:
                        dbEvent.image_size_med = event['image']['url'] if event['image']['url'] else ''
                        if event['image']['small']:
                            dbEvent.image_size_sm = event['image']['small']['url'] if event['image']['small']['url'] else ''
                        if event['image']['thumb']:
                            dbEvent.image_size_lg = event['image']['thumb']['url'] if event['image']['thumb']['url'] else ''
                        if event['image']['medium']:
                            dbEvent.image_size_xl = event['image']['medium']['url'] if event['image']['medium']['url'] else ''                                                        

                    
                    
                    vid = event['venue_id']
                    v, create = Venue.objects.get_or_create(external_id=vid)
                    v.url = event['venue_url']
                    v.name = event['venue_name'] if event['venue_name'] else ''
                    v.street = event['venue_address'] if event['venue_address'] else '' 
                    v.city = event['city_name'] if event['city_name'] else ''
                    v.country  = event['country_name'] if event['country_name'] else ''
                    v.lat = event['latitude'] 
                    v.long = event['longitude'] 
                    v.source = self.source
                    v.save()
                    
                    dbEvent.venue = v
                    dbEvent.source = self.source
                    dbEvent.save()
                    
            
                
                 
                
                
            
             
    