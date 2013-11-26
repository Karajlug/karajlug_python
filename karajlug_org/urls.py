# -----------------------------------------------------------------------------
#    Karajlug.org
#    Copyright (C) 2010  Karajlug community
#
#    This program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 2 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License along
#    with this program; if not, write to the Free Software Foundation, Inc.,
#    51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
# -----------------------------------------------------------------------------

import os

from django.conf.urls import *
from django.contrib import admin
from django.conf import settings

admin.autodiscover()

urlpatterns = patterns(
    '',
    (r'^faq/$', "faq.views.index"),
    (r'^news/', include('news.urls')),
    (r'^page/', include('page.urls')),
    (r'^members/', include('members.urls')),
    (r'^books/', include('books.urls')),
    (r'^bot/', include('dbot.urls')),
    (r'^contact/$', 'karajlug_org.views.contact'),
    (r'^$', 'karajlug_org.views.index'),
    (r'^admin/', include(admin.site.urls)),
)

# Local media serving.
if settings.DEBUG:
    urlpatterns += patterns(
        '',
        (r'^statics/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': os.path.join(os.path.dirname(__file__),
         '../statics').replace('\\', '/')}),
    )
