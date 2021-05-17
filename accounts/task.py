from django.contrib.auth import get_user_model
User = get_user_model()
# from celery import shared_task
# from time import sleep
# import os
# from celery import shared_task

# from datetime import datetime, timedelta
# from .models import Test


from qna.celery import app
@app.task(name="delete_users")
def delete_users():
    print('Delete user called')


# @shared_task
# def delete_users(hours=5):
#     try:
#         Test.objects.create(name = "abhijeet")
#         time_threshold = datetime.now() - timedelta(hours=hours)
#         user_objs = User.objects.filter(created_at__gte=time_threshold ,is_verified=False)
        
#         for user_obj in user_objs:
#             user_obj.delete()
        
#     except Exception as e:
#         print(e)



