import mysql.connector
import os
import random
import time
from geopy.distance import distance as geopy_distance
from tarina import hae_tarina  # Importoi tarina uudesta tiedostosta

# Creates and manages the database connection
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

# Resets the game state for the player
def reset_game_on_start(player_id):
    reset_player_stats(player_id)
    reset_airports()
    reset_inventory(player_id)  # Resets the player's inventory at the start
    print("Peli on nollattu ja aloitat alusta!")

# Resets player stats like location, fuel, and war points
def reset_player_stats(player_id):
    conn = create_connection()
    if conn:
        cursor = conn.cursor()
        query = "UPDATE game SET location=(SELECT location FROM game WHERE id = 1), fuel=100, war_points=0 WHERE id = %s"
        cursor.execute(query, (player_id,))
        conn.commit()
        cursor.close()
        conn.close()

# Resets the ownership of all airports to their default values
def reset_airports():
    conn = create_connection()
    if conn:
        cursor = conn.cursor()
        query = """
            UPDATE airport 
            SET owner='Russia' 
            WHERE difficulty > 0 AND ident != 'EFTP'
        """
        cursor.execute(query)
        cursor.execute("UPDATE airport SET owner='Finland' WHERE ident = 'EFTP'")
        conn.commit()
        cursor.close()
        conn.close()

# Clears the player's inventory, removing all items they possess
def reset_inventory(player_id):
    conn = create_connection()
    if conn:
        cursor = conn.cursor()
        query = "DELETE FROM inventory WHERE player_id = %s"
        cursor.execute(query, (player_id,))
        conn.commit()
        cursor.close()
        conn.close()
        print("Inventaario on nollattu.")

# Displays the star rating based on the airport's difficulty level
def get_star_rating(difficulty):
    stars = '⭐' * difficulty
    spaced_stars = ' '.join(stars)
    return spaced_stars

# Retrieves detailed information about a specific airport
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

# Retrieves player status like location, fuel, and remaining airports to be liberated
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

# Lists airports controlled by a specific owner (Finland or Russia)
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

# Lists all airports by difficulty level
def list_airports_by_difficulty():
    conn = create_connection()
    if conn:
        cursor = conn.cursor(dictionary=True)
        query = "SELECT ident, name, difficulty, owner FROM airport ORDER BY difficulty DESC"
        cursor.execute(query)
        airports = cursor.fetchall()
        cursor.close()
        conn.close()

        print("\nLentokentät vaikeustason mukaan:")
        for airport in airports:
            emoji = "🟦" if airport['owner'] == 'Finland' else "🟥"
            stars = get_star_rating(airport['difficulty'])
            print(f"{emoji} - {airport['ident']} ({airport['name']}) {stars}")

# Calculates the percentage of airports liberated from Russian control
def calculate_liberation_percentage():
    conn = create_connection()
    if conn:
        cursor = conn.cursor(dictionary=True)
        query_total = "SELECT COUNT(*) as total_airports FROM airport"
        query_finland = "SELECT COUNT(*) as finland_airports FROM airport WHERE owner = 'Finland'"
        cursor.execute(query_total)
        total_airports = cursor.fetchone()['total_airports']
        cursor.execute(query_finland)
        finland_airports = cursor.fetchone()['finland_airports']
        cursor.close()
        conn.close()

        liberation_percentage = (finland_airports / total_airports) * 100
        return liberation_percentage

# Lists the nearest airports from the player's current location
def list_nearest_airports(player_location):
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

            nearest_airports = sorted(airports_with_distance, key=lambda x: x[1])
            print("\nValitse seuraava kohde:")
            for airport, distance in nearest_airports:
                stars = get_star_rating(airport['difficulty'])
                print(f"• {airport['ident']} ({airport['name']}) {stars} 🟥 - Etäisyys: {int(distance)} km")
        else:
            print("Nykyisen sijainnin tietoja ei löydy.")

# Updates the ownership of an airport
def update_airport_owner(icao_code, new_owner):
    conn = create_connection()
    if conn:
        cursor = conn.cursor()
        query = "UPDATE airport SET owner = %s WHERE ident = %s"
        cursor.execute(query, (new_owner, icao_code))
        conn.commit()
        cursor.close()
        conn.close()

# Updates the player's fuel after movement or attack
def update_player_fuel(player_id, fuel_cost):
    conn = create_connection()
    if conn:
        cursor = conn.cursor()
        query = "UPDATE game SET fuel = fuel - %s WHERE id = %s"
        cursor.execute(query, (fuel_cost, player_id))
        conn.commit()
        cursor.close()
        conn.close()

# Debug function to manually set a player's fuel level
def set_player_fuel_debug(player_id, new_fuel):
    conn = create_connection()
    if conn:
        cursor = conn.cursor()
        query = "UPDATE game SET fuel = %s WHERE id = %s"
        cursor.execute(query, (new_fuel, player_id))
        conn.commit()
        cursor.close()
        conn.close()

# Debug function to manually set a player's war points
def set_player_war_points_debug(player_id, new_war_points):
    conn = create_connection()
    if conn:
        cursor = conn.cursor()
        query = "UPDATE game SET war_points = %s WHERE id = %s"
        cursor.execute(query, (new_war_points, player_id))
        conn.commit()
        cursor.close()
        conn.close()

# Displays the player's inventory, showing items and their quantities
def display_inventory(player_id):
    conn = create_connection()
    if conn:
        cursor = conn.cursor(dictionary=True)
        query = """
            SELECT i.name, inv.quantity 
            FROM inventory inv
            JOIN item i ON inv.item_id = i.id
            WHERE inv.player_id = %s
        """
        cursor.execute(query, (player_id,))
        items = cursor.fetchall()
        cursor.close()
        conn.close()

        if items:
            print("\n🎒 Inventaario:")
            for item in items:
                print(f"- {item['name']} (Määrä: {item['quantity']})")
        else:
            print("Inventaario on tyhjä.")
    else:
        print("Tietokantavirhe: inventaariota ei voitu hakea.")

# Checks if a player has a specific item with a given effect
def has_item(player_id, item_effect):
    conn = create_connection()
    if conn:
        cursor = conn.cursor(dictionary=True)
        query = """
            SELECT i.id FROM inventory inv
            JOIN item i ON inv.item_id = i.id
            WHERE inv.player_id = %s AND i.effect = %s
        """
        cursor.execute(query, (player_id, item_effect))
        item = cursor.fetchone()
        cursor.close()
        conn.close()
        return item is not None  # Returns True if the item is found, otherwise False
    return False

# Calculates the fuel cost for a movement or attack, considering item effects
def calculate_fuel_cost(player_id, base_fuel_cost):
    # Check for specific fuel boosters and reduce the fuel cost accordingly
    if has_item(player_id, 'debug_fuel_saver'):
        return base_fuel_cost * 0.10  # Reduces fuel consumption by 90%
    elif has_item(player_id, 'fuel_efficiency_booster_15_percent'):
        return base_fuel_cost * 0.85  # Reduces fuel consumption by 15%
    elif has_item(player_id, 'fuel_efficiency_booster_10_percent'):
        return base_fuel_cost * 0.90  # Reduces fuel consumption by 10%
    elif has_item(player_id, 'fuel_efficiency_booster_5_percent'):
        return base_fuel_cost * 0.95  # Reduces fuel consumption by 5%
    else:
        return base_fuel_cost  # No booster found, return the original cost


# Guide to create a new item:
# 1. Insert a new item into the item table in the database.
# 2. Set the name, description, price, and effect for the item.
# 3. Example SQL command to create a new item:
#    INSERT INTO item (name, description, price, effect) VALUES ('Super Fuel Booster', 'Reduces fuel cost by 15%', 20, 'fuel_booster');
# 4. Ensure that the effect matches the name used in the has_item function logic.




# Muutetaan polttoaineen kulutus funktiota käyttäessä liikkumista ja hyökkäystä
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
                if destination_airport['owner'] == 'Russia':
                    print("\n⚠️ VAROITUS! Yrität liikkua Venäjän omistamaan lentokenttään.")
                    print("Sinun täytyy hyökätä ennen kuin voit siirtyä sinne.")
                    attack_airport(player_id, destination_icao)
                    return

                current_coords = (current_airport['latitude_deg'], current_airport['longitude_deg'])
                destination_coords = (destination_airport['latitude_deg'], destination_airport['longitude_deg'])
                base_fuel_cost = geopy_distance(current_coords, destination_coords).km
                fuel_cost = calculate_fuel_cost(player_id, base_fuel_cost)

                if fuel_cost > current_fuel:
                    print(f"❌ Sinulla ei ole tarpeeksi polttoainetta tähän matkaan. Tarvittava polttoaine: {fuel_cost:.2f} km.")
                else:
                    new_fuel = current_fuel - fuel_cost
                    cursor.execute("UPDATE game SET location = %s, fuel = %s WHERE id = %s", (destination_icao, new_fuel, player_id))
                    conn.commit()
                    print(f"Olet nyt saapunut kohteeseen {destination_icao}. Matka oli {base_fuel_cost:.2f} km, polttoainetta jäljellä: {new_fuel:.2f} km.")
        cursor.close()
        conn.close()

def attack_airport(player_id, destination_icao):
    destination_airport = get_airport_info(destination_icao)
    player = get_player_status(player_id)[0]

    if destination_airport and destination_airport['owner'] == 'Russia' and player:
        current_airport = get_airport_info(player['location'])
        current_coords = (current_airport['latitude_deg'], current_airport['longitude_deg'])
        destination_coords = (destination_airport['latitude_deg'], destination_airport['longitude_deg'])
        distance = geopy_distance(current_coords, destination_coords).km

        fast_attack_success_range = {
            1: (35, 45),
            2: (30, 40),
            3: (25, 35),
            4: (20, 30),
            5: (15, 25)
        }
        precise_attack_success_range = {
            1: (50, 60),
            2: (45, 55),
            3: (40, 50),
            4: (35, 45),
            5: (30, 40)
        }

        # Lasketaan polttoainekustannus ottaen huomioon esineiden vaikutus
        fast_attack_cost = calculate_fuel_cost(player_id, distance * 0.5)
        precise_attack_cost = calculate_fuel_cost(player_id, distance)

        print("\n⚔️ Valitse hyökkäystyyli:")
        print(f"1. ⚡ Nopeampi hyökkäys - Polttoainekustannus: {fast_attack_cost:.2f} km")
        print(f"2. 🎯 Tarkempi hyökkäys - Polttoainekustannus: {precise_attack_cost:.2f} km")

        attack_choice = input("\nValintasi (1 tai 2): ").strip()

        if attack_choice == '2' and precise_attack_cost > player['fuel']:
            print("⚠️ VAROITUS! Sinulla ei ole tarpeeksi polttoainetta tarkempaan hyökkäykseen.")
            varmistus = input("Haluatko hyökätä nopeasti sen sijaan? (K/E): ").strip().upper()
            if varmistus == 'K':
                attack_choice = '1'
            else:
                print("⚠️ Hyökkäys peruutettu.")
                return

        # Määritetään hyökkäyksen onnistumismahdollisuus ja valittu polttoainekustannus
        if attack_choice == '1':
            success_chance = random.randint(*fast_attack_success_range[destination_airport['difficulty']])
            fuel_cost = fast_attack_cost
        elif attack_choice == '2':
            success_chance = random.randint(*precise_attack_success_range[destination_airport['difficulty']])
            fuel_cost = precise_attack_cost
        else:
            print("⚠️ Virheellinen valinta, hyökkäys peruutettu.")
            return

        # Tarkistetaan, onko pelaajalla DEBUG ATTACK BOOSTER ja asetetaan onnistumistodennäköisyys 100 %:iin
        if has_item(player_id, 'debug_attack_booster'):
            success_chance = 100
            print("🎯 DEBUG ATTACK BOOSTER käytössä! Hyökkäys onnistuu varmasti.")

        # Tarkistetaan, onko pelaajalla tarpeeksi polttoainetta
        if fuel_cost > player['fuel']:
            print("❌ Sinulla ei ole tarpeeksi polttoainetta hyökätä tähän kohteeseen!")
        else:
            print(f"🚀 Hyökkäys käynnissä! Onnistumistodennäköisyys: {success_chance}%, Polttoainekustannus: {fuel_cost:.2f} km")
            print(f"Polttoainetta jäljellä ennen hyökkäystä: {player['fuel']:.2f} km")

            time.sleep(1)
            print("\n🛩️ Hyökkäys käynnissä...")
            time.sleep(2)
            print("\n🚀 Ammuit raketin niitä päin!")
            time.sleep(2)

            # Arvotaan hyökkäyksen onnistuminen
            if random.randint(1, 100) <= success_chance:
                print(f"🏆 Hyökkäys kohteeseen {destination_airport['name']} onnistui! Lentokenttä on nyt Suomen hallinnassa.")
                update_airport_owner(destination_icao, 'Finland')
                add_war_points(player_id, 10)  # Pelaajalle annetaan 10 sotapistettä onnistuneesta hyökkäyksestä
                print("🛡️ Sinulle on annettu 10 sotapistettä onnistuneesta hyökkäyksestä!")
            else:
                print("❌ Hyökkäys epäonnistui! Kohde pysyi Venäjän hallinnassa.")
                update_player_fuel(player_id, fuel_cost)
                print(f"Menetit hyökkäyksen aikana polttoainetta: {fuel_cost:.2f} km")
                print(f"Polttoainetta jäljellä hyökkäyksen jälkeen: {player['fuel'] - fuel_cost:.2f} km")

        wait_for_enter()
    else:
        print("⚠️ Kohdetta ei voida hyökätä. Tarkista kohde ja yritä uudelleen.")







def add_war_points(player_id, points):
    conn = create_connection()
    if conn:
        cursor = conn.cursor()
        try:
            query = "UPDATE game SET war_points = war_points + %s WHERE id = %s"
            cursor.execute(query, (points, player_id))
            conn.commit()
        except mysql.connector.Error as err:
            print(f"Tietokantavirhe sotapisteiden lisäämisessä: {err}")
        finally:
            cursor.close()
            conn.close()

def open_shop(player_id):
    os.system('cls' if os.name == 'nt' else 'clear')
    print("🛒 Kauppa on avoinna! Valitse ostettava esine:")
    
    # Haetaan esineet tietokannasta
    conn = create_connection()
    if conn:
        cursor = conn.cursor(dictionary=True)
        query = "SELECT id, name, description, price FROM item"
        cursor.execute(query)
        items = cursor.fetchall()
        cursor.close()
        conn.close()
        
        # Näytetään esineet pelaajalle
        for item in items:
            print(f"{item['id']} - {item['name']} ({item['description']}) - Hinta: {item['price']} sotapistettä")
        
        item_choice = input("\nSyötä ostettavan esineen ID tai 'CANCEL' peruuttaaksesi: ").strip()
        if item_choice.lower() == 'cancel':
            print("Kauppa suljettu.")
            return
        
        try:
            item_choice = int(item_choice)
            selected_item = next((item for item in items if item['id'] == item_choice), None)
            
            if selected_item:
                purchase_item(player_id, selected_item)
            else:
                print("⚠️ Virheellinen valinta.")
        except ValueError:
            print("⚠️ Virheellinen valinta.")

def purchase_item(player_id, item):
    conn = create_connection()
    if conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT war_points FROM game WHERE id = %s", (player_id,))
        player = cursor.fetchone()

        if player and player['war_points'] >= item['price']:
            # Tarkistetaan onko pelaajalla jo kyseinen esine
            cursor.execute("SELECT quantity FROM inventory WHERE player_id = %s AND item_id = %s", (player_id, item['id']))
            existing_item = cursor.fetchone()

            if existing_item and existing_item['quantity'] > 0:
                print(f"❌ Sinulla on jo esine {item['name']} inventaariossasi.")
            else:
                cursor.execute("UPDATE game SET war_points = war_points - %s WHERE id = %s", (item['price'], player_id))
                cursor.execute("INSERT INTO inventory (player_id, item_id, quantity) VALUES (%s, %s, 1) ON DUPLICATE KEY UPDATE quantity = 1", (player_id, item['id']))
                conn.commit()
                print(f"✅ Ostit esineen {item['name']} onnistuneesti!")
        else:
            print("❌ Sinulla ei ole tarpeeksi sotapisteitä tämän esineen ostamiseen.")

        cursor.close()
        conn.close()



def display_player_status(player, remaining_airports):
    current_airport = get_airport_info(player['location'])
    liberation_percentage = calculate_liberation_percentage()

    if current_airport:
        emoji = "🟦" if current_airport['owner'] == 'Finland' else "🟥"
        stars = get_star_rating(current_airport['difficulty'])
        print(f"\n✈️ Pelaaja on lentokentällä: {emoji} {current_airport['name']} ({player['location']}) {stars}")
    else:
        print("Virhe: Lentokentän tietoja ei löytynyt.")

    print(f"🚀 Polttoainetta: {player['fuel']} km")
    print(f"🎯 Vapauttamattomia kenttiä: {remaining_airports}")
    print(f"🛡️ Sotapisteet: {player['war_points']}")
    print(f"🌍 Olet vallannut takaisin {liberation_percentage:.2f}% Suomen lentokentistä.")

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
    player_id = '1'  # Määritellään player_id ennen kuin kutsutaan reset_game_on_start
    display_story()
    reset_game_on_start(player_id)  # Nollataan peli aina käynnistettäessä
    os.system('cls' if os.name == 'nt' else 'clear')
    print("Tarinan loppu. Paina enter aloittaaksesi seikkailun...")
    wait_for_enter()

    while True:  # Lisätään while True -silmukka
        os.system('cls' if os.name == 'nt' else 'clear')  # Tyhjennä näyttö ennen valikon näyttämistä

        player, remaining_airports = get_player_status(player_id)  # Hae pelaajan tiedot jokaisen silmukan alussa

        if player:  # Varmistetaan, että pelaajatiedot haetaan onnistuneesti
            display_player_status(player, remaining_airports)  # Näytetään pelaajan status

        print("\n📒✏️: Valitse seuraava toimintasi:")
        print("1 - Selaa lentokenttiä")
        print("2 - Hyökkää lentokentälle")
        print("3 - Liiku lentokentälle")
        print("4 - Debug-valikko")
        print("5 - Näytä inventaario")  # Lisätään inventaarion tarkasteluvaihtoehto

        choice = input("Valitse vaihtoehto: ")

        if choice == '1':
            print("\n1 - Listaa Suomen hallussa olevat lentokentät")
            print("2 - Listaa Venäjän vallassa olevat lentokentät")
            print("3 - Listaa lentokentät etäisyyden mukaan")
            print("4 - Listaa lentokentät vaikeustason mukaan")
            sub_choice = input("Valitse luokittelu: ")

            if sub_choice == '1':
                list_airports_by_owner('Finland', '🟦')
            elif sub_choice == '2':
                list_airports_by_owner('Russia', '🟥')
            elif sub_choice == '3':
                list_nearest_airports(player['location'])
            elif sub_choice == '4':
                list_airports_by_difficulty()
            else:
                print("⚠️ Virheellinen valinta.")
            wait_for_enter()

        elif choice == '2':
            list_nearest_airports(player['location'])
            destination = input("\n🎯 Syötä hyökkäyskohteen ICAO-tunnus: ").upper()
            if destination != 'CANCEL':
                attack_airport(player_id, destination)
            wait_for_enter()

        elif choice == '3':
            destination = input("\n✈️ Syötä kohteen ICAO-tunnus: ").upper()
            if destination != 'CANCEL':
                move_player(player_id, destination)
            wait_for_enter()

        elif choice == '4':
            print("\n🛠️ Debug-valikko:")
            print("1 - Muuta polttoainetta")
            print("2 - Muuta sotapisteitä")
            print("3 - Avaa kauppa")
            debug_choice = input("Valitse debug-toiminto: ")

            if debug_choice == '1':
                new_fuel = input("🔧 Syötä uusi polttoainemäärä (km): ")
                if new_fuel.isdigit():
                    set_player_fuel_debug(player_id, int(new_fuel))
                    print(f"Polttoainemäärä päivitetty: {new_fuel} km")
                else:
                    print("⚠️ Virheellinen arvo.")
                wait_for_enter()

            elif debug_choice == '2':
                new_war_points = input("🛡️ Syötä uusi sotapistemäärä: ")
                if new_war_points.isdigit():
                    set_player_war_points_debug(player_id, int(new_war_points))
                    print(f"Sotapisteet päivitetty: {new_war_points}")
                else:
                    print("⚠️ Virheellinen arvo.")
                wait_for_enter()

            elif debug_choice == '3':
                print("🛠️ Debug: Avaamassa kauppa...")
                open_shop(player_id)
                wait_for_enter()

            else:
                print("⚠️ Virheellinen valinta.")
                wait_for_enter()

        elif choice == '5':
            display_inventory(player_id)  # Kutsutaan inventaarion näyttöfunktiota
            wait_for_enter()

        else:
            print("⚠️ Virheellinen valinta, jatketaan...")
            wait_for_enter()
