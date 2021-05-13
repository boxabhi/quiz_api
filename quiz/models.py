from django.db import models
from django.contrib.auth.models import User


class QuestionCategory(models.Model):
    category_name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'QuestionCategory'
    
    
    def __str__(self):
        return self.category_name



class Question(models.Model):
    question_category = models.ForeignKey("QuestionCategory", on_delete=models.CASCADE , null=True , blank=True)
    question_text = models.CharField(max_length=1000)
    question_type = models.IntegerField(choices = ((1 , 'MCQ') , (2 , 'SUBJECTIVE')))
    marks_per_question = models.IntegerField(default=5)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.question_text
    
    def get_question_type(self):
        if self.question_type == 1:
            return "MCQ"
        return "SUBJECTIVE"


class Choice(models.Model):
    question = models.ForeignKey("Question", related_name="choices" , on_delete=models.CASCADE)
    choice = models.CharField("Choice", max_length=50)
    is_correct = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = [
            ("question", "choice"), 
        ]

    def __str__(self):
        return self.choice


class Quiz(models.Model):
    quiz_name = models.CharField(max_length=100)
    question_category = models.ManyToManyField(QuestionCategory)
    question_limit_per_section = models.IntegerField(default=5)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.quiz_name

    

class QuizStatus(models.Model):
    user = models.ForeignKey(User , on_delete=models.SET_NULL ,null =True , blank = True)
    quiz = models.ForeignKey(Quiz , on_delete=models.SET_NULL , null = True , blank =True)
    quiz_status_json = models.TextField(default="[]")
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    
    def generate_random_questions(self):
        try:
            question_limit_per_section = self.quiz.question_limit_per_section
            quiz_categories = self.quiz.question_category.all()
            questions_by_categories = Question.objects.filter(question_category__in = quiz_categories )
            return questions_by_categories
            
            
            
        except Exception as e:
            print(e)
        
        
class QuestionAttempted(models.Model):
    quiz_status = models.ForeignKey(QuizStatus , on_delete=models.CASCADE)
    question = models.ForeignKey(Question , on_delete=models.SET_NULL , null=True , blank=True)
    answer_answered_by_user = models.ForeignKey(Choice , on_delete=models.SET_NULL , null=True , blank=True)
    subjective_answer = models.TextField(blank=True , null=True)
    marks = models.IntegerField(default=-1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    
 
    
    
     