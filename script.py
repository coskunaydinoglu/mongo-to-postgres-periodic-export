from pymongo import MongoClient
import psycopg2
import csv
import os


# MongoDB connection
mongodb_uri = os.getenv('MONGODB_URI')
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
    host='postgres'
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
        writer.writerow([doc['full_name'], doc['username'], doc['email'], doc['api_key'], doc['active_app_id'], doc['_id']])  # Field mapping

#it makes full export of the collection to csv file

# Import CSV to PostgreSQL.  
# better implementation can be done. For sake of simplicity 
# CSV file is read and upserted into PostgreSQL table
# if recorod exists with the same source id it will be updated
# delete the records if source id is not present in the csv file
        
upsert_sql = """
    INSERT INTO members (full_name, username, email, api_key, active_app_id, source_id)
    VALUES (%s, %s, %s, %s, %s, %s)
    ON CONFLICT (source_id) DO UPDATE
    SET full_name = EXCLUDED.full_name, 
        username = EXCLUDED.username, 
        email = EXCLUDED.email, 
        api_key = EXCLUDED.api_key, 
        active_app_id = EXCLUDED.active_app_id;
"""

source_ids_from_csv = set()
with open('export.csv', 'r') as file:
    csv_reader = csv.reader(file)
    next(csv_reader)  # Skip the header row
    for row in csv_reader:
        # Assuming your CSV columns are in the correct order as your SQL placeholders
        # Adjust the row slicing as necessary to match the columns in your table
        pg_cur.execute(upsert_sql, row)
        # Assume the last column in each row is source_id
        source_ids_from_csv.add(row[-1])

# Step 2: Delete records not in source_ids_from_csv
# Convert set to list for psycopg2 compatibility
source_ids_list = list(source_ids_from_csv)
# Using ANY requires a list; format the list to a string representation for the query.
ids_format_str = ','.join(['%s'] * len(source_ids_list))
delete_sql = f"""
    DELETE FROM members WHERE source_id NOT IN (SELECT unnest(ARRAY[{ids_format_str}]));
"""
pg_cur.execute(delete_sql, source_ids_list)


pg_conn.commit()

# Cleanup
pg_cur.close()
pg_conn.close()
os.remove('export.csv')
