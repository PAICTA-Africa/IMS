from django.urls import path
from Login import views

urlpatterns = [
    path('', views.landing, name="landing"),
    path('auth', views.login, name="login"),
    # path('register/' views)
    path('register/', views.register, name="register"),
    path('auth/', views.login_user, name="login_user"),
    path('index/', views.ClockingView, name="index"),
    path('clock_action/<str:user_id>/', views.clock_action, name="clock_action"),
    path('account', views.account, name="account"),
    path('profile', views.my_profile, name="profile"),
    path('update_profile', views.update_profile, name='update_profile'),
    path('update_info', views.update_info, name='update_info'),
    path('update_emerg', views.update_emerg, name='update_emerg'),
    path('update_family_info', views.update_family_info, name='update_family_info'),
    path('update_education_info', views.update_education_info, name='update_education_info'),
    path('update_experience_info', views.update_experience_info, name='update_experience_info'),
    path('Dashboard', views.DashboardApp, name="DashboardApp"),
    path('employees', views.employees, name="employees"),
    path('leaves', views.leaves_view, name="leaves.html"),
    path('resignation', views.resignation, name="resignation"),
    path('termination', views.termination, name="termination"),
    path('employee', views.employee, name="employees.html"),
    path('project_view', views.project_view, name='project_view'),
    path('leaves_view', views.leaves_view, name="leaves_view"),
]