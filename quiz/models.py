from django.db import models
import random 
import logging
import sys
import uuid
from base_rest.models import BaseModel
from django.contrib.auth import get_user_model
User = get_user_model()

logger = logging.getLogger(__name__)





class QuestionCategory(BaseModel):
    category_name = models.CharField(max_length=100)
   
    
    class Meta:
        verbose_name = 'QuestionCategory'
    
    
    def __str__(self):
        return self.category_name



class Question(BaseModel):
   
    question_category = models.ForeignKey("QuestionCategory",related_name="question_category", on_delete=models.CASCADE , null=True , blank=True)
    question_text = models.CharField(max_length=1000)
    question_type = models.IntegerField(choices = ((1 , 'MCQ') , (2 , 'SUBJECTIVE')))
    marks_per_question = models.IntegerField(default=5)

    
    def __str__(self):
        return self.question_text
    
    def get_question_type(self):
        if self.question_type == 1:
            return "MCQ"
        return "SUBJECTIVE"


class Choice(BaseModel):
   
    question = models.ForeignKey("Question", related_name="choices" , on_delete=models.CASCADE)
    choice = models.CharField("Choice", max_length=50)
    is_correct = models.BooleanField(default=False)
    
    
    class Meta:
        unique_together = [
            ("question", "choice"), 
        ]

    def __str__(self):
        return self.choice


class Quiz(BaseModel):

    quiz_name = models.CharField(max_length=100)
    question_category = models.ManyToManyField(QuestionCategory)
    question_limit_per_section = models.IntegerField(default=5)
    
    
    def __str__(self):
        return self.quiz_name

    

class QuizStatus(BaseModel):
   
    user = models.ForeignKey(User , related_name="user" , on_delete=models.SET_NULL ,null =True , blank = True)
    quiz = models.ForeignKey(Quiz , related_name="quiz" , on_delete=models.SET_NULL , null = True , blank =True)
    quiz_status_json = models.TextField(default="[]")
    is_completed = models.BooleanField(default=False)
   
    
    def generate_random_questions(self):
        try:
            question_limit_per_section = self.quiz.question_limit_per_section
            quiz_categories = self.quiz.question_category.all()
            
            questions  = []
        
            
            for quiz_category in quiz_categories:
                questions_by_category = Question.objects.filter(question_category = quiz_category )
                random_question_by_category = (list(questions_by_category))
                # shuffling to get random data
                random.shuffle(random_question_by_category)
                random_question_by_category = random_question_by_category[0:question_limit_per_section]                    
                for random_question in random_question_by_category:
                    questions.append(random_question)
            
            return questions
            
            
            
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            logger.error("generate_random_questions: %s at %s", str(e), str(exc_tb.tb_lineno))

        
        
class QuestionAttempted(BaseModel):
 
    quiz_status = models.ForeignKey(QuizStatus , on_delete=models.CASCADE)
    question = models.ForeignKey(Question , on_delete=models.SET_NULL , null=True , blank=True)
    answer_answered_by_user = models.ForeignKey(Choice , on_delete=models.SET_NULL , null=True , blank=True)
    subjective_answer = models.TextField(blank=True , null=True)
    marks = models.IntegerField(default=-1)
  
 


    
    
     