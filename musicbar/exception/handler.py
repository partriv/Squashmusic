'''
Created on May 12, 2009

@author: par
'''
import logging

import traceback


class middleware:
    """
    Exception handling middleware to intercept the 
    exception and output to a log file
    """
    
    
    def process_exception(self, request, exception):
        tb_text = traceback.format_exc()
        url = request.build_absolute_uri()
        request.META['wsgi.errors'].write(url + '\n' + str(tb_text) + '\n')
        logging.debug("Musicbar fatal exception" + str(exception))
        #logging.fatal(traceback.format_exc())
        return None