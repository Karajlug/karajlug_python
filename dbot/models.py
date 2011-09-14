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

import socket

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.admin.models import LogEntry
from django.contrib.contenttypes.models import ContentType


@receiver(post_save, sender=LogEntry)
def irc_send(signal, sender, **kwargs):

    obj = ContentType.objects.get(
        app_label=kwargs["instance"].content_type.app_label,
        model=kwargs["instance"].content_type.model)
    obj = obj.get_object_for_this_type(id=kwargs["instance"].object_id)

    func = getattr(obj, "irc_repr", None)

    msg = "Karajlug.org: %s model has been changed by %s.\n" % \
          (kwargs["instance"].content_type, kwargs["instance"].user)

    if func:
        msg = func()
        msg = "\r\n".join(msg)

    sock = socket.socket(socket.AF_UNIX,
                         socket.SOCK_STREAM)
    try:
        sock.connect("/tmp/socket")

        sock.send(msg)
        sock.recv(1024)
    except socket.error:
        pass
    sock.close()
