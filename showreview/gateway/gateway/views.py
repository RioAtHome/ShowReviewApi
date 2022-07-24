import requests, json
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from django.core.cache import cache
from django.conf import settings
from .models import Api



CACHE_TTL = getattr(settings, 'CACHE_TTL')

class Routing(APIView):
	def send(self, request):
		request_path = request.get_full_path() 
		if request_path[-1] != '/':
			request_path += '/' 

		path = request_path.split('/')
		if len(path) < 2:
			return Response('bad request', status=status.HTTP_400_BAD_REQUEST)
		api = Api.objects.filter(name=path[2]).first()
		user_api = Api.objects.filter(name='user').first()

		if api is None:
			return Response('bad request', status=status.HTTP_400_BAD_REQUEST)
		token = request.META['HTTP_JWT']
		requested_service = '/'.join(path[2:])

		if requested_service == 'user/register/':
			resp = api[0].handle_request(request, requested_service)

		elif requested_service == 'user/verify/':
			resp = api.handle_request(request, requested_service, token)	
		else:	
			token = request.META.get('HTTP_JWT')
			if not token:
				return Response('Token is needed', status=status.HTTP_400_BAD_REQUEST)
			if not token in cache:
				headers = {'content-type': 'application/json', 'JWT':token}
				api = Api.objects.filter(name='user').first()
				url = user_api.main_url + 'user/verify/'
				
				resp = requests.post(url, headers=headers, timeout=2.50) 
				if resp.status_code == 200:
					cache.set(token, '', timeout=CACHE_TTL)
				else:
					return Response('Token is unvalid', status=status.HTTP_400_BAD_REQUEST)
			request.META['HTTP_JWT'] = token
			resp = api.handle_request(request, requested_service, token)
		
		if resp.headers.get('Content-Type', '').lower() == 'application/json':
			data = resp.json()
		else:
			data = resp.content

		return Response(data=data, status=resp.status_code)

	def get(self, request):
		return self.send(request)

	def post(self, request):
		return self.send(request)