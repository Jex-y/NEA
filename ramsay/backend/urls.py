from django.urls import path, include
from rest_framework import routers
from .views import *

urlpatterns = [
        path('menus/', ItemMenuListView.as_view(), name='toplevel'),
        path('menus/<str:url_name>', ItemMenuListView.as_view(), name='menu'),
        path('items/search=<str:query>', ItemSearchView.as_view(), name='search'),
        path('items/filter/tags=<str:tags>', ItemFilterView.as_view(), name='filter'),
        path('items/<str:item_id>', ItemDetailView.as_view(), name='itemdetail'),
        path('sessions/new', SessionCreateView.as_view(), name='newsess'),
        path('sessions/validate', SessionValidateView.as_view(), name='validsess'),
        path('sessions/close', SessionCloseView.as_view(), name='closesess'),
        path('orders/new', OrderCreateView.as_view(), name='neworder'),
        path('orders/', ItemOrderListView.as_view(), name='itemorderlist'),
        path('orders/markcompleted', ItemOrderCompleteView.as_view(), name='itemordercomplete'),
        path('orders/session/<str:sess_id>', SessionOrderListView.as_view(), name='sessionorderlist'),
        path('tags/', TagListView.as_view(), name='tags'),
    ]