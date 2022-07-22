from rest_framework.views import APIView

class Routing(APIView):
	def get(self, request):
		return self.send(request)

	def post(self, request):
		return self.send(request)