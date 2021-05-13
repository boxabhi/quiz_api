from django.urls import path, include
from .views import QuizAttemptViewSet,AnswerViewSet
from rest_framework import routers


router = routers.DefaultRouter()
router.register('quiz' ,QuizAttemptViewSet )
router.register('answer' , AnswerViewSet)


urlpatterns = [
    path('' , include(router.urls)),    
   
]
