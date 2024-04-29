import pandas as pd
import pymysql  
# Database connection details (replace with yours)
# db_user = "root"
# db_password = "rootroot@123"
# db_host = "127.0.0.1"
# db_name = "bank"

# # Connect to the database
# conn = pymysql.connect(
#     host=db_host,
#     user=db_user,
#     password=db_password,
#     database=db_name
# )

# # SQL query to retrieve conversation logs
# sql_query = """SELECT * FROM question_response
#                ORDER BY id DESC
#                LIMIT 5;"""

# # Execute the query and store results in a DataFrame
# df = pd.read_sql(sql_query, conn)

# # Close the connection
# conn.close()



# df.to_excel("backend/database_logs/conversation_logs.xlsx", index=False)  # Save as 'conversation_logs.xlsx' without index column

def get_and_export_conversation_logs():
  """
  Connects to the database, retrieves the last 5 conversation logs,
  stores them in a Pandas DataFrame, and exports the DataFrame to an Excel file.

  Returns:
      None
  """

  # Database connection details (replace with yours)
  db_user = "root"
  db_password = "rootroot@123"
  db_host = "127.0.0.1"
  db_name = "bank"

  try:
    # Connect to the database
    conn = pymysql.connect(
        host=db_host,
        user=db_user,
        password=db_password,
        database=db_name
    )

    # SQL query to retrieve conversation logs
    sql_query = """SELECT * FROM question_response
                    ORDER BY id DESC
                    LIMIT 5;"""

    # Execute the query and store results in a DataFrame
    df = pd.read_sql(sql_query, conn)

  except pymysql.Error as e:
    print(f"Error connecting to database:{e}")
    return

  finally:
    # Close the connection (always execute, even in case of errors)
    conn.close()

  # Export DataFrame to Excel (assuming successful database connection)
  df.to_excel("backend/database_logs/conversation_logs.xlsx", index=False)

