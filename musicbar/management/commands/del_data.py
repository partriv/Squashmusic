'''
Created on Sept 10, 2011

@author: par
'''
from django.core.management.base import BaseCommand
from musicbar.models import Event
import datetime
import logging


'''
Created on Jan 2, 2011

@author: par
'''



class Command(BaseCommand):

    def handle(self, *args, **options):
        
        # clear out old shizen
        now = datetime.datetime.now()
        events = Event.objects.filter(end_time__lte=now)
        for e in events:
            e.delete()
        