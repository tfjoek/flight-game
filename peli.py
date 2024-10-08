import mysql.connector
import os
import random
import time
from geopy.distance import distance as geopy_distance
from tarina import hae_tarina  # Importoi tarina uudesta tiedostosta

def create_connection():
    try:
        conn = mysql.connector.connect(
            host='127.0.0.1',
            port=3306,
            database='flight_game',
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


def get_star_rating(difficulty):
    stars = '⭐' * difficulty
    spaced_stars = ' '.join(stars)
    return spaced_stars

def get_airport_info(icao_code):
    conn = create_connection()
    if conn:
        cursor = conn.cursor(dictionary=True)
        query = "SELECT name, owner, latitude_deg, longitude_deg, difficulty FROM airport WHERE ident = %s"
        cursor.execute(query, (icao_code,))
        airport = cursor.fetchone()
        cursor.close()
        conn.close()
        return airport
    return None

def get_player_status(player_id):
    conn = create_connection()
    if conn:
        cursor = conn.cursor(dictionary=True)
        query = "SELECT location, fuel, war_points FROM game WHERE id = %s"
        cursor.execute(query, (player_id,))
        player = cursor.fetchone()

        cursor.execute("SELECT COUNT(*) AS remaining_airports FROM airport WHERE owner = 'Russia'")
        remaining_airports = cursor.fetchone()['remaining_airports']

        cursor.close()
        conn.close()

        return player, remaining_airports
    return None, None

def list_airports_by_owner(owner, emoji):
    os.system('cls' if os.name == 'nt' else 'clear')
    conn = create_connection()
    if conn:
        cursor = conn.cursor(dictionary=True)
        query = "SELECT ident, name, difficulty FROM airport WHERE owner = %s ORDER BY name"
        cursor.execute(query, (owner,))
        airports = cursor.fetchall()
        cursor.close()
        conn.close()

        if airports:
            print(f"Lentokentät {emoji} {owner}:n hallussa:")
            for airport in airports:
                stars = get_star_rating(airport['difficulty'])
                print(f"{emoji} - {airport['ident']} ({airport['name']}) {stars}")
        else:
            print(f"Ei lentokenttiä {emoji} {owner}:n hallussa.")

def list_all_airports():
    os.system('cls' if os.name == 'nt' else 'clear')
    conn = create_connection()
    if conn:
        cursor = conn.cursor(dictionary=True)
        query = "SELECT ident, name, owner, difficulty FROM airport ORDER BY name"
        cursor.execute(query)
        airports = cursor.fetchall()
        cursor.close()
        conn.close()

        if airports:
            print("Kaikki lentokentät aakkosjärjestyksessä:")
            for airport in airports:
                emoji = "🟦" if airport['owner'] == 'Finland' else "🟥"
                stars = get_star_rating(airport['difficulty'])
                print(f"{emoji} - {airport['ident']} ({airport['name']}) {stars}")
        else:
            print("Ei lentokenttiä löydetty.")

def open_store(itemBoostPercentage):
    conn = create_connection()
    if conn:
        cursor = conn.cursor(dictionary=True)
        query = "SELECT id, item, effect, price FROM store"
        cursor.execute(query)
        store = cursor.fetchall()

        cursor.close()
        conn.close()

        for item in store:
            print(f"{item['id']} {item['item']} {item['price']}€, {item['effect']}.")
        while True:
            storeChoice = input("Valitse numerolla:")
            if storeChoice == '1':
                itemBoostPercentage = 10
                break
            elif storeChoice == '2':
                itemBoostPercentage = 20
                break
            else:
                print("FAIL!")

    return itemBoostPercentage

def list_nearest_airports(player_location, limit=5):
    os.system('cls' if os.name == 'nt' else 'clear')
    conn = create_connection()
    if conn:
        cursor = conn.cursor(dictionary=True)
        query = """
            SELECT ident, name, latitude_deg, longitude_deg, owner, difficulty
            FROM airport
            WHERE owner = 'Russia'
        """
        cursor.execute(query)
        airports = cursor.fetchall()
        cursor.close()
        conn.close()

        player_airport = get_airport_info(player_location)
        if player_airport:
            player_coords = (player_airport['latitude_deg'], player_airport['longitude_deg'])

            airports_with_distance = []
            for airport in airports:
                airport_coords = (airport['latitude_deg'], airport['longitude_deg'])
                distance = geopy_distance(player_coords, airport_coords).km
                airports_with_distance.append((airport, distance))

            nearest_airports = sorted(airports_with_distance, key=lambda x: x[1])[:limit]
            print("\nValitse seuraava kohde:")
            for airport, distance in nearest_airports:
                stars = get_star_rating(airport['difficulty'])
                print(f"• {airport['ident']} ({airport['name']}) {stars} 🟥 - Etäisyys: {int(distance)} km")
        else:
            print("Nykyisen sijainnin tietoja ei löydy.")

def update_airport_owner(icao_code, new_owner):
    conn = create_connection()
    if conn:
        cursor = conn.cursor()
        query = "UPDATE airport SET owner = %s WHERE ident = %s"
        cursor.execute(query, (new_owner, icao_code))
        conn.commit()
        cursor.close()
        conn.close()

def update_player_fuel(player_id, fuel_cost):
    conn = create_connection()
    if conn:
        cursor = conn.cursor()
        query = "UPDATE game SET fuel = fuel - %s WHERE id = %s"
        cursor.execute(query, (fuel_cost, player_id))
        conn.commit()
        cursor.close()
        conn.close()

#debug 
def set_player_fuel_debug(player_id, new_fuel):
    conn = create_connection()
    if conn:
        cursor = conn.cursor()
        query = "UPDATE game SET fuel = %s WHERE id = %s"
        cursor.execute(query, (new_fuel, player_id))
        conn.commit()
        cursor.close()
        conn.close()




def move_player(player_id, destination_icao):
    conn = create_connection()
    if conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT location, fuel FROM game WHERE id = %s", (player_id,))
        player = cursor.fetchone()

        if player:
            current_location = player['location']
            current_fuel = player['fuel']

            current_airport = get_airport_info(current_location)
            destination_airport = get_airport_info(destination_icao)

            if current_airport and destination_airport:
                # Check if the destination airport is controlled by Russia
                if destination_airport['owner'] == 'Russia':
                    print("\n⚠️ VAROITUS! Yrität liikkua Venäjän omistamaan lentokenttään.")
                    print("Sinun täytyy hyökätä ennen kuin voit siirtyä sinne.")
                    print("1 - Hyökkää lentokentälle")
                    print("2 - Peruuta")

                    attack_choice = input("Valitse toiminto (1 tai 2): ")

                    if attack_choice == '1':
                        attack_airport(player_id, destination_icao)
                        return  # Exit the move function after the attack process
                    elif attack_choice == '2':
                        print("Liikkuminen peruutettu.")
                        return  # Exit the move function without moving the player
                    else:
                        print("⚠️ Virheellinen valinta, liikkuminen peruutettu.")
                        return  # Exit the move function without moving the player

                # If the airport is not controlled by Russia, proceed with the move
                current_coords = (current_airport['latitude_deg'], current_airport['longitude_deg'])
                destination_coords = (destination_airport['latitude_deg'], destination_airport['longitude_deg'])
                distance = geopy_distance(current_coords, destination_coords).km
                fuel_cost = distance  # Fuel cost equals the distance traveled

                if fuel_cost > current_fuel:
                    print(f"❌ Sinulla ei ole tarpeeksi polttoainetta tähän matkaan. Tarvittava polttoaine: {fuel_cost:.2f} km.")
                else:
                    new_fuel = current_fuel - fuel_cost
                    cursor.execute("UPDATE game SET location = %s, fuel = %s WHERE id = %s", (destination_icao, new_fuel, player_id))
                    conn.commit()
                    print(f"Olet nyt saapunut kohteeseen {destination_icao}. Matka oli {distance:.2f} km, polttoainetta jäljellä: {new_fuel:.2f} km.")
            else:
                print("Virhe: Kohteen tai lähtöpaikan tietoja ei löytynyt.")
        cursor.close()
        conn.close()


def attack_airport(player_id, destination_icao):
    destination_airport = get_airport_info(destination_icao)
    player = get_player_status(player_id)[0]

    if destination_airport and destination_airport['owner'] == 'Russia' and player:
        current_airport = get_airport_info(player['location'])

        # Lasketaan etäisyys nykyisestä sijainnista kohteeseen
        current_coords = (current_airport['latitude_deg'], current_airport['longitude_deg'])
        destination_coords = (destination_airport['latitude_deg'], destination_airport['longitude_deg'])
        distance = geopy_distance(current_coords, destination_coords).km

        # Vaikeustason määrittely
        difficulty = destination_airport['difficulty']
        fast_attack_success_range = {
            1: (35, 45),  # Muutettu vaikeammaksi
            2: (30, 40),
            3: (25, 35),
            4: (20, 30),
            5: (15, 25)
        }
        precise_attack_success_range = {
            1: (50, 60),  # Muutettu vaikeammaksi
            2: (45, 55),
            3: (40, 50),
            4: (35, 45),
            5: (30, 40)
        }

        print("\n⚔️ Valitse hyökkäystyyli:")
        print(f"1. ⚡ Nopeampi hyökkäys (vähemmän tarkka) - Polttoainekustannus: {distance * 0.5:.2f} km")
        print(f"2. 🎯 Tarkempi hyökkäys (suurempi onnistumismahdollisuus) - Polttoainekustannus: {distance:.2f} km")

        attack_choice = input("\nValintasi (1 tai 2): ")

        if attack_choice == '1':
            success_chance_range = fast_attack_success_range[difficulty]
            success_chance = random.randint(*success_chance_range)
            fuel_cost = distance * 0.5  # Nopeampi hyökkäys kuluttaa vähemmän polttoainetta

            if fuel_cost > player['fuel']:
                print("❌ Sinulla ei ole tarpeeksi polttoainetta hyökätä tähän kohteeseen!")
            else:
                print(f"\n⚡ Valitsit nopeamman hyökkäyksen! Onnistumistodennäköisyys: {success_chance}%, Polttoainekustannus: {fuel_cost:.2f} km")
                print(f"🚀 Polttoainetta jäljellä ennen hyökkäystä: {player['fuel']:.2f} km")
                time.sleep(1)
                print("\n🛩️ Hyökkäys käynnissä...")
                time.sleep(2)
                print("\n🚀 Ammuit raketin niitä päin!")
                time.sleep(2)

                if random.randint(1, 100) <= success_chance:
                    print(f"🏆 Hyökkäys kohteeseen {destination_airport['name']} onnistui! Hyvin pelattu! Lentokenttä on nyt Suomen hallinnassa.")
                    update_airport_owner(destination_icao, 'Finland')
                else:
                    print("❌ Hyökkäys epäonnistui! Menetit polttoainetta, mutta kohde pysyi Venäjän hallinnassa...")
                    update_player_fuel(player_id, fuel_cost)
                    print(f"Polttoainetta jäljellä hyökkäyksen jälkeen: {player['fuel'] - fuel_cost:.2f} km")

        elif attack_choice == '2':
            success_chance_range = precise_attack_success_range[difficulty]
            success_chance = random.randint(*success_chance_range)
            fuel_cost = distance  # Tarkempi hyökkäys kuluttaa enemmän polttoainetta

            if fuel_cost > player['fuel']:
                print("❌ Sinulla ei ole tarpeeksi polttoainetta hyökätä tähän kohteeseen!")
            else:
                print(f"\n🎯 Valitsit tarkemman hyökkäyksen! Onnistumistodennäköisyys: {success_chance}%, Polttoainekustannus: {fuel_cost:.2f} km")
                print(f"🚀 Polttoainetta jäljellä ennen hyökkäystä: {player['fuel']:.2f} km")
                time.sleep(1)
                print("\n🛩️ Hyökkäys käynnissä...")
                time.sleep(2)
                print("\n🚀 Hiivit heidän taakse... ja HYÖKKÄÄT!")
                time.sleep(2)

                if random.randint(1, 100) <= success_chance:
                    print(f"🏆 Hyökkäys kohteeseen {destination_airport['name']} onnistui! Lentokenttä on nyt Suomen hallinnassa.")
                    update_airport_owner(destination_icao, 'Finland')
                else:
                    print("❌ Hyökkäys epäonnistui! Menetit polttoainetta, mutta kohde pysyi Venäjän hallinnassa...")
                    update_player_fuel(player_id, fuel_cost)
                    print(f"Polttoainetta jäljellä hyökkäyksen jälkeen: {player['fuel'] - fuel_cost:.2f} km")
        else:
            print("⚠️ Virheellinen valinta, hyökkäys peruutettu.")
    else:
        print("⚠️ Et voi hyökätä tähän lentokenttään, koska se ei ole Venäjän hallussa.")




def display_player_status(player, remaining_airports):
    current_airport = get_airport_info(player['location'])
    if current_airport:
        emoji = "🟦" if current_airport['owner'] == 'Finland' else "🟥"
        stars = get_star_rating(current_airport['difficulty'])
        print(f"\n✈️  Pelaaja on lentokentällä: {emoji} {current_airport['name']} ({player['location']}) {stars}")
    else:
        print("Virhe: Lentokentän tietoja ei löytynyt.")

    print(f"🚀 Polttoainetta: {player['fuel']} km")
    print(f"🎯 Vapauttamattomia kenttiä: {remaining_airports}")
    print(f"🛡️  Sotapisteet: {player['war_points']}")

def wait_for_enter():
    input("Paina enter jatkaaksesi...")

def display_story():
    tarina = hae_tarina()
    tarinaHalu = input("Halutako lukea tarinan (Y/N): ")
    if tarinaHalu.upper() == 'Y':
        for osa in tarina:
            os.system('cls' if os.name == 'nt' else 'clear')
            print(osa)
            wait_for_enter()

if __name__ == "__main__":
    display_story()
    os.system('cls' if os.name == 'nt' else 'clear')
    print("Tarinan loppu. Paina enter aloittaaksesi seikkailun...")
    wait_for_enter()

    player_id = '1'
    itemBoostPercentage = 0  

    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        player, remaining_airports = get_player_status(player_id)
        if player:
            display_player_status(player, remaining_airports)
        else:
            print("Pelaajan tietojen haku epäonnistui.")

        print("\n📒✏️: Valitse seuraava toimintasi:")
        print("1 - Selaa lentokenttiä")
        print("2 - Hyökkää lentokentälle")
        print("3 - Liiku lentokentälle")
        print("4 - Debug: Muuta pelaajan polttoainetta")
        print("5 - Listaa kaikki lentokentät")
        print("6 - Avaa kauppa") 

        choice = input("Valitse vaihtoehto: ")

        if choice == '1':
            print("\n1 - Listaa Suomen hallussa olevat lentokentät")
            print("2 - Listaa Venäjän vallassa olevat lentokentät")
            print("3 - Listaa lentokentät etäisyyden mukaan")
            print("4 - Listaa lentokentät aakkosjärjestyksessä")
            sub_choice = input("Valitse luokittelu: ")

            if sub_choice == '1':
                list_airports_by_owner('Finland', '🟦')
            elif sub_choice == '2':
                list_airports_by_owner('Russia', '🟥')
            elif sub_choice == '3':
                list_nearest_airports(player['location'])
            elif sub_choice == '4':
                list_all_airports()
            else:
                print("⚠️ Virheellinen valinta.")
            wait_for_enter()
        elif choice == '2':
            print("Valitset hyökkäyskohteen lähimmistä kohteista:")
            list_nearest_airports(player['location'])
            destination = input("\n🎯 Syötä hyökkäyskohteen ICAO-tunnus (esim. EFHK tai 'cancel' peruuttaaksesi): ").upper()
            if destination == 'CANCEL':
                print("Peruutettu.")
            else:
                attack_airport(player_id, destination)
            wait_for_enter()
        elif choice == '3':
            destination = input("\n✈️ Syötä kohteen ICAO-tunnus (esim. EFHK tai 'cancel' peruuttaaksesi): ").upper()
            if destination == 'CANCEL':
                print("Peruutettu.")
            else:
                move_player(player_id, destination)
            wait_for_enter()
        elif choice == '4':
            new_fuel = input("🔧 Syötä uusi polttoainemäärä (km): ")
            if new_fuel.isdigit():
                set_player_fuel_debug(player_id, int(new_fuel))
                print(f"Polttoainemäärä päivitetty: {new_fuel} km")
            else:
                print("Virheellinen syöte, polttoainetta ei päivitetty.")
            wait_for_enter()

        elif choice == '5':
            list_all_airports()
            wait_for_enter()
        elif choice == '6':  
            itemBoostPercentage = open_store(itemBoostPercentage)
            wait_for_enter()
        else:
            print("⚠️ Virheellinen valinta, jatketaan...")
            wait_for_enter()
