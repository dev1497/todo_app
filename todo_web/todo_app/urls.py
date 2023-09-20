from django.urls import path
from . import views
urlpatterns = [
    path('', views.home, name="home"),
    path('signup/', views.signup_user, name="signup"),
    path('login/', views.login_user, name="login"),
    path('dashboard/', views.dashboard, name="dashboard"),
    path('logout/', views.logout_user, name="logout"),
    path('schedule_task/', views.schedule_task, name="schedule_task"),
    path('task/<int:pk>', views.user_task, name='task'),
    path('update_task/<int:pk>', views.update_task, name='update_task'),
    path('mark_task/<int:pk>', views.mark_complete, name='mark_task'),
    path('delete_task/<int:pk>', views.delete_task, name='delete_task'),

]