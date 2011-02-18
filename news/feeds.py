from django.contrib.syndication.views import Feed
from django.conf import settings

from models import News


class LatestNews(Feed):
    title = "Latest Karajlug news."
    link = "/news/"
    description = "What happend in Karajlug?"

    def items(self):
        return News.objects.order_by('-date')[:settings.NEWS_LIMIT]

    def item_content(self, item):
        return item.content

    def item_date(self, item):
        return item.date

    def item_link(self, item):
        return "http://karajlug.org/news/%s/" % item.id
