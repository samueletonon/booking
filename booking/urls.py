from django.urls import path

from . import views

urlpatterns = [
    path('', views.book, name='book'),
    path('pubsub', views.pubsub, name='pubsub'),
]
