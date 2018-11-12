# Motor de sistema de recomendación basado en contenido (en el ítem)

# Dependencias
import core.dao as dao
#import dao
import core.ka as ka
#import ka
import json
import nltk
from nltk.corpus import stopwords
import numpy as np
import operator
import pandas as pd
import requests
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import pairwise_distances
from sklearn.neighbors import NearestNeighbors
import sqlite3

# Variables globales
tfidf_vectorizer = None
nearest_neigbors = None
nltk.download('stopwords')
stop_words =  stopwords.words('spanish')
token_pattern = '(?u)\\b[a-zA-Z]\\w\\w+\\b'
metric = 'cosine'
n_neighbors = 20
tfidf_vectorizer = TfidfVectorizer(stop_words=stop_words, token_pattern=token_pattern)
nearest_neigbors = NearestNeighbors(metric=metric, n_neighbors=n_neighbors, algorithm='brute')

def get_data():
	dao.create_db()

	if not dao.articles_exist():
		dao.save_articles(ka.get_learning_objects())

	return dao.get_dataframes()

def fit(data, column):
	datos_por_tags = tfidf_vectorizer.fit_transform(data[column])

	nearest_neigbors.fit(datos_por_tags)

def predict(data, description):
	descripcion_tags = tfidf_vectorizer.transform(description)

	if descripcion_tags.sum() == 0:
		return pd.DataFrame(columns=data.columns)
	else:
		_, indices = nearest_neigbors.kneighbors(descripcion_tags)

		return data.iloc[indices[0], :]

def get_predictions(query):
	data = get_data()

	fit(data, 'content')

	return predict(data, query.split(' ')).to_json()
