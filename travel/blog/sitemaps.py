from django.contrib.sitemaps import Sitemap
from django.urls import reverse


class StaticViewSitemap(Sitemap):
    priority = 1.0
    changefreq = 'weekly'

    def items(self):
        return ['index', 'about', 'contact', 'destination', 'blogz',
                'vacancy', 'search', 'covid19nepal',
                'newsletter_unsubscribe']

    def location(self, item):
        return reverse(item)
