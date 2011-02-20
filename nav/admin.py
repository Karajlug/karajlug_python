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

import re
from django.contrib import admin

from models import NavigationItem, NavigationTree


url_re = re.compile(r'^(https??://([a-zA-Z0-9]+\.)+[a-zA-Z0-9]([:@][a-zA-Z0-9@%-_\.]){0,2})?/\S*$')


class NavigationItemAdmin(admin.ModelAdmin):
    list_filter = ('tree',)
    list_display = ('label', 'title', 'location',)


class NavigationTreeAdmin(admin.ModelAdmin):
    pass

admin.site.register(NavigationItem, NavigationItemAdmin)
admin.site.register(NavigationTree, NavigationTreeAdmin)
