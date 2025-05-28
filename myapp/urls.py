from django.urls import path
from . import views
from rest_framework.routers import DefaultRouter
# from .views import PlannerTaskViewSet, planner_home, add_task
from .views import PlannerTaskViewSet, planner_home, add_task, question_generator_view

from .views import note_summarizer, summarize_view, verify_otp_view
urlpatterns = [
    path('', views.spinner_view, name='spinner'), 
    path('how_it_works/',views.how_it_works_view,name='how_it_works'),
    path('login/', views.user_login, name='login'),          # Login page
    path('register/', views.register_view, name='register'),  # Register page
    path('activate/<uidb64>/<token>/', views.activate_view, name='activate'),
    path('dashboard/', views.dashboard, name='dashboard'), 
    path('password_reset/',views.password_reset, name='password_reset'),
    path('summarize/', note_summarizer, name='note_summarizer'),
    path('verify-otp/', verify_otp_view, name='verify_otp'),
    path('summarizes/', summarize_view, name='summarizes'),
    path('generate_questions/', question_generator_view, name='generate_questions'),
    path('generate/', views.generate_question, name='generate'),
    path('index', views.index, name='index'),
    path('planner', views.planner, name='planner'),
    path('planner_home', planner_home, name='planner_home'),
    path('add/', add_task, name='add_task'),
    path('', views.task_list, name='task_list'),
    path('edit/<int:task_id>/', views.edit_task, name='edit_task'),
    path('delete/<int:task_id>/', views.delete_task, name='delete_task'),
      path('verify-code/', views.verify_otp_view, name='verify_code'),  # <-- use verify_otp_view here
    # path("simulate-whatsapp/", views.simulate-whatsapp, name='simulate-whatsapp'), # type: ignore
    path('accounts/login/', views.user_login, name='login'),  # Add this
]
