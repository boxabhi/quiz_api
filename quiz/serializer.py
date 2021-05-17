from rest_framework import serializers
from quiz.models import QuestionCategory,Question,Choice,Quiz , QuizStatus,QuestionAttempted
from django.contrib.auth.models import User
import logging
import sys
logger = logging.getLogger(__name__)


class GetAllQuizStatusSerlizer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

        
    def get_assigned_quizs(user ,completed_or_not_completed):
        try:
            print(completed_or_not_completed)
            queryset = QuizStatus.objects.filter(is_completed=completed_or_not_completed, user = user)            
            #queryset = Quiz.objects.filter(id__in = quiz_status)
            quizstatus_serializer = QuizStatusSerializer(queryset , many=True)
           
           
            return quizstatus_serializer.data
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            print(("get_assigned_quizs: %s at %s", str(e), str(exc_tb.tb_lineno)))
            return {}
    
#student = {'first_name' : 'John', 'last_name' : 'gupta' , 'is_gupta' : True}

        




class QuestionCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionCategory 
        exclude = ('id' , 'created_at', 'updated_at')



class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        exclude = ('question' ,'created_at', 'updated_at')

   


class QuestionSerializer(serializers.ModelSerializer):    
    choices = ChoiceSerializer(read_only=True, many=True)
    question_type =  serializers.CharField(source='get_question_type')
    question_category =  QuestionCategorySerializer(read_only=True)
    class Meta:
        model = Question
        exclude =  ('created_at', 'updated_at')
        depth = 2



        


class QuizSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quiz
        exclude = ('question_category','created_at', 'updated_at')


class QuizQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quiz
        exclude = ('question_category','created_at', 'updated_at')
    
      


class StoreAnswerSerializer(serializers.Serializer):
    quiz_status_id = serializers.IntegerField(required=True)
    question_id = serializers.IntegerField(required=True)
    answer_id = serializers.IntegerField()
    subjective_answer = serializers.CharField(max_length=10000 , required=False)
    is_subjective = serializers.BooleanField(required=True)
    
    
    

        

class QuizStatusSerializer(serializers.ModelSerializer):
    quiz = QuizSerializer()
    
    class Meta:
        model = QuizStatus
        exclude = ('created_at', 'updated_at' , 'quiz_status_json' , 'user')
        
    def get_assigned_quiz(self):
        
        queryset = self.get_assigned_quiz()
        
    def get_questions(self):
        ''' Calling method on model class generate_random_questions to get random questions '''
        
        queryset = self.generate_random_questions()
       
        question_serializer = QuestionSerializer(queryset , many=True)
        return question_serializer.data
    
    def create(self , validated_data):
        try:
            quiz_status_obj = QuizStatus.objects.get(id = validated_data['quiz_status_id'])
            question_obj = Question.objects.get(id = validated_data['question_id'])
            
            if quiz_status_obj.is_completed:
                return False , 'You have already completed quiz'
 
            if validated_data['is_subjective']:
                question_attempted_obj = QuestionAttempted.objects.create(
                    quiz_status = quiz_status_obj,
                    question = question_obj,
                    subjective_answer = validated_data['subjective_answer']
                )
                
            else:
                correct_answer_obj = Choice.objects.filter(is_correct=True , question__id= validated_data['question_id']).first()
                if correct_answer_obj is None:
                    return False , ''
                
                user_answer_obj = Choice.objects.get(id = validated_data['answer_id'])
                question_attempted_obj = QuestionAttempted.objects.create(
                    quiz_status = quiz_status_obj,
                    question = correct_answer_obj.question,
                    answer_answered_by_user = user_answer_obj
                )
            
                if user_answer_obj == correct_answer_obj:
                    question_attempted_obj.marks = correct_answer_obj.question.marks_per_question
                    question_attempted_obj.save()
            
            return True , ''

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            logger.error("store_answer: %s at %s", str(e), str(exc_tb.tb_lineno))
            
            return False , 'Something went wrong'
    
        
    
    def get_result(obj):
        try:
            question_attempted_objs= QuestionAttempted.objects.filter(quiz_status = obj)
            data = []
            tototal_score = 0
            for question_attempted_obj in question_attempted_objs:
                result = {
                    'question' : question_attempted_obj.question.question_text,
                }
                if question_attempted_obj.answer_answered_by_user:
                    result['answer'] = question_attempted_obj.answer_answered_by_user.choice
                else:
                    result['answer'] = question_attempted_obj.subjective_answer
                    
        except Exception as e:
            print(e)
        

