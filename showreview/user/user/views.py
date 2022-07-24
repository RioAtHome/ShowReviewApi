from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from django.conf import settings
import jwt, datetime
from .serializers import ApiUserSerializer
from .models import ApiUser

# Create your views here.
@api_view(['POST'])
def register(request):
	serializer = ApiUserSerializer(data=request.data)
	serializer.is_valid(raise_exception=True)
	serializer.save()

	payload = {
		'username':user.username,
		'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=360),
		'iat': datetime.datetime.utcnow(),
	}

	token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')

	return Response(serializer.data, headers={'JWT': token})


@api_view(['POST'])
def verify(request):
	try:
		token = request.META['HTTP_JWT']
	except KeyError:
		raise AuthenticationFailed('Token not provided')
	try:
		payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
	except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
		raise AuthenticationFailed('Unauthenticated!')


	user = ApiUser.objects.filter(username=payload['username']).first()


	if user is None:
		raise AuthenticationFailed('User Not Found')
	
	return Response({'message':'A-Okay buddy!'}, headers={'JWT': token})