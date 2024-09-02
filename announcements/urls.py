from django.urls import path
from django.conf.urls.static import static
from django.conf import settings

from . import views

urlpatterns=[
    path('',views.home,name='home'),
    path('register',views.register,name='register'),
    path('login',views.login,name='login'),
    path('club_login',views.club_login,name='club_login'),
    path('logout',views.logout,name='logout'),
    path('club/<club_id>',views.club,name='club_page'),
    path('create_event/<club_id>',views.create_event,name='create_event'),
    path('clogin',views.clogin,name='clogin'),
    path('slogin',views.slogin,name='slogin'),
    path('event_register/<event_id>',views.event_register,name='event_register'),
    path('edit_details',views.edit_details,name='edit_details'),
    path('upd_stu',views.upd_stu,name='upd_stu'),
    path('add_member',views.add_member,name='add_member'),
    path('dashboard',views.dashboard,name='dashboard'),
    path('mark_complete/<event_id>',views.mark_complete,name='mark_complete'),
    path('view_details/<event_id>',views.view_details,name='view_details'),
    path('uppic/<event_id>',views.uppic,name='uppic'),
    path('upload_pic',views.upload_pic,name='upload_pic'),
    path('upd_event/<event_id>',views.upd_event,name='upd_event'),
]

urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)