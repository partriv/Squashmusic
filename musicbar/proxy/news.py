'''
Created on Jan 1, 2011
s
@author: par
'''

from musicbar import util
from musicbar.const import datetime_formats
import datetime


class RssProxy(object):
    def __init__(self, source):
        self.source = source
    
    ITEM_TAG = 'item'
    
    def set_item(self, item):
        self.item = item    
    
    def get_title(self):        
        title = util.getNodeText(self.item.getElementsByTagName('title')[0].childNodes)
        if title.find('CDATA') > -1 or title.strip() == '':        
            title = util.getCData(self.item.getElementsByTagName('title')[0]) # village voice, style peterson
        return title.strip()
        
    def get_url(self):
        url = ''
        if len(self.item.getElementsByTagName('link')) == 1:
            url = util.getNodeText(self.item.getElementsByTagName('link')[0].childNodes)
            if url == None or url.strip() == '':
                url = self.item.getElementsByTagName('link')[0].getAttribute('href') #bk vegan, flaming pab
        else:
            for l in self.item.getElementsByTagName('link'): #style peterson
                if l.getAttribute('rel') == 'alternate':
                    url = l.getAttribute('href')
                    break
                
        if url == None: 
            url = ''
        return url.strip()
    
    def get_description(self, tag='description'):
        desc = ''
        
        if len(self.item.getElementsByTagName(tag)) > 0:
            desc = util.getNodeText(self.item.getElementsByTagName(tag)[0].childNodes)            
            if desc == None or desc.strip() == '' or desc.find('CDATA') > -1:
                desc = util.getCData(self.item.getElementsByTagName(tag)[0])                
        if desc == None or desc.strip() == '':
            if len(self.item.getElementsByTagName('content')) > 0:
                desc = util.getNodeText(self.item.getElementsByTagName('content')[0].childNodes)                
                if desc == None or desc.strip() == '' or desc.find('CDATA') > -1:
                    desc = util.getCData(self.item.getElementsByTagName('content')[0])
        if desc == None or desc.strip() == '':
            if len(self.item.getElementsByTagName('summary')) > 0:
                desc = util.getNodeText(self.item.getElementsByTagName('summary')[0].childNodes)
        return desc.strip()

    
    def get_category(self):
        if self.source.category == '':
            if (len(self.item.getElementsByTagName('category')) > 0):
                return util.getNodeText(self.item.getElementsByTagName('category')[0].childNodes)
        else:
            return self.source.category
        return ''
    
    def get_creator(self, tag='dc:creator'):
        creator = ''
        if len(self.item.getElementsByTagName(tag)) > 0:
            creator = util.getNodeText(self.item.getElementsByTagName(tag)[0].childNodes)
            if creator == None or creator.strip() == '':
                creator = util.getCData(self.item.getElementsByTagName(tag)[0])
        if creator == None or creator.strip() == '':
            if len(self.item.getElementsByTagName('author')) > 0 and len(self.item.getElementsByTagName('author')[0].getElementsByTagName('name')) > 0:                
                creator = util.getNodeText(self.item.getElementsByTagName('author')[0].getElementsByTagName('name')[0].childNodes)                
        return creator.strip()

    def get_date(self):
        if (len(self.item.getElementsByTagName('pubDate')) > 0):
            dateStr = util.getNodeText(self.item.getElementsByTagName('pubDate')[0].childNodes)
            if dateStr =='':
                return None
            #<pubDate>Fri, 31 Dec 2010 15:56:00 -0500</pubDate>
            dateStr = dateStr[dateStr.find(',')+1:].strip()
            # 31 Dec 2010 15:56:00 -0500
            dateStr = dateStr[0:dateStr.rfind('-')].strip()
            # 31 Dec 2010 15:56:00 
            date = datetime.datetime.strptime(dateStr, datetime_formats.L_MAG_TIME_FORMAT)
            return date  
        return None    
    
    
class Gothamist(RssProxy):
    def get_date(self):
        if (len(self.item.getElementsByTagName('dc:date')) > 0):
            dateStr = util.getNodeText(self.item.getElementsByTagName('dc:date')[0].childNodes)
            if dateStr =='':
                return None            
            #2011-01-01T14:00:18-05:00
            date = datetime.datetime.strptime(dateStr[0:dateStr.rfind('-')], datetime_formats.GOTHAMIST_TIME_FORMAT)
            return date  
        return None
      

    

class TheLMagazine(RssProxy):
    def get_category(self):        
        if (len(self.item.getElementsByTagName('category')) > 0):
            cat = util.getNodeText(self.item.getElementsByTagName('category')[0].childNodes)
            if cat == 'Film':
                return 'Movies'
            if cat == 'Art':
                return 'Art'
            if cat == 'Theater':
                return 'Art'
            return cat
        return 'News'
        

class TheVillageVoice(RssProxy):
    
    def get_date(self):
        if (len(self.item.getElementsByTagName('pubDate')) > 0):
            link = self.source.url;
            dateStr = util.getNodeText(self.item.getElementsByTagName('pubDate')[0].childNodes)
            if dateStr =='':
                return None
            if link.find('promoEvents') > -0:
                #<pubDate>2010-10-14 15:39:09</pubDate>                                 
                date = datetime.datetime.strptime(dateStr, datetime_formats.VILLAGE_VOICE_PROMO_TIME_FORMAT)
                return date
            else:
                #<pubDate>Fri, 31 Dec 2010 15:56:00 -0500</pubDate>
                dateStr = dateStr[dateStr.find(',')+1:].strip()
                # 31 Dec 2010 15:56:00 -0500
                dateStr = dateStr[0:dateStr.rfind('-')].strip()
                # 31 Dec 2010 15:56:00                 
                date = datetime.datetime.strptime(dateStr, datetime_formats.VILLAGE_VOICE_TIME_FORMAT)
                return date  
        return None    
                    

class BrooklynVegan(RssProxy):
    
    ITEM_TAG = 'entry'
    
    def get_category(self):
        if (len(self.item.getElementsByTagName('dc:subject')) > 0):
            return util.getNodeText(self.item.getElementsByTagName('dc:subject')[0].childNodes)
        return 'News'

    def get_date(self):
        if (len(self.item.getElementsByTagName('created')) > 0):
            dateStr = util.getNodeText(self.item.getElementsByTagName('created')[0].childNodes)
            if dateStr =='':
                return None                        
            date = datetime.datetime.strptime(dateStr, datetime_formats.BK_VEGAN_FORMAT)
            date = date - datetime.timedelta(hours=5)
            return date  
        return None   


                

class BoweryBoogie(RssProxy):
    def get_date(self):
        if (len(self.item.getElementsByTagName('pubDate')) > 0):
            dateStr = util.getNodeText(self.item.getElementsByTagName('pubDate')[0].childNodes)
            if dateStr =='':
                return None
            #<pubDate>Mon, 03 Jan 2011 14:19:06 +0000</pubDate>
            dateStr = dateStr[dateStr.find(',')+1:].strip()
            dateStr = dateStr[0:dateStr.rfind('+')].strip()
            date = datetime.datetime.strptime(dateStr, datetime_formats.VILLAGE_VOICE_TIME_FORMAT)
            date = date - datetime.timedelta(hours=5)            
            return date  
        return None    
    

class FlamingPablum(RssProxy):
    ITEM_TAG = 'entry'

    def get_date(self):
        if (len(self.item.getElementsByTagName('published')) > 0):
            dateStr = util.getNodeText(self.item.getElementsByTagName('published')[0].childNodes)
            if dateStr =='':
                return None
            #2010-12-24T08:27:44-05:00
            dateStr = dateStr[0:dateStr.rfind('-')].strip()
            # 2010-12-24T08:27:44                 
            date = datetime.datetime.strptime(dateStr, datetime_formats.GOTHAMIST_TIME_FORMAT)
            return date  
        return None       


    
class StylePeterson(FlamingPablum):
    def get_date(self):
        if (len(self.item.getElementsByTagName('updated')) > 0):
            dateStr = util.getNodeText(self.item.getElementsByTagName('updated')[0].childNodes)
            if dateStr =='':
                return None                        
            date = datetime.datetime.strptime(dateStr, datetime_formats.BK_VEGAN_FORMAT)
            date = date - datetime.timedelta(hours=5)
            return date  
        return None   
      

class GoogleFood(FlamingPablum):
    def get_date(self):
        if (len(self.item.getElementsByTagName('published')) > 0):
            dateStr = util.getNodeText(self.item.getElementsByTagName('published')[0].childNodes)
            if dateStr =='':
                return None
            #2009-08-13T17:33:20.000Z
            dateStr = dateStr[0:dateStr.find('.')]
            #2009-08-13T17:33:20                 
            date = datetime.datetime.strptime(dateStr, datetime_formats.GOTHAMIST_TIME_FORMAT)
            date = date - datetime.timedelta(hours=5)            
            return date  
        return None       

class StyleDefined(FlamingPablum):
    def get_date(self):
        if (len(self.item.getElementsByTagName('updated')) > 0):
            dateStr = util.getNodeText(self.item.getElementsByTagName('updated')[0].childNodes)
            if dateStr =='':
                return None
            #2009-08-13T17:33:20.000Z
            dateStr = dateStr[0:dateStr.find('.')]
            #2009-08-13T17:33:20                 
            date = datetime.datetime.strptime(dateStr, datetime_formats.GOTHAMIST_TIME_FORMAT)
            date = date - datetime.timedelta(hours=5)            
            return date  
        return None   

class DapperLou(FlamingPablum):
    def get_date(self):
        if (len(self.item.getElementsByTagName('published')) > 0):
            dateStr = util.getNodeText(self.item.getElementsByTagName('published')[0].childNodes)
            if dateStr =='':
                return None
            #2011-01-16T14:03:20.364-05:00
            dateStr = dateStr[0:dateStr.find('.')]
            #2011-01-16T14:03:20                 
            date = datetime.datetime.strptime(dateStr, datetime_formats.GOTHAMIST_TIME_FORMAT)
            return date  
        return None     
    

class NyObserver(RssProxy):
    def get_date(self):
        if (len(self.item.getElementsByTagName('pubDate')) > 0):
            dateStr = util.getNodeText(self.item.getElementsByTagName('pubDate')[0].childNodes)
            
            if dateStr =='':
                return None
            # <pubDate>Fri, 24 Sep 2010 10:44:43 -0400</pubDate>
            dateStr = dateStr[dateStr.find(',')+1:].strip()
            # 31 Dec 2010 15:56:00 -0400
            dateStr = dateStr[0:dateStr.rfind('-')].strip()
            # 31 Dec 2010 15:56:00                 
            date = datetime.datetime.strptime(dateStr, datetime_formats.VILLAGE_VOICE_TIME_FORMAT)
            date = date - datetime.timedelta(hours=1)
            return date  
        return None       


class NymagFeedburner(RssProxy):
    def get_date(self):
        if (len(self.item.getElementsByTagName('pubDate')) > 0):
            dateStr = util.getNodeText(self.item.getElementsByTagName('pubDate')[0].childNodes)
            if dateStr =='':
                return None
            #<pubDate>Sun, 02 Jan 2011 23:35:40 GMT</pubDate>
            dateStr = dateStr[dateStr.find(',')+1:].strip()
            # 31 Dec 2010 15:56:00 GMT
            dateStr = dateStr.replace('GMT', '').strip()
            # 31 Dec 2010 15:56:00 
            date = datetime.datetime.strptime(dateStr, datetime_formats.L_MAG_TIME_FORMAT)
            date = date - datetime.timedelta(hours=5)
            return date  
        return None    

class NyReviewBooks(RssProxy):
    def get_date(self):
        if (len(self.item.getElementsByTagName('pubDate')) > 0):
            dateStr = util.getNodeText(self.item.getElementsByTagName('pubDate')[0].childNodes)
            if dateStr =='':
                return None
            #<pubDate>Fri, 24 Dec 2010 21:00:08 -0800</pubDate>
            dateStr = dateStr[dateStr.find(',')+1:].strip()
            dateStr = dateStr[0:dateStr.rfind('-')].strip() 
            date = datetime.datetime.strptime(dateStr, datetime_formats.L_MAG_TIME_FORMAT)
            date = date + datetime.timedelta(hours=3)
            return date  
        return None    
    
    
    

class NyDailyPhoto(RssProxy):
    def get_date(self):
        if (len(self.item.getElementsByTagName('pubDate')) > 0):
            dateStr = util.getNodeText(self.item.getElementsByTagName('pubDate')[0].childNodes)
            if dateStr =='':
                return None
            #<pubDate>Mon, 03 Jan 2011 14:19:06 +0000</pubDate>
            dateStr = dateStr[dateStr.find(',')+1:].strip()
            dateStr = dateStr[0:dateStr.rfind('+')].strip()
            date = datetime.datetime.strptime(dateStr, datetime_formats.VILLAGE_VOICE_TIME_FORMAT)
            date = date - datetime.timedelta(hours=5)            
            return date  
        return None
    
    def get_creator(self):
        return super(NyDailyPhoto, self).get_creator('author')                                                                    