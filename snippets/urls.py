"""tutorial URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.views.decorators.cache import cache_page
from rest_framework import routers
from rest_framework.urlpatterns import format_suffix_patterns

from snippets import views

urlpatterns = [

    url(r'^$', views.SnippetList.as_view()),
    url(r'(?P<pk>[0-9]+)$', views.SnippetDetail.as_view()),

    # url(r'^users/$',cache_page(60*15)(views.UserList.as_view())),
    url(r'^users/$',views.UserList.as_view()),
    url(r'^users/(?P<pk>[0-9]+)/$',views.UserDetail.as_view()),
    # url(r'^$', views.snippet_list),
    # url(r'(?P<pk>[0-9]+)$', views.snippet_detail),

    # url(r'^', include(router.urls)),
    # url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
    # path('admin/', admin.site.urls),
]

urlpatterns = format_suffix_patterns(urlpatterns)
