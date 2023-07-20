import psycopg2, select, os
from dotenv import load_dotenv
load_dotenv()

# Connect to the PostgreSQL database
user = os.environ.get('POSTGRES_USER')
password = os.environ.get('POSTGRES_PASSWORD')
host = os.environ.get('POSTGRES_HOST')
database = os.environ.get('POSTGRES_DATABASE')
connection_string = f'postgresql://{user}:{password}@{host}:5432/{database}'

conn = psycopg2.connect(connection_string)

cursor = conn.cursor()

# Listen to the channel
cursor.execute("LISTEN hls_channel;")
conn.commit()

while True:
    if select.select([conn], [], [], 10) == ([], [], []):
        # No notification received in the last 10 seconds
        print("Waiting for notifications...")
    else:
        # Received a notification
        conn.poll()
        while conn.notifies:
            notification = conn.notifies.pop(0)
            print("Received:", notification.payload)

