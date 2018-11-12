# Gestión de la base de datos
import json
import pandas as pd
import sqlite3

db_path = 'core/ka.db'

def create_db():

	connection = sqlite3.connect(db_path)

	cursor = connection.cursor()

	cursor.execute("""CREATE TABLE IF NOT EXISTS article (
        article_id text primary key,
        title text,
        creation_date text,
        url text,
        author text,
        description text,
        content text,
		json json
    )""")

	cursor.execute("""CREATE TABLE IF NOT EXISTS keyword (
        keyword_id text primary key
    )""")

	cursor.execute("""CREATE TABLE IF NOT EXISTS tfidf (
        article_id text,
		keyword_id text,
		value real,
		FOREIGN KEY(article_id) REFERENCES article(article_id),
		FOREIGN KEY(keyword_id) REFERENCES keyword(keyword_id),
		PRIMARY KEY(article_id, keyword_id)
    )""")

	cursor.close()	

	connection.close()

def delete_db():
	connection = sqlite3.connect(db_path)
	cursor = connection.cursor()

	cursor.execute("DROP TABLE IF EXISTS article")
	cursor.execute("DROP TABLE IF EXISTS keyword")
	cursor.execute("DROP TABLE IF EXISTS tfidf")

	cursor.close()	
	connection.close()

def save_articles(learning_objects):
	connection = sqlite3.connect(db_path)
	cursor = connection.cursor()

	for key in learning_objects.keys():
		cursor.execute("INSERT INTO article values (?, ?, ?, ?, ?, ?, ?, ?)", [key, learning_objects[key]['translated_title'], learning_objects[key]['creation_date'], learning_objects[key]['ka_url'], 'Khan Academy', learning_objects[key]['translated_description'], json.loads(learning_objects[key]['translated_perseus_content'])[0]['content'], json.dumps(learning_objects[key])])

	connection.commit()
	cursor.close()	
	connection.close()

def articles_exist():
	connection = sqlite3.connect(db_path)
	cursor = connection.cursor()

	cursor.execute("SELECT * FROM article")

	rows = cursor.fetchall()

	return len(rows) > 0

	cursor.close()	
	connection.close()

def get_dataframes():
	connection = sqlite3.connect(db_path)
	result = pd.read_sql_query("SELECT * FROM article", connection)

	connection.close()

	return result