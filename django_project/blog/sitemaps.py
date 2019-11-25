from django.contrib.sitemaps import Sitemap
from .models import Post


class PostSitemap(Sitemap):
    changefreq = 'always'
    priority = 1.0

    def items(self):
        return Post.published.all()

    def lastmod(self, obj):
        return obj.updated
