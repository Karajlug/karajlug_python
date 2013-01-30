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

from calverter import calverter

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
        return "/news/%s" % self.id

    def full_path(self):
        from django.conf import settings
        site = getattr(settings, "URL", "www.karajlug.org")
        return "%s%s" % (site, self.get_absolute_url())

    def to_persian_digits(self, datestr):
        pnum = {"1": u"۱", "2": u"۲", "3": u"۳", "4": u"۴", "5": u"۵",
                "6": u"۶", "7": u"۷", "8": u"۸", "9": u"۹", "0": u"۰"}
        
        for i in pnum:
            datestr = datestr.replace(i, pnum[i])
        
        return datestr
        
    def pdate(self):
        days_names = (u"شنبه", u"یک‌شنبه", u"دوشنبه", u"سه‌شنبه", u"چهارشنبه", u"پنج‌شنبه")
        months_names = (u"فروردین", u"اردیبهشت", u"خرداد", u"تیر", u"مرداد", u"شهریور",
                        u"مهر", u"آبان", u"آذر", u"دی", u"بهمن", u"اسفند")
        
        date = self.date
        cal = calverter()
        jd = cal.gregorian_to_jd(date.year, date.month, date.day)
        wday = cal.jwday(jd)
        jalali = cal.jd_to_jalali(jd)
        result = u"%s، %d %s %d" % (days_names[wday], jalali[2], months_names[jalali[1]], jalali[0])
        
        return self.to_persian_digits(result)

    def irc_repr(self, logentry):

        if logentry.is_addition():
            return ["News: %s added by %s at %s" % (
                self.title,
                self.user,
                self.full_path())]

        phrase = ""
        if logentry.is_change():
            phrase = "changed"
        elif logentry.is_delete():
            phrase = "deleted"

        return ["%s %s a news: %s" % (
            self.user,
            phrase,
            self.full_path())]

    class Meta:
        verbose_name_plural = _("News")
        verbose_name = _('News')
