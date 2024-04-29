from langchain.llms import GooglePalm
from langchain.utilities import SQLDatabase
from langchain_experimental.sql import SQLDatabaseChain

import pymysql
import os
from dotenv import load_dotenv
load_dotenv()  # take environment variables from .env (especially openai api key)

# db = SQLDatabase.from_uri(f"mysql+pymysql://{db_user}:{db_password}@{db_host}/{db_name}",sample_rows_in_table_info=3)
conn = pymysql.connect(
    host = '127.0.0.1',
    port = 3306,
    user = 'root',
    passwd = 'rootroot@123',
    db = 'bank'
)

# # Create a cursor object
cursor = conn.cursor()

# SQL query to select all rows from exptable
sql_query = "select * from bank_inventory limit 5;"#"SELECT FROM bank_inventory"

# Execute the query
cursor.execute(sql_query)

# Fetch all rows
rows = cursor.fetchall()

cursor.close()
conn.close()

# llm = GooglePalm(google_api_key=os.environ["GOOGLE_API_KEY"], temperature=0.1)
print(rows)


# Print the rows
# for row in rows:
#     # Assuming each row contains text data to be processed
#     text_data = row[0]  # Adjust accordingly based on your table schema

#     # Process text data using Google Palm
#     response = llm.predict(text_data)
    
#     # Print or process the response as needed
#     print(response)

# Close the cursor and connection
# cursor.close()
# conn.close()

# llm = GooglePalm(google_api_key=os.environ["GOOGLE_API_KEY"], temperature=0.1)

# chain = SQLDatabaseChain(llm, cursor, verbose=True, prompt=sql_query)
# # chain= SQLDatabaseChain.from_llm(llm, cursor, verbose=True)
# print(chain({sql_query}))


# def get_few_shot_db_chain():
#     db_user = "root"
#     db_password = "rootroot@123"
#     db_host = "localhost"
#     db_name = "bank"

#     db = SQLDatabase.from_uri(f"mysql+pymysql://{db_user}:{db_password}@{db_host}/{db_name}",
#                               sample_rows_in_table_info=3)
#     llm = GooglePalm(google_api_key=os.environ["GOOGLE_API_KEY"], temperature=0.1)

#     mysql_prompt = """Find average Price of all products whose Geo_Location is usa
#     """
#     chain = SQLDatabaseChain.from_llm(llm, db, verbose=True, prompt=mysql_prompt)
#     return chain

# get_few_shot_db_chain()
