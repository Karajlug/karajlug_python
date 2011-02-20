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
from django.contrib.auth.models import Permission, Group
from django.template.defaultfilters import slugify


class NavigationTree(models.Model):
    name = models.CharField(max_length=16)
    slug = models.CharField(max_length=16, blank=True, null=True)

    def __unicode__(self):
        return self.name

    def get_trunk(self):
        return NavigationItem.objects.filter(\
            tree=self, parent=None).all().order_by('priority')

    def save(self):
        if self.slug == "":
            self.slug = slugify(self.name).replace('-', '_')

        super(NavigationTree, self).save()


class NavigationItem(models.Model):
    label = models.CharField(max_length=32)
    title = models.CharField(max_length=128, blank=True, null=True)
    location = models.CharField(max_length=256)
    priority = models.PositiveIntegerField(default=0)
    required_permissions = models.ManyToManyField(Permission,
                                                  null=True, blank=True)
    required_group = models.ManyToManyField(Group, null=True, blank=True)
    image = models.ImageField(upload_to='statics/upload/image',
                              null=True, blank=True)
    parent = models.ForeignKey('self', blank=True, null=True,
        related_name='children')
    # TODO: mark the helptext for translation.
    tree = models.ManyToManyField(NavigationTree, blank=True, null=True,
                            help_text="A navigation tree is a certain collection of"
                            "navigation items, so that different navigation bars"
                            "can exist.")

    def get_children(self):
        return self.children.all().order_by('priority')

    def __unicode__(self):
        return self.label
