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
from django.core.paginator import Paginator
from django.template import RequestContext
from django.http import Http404
from django.utils.translation import get_language

from .models import Member


def members_index(request):
    """
    Main index of members.
    """
    members = Member.objects.all().order_by("weight")
    # god damn b3hnam's server
    members = [(i + 1, j) for i, j in enumerate(members)]
    # ---
    return rr("members.html", {"members": members},
              context_instance=RequestContext(request))


def member_view(request, id):
    """
    View each member details.
    """
    from models import MemberDetail

    try:
        member = Member.objects.get(id=id)
    except Member.DoesNotExist:
        raise Http404()

    # TODO: lang code here
    details = MemberDetail.objects.filter(member=member).order_by("weight")
    return rr("member_view.html", {"member": member,
                                   "details": details},
              context_instance=RequestContext(request))
