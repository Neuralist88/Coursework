import os
import psycopg2
import pandas as pd

def connect(connection_string):

   """Connect to database"""  
   # Create a connection
   conn = psycopg2.connect(connection_string)
   print('All good, Connection successful!')
   return conn

def sql_to_df(conn, query, column_names):

   """Import data from a PostgreSQL database using a SELECT query """   
   # Create a cursor object
   cursor = conn.cursor()  
   # Execute SQL commands to retrieve the current time and version from PostgreSQL 
   cursor.execute(query)
   # The execute returns a list of tuples:
   tuples_list = cursor.fetchall()
   # Close the cursor 
   cursor.close()
   # Now we need to transform the list into a pandas DataFrame:
   df = pd.DataFrame(tuples_list, columns=column_names)   
   return df