import sys
import os
import socket

from django.db import models

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.admin.models import LogEntry


@receiver(post_save, sender=LogEntry)
def irc_send(signal, sender, **kwargs):

    print "<<< ", sender.user.field.__dict__

    msg = "model %s has been changed by %s\n" % \
                            (sender.content_type, signal)
    sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    sock.connect("/tmp/socket")
    sock.send(msg)
    data = sock.recv(1024)
    sock.close()
