# coding: utf-8
# -----------------------------------------------------------------------------
#    Karajlug.org
#    Copyright (C) 2010-2013  Karajlug community
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
from calverter import Calverter

from django.conf import settings

import urllib


DAYS_NAMES = ("شنبه", "یکشنبه", "دوشنبه", "سه شنبه",
              "چهارشنبه", "پنج شنبه", "جمعه")

PERSIAN_DIGITS = {"1": "۱", "2": "۲", "3": "۳", "4": "۴", "5": "۵",
                  "6": "۶", "7": "۷", "8": "۸", "9": "۹", "0": "۰"}

MONTHS_NAMES = ("فروردین", "اردیبهشت", "خرداد", "تیر", "مرداد",
                "شهریور", "مهر", "آبان", "آذر", "دی", "بهمن",
                "اسفند")


def format_date(date, lang):
    if lang == "fa":
        cal = Calverter()
        jd = cal.gregorian_to_jd(date.year, date.month,
                                 date.day)

        wday = cal.jwday(jd)
        jalali = cal.jd_to_jalali(jd)

        result = "%s، %d %s %d" % (DAYS_NAMES[wday], jalali[2],
                                   MONTHS_NAMES[jalali[1] - 1], jalali[0])
        return to_persian_digits(result)
    return date


def to_persian_digits(datestr):
    for i in PERSIAN_DIGITS:
        datestr = datestr.replace(i, PERSIAN_DIGITS[i])

    return datestr


def quote(url):
    return urllib.quote_plus("%s" % url)


def full_path(absolute_url):
    site = getattr(settings, "URL", "www.karajlug.org")
    return "http://%s%s" % (site, absolute_url)