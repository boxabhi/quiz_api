from base_rest.exceptions import BaseValidationError
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from .serializer import (StoreAnswerSerializer)
from django.contrib.auth import get_user_model
User = get_user_model()




class QuizMixin:
    
    @action(detail=True, methods=["get"] , url_path = 'get-quizes' , url_name ="get-quizes")
    def get_all_quizs(self, request, pk, *args, **kwargs):
        
        ''' Action to get all quizes  according to is_completed True/False '''
        
        try:
            completed_or_not_completed = request.GET.get('is_completed' , False)
            user_obj = User.objects.first()
            serializer = self.get_serializer(user_obj , completed_or_not_completed)
            return Response({
                    'status': True,
                    'message': 'Your Quizes',
                    'data': serializer.data
                })
        except Exception as e:
            print(e)
            raise BaseValidationError('something went wrong')
     
    
    @action(detail=True, methods=["get"] , url_path = 'get-quizes-questions' , url_name ="get-quizes-questions")
    def get_quiz_questions_from_quiz_status(self, request, pk, *args, **kwargs):
        ''' Getting quiz from quiz status '''
        
        try:
            obj = self.get_object(pk=pk)
            return Response({
                    'status': True,
                    'message': 'Your quiz Questions. Good Luck 😁',
                    'data': self.serializer_class.get_questions(obj)
                })
        
        except Exception as e: 
            print(e)
            raise BaseValidationError('something went wrong')

           


class AnswerMixin:
    
    @action(detail=True, methods=["post"] , url_path = 'check-answer' , url_name ="check-answer")
    def store_answer_in_quiz_status(self, request, pk, *args, **kwargs): 
        serializer = StoreAnswerSerializer(data = request.data)
        
        if not serializer.is_valid():
            raise BaseValidationError(serializer.errors)
         
        _serializer, message = self.serializer_class.store_answer(serializer.data)
        
        if _serializer is False:
            raise BaseValidationError(message)

        return Response({
                    'status': True,
                    'message': 'Your answer submitted',
                })
    
    
            
            
        
        
    
        
