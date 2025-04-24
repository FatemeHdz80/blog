from django.urls import path
from . import views
from django.contrib.auth import views as auth_views



app_name = 'blog'

urlpatterns = [
    # path("", views.PostListView.as_view(), name="post_list"),
    path("", views.post_list, name="post_list"),
    path("tag/<slug:tag_slug>/", views.post_list, name="post_list_by_tag"),
    path("<int:year>/<int:month>/<int:day>/<slug:post>/", views.post_detail, name="post_detail"),
    path("<int:post_id>/share/", views.post_share, name="post_share"),
    path('login/', views.login_user, name="login_user"),
    path('logout/', views.logout_user, name="logout_user"),
    path('about/', views.about, name="about"),
    path('contact/', views.contact_view, name='contact'),
    path('signup/', views.signup_user, name='signup_user'),
]
