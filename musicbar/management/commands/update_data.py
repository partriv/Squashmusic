'''
Created on Sept 10, 2011

@author: par
'''

from django.core.management.base import BaseCommand
from musicbar.service import event_service
import datetime
import logging


class Command(BaseCommand):

    def handle(self, *args, **options):
        com = None
        if len(args) == 1:
            com = args[0]
        
        logging.info(str(datetime.datetime.now()))
        event_service.update_event_data()
        