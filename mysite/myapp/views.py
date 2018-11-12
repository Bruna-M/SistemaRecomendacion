from core.ContentBased_Engine import get_predictions
from django.shortcuts import render
from django.http import HttpResponse
import json

# Create your views here.
def index(request):
	return render(request, 'index.html')

def get_recommendations(request):
	query = request.GET.get('query', '')
	response = {}
	response['error'] = False

	if query == '':
		response['error'] = True
	else:
		response['result'] = json.loads(get_predictions(query))

	return HttpResponse(json.dumps(response), content_type='text/json')