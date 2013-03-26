# coding: utf-8
# -----------------------------------------------------------------------------
#    Karajlug.org
#    Copyright (C) 2010-2012  Karajlug community
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
from django.conf import settings

from locales.managers import I18nManager


class News(models.Model):
    """
    News module main model
    """
    user = models.ForeignKey(User, editable=False,
                             verbose_name=_("User"))
    title = models.CharField(max_length=60,
                             verbose_name=_("Title"))
    content = models.TextField(verbose_name=_("News content"))
    lang = models.CharField(_("Language"), max_length=8,
                            choices=settings.LANGUAGES,
                            default=settings.LANGUAGE_CODE)

    date = models.DateTimeField(auto_now_add=True, auto_now=False,
                                verbose_name=_('Date and Time'))

    objects = I18nManager()

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return "/%s/news/%s" % (self.lang, self.id)

    #def irc_repr(self, logentry):
    #    if logentry.is_addition():
    #        return ["News: %s added by %s at %s" % (
    #            self.title,
    #            self.user,
    #            self.full_path())]
    #
    #    phrase = ""
    #    if logentry.is_change():
    #        phrase = "changed"
    #    elif logentry.is_delete():
    #        phrase = "deleted"
    #
    #    return ["%s %s a news: %s" % (
    #        self.user,
    #        phrase,
    #        self.full_path())]

    class Meta:
        verbose_name_plural = _("News")
        verbose_name = _('News')
