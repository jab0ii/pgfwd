from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = patterns(
    '',
    url(r'^$', 'pageitforward.views.index', name='landing'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^API/loginStatus', 'users.views.APILoginStatus'),
    url(r'^API/login', 'users.views.APILogin'),
    url(r'^API/logout', 'users.views.APILogout'),
    url(r'^API/users$', 'users.views.APIUsers'),
    url(r'^API/contactmethods$', 'users.views.APIContactMethods'),
    url(r'^API/contactmethods/(?P<contactMethodID>[0-9]+)$',
        'users.views.APIContactMethodUpdateDelete'),
    url(r'^API/orgs$', 'orgs.views.APIOrgsPost'),
    url(r'^API/associateUser$', 'orgs.views.APIJoinOrg'),
    url(r'^API/orgs/(?P<orgID>[0-9]+)$', 'orgs.views.APIOrgsGet'),
    url(r'^API/orgUsers/(?P<orgID>[0-9]+)$', 'orgs.views.APIOrgMembers'),
    url(r'^API/eventhandlers$', 'eventhandlers.views.APIEventHandlers'),
    url(r'^API/eventhandlers/(?P<handlerID>[0-9]+)$',
        'eventhandlers.views.APIEventHandlerUpdateDelete'),
    url(r'API/getEscalationData',
        'events.views.APIGetEscalationData'),
    url(r'API/getEventStatus',
        'events.views.APIGetEventStatus'),
    url(r'API/createEvent',
        'events.views.APICreateEvent'),
    url(r'API/ackEvent',
        'events.views.APIAckEvent'),
    url(r'API/createLogEvent', 'logevent.views.APICreateLogEvent'),
    url(r'^API/getLogEvent$', 'logevent.views.APIGetLogEvent'),

) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
