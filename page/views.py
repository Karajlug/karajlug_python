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

from django.shortcuts import render_to_response as rr
from django.http import Http404
from django.template import RequestContext
from django.utils.translation import ugettext as _

from page.models import Page


def show_page(request, slug):
    """
    show the page with the given slug
    """
    try:
        page = Page.objects.get(slug=slug,
                                publish=True)

    except Page.DoesNotExist:
        raise Http404()

    return rr("page.html",
              {"page": page,
               "title": "%s | %s" % (_("Karajlug"), page.title)},
              context_instance=RequestContext(request))
