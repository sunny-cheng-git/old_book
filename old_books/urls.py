"""old_books URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path,re_path
from app01 import views
from django.views.static import serve
from old_books import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('index/',views.index ),
    path('',views.home ),
    path('home/',views.home ),
    path('search/',views.search ),
    re_path('book_detail/(?P<id>\d+)$',views.book_detail ),
    path('category/',views.category ),
    path('shop_car/',views.shop_car ),
    path('sell_book/',views.sell_book ),
    path('sell_in/',views.sell_in ),
    re_path('sell_in_del/(?P<id>\d+)$',views.sell_in_del ),
    re_path('sell_in_edit/(?P<id>\d+)$',views.sell_in_edit ),
    path('login/',views.login ),
    path('logout/',views.logout ),
    path('register/',views.register ),
    path('my_zone/',views.my_zone ),
    path('my_zone/sell_books/',views.my_zone ),
    path('my_balance/',views.my_balance ),
    path('my_bookrack/', views.my_bookrack),
    path('my_zone_info/', views.info),
    path('diggit/', views.diggit),
    re_path('comment_reply/(?P<book_id>\d+)/(?P<comt_id>\d+)/$', views.comment_reply),
    re_path('appraise/(?P<book_id>\d+)/$', views.appraise),
    re_path('shipping_car/(?P<id>.*)$', views.shipping_car),
    re_path('shopping_car_del/(?P<id>.*)$', views.shopping_car_del),
    re_path(r"media/(?P<path>.*)$", serve, {"document_root": settings.MEDIA_ROOT}),

]
