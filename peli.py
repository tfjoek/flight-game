import mysql.connector

#VAIHDA NÄMÄ SUN OMIIN SALASANOIIN JA USERNAMEEN JA JOS SUL ERI NIMINEN DB LOKAALISESTI
#VAIHDA NÄMÄ SUN OMIIN SALASANOIIN JA USERNAMEEN JA JOS SUL ERI NIMINEN DB LOKAALISESTI
#VAIHDA NÄMÄ SUN OMIIN SALASANOIIN JA USERNAMEEN JA JOS SUL ERI NIMINEN DB LOKAALISESTI
#VAIHDA NÄMÄ SUN OMIIN SALASANOIIN JA USERNAMEEN JA JOS SUL ERI NIMINEN DB LOKAALISESTI
#VAIHDA NÄMÄ SUN OMIIN SALASANOIIN JA USERNAMEEN JA JOS SUL ERI NIMINEN DB LOKAALISESTI
conn = mysql.connector.connect(
    host='127.0.0.1',
    port=3306,
    database='flight_game',
    user='vennilim',
    password='godpassword',
    autocommit=True
)

#    jos tulee hintti error voi kokeilla laittaa nää tohon yhistykseen
#    charset='utf8mb4',            
#    collation='utf8mb4_general_ci', 


#yhteys testo
if conn.is_connected():
    print("Yhteys tietokantaan on muodostettu onnistuneesti!")

cursor = conn.cursor(dictionary=True)
cursor.execute("SELECT name FROM airport WHERE iso_country = 'FI' LIMIT 10;")  # Haetaan Suomen 10 ekaa lentokenttää
airports = cursor.fetchall()
for airport in airports:
    print(airport['name'])

