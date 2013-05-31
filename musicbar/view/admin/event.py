'''
Created on Dec 31, 2010

@author: par
'''
from musicbar.view import base
from musicbar.models import EventSource, Event
from django.http import HttpResponse
from django.shortcuts import render_to_response
from musicbar.service.lastfm_service import LastFmService
from django.core.paginator import Paginator



def sources(request):
    vars = {'admin_title':'Manage Event Sources'}
    sources = EventSource.objects.filter()
    vars['sources'] = sources
    return base.render(request, "admin/event_sources.html", vars, True)

def manage(request):
    vars = {'admin_title':'Manage Events'}
    try:
        pg = int(request.GET.get('pg', 1))
    except ValueError:
        pg = 1
    cat = request.GET.get('cat', 'All')
    
    vars['cat'] = cat
    
    events = Event.objects.filter(deleted=False).order_by('start_time')
    if cat != 'All':
        events = events.filter(category=cat)
    paginator = Paginator(events, 100)
    page = paginator.page(pg)
    vars['events']=  page.object_list
    vars['paginator'] = paginator
    vars['page'] = page 
    vars['pg'] = pg
    return base.render(request, "admin/manage_events.html", vars)



#####################
# ajax be down yonder
#####################


def add_source(request):
    url = request.GET.get('url', '')
    name = request.GET.get('name', '')
    proxy = request.GET.get('proxy', '')
    if id != None and name != None:
        s = EventSource()
        s.name = name.strip()
        s.url = url.strip()
        s.proxy = proxy.strip()
        s.save()
        return HttpResponse(content="Added!")
    return HttpResponse(content="Problemo %s %s" % (url, name))
        
def remove_source(request):
    id = request.GET.get('id', None)
    if id != None:
        s = EventSource.objects.get(id=id)
        s.delete()
        return HttpResponse(content='Done!')
    return HttpResponse(content='El Nopeo')

def remove_event(request):
    id = request.GET.get('id', None)
    if id != None:
        e = Event.objects.get(id=id)
        e.deleted = True
        e.save()
        return HttpResponse(content='Done!')
    return HttpResponse(content='El Nopeo')

def toggle_event(request):
    id = request.GET.get('id', None)
    if id == None:
        return HttpResponse(content="Nope")
    e = Event.objects.get(id=id)
    e.featured = not e.featured
    e.save()
    if e.featured:        
        return HttpResponse(content="Featured!")
    else:
        return HttpResponse(content="Un-featured!")

def toggle_source(request):
    id = request.GET.get('id', None)
    if id == None:
        return HttpResponse(content="Nope")
    source = EventSource.objects.get(id=id)
    source.active = not source.active
    source.save()
    if source.active:        
        return HttpResponse(content="Activated!")
    else:
        return HttpResponse(content="De-activated!")

def change_event_source_cat(request):
    id = request.GET.get('id', None)
    cat = request.GET.get('cat', None)
    if id == None or cat == None:
        return HttpResponse(content="Nope")
    source = EventSource.objects.get(id=id)
    source.category = cat
    source.save()
    return HttpResponse(content="Saved category: " + cat)

def change_event_cat(request):
    id = request.GET.get('id', None)
    cat = request.GET.get('cat', None)
    if id == None or cat == None:
        return HttpResponse(content="Nope")
    source = Event.objects.get(id=id)
    source.category = cat
    source.save()
    return HttpResponse(content="Saved category: " + cat)    

def find_events(request):
    name = request.GET.get('name', None)
    start = request.GET.get('start', None)
    end = int(request.GET.get('end', 20))
    if start == None:
        start = end - 20
    vars= {}
    
    events = Event.objects.filter().order_by('start_time')
    if name != None:
        events = events.filter(artists__name__istartswith=name)
    vars['events'] = events[start:end]
    return render_to_response("admin/ajax/event_list_item.html", vars)
