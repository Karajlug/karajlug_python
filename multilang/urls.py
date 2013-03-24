# -----------------------------------------------------------------------------
#    Vanda multilang
#    Copyright (C) 2012  Sameer Rahmani <lxsameer@gnu.org>
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

from django.conf.urls import patterns, include, url
from django.conf import settings

from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^admin/', include(admin.site.urls)),
)

if settings.DEBUG:
    urlpatterns += patterns(
        '',
        (r'^statics/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': os.path.join(os.path.dirname(__file__),
         '../statics/').replace('\\', '/')}),
    )

urlpatterns += patterns(
    '',
    (r'^(en|fa)/', 'multilang.dispatcher.dispatch_url'),
    (r'^(en|fa)$', 'multilang.dispatcher.dispatch_url'),
    (r'^$', 'multilang.dispatcher.dispatch_url'),
    (r'.*', 'multilang.dispatcher.dispatch_url'),
)
