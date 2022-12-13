from django.urls import path
from .views import PersonalityProcessorView
from django.contrib import admin

urlpatterns = [
    path('home', PersonalityProcessorView.index, name='home'),

    path('predict_personality',PersonalityProcessorView.PredictPersonality,name='predict_personality'),

    # path('Getdata',DailyStockPredictionViews.StockPrediction_Get,name='GetPrediction'),
    # path('Getgraph',DailyStockPredictionViews.StockPrediction_Getgraph,name='Getgraph'),
    # path('AddTradingAction',TradingActionViews.TradingAction_Add,name='AddTradingAction'),
    # path('GetTradingAction',TradingActionViews.TradingAction_Get,name='GetTradingAction'),
    
]


