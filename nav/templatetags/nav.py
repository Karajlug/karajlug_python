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

from django import template
from django.template.loader import get_template
from django.conf import settings
from apps.nav.models import NavigationTree, NavigationItem

register = template.Library()

class NavigationTreeNode(template.Node):
    slug = None
    user = None

    def __init__(self, slug, user):
        self.slug = template.Variable(slug)
        self.user = template.Variable(user)

    def get_tree(self, tree, user):
        t = get_template('navigation/tree.html')
        c = template.Context(
            {
                'mainitem': tree.get_trunk(),
                'parent' : tree,
                'user': user 
            }
        )
        return t.render(c)

    def render(self, context):
        try:
            navigation = NavigationTree.objects.get(slug=self.slug)

            return self.get_tree(navigation, self.user)

        except template.VariableDoesNotExist:
            return ''

@register.tag(name='navtree')
def navtree(parser, token):
    try:
        tag_name, tree_name, user = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError, "%s tag requires exactly 2 arguments. A tree access name and a user."

    return NavigationTreeNode(tree_name, user)


class NavigationChildNode(template.Node):
    tree = None
    user = None

    def __init__(self, tree, user):
        self.tree = template.Variable(tree)
        self.user = template.Variable(user)

    def get_child(self, navnode, user):
        t = get_template('navigation/children.html')
        
        c = template.Context(
            
            {
                'mainitem': navnode.get_children(),

                'user': user 
            }
        )
        
        return t.render(c)

    def render(self, context):
        try:
            navnode = NavigationItem.objects.get(id=self.tree.resolve(context).id)
            return self.get_child(navnode, self.user)

        except : # template.VariableDoesNotExist:
            return ''

@register.tag(name='navchild')
def navtree(parser, token):
    try:
        tag_name, tree, user = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError, "%s tag requires exactly 2 arguments. A tree access name and a user."

    return NavigationChildNode(tree, user)

"""
class NavigationBranchNode(template.Node):
#    branch = None
#    user = None

    def __init__(self, branch, user):
        self.branch = template.Variable(branch)
        self.user = template.Variable(user)

    def render(self, context):
        try:
            t = get_template('navigation/branch.html')
            c = template.Context(
                {
                    'branch': self.branch.resolve(context),
                    'user': self.user.resolve(context),
                    'list_a': [1,2,3,4],
                    'list_b': [1,2,3,4,5,6,7,8,9],
                }
            )

        except template.VariableDoesNotExist:
            return ''

        return t.render(c)

@register.tag(name='navbranch')
def navbranch(parser, token):
    try:
        tag_name, branch, user = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError, "%s tag requires exactly 2 arguments. A branch and the user."

    return NavigationBranchNode(branch, user)

@register.filter(name='navleaf_authorized')
def navleaf_authorized(user, leaf):
    if leaf.guests_hidden and user.is_authenticated() is False:
        return False

    if leaf.guests_only and user.is_authenticated() is True:
        return False

    if leaf.staff_only and user.is_staff is False:
        return False

    return user.has_perms(leaf.required_permissions.all())
"""


