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

from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _


class FAQ(models.Model):
    """
    FAQ main model
    """
    user = models.ForeignKey(User, editable=False,
                             verbose_name=_("User"))
    question = models.CharField(max_length=150,
                                verbose_name=_("Question"))
    answer = models.TextField(verbose_name=_("Answer"))

    lang = models.CharField(_("Language"), max_length=8,
                            choices=settings.LANGUAGES,
                            default=settings.LANGUAGE_CODE)

    date = models.DateTimeField(auto_now_add=True, auto_now=False,
                                verbose_name=_('Date and Time'))

    def __unicode__(self):
        return self.question

    class Meta:
        verbose_name_plural = _("FAQ")
        verbose_name = _('Question')
