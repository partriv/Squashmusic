'''
Created on Jan 3, 2011

@author: par
'''

from django.db.models.query_utils import Q
from django.template import defaultfilters
from musicbar import util
from musicbar.const import datetime_formats, const
from musicbar.models import Venue, City
from musicbar.proxy.news import RssProxy, TheVillageVoice
from musicbar.service import lastfm_service, eventful_service
import datetime
import logging




class EventProxy():
    def __init__(self, source):
        self.source = source

    


class LastFm(EventProxy):
    def update(self):
        lfm = lastfm_service.LastFmService(self.source)
        # city id 30 = uk, 31 = usa
        # 185 london
        for c in City.objects.filter(Q(country__id__in=[const.LFM_COUNTRY_ID_USA]) | Q(id=const.LFM_LONDON_CID)):            
            lfm.update_events_from_api(location=c.name)

class Eventful(EventProxy):
    def update(self):
        e = eventful_service.EventfulService(self.source)
        e.update_events()

class VillageVoice(TheVillageVoice):
    
    def get_image(self):
        return ''
    
    def get_external_id(self):
        url = self.get_url()
        eid = url[url.rfind('-')+1:].strip('/').strip()
        return 'vv' + str(eid)

    def get_description(self):
        if len(self.item.getElementsByTagName('description')) > 0:
            desc = util.getCData(self.item.getElementsByTagName('description')[0])
            self.orig_desc = desc 
            return desc[desc.find('-')+1:].strip()
        return ''    
        
    def get_date(self):
        now = datetime.datetime.now()
        self.get_description()
        desc = self.orig_desc
        if desc != '':
            dateStr = ''
            try:
                if desc.find('-') > -1:
                    dateStr = desc[:desc.find('-')].strip()
                else:
                    # try this
                    dateStr = desc.strip()
                if dateStr =='':
                    return None
                #Tue., January 4, 9:00pm                
                dateStr = dateStr[dateStr.find(',')+1:].strip()
                #January 4, 9:00pm
                dateStr = dateStr.replace(',', '').strip()
                #January 4 9:00pm
                dateStrAr = dateStr.split(' ')
                if len(dateStrAr[1]) == 1:
                        dateStrAr[1] = '0' + dateStrAr[1]
                if len(dateStrAr) == 2:                    
                    dateStr = dateStrAr[0] + ' ' + dateStrAr[1] + ' ' + str(now.year) + ' 07:00pm'
                    #January 04 2010 09:00pm                                             
                    date = datetime.datetime.strptime(dateStr, datetime_formats.VILLAGE_VOICE_EVENT_TIME_FORMAT)
                    return date
                elif len(dateStrAr) == 3:
                    if len(dateStrAr[2]) == 6:
                        dateStrAr[2] = '0' + dateStrAr[2]
                    dateStr = dateStrAr[0] + ' ' + dateStrAr[1] + ' ' + str(now.year) + ' ' + dateStrAr[2]
                    #January 04 2010 09:00pm                                             
                    date = datetime.datetime.strptime(dateStr, datetime_formats.VILLAGE_VOICE_EVENT_TIME_FORMAT)
                    return date
            except Exception, e:
                logging.log(logging.DEBUG, "Could not get date from " + dateStr + " desc: " + str(desc[:30]) + "... " + str(e))

    
    def get_start_date(self):
        if self.get_date():
            return self.get_date()         
    
    def get_end_date(self):
        if self.get_date():
            return self.get_date() + datetime.timedelta(hours=6)
        
    def get_venue(self):
        return None
