import requests
import json
import sqlite3
import operator

KA_URI='http://www.khanacademy.org'

KA_URI_ES='https://es.khanacademy.org/'

TOPIC_TREE = "/api/v1/topictree?kind=topic"

ARTICLE_URI = "/api/v1/articles/"

articles_ids = []
learning_objects = {}

def get_topictree():

	response = requests.get(KA_URI + TOPIC_TREE)

	data = response.content

	parsedData = json.loads(data)

	return parsedData


def get_science_articles_list(parsedData):

	found = False

	i = 0

	sciencelist = []

	while (not found and i<len(parsedData['children'])):
		
		if parsedData['children'][i]['relative_url'] == '/science':

			sciencelist = parsedData['children'][i]['children']

			found = True

		i = i + 1

	return sciencelist


def get_modules_list(sciencelist):

	hsblist = []

	for i in range (0,len(sciencelist)):

		if ((sciencelist[i]['relative_url'] == '/science/high-school-biology') or 
			(sciencelist[i]['relative_url'] == '/science/chemistry') or
			(sciencelist[i]['relative_url'] == '/science/organic-chemistry') or
			(sciencelist[i]['relative_url'] == '/science/biology') or
			(sciencelist[i]['relative_url'] == '/science/health-and-medicine'))  : 

			hsblist = hsblist + sciencelist[i]['children']

	return hsblist


def get_articles(child):

	# Verificar que el hijo realmente tenga el atributo children

	if 'children' in child :

		for i in range (0,len(child['children'])) :

			get_articles(child['children'][i])


	if 'child_data' in child :

		for i in range (0,len(child['child_data'])) :

			if (child['child_data'][i]['kind'].lower() == 'article' and child['child_data'][i]['id'] not in articles_ids):	

				articles_ids.append(child['child_data'][i]['id'])


def iterate_hsb_list(hsb_list):

	for i in range (0,len(hsb_list)):

		get_articles(hsb_list[i])


def get_articles_content():
	
	print('Total: ' + str(len(articles_ids))) #len(articles_ids)

	for i in range (0, len(articles_ids)):

		print('Obteniendo contenido de articulo ({0}/{1})'.format(i + 1, len(articles_ids)))

		response = requests.get(KA_URI_ES + ARTICLE_URI + articles_ids[i])

		if response.status_code == 200:

			data = response.content

			parsedData = json.loads(data)

			if len(parsedData['translated_description'])>0:

				learning_objects[articles_ids[i]] = parsedData

def execute():

	 topictree = get_topictree()

	 sc_art_list = get_science_articles_list(topictree)

	 hsb_list = get_modules_list(sc_art_list)

	 iterate_hsb_list(hsb_list) # 245 articles - 83

	 get_articles_content()

	 return learning_objects