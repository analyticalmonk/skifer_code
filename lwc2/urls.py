from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
      url(r'^booboo', include(admin.site.urls)),
      url(r'^$', 'joins.views.home', name='home'),
      url(r'^legal$', 'joins.views.legal', name='legal'),
      url(r'^logodesign$', 'joins.views.logodesign', name='logodesign'),
      url(r'^(?P<ref_id>.*)$', 'joins.views.share', name = 'share'),
    # url(r'^blog/', include('blog.urls')),
)
