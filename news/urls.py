from django.conf.urls.defaults import patterns
from news.feeds import LatestNews


urlpatterns = patterns('',
        (r'^feed/$', LatestNews()),
        (r'^(\d+)/$', 'news.views.news_entry'),
        (r'^$', 'news.views.index'),

)
