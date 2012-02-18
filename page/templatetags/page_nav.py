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

from django import template
from django.template.loader import render_to_string

from page.models import Page


register = template.Library()


def navigation(parser, token):
    return NavigationNode()


class NavigationNode(template.Node):

    def render(self, context):
        nav_pages = Page.pages.filter(menu=True).order_by("-weight")
        rendered_template = render_to_string("nav.html",
                                             {"pages": nav_pages})
        return rendered_template

register.tag("navigation", navigation)
