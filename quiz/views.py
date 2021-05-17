from django.contrib.auth import get_user_model
User = get_user_model()
from base_rest.exceptions import BaseValidationError
from base_rest.viewsets import BaseAPIViewSet
from django.db import transaction
from rest_framework import status

from rest_framework.response import Response
from rest_framework.views import APIView
from .models import QuizStatus
from .mixins import QuizMixin , AnswerMixin
import logging
import sys
from django.contrib.auth import get_user_model
from base_rest.permissions import IsOwnerAttributes
from .serializer import (GetAllQuizStatusSerlizer,QuizStatusSerializer)
logger = logging.getLogger(__name__)







class QuizAttemptViewSet(BaseAPIViewSet , QuizMixin):
    queryset = QuizStatus.objects.all()
    serializer_class = QuizStatusSerializer
    model_class = QuizStatus
    instance_name = "quiz_attempt"
    
    ACTION_SERIALIZERS = {'approve': QuizStatusSerializer ,'get_all_quiz_status' : GetAllQuizStatusSerlizer}
    
    permission_classes = (IsOwnerAttributes,)
    
    def get_serializer(self, *args, **kwargs):
        return self.ACTION_SERIALIZERS.get(self.action,
                                           self.serializer_class)(*args,
                                                                  **kwargs)

    
    def list(self , request ,*args, **kwargs):
        try:
            ''' To get completed or uncompleted quizes '''
            completed_or_not_completed = request.GET.get('is_completed' , False)
            
            user_obj = request.user
            #user_obj = User.objects.first()
            serializer = GetAllQuizStatusSerlizer
            
            ''' getting assiged quiz from serlizers method '''
            
            return Response({
                    'status': True,
                    'message': 'Your Quizes',
                    'data': serializer.get_assigned_quizs(user_obj , completed_or_not_completed)
                })
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            logger.error("QuizAttemptViewSet: %s at %s", str(e), str(exc_tb.tb_lineno))

            raise BaseValidationError('something went wrong')



            
class AnswerViewSet(BaseAPIViewSet , AnswerMixin):
    
    
    
    queryset = QuizStatus.objects.all()
    serializer_class = QuizStatusSerializer
    model_class = QuizStatus
    instance_name = "quiz_attempt"
    ACTION_SERIALIZERS = {'approve': QuizStatusSerializer ,'get_all_quiz_status' : GetAllQuizStatusSerlizer}
    
    permission_classes = (IsOwnerAttributes,)
    
    def get_serializer(self, *args, **kwargs):
        return self.ACTION_SERIALIZERS.get(self.action,
                                           self.serializer_class)(*args,
                                                                  **kwargs)
                                           
                                           


class GetResultForQuizStatus(APIView):
    serializer_class = QuizStatusSerializer
    instance_name = "get_result"
    logger = logger
    model_class = QuizStatus
    
    
    def get(self,request):
        try:
            quiz_status_id = self.get_object(pk= request.GET.get('quiz_status_id'))
            
            return Response({
                    'status': True,
                    'message': 'Your Quize result',
                    'data': self.serializer_class.get_result()
                })
        except Exception as e:
            raise BaseValidationError('something went wrong')
            
            

        
      

        
        



