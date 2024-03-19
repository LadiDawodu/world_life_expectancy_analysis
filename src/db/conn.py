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



        except mysql.connector.Error as err:
                print("Error:", err)
                return None

conn = get_conn()
print(get_conn)