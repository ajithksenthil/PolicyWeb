from django.urls import path
from . import views

urlpatterns = [
    path('', views.PostListView.as_view(), name='all-policy-cards'),
    path('<uuid:eid>/', views.PostView.as_view(), name='specific-policy-cards'),
    path('<uuid:eid>/comments/', views.PostCommentsView.as_view(), name='post-comments'),

]
