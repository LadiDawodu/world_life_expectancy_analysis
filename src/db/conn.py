import mysql.connector

# Connect to MySQL database

def get_conn():

        try:
                conn = mysql.connector.connect(
                host="127.0.0.1",
                user="root",
                password="Trickstar2andrew95!",
                database="work_life_expectancy"
        )
                if conn.is_connected():
                        print("Connection to MySQL database established successfully!")
                        return conn
                else:
                         print("Failed to establish connection to MySQL database!")
                         return None

#                cursor = conn.cursor(buffered=True)
        # Open and read the SQL file
#                with open('src/data/world_life_expectancy_EDA.sql', 'r') as file:
#                        queries = file.read()

        # Split queries by delimiter (assuming ';' delimiter)

#                query_list = queries.split(';')

#                for query in query_list:
#                        if query.strip():
#                                cursor.execute(query)

        # ... (optional: handle results if needed)

#                conn.commit()  # Assuming changes were made

        except mysql.connector.Error as err:
                print("Error:", err)
                return None

#        finally:
#       if cursor:
#                cursor.close()
#        if conn:
#                conn.close()

#        print("Database operations completed.")
conn = get_conn()
print(get_conn)