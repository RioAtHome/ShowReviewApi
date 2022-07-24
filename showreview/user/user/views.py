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

def get_payload(request):
	try:
		print(request.META)
		token = request.META['HTTP_JWT']
	except KeyError:
		raise AuthenticationFailed('Token not provided')
	try:
		payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
	except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
		raise AuthenticationFailed('Unauthenticated!')

	return payload


@api_view(['POST'])
def register(request):
	serializer = ApiUserSerializer(data=request.data)
	serializer.is_valid(raise_exception=True)
	serializer.save()

	payload = {
		'username':serializer.data['username'],
		'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=360),
		'iat': datetime.datetime.utcnow(),
	}

	token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
	
	data = {'JWT': token}
	data.update(serializer.data)
	
	return Response(data)


@api_view(['POST'])
def verify(request):
	payload = get_payload(request)
	user = ApiUser.objects.filter(username=payload['username']).first()
	if user is None:
		raise AuthenticationFailed('User Not Found')

	return Response({'message':'A-Okay buddy!'}, headers={'JWT': request.META['HTTP_JWT']})


@api_view(['POST'])
def change_role(request):
	payload = get_payload(request)

	flip_user = request.data['username']
	admin_user = payload['username']

	admin = ApiUser.objects.filter(username=admin_user).first()
	if admin.role == 1:
		pass
	else:
		raise AuthenticationFailed('User Not authorized')
	
	user = ApiUser.objects.filter(username=flip_user).first()

	if user is None:
		raise AuthenticationFailed('User Not Found')
	
	role = user.role
	role ^= 1

	changes = ApiUser.objects.filter(username=flip_user).update(role=role)

	return Response({'message':'Fliped user!'})


@api_view(['GET'])
def view_comments(request):
	pass

@api_view(['GET'])
def view_reviews(request):
	pass

@api_view(['GET'])
def view_favorites(request):
	pass

@api_view(['GET'])
def view_homepage(request):
	pass


