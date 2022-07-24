from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from .serializers import ApiUserSerializer
from .models import ApiUser

# Create your views here.
@api_view(['POST'])
def register(request):
	serializer = ApiUserSerializer(data=request.data)
	serializer.is_valid(raise_exception=True)
	serializer.save()

	return Response(serializer.data)
@api_view(['POST'])
def verify(request):
	username = request.data['username']
	password = request.data['password']

	user = ApiUser.objects.filter(username=username).first()

	if user is None:
		raise AuthenticationFailed('User Not Found')

	if not user.check_password(password):
		raise AuthenticationFailed('Incorrect Password')

	return Response({'message':'A-Okay buddy!'})