from django.conf.urls.defaults import patterns
from news.feeds import LatestNews


urlpatterns = patterns('',
        (r'^feed/$', LatestNews()),
        (r'^(\d+)/$', 'views.news_entry')
        (r'^$', '.views.index'),

)
