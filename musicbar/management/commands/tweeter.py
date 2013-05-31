'''
Created on Mar 5, 2012

@author: par
'''
from django.core.management.base import BaseCommand
from django.template import defaultfilters
from musicbar.models import City, Event, Venue
import datetime
import twitter
import urllib
import urllib2


VID_BOWERY = 1169
VID_MUSIC_HALL = 1168
VID_TERMINAL_5 = 1175
VID_WEBSTER = 1183
NYC_VIDS = [VID_BOWERY, VID_MUSIC_HALL, VID_TERMINAL_5, VID_WEBSTER]


class Command(BaseCommand):

    def removeNonAscii(self, s): return "".join(i for i in s if ord(i)<128)
    
    def handle(self, *args, **options):

        try:

            dt = datetime.datetime.now()
            if dt.hour % 2 == 0:
                
                twitter_api =  twitter.Api(consumer_key='DOrJEk1DUOZhORAd9nQ7ug',
                                     consumer_secret='aji0VPGFINJAsh7XA5EmHXLbaZfBilgOmJ2Xmm74',
                                     access_token_key='518215207-vYU96NwUSz38tiXCU7Pkd4KNOVBAGSuBuMWAaIqe',
                                     access_token_secret='InZah2EUjb5APUz014lv6G02LchVPIU25oqZ8kvQ' )
                
                # local vars
                nycity = City.objects.get(id=216)                
                bowery = Venue.objects.filter(name='Bowery Ballroom')[0]
                music_hall = Venue.objects.filter(name='Music Hall of Williamsburg')[0]
                t5 = Venue.objects.filter(name='Terminal 5')[0]
                webster = Venue.objects.filter(name='Webster Hall')[0]
                nyc_venues = [bowery, music_hall, t5, webster]
                thirtdays = datetime.datetime.now() + datetime.timedelta(days=30)
                events = Event.objects.filter(venue__in=nyc_venues, tweeted=None, start_time__lte=thirtdays).exclude(start_time=None).order_by('start_time')
                for e in events:                                        
                    mesg = e.name + ", " + defaultfilters.date(e.start_time, "D, M d") + ' @ ' + e.venue.name
                    
                    # tinyurl'ze the object's link
                    #create_api = 'http://tinyurl.com/api-create.php'
                    #data = urllib.urlencode(dict(url='http://musicbar.fm/new-york/'))
                    #link = urllib2.urlopen(create_api, data=data).read().strip()
                    link = 'http://musicbar.fm/new-york/#event' + str(e.id)
                                            
                    others = ''
                    for a in e.artists.all():
                        if a.name.lower().strip() != e.name.lower().strip():
                            others += a.name.strip() + ', '
                    others = others.strip().strip(',')
                    if others:
                        others = 'w/ ' + others
                    
                    mesg = mesg + ' ' + link + ' ' + others
                    mesg = self.removeNonAscii(mesg)
                    mesg = mesg[:140]
            
                    twitter_api.PostUpdate(mesg)
                    e.tweeted = datetime.datetime.now()
                    e.save()
                    
                    break
                
        except urllib2.HTTPError, ex:
            print 'ERROR:', str(ex)
            return False