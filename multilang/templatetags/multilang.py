# -----------------------------------------------------------------------------
#    Vanda multilang
#    Copyright (C) 2012  Sameer Rahmani <lxsameer@gnu.org>
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
from django import template
from django.core.urlresolvers import reverse as rev
from django.conf import settings


register = template.Library()


@register.tag(name="reverse")
def reverse(parser, token):
    try:
        # split_contents() knows not to split quoted strings.
        tag_name, format_string = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError(
            "%r tag requires a single argument" % token.contents.split()[0])
    if not (
        format_string[0] == format_string[-1] and \
        format_string[0] in ('"', "'")):

        raise template.TemplateSyntaxError(
            "%r tag's argument should be in quotes" % tag_name)

    return ReverseUrl(format_string[1:-1])


class ReverseUrl(template.Node):

    def __init__(self, format_string):
        self.path = format_string

    def render(self, context):
        return rev(self.path, args=[], urlconf=settings.LEAF_URLCONF)
