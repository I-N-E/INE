from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('',main,name='main'),
    path('logout/',user_logout,name='user_logout'),
    path('dashboard/<str:name>/',dashboard,name='dashboard'),
    path('dashboard/<str:name>/profile/',profile,name='profile'),
    path('dashboard/<str:name>/public/',public,name='public'),
    path('dashboard/<str:name>/idea/<int:id>/',idea,name='idea'),
    path('view/<int:pk>/',view_project,name='view'),
    path('view/<int:pk>/owner',owner,name='owner'),
    path('following/<int:pk>/',following,name='following'),
    path('good/<int:pk>/',good,name='good'),
    path('follow/<int:pk>/',follow,name='follow'),
    path('follow/<int:pk>/user',folloW,name='folloW'),
    path('delete/<int:pk>/',delete,name='delete'),
    path('idea/complete/<str:name>/<int:id>/',idea_complete,name='idea_complete'),
    path('method/complete/<str:name>/<int:id>/<int:pk>/',method_complete,name='method_complete'),
]

urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

