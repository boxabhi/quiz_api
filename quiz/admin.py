from django.contrib import admin
from django.db import models
from django.forms import CheckboxSelectMultiple
from .models import QuestionCategory ,Question,Choice, Quiz, QuizStatus,QuestionAttempted


admin.site.register(QuestionCategory)


class QuestionAdmin(admin.StackedInline):
    model = Question
class ChoiceAdmin(admin.StackedInline):
    model = Choice

class UserProfileAdmin(admin.ModelAdmin):
    inlines = [ ChoiceAdmin ]
    

class QuizAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.ManyToManyField: {'widget': CheckboxSelectMultiple},
    }
    
    
admin.site.register(Question , UserProfileAdmin)
admin.site.register(Choice)
admin.site.register(Quiz , QuizAdmin)
admin.site.register(QuizStatus)
admin.site.register(QuestionAttempted)