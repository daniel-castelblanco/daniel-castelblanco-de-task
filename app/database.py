import psycopg2
import os
from sqlalchemy import create_engine
import pandas as pd
import logging

def connect_db():
    # Should be a secret
    conn = psycopg2.connect(
        dbname='booksdb',
        user='postgres',
        password='your_password',
        host='db',
        port='5432'
    )
    cursor = conn.cursor()
    return conn, cursor

# Function to insert data into the table from a DataFrame
def append_to_postgres(df, table_name):

    # Connect to PostgreSQL database
    engine = create_engine(os.getenv('DATABASE_URL'))
    # Create table and insert data
    df.to_sql(table_name, engine,  if_exists='append', index=False)

def query_db(query):
    conn, cursor = connect_db()
    cursor.execute(query)
    records = cursor.fetchall()
    conn.close()
    return records






