from pymongo import MongoClient
import psycopg2
import csv
import os


# MongoDB connection
mongodb_uri = os.getenv('MONGODB_URI',)
print('mongodb_uri:', mongodb_uri)
print('POSTGRES_DB:', os.getenv('POSTGRES_DB'))
print('POSTGRES_USER:', os.getenv('POSTGRES_USER'))
print('POSTGRES_PASSWORD:', os.getenv('POSTGRES_PASSWORD'))

mongo_client = MongoClient(mongodb_uri)
print('mongo_db:', os.getenv('MONGODB_DB'))
mongo_db = mongo_client[os.getenv('MONGODB_DB')]
collection = mongo_db['members']

# PostgreSQL connection
pg_conn = psycopg2.connect(
    dbname=os.getenv('POSTGRES_DB'),
    user=os.getenv('POSTGRES_USER'),
    password=os.getenv('POSTGRES_PASSWORD'),
    host='localhost'
)
pg_cur = pg_conn.cursor()

print('mongodb_uri:', mongodb_uri)
print('mongo_db:', os.getenv('MONGODB_DB'))





# Export MongoDB collection to CSV 
mongo_docs = collection.find({})
with open('export.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['full_name', 'username', 'email', 'api_key', 'active_app_id'])  # Header
    for doc in mongo_docs:
        writer.writerow([doc['full_name'], doc['username'], doc['email'], doc['api_key'], doc['active_app_id']])  # Field mapping

# Import CSV to PostgreSQL
with open('export.csv', 'r') as file:
    next(file)  # Skip the header row
    pg_cur.copy_from(file, 'members', sep=',', columns=('full_name', 'username', 'email', 'api_key', 'active_app_id'))
pg_conn.commit()

# Cleanup
pg_cur.close()
pg_conn.close()
os.remove('export.csv')
