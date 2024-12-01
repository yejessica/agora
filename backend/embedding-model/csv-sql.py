import pandas as pd
import sqlite3

# CSV file path
csv_file = 'yc-companies.csv'

# Read CSV into a DataFrame
df = pd.read_csv(csv_file)

# SQLite database file (it will be created if it doesn't exist)
db_file = 'yc-companies.db'

# Connect to SQLite database
conn = sqlite3.connect(db_file)

# Specify the table name
table_name = 'companies'

# Write the DataFrame to the SQL table
try:
    df.to_sql(table_name, conn, if_exists='replace', index=False)  # Creates the table if it doesn't exist
    print(f"Data successfully written to the '{table_name}' table in '{db_file}'!")
except Exception as e:
    print(f"An error occurred: {e}")
finally:
    conn.close()  # Close the connection
