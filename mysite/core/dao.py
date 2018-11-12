# Gestión de la base de datos
import json
import pandas as pd
import psycopg2

def get_connection():
	try:
		return psycopg2.connect("dbname='d1ekcgpj2q4ci2' user='xzsivefqhsbocy' host='ec2-54-225-115-234.compute-1.amazonaws.com' port='5432' password='e41446f5f31e0d3264b18d9f5775e5ca230865d1671302bcb9d52b037aa4e39c'")
	except:
		return None

def create_db():
	connection = get_connection()
	cursor = connection.cursor()

	cursor.execute("CREATE SCHEMA IF NOT EXISTS myschema")
	cursor.execute("""CREATE TABLE IF NOT EXISTS myschema.article (
        article_id text primary key,
        title text,
        creation_date text,
        url text,
        author text,
        description text,
        content text,
		json json
    )""")

	connection.commit()
	cursor.close()	
	connection.close()

	return True

def delete_db():
	connection = get_connection()
	cursor = connection.cursor()

	cursor.execute("DROP TABLE IF EXISTS myschema.article")
	cursor.execute("DROP SCHEMA IF EXISTS myschema")

	connection.commit()
	cursor.close()	
	connection.close()

def save_articles(learning_objects):
	connection = get_connection()
	cursor = connection.cursor()

	for key in learning_objects.keys():
		cursor.execute("INSERT INTO myschema.article values (%s, %s, %s, %s, %s, %s, %s, %s)", ([key, learning_objects[key]['translated_title'], learning_objects[key]['creation_date'], learning_objects[key]['ka_url'], 'Khan Academy', learning_objects[key]['translated_description'], json.loads(learning_objects[key]['translated_perseus_content'])[0]['content'], json.dumps(learning_objects[key])]))

	connection.commit()
	cursor.close()	
	connection.close()

def articles_exist():
	connection = get_connection()
	cursor = connection.cursor()

	cursor.execute("SELECT * FROM myschema.article")

	rows = cursor.fetchall()
	articles_count = len(rows)

	cursor.close()	
	connection.close()

	return articles_count > 0

def get_dataframes():
	connection = get_connection()
	result = pd.read_sql_query("SELECT * FROM myschema.article", connection)

	connection.close()

	return result