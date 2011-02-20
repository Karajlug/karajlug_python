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


def _item_is_active(request, item):
    return (item.location == request.GET('REQUEST_URI'))


def navigation_items(request):
    from models import NavigationItem, NavigationTree

    navigation_trees = NavigationTree.objects.all()
    navigation_items = {}

    for tree in navigation_trees:
        navigation_items['navigation_%s' % tree.access_name] = \
                NavigationItem.objects.filter(tree=tree, parent=None).order_by('priority')

    return navigation_items
