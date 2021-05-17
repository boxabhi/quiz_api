from django.contrib.auth import get_user_model
User = get_user_model()
import uuid
from rest_framework.response import Response
from .serializers import (LoginSerializer,
                            UserSerializer , ForgetPasswordSerializer)
from rest_framework import status
from base_rest.viewsets import BaseAPIViewSet
from .mixins import AccountMixin



''' ModelViewSet for registering user '''




class AccountViewSet(BaseAPIViewSet , AccountMixin):
    queryset = User.objects.all()
    model_class = User
    serializer_class = UserSerializer
    instance_name = "user"
    ACTION_SERIALIZERS = {
        'reset': ForgetPasswordSerializer,
        'login': LoginSerializer,
    }
 
    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'staus' : 200 , 'data' : serializer.data} ,status.HTTP_200_OK )



  
    
    
   
            
        
    




    