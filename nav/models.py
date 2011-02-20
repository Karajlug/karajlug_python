from django.db import models
from django.contrib.auth.models import Permission, Group
from django.template.defaultfilters import slugify

class NavigationTree(models.Model):
    name = models.CharField(max_length=16)
    slug = models.CharField(max_length=16, blank=True, null=True)

    def __unicode__(self):
        return self.name

    def get_trunk(self):
        return NavigationItem.objects.filter(tree=self, parent=None).all().order_by('priority')

    def save(self):
        if self.slug == "":
            self.slug = slugify(self.name).replace('-', '_')

        super(NavigationTree, self).save()

        
class NavigationItem(models.Model):
    label = models.CharField(max_length=32)
    title = models.CharField(max_length=128, blank=True, null=True)
    location = models.CharField(max_length=256)
    priority = models.PositiveIntegerField(default=0)
    required_permissions = models.ManyToManyField(Permission, null=True, blank=True)
    required_group = models.ManyToManyField(Group, null=True, blank=True)
    image = models.ImageField(upload_to='navigation/image',null=True, blank=True)
    parent = models.ForeignKey('self', blank=True, null=True,
        related_name='children')

    tree = models.ManyToManyField(NavigationTree, blank=True, null=True,
                                  help_text="A navigation tree is a certain collection of"
                                      "navigation items, so that different navigation bars"
                                      "can exist.")

    def get_children(self):
        return self.children.all().order_by('priority')

    def __unicode__(self):
        return self.label

