from django.conf.urls.defaults import *
from django.contrib import admin


admin.autodiscover()

urlpatterns = patterns('',
    (r'^$', 'views.index'),
    (r'^admin/', include(admin.site.urls)),
)
