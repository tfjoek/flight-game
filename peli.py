import mysql.connector
import os
import math
from tarina import hae_tarina  # Importoi tarina uudesta tiedostosta

def create_connection():
    try:
        conn = mysql.connector.connect(
            host='127.0.0.1',
            port=3306,
            database='testi1',
            user='vennilim',
            password='kappa123',
            charset='utf8mb4',
            collation='utf8mb4_general_ci',
            autocommit=True
        )
        if conn.is_connected():
            return conn
        else:
            print("Yhteyttä ei voitu muodostaa.")
            return None
    except mysql.connector.Error as err:
        print(f"Tietokantavirhe: {err}")
        return None

def get_airport_info(icao_code):
    """Hakee lentokentän tiedot ICAO-koodilla."""
    conn = create_connection()
    if conn:
        cursor = conn.cursor(dictionary=True)
        query = "SELECT name, owner FROM airport WHERE ident = %s"
        cursor.execute(query, (icao_code,))
        airport = cursor.fetchone()
        cursor.close()
        conn.close()
        return airport
    return None

def calculate_distance(lat1, lon1, lat2, lon2):
    """Laskee etäisyyden kahden pisteen välillä Haversine-kaavalla."""
    R = 6371  # Maapallon säde kilometreinä
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2) ** 2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

def move_player(player_id, destination_icao):
    """Pelaajan liikkuminen kohteeseen ja polttoaineen vähentäminen."""
    conn = create_connection()
    if conn:
        cursor = conn.cursor(dictionary=True)

        # Hakee pelaajan sijainnin ja polttoaineen
        cursor.execute("SELECT location, fuel FROM game WHERE id = %s", (player_id,))
        player = cursor.fetchone()

        if player:
            current_location = player['location']
            current_fuel = player['fuel']

            # Hakee nykyisen sijainnin ja kohteen koordinaatit
            current_airport = get_airport_location(current_location)
            destination_airport = get_airport_location(destination_icao)

            if current_airport and destination_airport:
                lat1, lon1 = current_airport['latitude_deg'], current_airport['longitude_deg']
                lat2, lon2 = destination_airport['latitude_deg'], destination_airport['longitude_deg']

                distance = calculate_distance(lat1, lon1, lat2, lon2)

                if distance > current_fuel:
                    print(f"Sinulla ei ole tarpeeksi polttoainetta tähän matkaan. Tarvittava polttoaine: {distance:.2f} km.")
                else:
                    # Päivittää pelaajan sijainnin ja vähentää polttoainetta
                    new_fuel = current_fuel - distance
                    cursor.execute("UPDATE game SET location = %s, fuel = %s WHERE id = %s", (destination_icao, new_fuel, player_id))
                    conn.commit()
                    print(f"Olet nyt saapunut kohteeseen {destination_icao}. Matka oli {distance:.2f} km, polttoainetta jäljellä: {new_fuel:.2f} km.")
            else:
                print("Virhe: Kohteen tai lähtöpaikan tietoja ei löytynyt.")
        cursor.close()
        conn.close()

def update_player_fuel(player_id, new_fuel):
    # Päivittää pelaajan polttoainemäärän tietokantaan
    conn = create_connection()
    if conn:
        cursor = conn.cursor()
        query = "UPDATE game SET fuel = %s WHERE id = %s"
        cursor.execute(query, (new_fuel, player_id))
        conn.commit()
        cursor.close()
        conn.close()

def get_player_status(player_id):
    # Hakee pelaajan statsit tietokannasta
    conn = create_connection()
    if conn:
        cursor = conn.cursor(dictionary=True)
        query = "SELECT location, fuel, war_points FROM game WHERE id = %s"
        cursor.execute(query, (player_id,))
        player = cursor.fetchone()

        cursor.execute("SELECT COUNT(*) AS remaining_airports FROM airport WHERE ident NOT IN (SELECT location FROM game)")
        remaining_airports = cursor.fetchone()['remaining_airports']

        cursor.close()
        conn.close()

        return player, remaining_airports
    return None, None

def list_airports_by_owner(owner, emoji):
    """Hakee ja näyttää lentokentät omistajan mukaan """
    conn = create_connection()
    if conn:
        cursor = conn.cursor(dictionary=True)
        query = "SELECT ident, name FROM airport WHERE owner = %s ORDER BY name"
        cursor.execute(query, (owner,))
        airports = cursor.fetchall()

        cursor.close()
        conn.close()

        if airports:
            print(f"Lentokentät {emoji} {owner}:n hallussa:")
            for airport in airports:
                print(f"{emoji} - {airport['ident']} ({airport['name']})")
        else:
            print(f"Ei lentokenttiä {emoji} {owner}:n hallussa.")

def list_all_airports():
    """Hakee ja näyttää kaikki lentokentät aakkosjärjestyksessä."""
    conn = create_connection()
    if conn:
        cursor = conn.cursor(dictionary=True)
        query = "SELECT ident, name, owner FROM airport ORDER BY name"
        cursor.execute(query)
        airports = cursor.fetchall()

        cursor.close()
        conn.close()

        if airports:
            print("Kaikki lentokentät aakkosjärjestyksessä:")
            for airport in airports:
                emoji = "🟦" if airport['owner'] == 'Finland' else "🟥"
                print(f"{emoji} - {airport['ident']} ({airport['name']})")
        else:
            print("Ei lentokenttiä löydetty.")

# Pelaajan nykyiset statsit
def display_player_status(player, remaining_airports):
    os.system('cls' if os.name == 'nt' else 'clear')
    current_airport = get_airport_info(player['location'])
    if current_airport:
        emoji = "🟦" if current_airport['owner'] == 'Finland' else "🟥"
        location_line = f"✈️  Pelaaja on lentokentällä: {current_airport['name']} ({player['location']}) {emoji}"
    else:
        location_line = "Virhe: Lentokentän tietoja ei löytynyt."

    term_size = os.get_terminal_size()
    print('╔' + '═' * (term_size.columns - 2) + '╗')
    print(f"║ {location_line.center(term_size.columns - 4)} ║")
    print('╠' + '═' * (term_size.columns - 2) + '╣')
    print(f"║ 🚀 Polttoainetta: {player['fuel']} km".ljust(term_size.columns - 2) + '║')
    print(f"║ 🎯 Vapauttamattomia kenttiä: {remaining_airports}".ljust(term_size.columns - 2) + '║')
    print(f"║ 🛡️  Sotapisteet: {player['war_points']}".ljust(term_size.columns - 2) + '║')
    print('╠' + '═' * (term_size.columns - 2) + '╣')
    print(f"║ 🟦 1 - Listaa Suomen hallussa olevat lentokentät".ljust(term_size.columns - 2) + '║')
    print(f"║ 🟥 2 - Listaa Venäjän vallassa olevat lentokentät".ljust(term_size.columns - 2) + '║')
    print(f"║ ✈️  3 - Liiku lentokentälle".ljust(term_size.columns - 2) + '║')
    print(f"║ 🛠  4 - Debug: Muuta pelaajan polttoainetta".ljust(term_size.columns - 2) + '║')
    print(f"║ 🌍 5 - Listaa kaikki lentokentät aakkosjärjestyksessä".ljust(term_size.columns - 2) + '║')
    print('╚' + '═' * (term_size.columns - 2) + '╝')

def wait_for_enter():
    input("Paina enter jatkaaksesi...")

def display_story():
    # Hakee tarinan tiedostosta ja tulostaa sen
    tarina = hae_tarina()  
    tarinaHalu = input("Halutako lukea tarinan (Y/N): ")
    if tarinaHalu.upper() == 'Y':
        for osa in tarina:
            os.system('cls' if os.name == 'nt' else 'clear')
            print(osa)
            wait_for_enter()

if __name__ == "__main__":
    display_story()

    # Tarina loppuessa pelaajan perusnäyttö eli statsit näkyviin
    os.system('cls' if os.name == 'nt' else 'clear')
    print("Tarinan loppu. Paina enter aloittaaksesi seikkailun...")
    wait_for_enter()

    player_id = '1'

    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        player, remaining_airports = get_player_status(player_id)
        if player:
            display_player_status(player, remaining_airports)
        else:
            print("Pelaajan tietojen haku epäonnistui.")

        choice = input("Valitse toiminto (1, 2, 3, 4 tai 5): ")

        if choice == '1':
            list_airports_by_owner('Finland', '🟦')
        elif choice == '2':
            list_airports_by_owner('Russia', '🟥')
        elif choice == '3':
            destination = input("Syötä kohteen ICAO-tunnus (esim. EFHK tai 'cancel' peruuttaaksesi): ").upper()
            if destination == 'CANCEL':
                print("Peruutettu.")
            else:
                move_player(player_id, destination)
        elif choice == '4':
            new_fuel = input("Syötä uusi polttoainemäärä (km): ")
            if new_fuel.isdigit():
                update_player_fuel(player_id, int(new_fuel))
                print(f"Polttoainemäärä päivitetty: {new_fuel} km")
            else:
                print("Virheellinen syöte, polttoainetta ei päivitetty.")
        elif choice == '5':
            list_all_airports()
        else:
            print("Virheellinen valinta, jatketaan...")

        wait_for_enter()
