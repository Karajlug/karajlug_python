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

from django.contrib.syndication.views import Feed
from django.conf import settings

from .models import News


class LatestNews(Feed):
    title = "Latest Karajlug news."
    link = "/news/"
    description = "What happend in Karajlug?"

    def items(self):
        return News.objects.order_by('-date')[:settings.NEWS_LIMIT]

    def item_description(self, item):
        return item.content

    def item_date(self, item):
        return item.date

    def item_link(self, item):
        return "http://karajlug.org/news/%s/" % item.id
