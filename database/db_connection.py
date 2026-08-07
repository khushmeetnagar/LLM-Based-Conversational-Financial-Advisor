import mysql.connector

def connect_db():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="1234",
            database="financial_advisor_db"
        )

        if connection.is_connected():
            print("✅ Database Connected Successfully")

        return connection

    except mysql.connector.Error as err:
        print("❌ Database Connection Error:", err)
        return None