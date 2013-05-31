from django.conf.urls.defaults import *
from musicbar import settings

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Example:

    (r'^$', "musicbar.view.index.city_slug_handler"),
    (r'^init/$', "musicbar.view.base.init"),
    (r'^sitemap/$', "musicbar.view.index.sitemap"),
    
    
    (r'^ajax/find-events/$', "musicbar.view.ajax.find_events"),
    (r'^ajax/get-event/$', "musicbar.view.ajax.get_event"),
    
    #admin events
    (r'^admin/$', "musicbar.view.admin.home.index"),
    (r'^admin/event-sources/$', "musicbar.view.admin.event.sources"),
    (r'^admin/manage-events/$', "musicbar.view.admin.event.manage"),
    (r'^admin/toggle-event-source/$', "musicbar.view.admin.event.toggle_source"),    
    (r'^admin/add-event-source/$', "musicbar.view.admin.event.add_source"),
    (r'^admin/change-event-source-cat/$', "musicbar.view.admin.event.change_event_source_cat"),
    (r'^admin/change-event-cat/$', "musicbar.view.admin.event.change_event_cat"),
    (r'^admin/remove-event-source/$', "musicbar.view.admin.event.remove_source"),
    (r'^admin/remove-event/$', "musicbar.view.admin.event.remove_event"),        
    (r'^admin/ajax/toggle-event-featured/$', "musicbar.view.admin.event.toggle_event"),
    (r'^admin/ajax/find-events/$', "musicbar.view.admin.event.find_events"),
    
    (r'^(?P<city_slug>[^/]+)/$', "musicbar.view.index.city_slug_handler"),
    
    
    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # (r'^admin/', include(admin.site.urls)),
)

#if settings_local.STATIC_SERVER:
if settings.DEBUG:
    urlpatterns += patterns('', (r'^(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}))