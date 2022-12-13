from django.urls import path
from .views import PersonalityProcessorView
from django.contrib import admin

urlpatterns = [
    path('', PersonalityProcessorView.index, name='home'),
    path('home', PersonalityProcessorView.index, name='home'),

    path('predict_personality',PersonalityProcessorView.PredictPersonality,name='predict_personality'),
    path('predict_personality_by_resume',PersonalityProcessorView.PredictPeronalityByResume,name='predict_personality_by_resume'),
    
]


