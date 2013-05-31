'''
Created on Jan 2, 2011

@author: par
'''
from musicbar.view import base

def index(request):
    vars = {}
    return base.render(request, "admin/home.html", vars, True)