from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from forum.views import ForumHome, CategoryTopics, SingleTopic, CreateTopic, editReply, search
from member.views import CreateUser, LoginUser, logout, profile, createProfile, testView, PasswordsChangeView, PasswordsResetView, passwordResetDone, PasswordsResetConfirm
import os

urlpatterns = [
    path('', ForumHome.as_view(), name='home'),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('admin/', admin.site.urls),
    # Forum related urls
    path('topic/create-topic/', CreateTopic.as_view(), name='create_topic'),
    path('topic/<slug:slug>/', SingleTopic.as_view(), name='reply_list'),
    path('reply/<int:id>/edit', editReply, name='edit_reply'),
    path('forum/<category>/', CategoryTopics.as_view(), name='topic_list'),

    # Auth related urls
    path('register/', CreateUser.as_view(), name='register'),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', logout, name='logout'),

    # Profile related urls
    path('profile/settings/', createProfile, name='profile_setting'),
    path('profile/<str:username>/', profile, name='profile'),

    # Password related urls
    path('password-change/',
         PasswordsChangeView.as_view(), name='password_change'),
    path('password-reset/<uidb64>/<token>/',
         PasswordsResetConfirm.as_view(), name='password_reset_confirm'),
    path('password-reset/done', passwordResetDone, name='password_reset_done'),
    path('password-reset/',
         PasswordsResetView.as_view(), name='password_reset'),
    # Utilities stuff
    path('search/', search, name='search'),
    path('test/', testView, name='error'),


]

if 'WEBSITE_HOSTNAME' not in os.environ:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
