"""BiSheServer URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import path, re_path
from django.urls import path, include
from django.conf import settings
from django.views import static
from django.views.generic import RedirectView
from BiSheServer.settings import default


if default["use_log"] == 'True':
    # 启用日志定时任务
    from api import crontab

urlpatterns = [
    path('', include('BiShe.urls')),
    re_path('api/', include('api.urls')),
    re_path('user/', include('user.urls')),
    re_path('movie/', include('movie.urls')),
    # path('movieinfo/<int:movie_id>', ContentView.as_view(), name='movieinfo'),
    re_path('test/', include('TestServer.urls')),
    re_path('^static/(?P<path>.*)$', static.serve,
        {'document_root': settings.STATIC_ROOT}, name='static'),  # 静态资源加载
    re_path(r'^favicon.ico$', RedirectView.as_view(url=r'static/images/icon.ico')),

]

# 如果是调式状态
if settings.DEBUG:
    import debug_toolbar

    # 设置项目上线的静态资源路径
    # url('^static/(?P<path>.*)$', static.serve,
    #     {'document_root': settings.STATIC_ROOT}, name='static'),
    urlpatterns = [
                      path('__debug__/', include(debug_toolbar.urls)),
                  ] + urlpatterns

# 全局404,500配置
handler404 = "api.views.page_not_found"
handler500 = "api.views.page_error"
