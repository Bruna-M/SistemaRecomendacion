# Gestión de la base de datos
import sqlite3
import json
import pandas as pd

db_path = 'core/Khan_Academy.db'

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

def save_articles_in_db(learning_objects):
	connection = sqlite3.connect(db_path)

	cursor = connection.cursor()

	for key in learning_objects.keys():

		cursor.execute("INSERT INTO article values (?, ?, ?, ?, ?, ?, ?, ?)", [key, learning_objects[key]['translated_title'], learning_objects[key]['creation_date'], learning_objects[key]['ka_url'], 'Khan Academy', learning_objects[key]['translated_description'], json.loads(learning_objects[key]['translated_perseus_content'])[0]['content'], json.dumps(learning_objects[key])])

	connection.commit()

	cursor.close()	

	connection.close()

def list_articles_in_db():

	connection = sqlite3.connect(db_path)

	cursor = connection.cursor()

	cursor.execute("SELECT * FROM article")

	rows = cursor.fetchall()

	for row in rows:
		print(row)

	cursor.close()	

	connection.close()

def get_dataframes():

	connection = sqlite3.connect(db_path)

	result = pd.read_sql_query("SELECT * FROM article", connection)

	connection.close()

	return result


# def list_content_articles_in_db():

# 	list_content = []

# 	connection = sqlite3.connect(db_path)

# 	cursor = connection.cursor()

# 	cursor.execute("SELECT content FROM article")

# 	rows = cursor.fetchall()

# 	for row in rows:
# 		append(list_content)

# 	cursor.close()	

# 	connection.close()

# 	return list_content

def save_keywords_in_db():

	keywords_acum = []

	connection = sqlite3.connect(db_path)

	cursor = connection.cursor()

	cursor.execute("SELECT * FROM article")

	rows = cursor.fetchall()

	for i in range(0,len(rows)):
		
		print('Obteniendo keywords de articulo ({0}/{1})'.format(i + 1, len(rows)))

		data = json.loads(rows[i][1])

		content = json.loads(data['translated_perseus_content'])

		keywords = Khan_Academy_Engine.get_keywords(content[0]['content'])

		keywords_freqs = {}

		for j in range(0,len(keywords)):

			if keywords[j] in keywords_freqs:

				keywords_freqs[keywords[j]] = keywords_freqs[keywords[j]] + 1

			else:

				keywords_freqs[keywords[j]] = 0

		sorted_keywords_freqs = sorted(keywords_freqs.items(), key=operator.itemgetter(1), reverse=True)

		final_keywords = []

		if len(sorted_keywords_freqs) > 15:

			for k in range(0,15):

				final_keywords.append(sorted_keywords_freqs[k][0])

		else:

			for l in range(0,len(sorted_keywords_freqs)):

				final_keywords.append(sorted_keywords_freqs[l][0])

		for m in range(0,len(final_keywords)):

			if not final_keywords[m] in keywords_acum:

				keywords_acum.append(final_keywords[m])


	for k in range(0,len(keywords_acum)):

		cursor.execute("INSERT INTO keyword values (?)", [keywords_acum[k]])

	connection.commit()

	cursor.close()	

	connection.close()

def list_keywords_in_db():

	connection = sqlite3.connect(db_path)

	cursor = connection.cursor()

	cursor.execute("SELECT * FROM keyword")

	rows = cursor.fetchall()

	for row in rows:
		print(row)

	cursor.close()	

	connection.close()

def show_scores():

	connection = sqlite3.connect(db_path)

	cursor = connection.cursor()

	cursor.execute("SELECT * FROM tfidf")

	rows = cursor.fetchall()

	for row in rows:
		print(row)

	cursor.close()	

	connection.close()