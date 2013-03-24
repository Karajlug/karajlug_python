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
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _
from django.conf import settings

from locales.managers import I18nManager


class Page(models.Model):
    """
    Page main model class
    """
    user = models.ForeignKey(User, editable=False,
                             verbose_name=_("User"))
    title = models.CharField(max_length=64,
                             verbose_name=_("Title"))
    slug = models.SlugField(max_length=30, unique=True,
                            verbose_name=_("Slug"))

    # IMPORTANT: content field will render as html
    content = models.TextField(verbose_name=_("News content"))
    publish = models.BooleanField(default=False,
                                  verbose_name=_("Publish"))
    menu = models.BooleanField(default=False,
                               verbose_name=_("Appear in navigation?"))

    lang = models.CharField(_("Language"), max_length=8,
                            choices=settings.LANGUAGES,
                            default=settings.LANGUAGE_CODE)

    date = models.DateTimeField(auto_now_add=True, auto_now=False,
                                verbose_name=_('Date and Time'))

    weight = models.IntegerField(_("Weight"), default=50)

    pages = I18nManager()
    objects = models.Manager()

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return "/page/%s" % self.slug

    def irc_repr(self, logentry):

        phrase = "added"
        if logentry.is_change():
            phrase = "change"

        return ["%s page %s by %s at %s" % (
            self.title,
            phrase,
            self.user,
            self.get_absolute_url())]

    class Meta:
        verbose_name_plural = _("Pages")
        verbose_name = _('Page')


class FirstPage(models.Model):
    user = models.ForeignKey(User, editable=False,
                             verbose_name=_("User"))

    title = models.CharField(max_length=64,
                             verbose_name=_("Title"))

    # IMPORTANT: content field will render as html
    content = models.TextField(verbose_name=_("News content"))

    lang = models.CharField(_("Language"), max_length=8,
                            choices=settings.LANGUAGES,
                            default=settings.LANGUAGE_CODE)

    date = models.DateTimeField(auto_now_add=True, auto_now=False,
                                verbose_name=_('Date and Time'))

    objects = I18nManager()

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name_plural = _("First Pages")
        verbose_name = _('First Page')

        ordering = ["date", ]
