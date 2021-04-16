from django.urls import path

from .views import *

urlpatterns = [
    path('get_all/', get_all_data, name="get_all" ),
    path('post_base/', post_base_data, name="post_base" ),
    path('delete_all/', delete_all, name="delete_all" ),
]