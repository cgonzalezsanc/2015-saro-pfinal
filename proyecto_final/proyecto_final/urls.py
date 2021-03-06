from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'proyecto_final.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^login$', 'django.contrib.auth.views.login'),
    url(r'^logout$', 'actividades.views.log_out'),
    url(r'^accounts/profile/$', 'actividades.views.successful_login'),
    url(r'^$', 'actividades.views.main_page'),
    url(r'^rss$', 'actividades.views.main_rss'),
    url(r'^ranking/visitas$', 'actividades.views.ranking_visitas'),
    url(r'^css/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.STATIC2_URL
        }),
    url(r'^img/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.STATIC2_URL
        }),
    url(r'^ayuda$', 'actividades.views.help'),
    url(r'^todas$', 'actividades.views.all_events'),
    url(r'^todas/historial$', 'actividades.views.historial_actus'),
    url(r'^actividad/(.*)$', 'actividades.views.event'),
    url(r'^(.*)/rss$', 'actividades.views.user_rss'),
    url(r'^(.*)$', 'actividades.views.user'),
)
