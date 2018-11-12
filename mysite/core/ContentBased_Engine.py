#Motor de sistema de recomendación basado en contenido (en el ítem)

#Se importan las dependencias
import requests
import json
import sqlite3
import core.Khan_Academy as KA
#import Khan_Academy as KA
import operator
import core.BD as BD
#import BD
import pandas as pd
from sklearn.metrics.pairwise import pairwise_distances
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import NearestNeighbors
import numpy as np
from nltk.corpus import stopwords

#Variables globales
tfidf_vectorizer = ''
nearest_neigbors = ''
stop_words =  stopwords.words('spanish')
token_pattern = '(?u)\\b[a-zA-Z]\\w\\w+\\b'
metric = 'cosine'
n_neighbors = 20
#vectorizacion = CountVectorizer()	
tfidf_vectorizer = TfidfVectorizer(stop_words=stop_words, token_pattern=token_pattern)
nearest_neigbors = NearestNeighbors(metric=metric, n_neighbors=n_neighbors, algorithm='brute')
#learning_objects = {}
#---------------------------------------------------------------------

def saveData():

	#Obtener artículos
	#learning_objects = KA.execute()

	#Crear la base de datos
	#BD.delete_db()
	#BD.create_db()

	#Guardar artículos
	#BD.save_articles_in_db(learning_objects)

	return BD.get_dataframes()

	#Guardar keywords
	#BD.save_keywords_in_db()

def fit(data, column):
	datos_por_tags = tfidf_vectorizer.fit_transform(data[column])
	nearest_neigbors.fit(datos_por_tags)

def predict(data, description):
	descripcion_tags = tfidf_vectorizer.transform(description)		
	if descripcion_tags.sum() == 0:
		return pd.DataFrame(columns=data.columns)
	else:
		_, indices = nearest_neigbors.kneighbors(descripcion_tags)
		print(indices)
		return data.iloc[indices[0], :]

def get_predictions(query):
	data = saveData()

	fit(data, 'content')

	return predict(data, query.split(' ')).to_json()
