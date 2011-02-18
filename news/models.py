from django.db import models
from django.utils.translation import ugettext as _
from django.contrib.auth.models import User


class News(models.Model):
    """
    News module main model
    """
    user = models.ForeignKey(User,
                             verbose_name=_("User"))
    title = models.CharField(max_length=60,
                            verbose_name=_("Title"))
    content = models.TextField(verbose_name=_("News content"))
    date = models.DateTimeField(auto_now_add=True, auto_now=False,
                                     verbose_name=_('Date and Time'))

    def __init__(self):
        return self.title

    class Meta:
        verbose_name_plural = _("News")
        verbose_name = _('News')
