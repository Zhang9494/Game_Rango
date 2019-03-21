from django.conf.urls import url
from game import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^about/$', views.about, name='about'),
    url(r'^add_category/$', views.add_category, name='add_category'),

    url(r'^category/$', views.list_category, name='list_category'),

    url(r'^category/(?P<category_name_slug>[\w\-]+)/$',
        views.show_category,
        name='show_category'),

    url(r'^category/(?P<category_name_slug>[\w\-]+)/add_game/$',
        views.add_game,
        name='add_game'),

    url(r'^game/(?P<game_name_slug>[\w\-]+)/$',
        views.show_game,
        name='show_game'),

    url(r'^like/$',views.like_game, name='like_game'),

    url(r'^register/$',
        views.register,
        name='register'),

    url(r'^login/$', views.user_login, name='login'),
    url(r'^logout/$', views.user_logout, name='logout'),
    url(r'^profile/(?P<username>[\w\-]+)/$', views.profile, name='profile'),
]