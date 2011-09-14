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
import hashlib
import socket

from django.http import Http404, HttpResponse, HttpResponseForbidden
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt

from forms import WebServiceForm


@csrf_exempt
def webservice(request):
    """
    Simple HTTP POST service.
    """
    if not request.method == "POST":
        raise Http404()

    form = WebServiceForm(request.POST)
    if form.is_valid():
        try:
            user = User.objects.get(username=form.cleaned_data["user"])
        except User.DoesNotExist:
            raise Http404()

        m = hashlib.sha1()
        m.update("%s%s" % (form.cleaned_data["msg"],
                           user.password))

        hash_ = m.hexdigest()
        if not hash_ == form.cleaned_data["hash"]:
            return HttpResponseForbidden()
        sock = socket.socket(socket.AF_UNIX,
                             socket.SOCK_STREAM)
        try:
            sock.connect("/tmp/socket")

            sock.send(form.cleaned_data["msg"])
            sock.recv(1024)
        except socket.error:
            pass
        sock.close()
        return HttpResponse("0")
    else:
        return HttpResponse(form.errors)
