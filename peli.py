import mysql.connector
import random

# LAITA OMAT USERNAME JA PASSWORD
conn = mysql.connector.connect(
    host='127.0.0.1',
    port=3306,
    database='flight_game',
    user='vennilim',
    password='chungus',
    charset='utf8mb4',
    collation='utf8mb4_general_ci',
    autocommit=True
)

# YHTEYS
if conn.is_connected():
    print("Yhteys tietokantaan on muodostettu onnistuneesti!")

#JEeE
cursor = conn.cursor(dictionary=True)
cursor.execute("SELECT name FROM airport;")
airports = cursor.fetchall()

# 10 PRINT TEST
if len(airports) >= 10:
    random_airports = random.sample(airports, 10)
    for airport in random_airports:
        print(airport['name'])
else:
    print("Lentokenttiä ei ole tarpeeksi tulostettavaksi.")

# sulje yhteys
cursor.close()
conn.close()
