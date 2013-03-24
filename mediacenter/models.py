# -----------------------------------------------------------------------------
#    Karajlug.org
#    Copyright (C) 2010-2012 Karajlug community
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

from django.db import models
from django.utils.translation import ugettext as _
from django.contrib.auth.models import User


class UploadFile(models.Model):
    """
    This model store the address of uploads files.
    """

    ufile = models.FileField(_("File"), upload_to="uploads/")
    user = models.ForeignKey(User, editable=False,
                             verbose_name=_("User"))
    date = models.DateTimeField(auto_now_add=True, auto_now=False,
                                verbose_name=_('Date and Time'))

    def get_address(self):
        return "/statics/%s" % self.ufile

    class Meta:
        verbose_name = _("upload file")
        verbose_name_plural = _("upload files")
