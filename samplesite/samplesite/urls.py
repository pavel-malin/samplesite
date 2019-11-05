from django.contrib import admin
from django.urls import path

from bboard.views import index, by_rubric, BbCreateView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('<int:rubric_id>/', by_rubric, name='by_rubric'),
    path('', index),
    path('bboard/', index, name='index'),
    path('add/', BbCreateView.as_view(), name='add'),
]
