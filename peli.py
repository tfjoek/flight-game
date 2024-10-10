import mysql.connector
import os
import random
import time
from geopy.distance import distance as geopy_distance
from tarina import hae_tarina  # Importoi tarina uudesta tiedostosta
from rich.console import Console
from rich.panel import Panel
from rich.align import Align
from rich.text import Text

console = Console()

# Opas uuden itemin luomiseen:
# 1. Lisää uusi nimike tietokannan nimiketaulukkoon.
# 2. Aseta nimikkeelle nimi, kuvaus, hinta ja vaikutus.
# 3. Esimerkki SQL-komentosta uuden kohteen luomiseksi:
# INSERT INTO nimike (nimi, kuvaus, hinta, vaikutus) ARVOT ('Super Fuel Booster', 'Alentaa polttoainekustannuksia 15 %', 20, 'fuel_booster');
# 4. Varmista, että tehoste vastaa has_item-funktiologiikassa käytettyä nimeä eli voit ettii sen tuolt :)

##------------------------------- YHTEYDEN ASETTAMINEN -------------------------------##
def create_connection():
    """Luo ja hallitsee tietokantayhteyden."""
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


##-------------------------- PELIN NOLLAUSTOIMINNOT (RESET SYSTEM) --------------------------##
def reset_game_on_start(player_id):
    """Nollaa pelin tilan pelaajalle."""
    reset_player_stats(player_id)
    reset_airports()
    reset_inventory(player_id)
    print("Peli on nollattu ja aloitat alusta!")

def reset_player_stats(player_id):
    """Nollaa pelaajan tilastot, kuten sijainnin, polttoaineen ja sotapisteet."""
    conn = create_connection()
    if conn:
        cursor = conn.cursor()
        query = "UPDATE game SET location=(SELECT location FROM game WHERE id = 1), fuel=250, war_points=0 WHERE id = %s"
        cursor.execute(query, (player_id,))
        conn.commit()
        cursor.close()
        conn.close()

def reset_airports():
    """Nollaa lentokenttien omistajuuden alkuperäisiksi arvoiksi."""
    conn = create_connection()
    if conn:
        cursor = conn.cursor()
        query = "UPDATE airport SET owner='Russia' WHERE difficulty > 0 AND ident != 'EFTP'"
        cursor.execute(query)
        cursor.execute("UPDATE airport SET owner='Finland' WHERE ident = 'EFTP'")
        conn.commit()
        cursor.close()
        conn.close()

def reset_inventory(player_id):
    """Tyhjentää pelaajan inventaarion, poistamalla kaikki esineet."""
    conn = create_connection()
    if conn:
        cursor = conn.cursor()
        query = "DELETE FROM inventory WHERE player_id = %s"
        cursor.execute(query, (player_id,))
        conn.commit()
        cursor.close()
        conn.close()
        print("Inventaario on nollattu.")


##-------------------------- LENTOKENTTIEN TIEDOT (AIRPORT INFORMATION) --------------------------##
def get_star_rating(difficulty):
    """Näyttää lentokentän vaikeustason tähtinä."""
    stars = '⭐' * difficulty
    spaced_stars = ' '.join(stars)
    return spaced_stars

def get_airport_info(icao_code):
    """Hakee yksityiskohtaiset tiedot tietystä lentokentästä."""
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
    """Hakee pelaajan tilan, kuten sijainnin, polttoaineen ja jäljellä olevat kentät."""
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

##------------------------------- LENTOKENTTIEN LISTAUS -------------------------------##
def list_airports_by_owner(owner, emoji):
    """Listaa lentokentät, jotka ovat tietyn omistajan hallussa (Suomi tai Venäjä)."""
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
            airport_list_content = f"Lentokentät {emoji} {owner}:n hallussa:\n"
            for airport in airports:
                stars = get_star_rating(airport['difficulty'])
                airport_list_content += f"{emoji} - {airport['ident']} ({airport['name']}) {stars}\n"

            airport_list_panel = Panel(
                Align.center(airport_list_content, vertical="middle"),
                title=f"🛬 {owner} Lentokentät 🛫",
                border_style="bold green4",
                padding=(1, 2),
                width=80
            )
            console.print(airport_list_panel, justify="center")
        else:
            print(f"Ei lentokenttiä {emoji} {owner}:n hallussa.")


    def display_airports_menu():
            # Määritellään lentokenttien selausvalikko sisältö
            airports_menu_content = """
        1 - Listaa Suomen hallussa olevat lentokentät
        2 - Listaa Venäjän vallassa olevat lentokentät
        3 - Listaa lentokentät etäisyyden mukaan
        4 - Listaa lentokentät vaikeustason mukaan
            """

            # Luodaan paneli lentokenttien selausvalikkoa varten samalla tyylillä
            airports_menu_panel = Panel(
                Align.center(airports_menu_content, vertical="middle"),
                title="✈️ Lentokenttien Selaus ✈️",
                border_style="bold green4",
                padding=(2, 4)  # Lisää tilaa laatikon sisälle
            )

            # Näytetään lentokenttävalikko panelina
            console.print(airports_menu_panel, justify="center")


# Listaa kaikki lentokentät vaikeustason mukaanl
def list_airports_by_difficulty():
    os.system('cls' if os.name == 'nt' else 'clear')
    conn = create_connection()
    if conn:
        cursor = conn.cursor(dictionary=True)
        query = "SELECT ident, name, difficulty, owner FROM airport ORDER BY difficulty DESC"
        cursor.execute(query)
        airports = cursor.fetchall()
        cursor.close()
        conn.close()

        airport_list_content = "Lentokentät vaikeustason mukaan:\n"
        for airport in airports:
            emoji = "🟦" if airport['owner'] == 'Finland' else "🟥"
            stars = get_star_rating(airport['difficulty'])
            airport_list_content += f"{emoji} - {airport['ident']} ({airport['name']}) {stars}\n"

        # Luo paneelin näyttääksesi luettelon lentokentistä
        airport_list_panel = Panel(
            Align.center(airport_list_content, vertical="middle"),
            title="🔧 Lentokentät Vaikeustasoittain 🔧",
            border_style="bold green4",
            padding=(1, 2),
            width=80
        )
        console.print(airport_list_panel, justify="center")

# Laskee Venäjän hallinnasta vapautuneiden lentoasemien prosenttiosuuden
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

# Listaa lähimmät lentokentät pelaajan nykyisestä sijainnista
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

            airport_list_content = "Lähimmät Venäjän lentokentät:\n"
            for airport, distance in nearest_airports:
                stars = get_star_rating(airport['difficulty'])
                airport_list_content += f"• {airport['ident']} ({airport['name']}) {stars} 🟥 - Etäisyys: {int(distance)} km\n"

            # Paneeli
            nearest_airports_panel = Panel(
                Align.center(airport_list_content, vertical="middle"),
                title="📍 Lähimmät Lentokentät 📍",
                border_style="bold green4",
                padding=(1, 2),
                width=80
            )
            console.print(nearest_airports_panel, justify="center")
        else:
            print("Nykyisen sijainnin tietoja ei löydy.")

# Airport owner paivitys
def update_airport_owner(icao_code, new_owner):
    conn = create_connection()
    if conn:
        cursor = conn.cursor()
        query = "UPDATE airport SET owner = %s WHERE ident = %s"
        cursor.execute(query, (new_owner, icao_code))
        conn.commit()
        cursor.close()
        conn.close()

# Paivittaa pelajaan fuelin hyokkayksen jalkeen
def update_player_fuel(player_id, fuel_cost):
    conn = create_connection()
    if conn:
        cursor = conn.cursor()
        query = "UPDATE game SET fuel = fuel - %s WHERE id = %s"
        cursor.execute(query, (fuel_cost, player_id))
        conn.commit()
        cursor.close()
        conn.close()

# fuel debug
def set_player_fuel_debug(player_id, new_fuel):
    conn = create_connection()
    if conn:
        cursor = conn.cursor()
        query = "UPDATE game SET fuel = %s WHERE id = %s"
        cursor.execute(query, (new_fuel, player_id))
        conn.commit()
        cursor.close()
        conn.close()

# warpoint debug
def set_player_war_points_debug(player_id, new_war_points):
    conn = create_connection()
    if conn:
        cursor = conn.cursor()
        query = "UPDATE game SET war_points = %s WHERE id = %s"
        cursor.execute(query, (new_war_points, player_id))
        conn.commit()
        cursor.close()
        conn.close()

##-------------------------- INVENTAARION HALLINTA (INVENTORY MANAGEMENT) --------------------------##
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
            inventory_content = "🎒 Inventaario:\n"
            for item in items:
                inventory_content += f"- {item['name']} (Määrä: {item['quantity']})\n"

            
            inventory_panel = Panel(
                Align.center(inventory_content, vertical="middle"),
                title="🛠️ Pelaajan Inventaario 🛠️",
                border_style="bold green4",
                padding=(1, 2),
                width=80  
            )
            console.print(inventory_panel, justify="center")
        else:
          
            empty_inventory_panel = Panel(
                Align.center("Inventaario on tyhjä.", vertical="middle"),
                title="🛠️ Pelaajan Inventaario 🛠️",
                border_style="bold green4",
                padding=(1, 2),
                width=80  
            )
            console.print(empty_inventory_panel, justify="center")
    else:
        print("Tietokantavirhe: inventaariota ei voitu hakea.")

# Tarkistaa, onko pelaajalla tietty esine jolla on tietty vaikutus
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
        return base_fuel_cost * 0.05  # Reduces fuel consumption by 95%
    elif has_item(player_id, 'fuel_efficiency_booster_15_percent'):
        return base_fuel_cost * 0.75  # Reduces fuel consumption by 25%
    elif has_item(player_id, 'fuel_efficiency_booster_10_percent'):
        return base_fuel_cost * 0.80  # Reduces fuel consumption by 20%
    elif has_item(player_id, 'fuel_efficiency_booster_5_percent'):
        return base_fuel_cost * 0.90  # Reduces fuel consumption by 10%
    else:
        return base_fuel_cost * 0.80  # Default reduction in base fuel cost





##------------------------------- HYÖKKÄYSJÄRJESTELMÄ (ATTACK SYSTEM) -------------------------------##


def attack_airport(player_id, destination_icao):
    destination_airport = get_airport_info(destination_icao)
    player = get_player_status(player_id)[0]

    if destination_airport and destination_airport['owner'] == 'Russia' and player:
        current_airport = get_airport_info(player['location'])
        current_coords = (current_airport['latitude_deg'], current_airport['longitude_deg'])
        destination_coords = (destination_airport['latitude_deg'], destination_airport['longitude_deg'])
        distance = geopy_distance(current_coords, destination_coords).km


        #Eri tahtien difficulty prosentit
        fast_attack_success_range = {
            1: (50, 60),  
            2: (45, 55),
            3: (40, 50),
            4: (35, 45),
            5: (20, 30)
        }
        precise_attack_success_range = {
            1: (70, 80),  
            2: (65, 75),
            3: (60, 70),
            4: (55, 65),
            5: (30, 40)
        }

        fast_attack_cost = calculate_fuel_cost(player_id, distance * 0.5)
        precise_attack_cost = calculate_fuel_cost(player_id, distance)

        fast_attack_chance = fast_attack_success_range[destination_airport['difficulty']]
        precise_attack_chance = precise_attack_success_range[destination_airport['difficulty']]

     
        attack_options_content = f"""
⚔️ Valitse hyökkäystyyli:
1. ⚡ Nopeampi hyökkäys - Polttoainekustannus: {fast_attack_cost:.2f} km - Onnistumistodennäköisyys: {fast_attack_chance[0]}% - {fast_attack_chance[1]}%
2. 🎯 Tarkempi hyökkäys - Polttoainekustannus: {precise_attack_cost:.2f} km - Onnistumistodennäköisyys: {precise_attack_chance[0]}% - {precise_attack_chance[1]}%
        """

        attack_options_panel = Panel(
            Align.center(attack_options_content, vertical="middle"),
            title="⚔️ Hyökkäysvaihtoehdot ⚔️",
            border_style="bold green4",
            padding=(1, 2),
            width=80  # Width set to 80 for better display
        )
        console.print(attack_options_panel, justify="center")

        attack_choice = input("\nValintasi (1 tai 2): ").strip()

        if attack_choice == '1':
            success_chance = random.randint(*fast_attack_success_range[destination_airport['difficulty']])
            fuel_cost = fast_attack_cost
            attack_message = "⚡ Ammuit raketin kohti kohdetta nopealla hyökkäyksellä!"
        elif attack_choice == '2':
            success_chance = random.randint(*precise_attack_success_range[destination_airport['difficulty']])
            fuel_cost = precise_attack_cost
            attack_message = "🎯 Hiivit varovaisesti kohteen taakse ja ammut tarkan laukauksen!"
        else:
            print("⚠️ Virheellinen valinta, hyökkäys peruutettu.")
            return

        if fuel_cost > player['fuel']:
            print("❌ Sinulla ei ole tarpeeksi polttoainetta hyökätä tähän kohteeseen!")
        else:
            # attack delay juttu hieno :D
            console.print(Panel(attack_message, border_style="bold red", padding=(1, 2), width=80))
            time.sleep(2)

            attack_result_content = f"🚀 Hyökkäys käynnissä! Onnistumistodennäköisyys: {success_chance}%, Polttoainekustannus: {fuel_cost:.2f} km"
            console.print(Panel(attack_result_content, border_style="bold red", padding=(1, 2), width=80))

            time.sleep(2)  # Simulate a pause before the result
            if random.randint(1, 100) <= success_chance:
                success_content = f"🏆 Hyökkäys kohteeseen {destination_airport['name']} onnistui! Lentokenttä on nyt Suomen hallinnassa.\n\n🛡️ Onnistuneesta hyökkäyksestä ansaitsit yhteensä {destination_airport['difficulty'] * 5 + 25} sotapistettä!"
                update_airport_owner(destination_icao, 'Finland')
                add_war_points(player_id, destination_airport['difficulty'])
                console.print(Panel(success_content, border_style="bold green", padding=(1, 2), width=80))

                
                shop_chance = 100  # voi vaihta jos haluu et kauppa on rng
                if random.randint(1, 100) <= shop_chance:
                    shop_prompt = "🛒 Haluatko käydä kaupassa? (Y/N)"
                    console.print(Panel(shop_prompt, border_style="bold yellow", padding=(1, 2), width=80))
                    visit_shop = input().strip().upper()
                    if visit_shop == 'Y':
                        open_shop(player_id)  

            else:
                fail_content = f"❌ Hyökkäys epäonnistui! Kohde pysyi Venäjän hallinnassa."
                update_player_fuel(player_id, fuel_cost)
                console.print(Panel(fail_content, border_style="bold red", padding=(1, 2), width=80))

                fuel_loss_content = f"Menetit hyökkäyksen aikana polttoainetta: {fuel_cost:.2f} km\nPolttoainetta jäljellä hyökkäyksen jälkeen: {player['fuel'] - fuel_cost:.2f} km"
                console.print(Panel(fuel_loss_content, border_style="bold red", padding=(1, 2), width=80))

        wait_for_enter()
    else:
        error_content = "⚠️ Kohdetta ei voida hyökätä. Tarkista kohde ja yritä uudelleen."
        console.print(Panel(error_content, border_style="bold red", padding=(1, 2), width=80))

def set_all_airports_to_finland():
    """Asettaa kaikkien lentokenttien omistajuuden Suomelle."""
    conn = create_connection()
    if conn:
        cursor = conn.cursor()
        query = "UPDATE airport SET owner='Finland'"
        cursor.execute(query)
        conn.commit()
        cursor.close()
        conn.close()
        print("Kaikki lentokentät ovat nyt Suomen hallinnassa.")

def add_war_points(player_id, difficulty):
    base_points = 25  
    bonus_points = difficulty * 5
    total_points = base_points + bonus_points

    conn = create_connection()
    if conn:
        cursor = conn.cursor()
        try:
            query = "UPDATE game SET war_points = war_points + %s WHERE id = %s"
            cursor.execute(query, (total_points, player_id))
            conn.commit()
         
        except mysql.connector.Error as err:
            print(f"Tietokantavirhe sotapisteiden lisäämisessä: {err}")
        finally:
            cursor.close()
            conn.close()



def generate_fuel_canister():
    """Luo bensapaketti-esine satunnaisella määrällä polttoainetta (50-150 km)."""
    random_fuel_amount = random.randint(50, 150)
    return {
        'id': 'canister',  # Käytä yksilöllistä tunnistetta bensapaketille
        'name': f'Bensapaketti {random_fuel_amount} km',
        'description': f'Tarjoaa {random_fuel_amount} km polttoainetta, ostettavissa vain kerran per vierailu.',
        'price': 20,  # Aseta kiinteä hinta bensapaketille, tarvittaessa säädettävissä
        'fuel_value': random_fuel_amount  # Tallenna polttoainemäärä käytettäväksi ostettaessa
    }

########omgggggggggggggggggggggggggggggggggggggggg toimiiiiiiiiiiiiiiiiiiiiiiiiiiiii
def open_shop(player_id):
    os.system('cls' if os.name == 'nt' else 'clear')

    # Hae pelaajan nykyiset sotapisteet
    conn = create_connection()
    if conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT war_points FROM game WHERE id = %s", (player_id,))
        player = cursor.fetchone()
        player_war_points = player['war_points'] if player else 0
        cursor.close()
        conn.close()

    # Luo bensapaketti satunnaisella määrällä (50-150 km)
    fuel_canister = generate_fuel_canister()

    conn = create_connection()
    if conn:
        cursor = conn.cursor(dictionary=True)
        query = "SELECT id, name, description, price FROM item ORDER BY RAND() LIMIT 1"  # Hae 1 satunnainen esine tietokannasta
        cursor.execute(query)
        items = cursor.fetchall()
        cursor.close()
        conn.close()

        # Lisää satunnaisesti luotu bensapaketti esinevalikoimaan aina itemin kanssa
        items.append(fuel_canister)

    # Muodosta kauppasisältö, johon lisätään esineet
    shop_items_content = f"🛒 Kauppa on avoinna! Sinulla on tällä hetkellä {player_war_points} sotapistettä.\n"
    for item in items:
        shop_items_content += f"{item['id']} - {item['name']} ({item['description']}) - Hinta: {item['price']} sotapistettä\n"

    
    shop_content = f"""
{shop_items_content}
Valitse esine ostettavaksi tai peruuta ostos.
"""
    shop_panel = Panel(
        Align.center(shop_content, vertical="middle"),
        title="🛒 Kauppa 🛒",
        border_style="bold yellow",
        padding=(1, 2),
        width=80 
    )

    # Display the shop panel once
    console.print(shop_panel, justify="center")

    item_choice = input("\nSyötä ostettavan esineen ID tai 'CANCEL' peruuttaaksesi: ").strip()
    if item_choice.lower() == 'cancel':
        print("Kauppa suljettu.")
        return

    try:
        
        if item_choice == 'canister':
            selected_item = fuel_canister
        else:
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
            # Tarkista, onko esine bensapaketti ja käsittele ostos erikseen
            if item['id'] == 'canister':
                print(f"✅ Ostit esineen {item['name']} ja sait {item['fuel_value']} km polttoainetta!")
                update_player_fuel(player_id, -item['fuel_value'])  # Lisää polttoainemäärä pelaajan tankkiin

            else:
                # Tavallinen esineostoslogiikka
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

console = Console()

def display_player_status(player, remaining_airports):
    current_airport = get_airport_info(player['location'])
    liberation_percentage = calculate_liberation_percentage()

    if current_airport:
        emoji = "🟦" if current_airport['owner'] == 'Finland' else "🟥"
        stars = get_star_rating(current_airport['difficulty'])

        # Create the inner panels for each piece of information
        player_location_text = Text(f"{current_airport['name']} ({player['location']}) {stars}", style="bold white on green4")
        fuel_text = Text(f"🚀 Polttoainetta: {player['fuel']} km", style="bold white on dark_sea_green")
        airports_remaining_text = Text(f"🎯 Vapauttamattomia kenttiä: {remaining_airports}", style="bold white on yellow3")
        war_points_text = Text(f"🛡️ Sotapisteet: {player['war_points']}", style="bold white on gold3")
        progress_text = Text(f"🌍 Olet vallannut takaisin {liberation_percentage:.2f}% Suomen lentokentistä.", style="bold white on chartreuse4")

        # Combine all the text into a single main panel with appropriate spacing and borders
        main_panel_content = f"""
✈️ Pelaaja on lentokentällä: {emoji} {player_location_text}

{fuel_text}

{airports_remaining_text}

{war_points_text}

{progress_text}
        """

        main_panel = Panel(
            Align.center(main_panel_content),
            title="🛫 Pelaajan Tilannekatsaus 🛬",
            border_style="bold green4",
            padding=(4, 8),  # Doubled the padding for more space around the content
        )

        # Display the unified main panel
        console.print(main_panel, justify="center")




def wait_for_enter():
    liberation_percentage = calculate_liberation_percentage()

    if liberation_percentage == 100:
        os.system('cls' if os.name == 'nt' else 'clear')  # Tyhjennä näyttö ennen viestin näyttämistä
        success_message = """
        🎉 *** ONNEKSI OLKOON! OPERAATIO://NOKIHIUKKANEN ONNISTUI! *** 🎉
        ====================================================
        🌍 Suomi sai kaikki lentokentät takaisin!
        ====================================================
        """
       
        success_panel = Panel(
            Align.center(success_message, vertical="middle"),
            title="🏆 Voitto! 🏆",
            border_style="bold green",
            padding=(2, 4),
            width=100  
        )
        console.print(success_panel, justify="center")
        time.sleep(1000)  
    else:
        input("Paina enter jatkaaksesi...")


def display_story():
    tarina = hae_tarina()
    tarinaHalu = input("Halutako lukea tarinan (Y/N): ")
    if tarinaHalu.upper() == 'Y':
        for osa in tarina:
            os.system('cls' if os.name == 'nt' else 'clear')
            print(osa)
            wait_for_enter()

def display_main_menu():
    """Näyttää päävalikon, jossa pelaaja voi valita seuraavan toimintonsa."""
    menu_content = """
📒✏️ Valitse seuraava toimintasi:
1 - Selaa lentokenttiä
2 - Hyökkää lentokentälle
3 - Näytä inventaario
4 - Debug-valikko
"""
    main_menu_panel = Panel(
        Align.center(menu_content, vertical="middle"),
        title="🔧 Päävalikko 🔧",
        border_style="bold green4",
        padding=(1, 2),
        width=80  # Laatikon leveys
    )
    console.print(main_menu_panel, justify="center")



def display_airports_menu():
    """Näyttää lentokenttien selausvalikon."""
    airports_menu_content = """
1 - Listaa Suomen hallussa olevat lentokentät
2 - Listaa Venäjän vallassa olevat lentokentät
3 - Listaa lentokentät etäisyyden mukaan
4 - Listaa lentokentät vaikeustason mukaan
"""
    airports_menu_panel = Panel(
        Align.center(airports_menu_content, vertical="middle"),
        title="✈️ Lentokenttien Selaus ✈️",
        border_style="bold green4",
        padding=(1, 2),
        width=80
    )
    console.print(airports_menu_panel, justify="center")

def display_debug_menu():
    """Näyttää debug-valikon, jossa voi tehdä erityisiä pelin hallintatoimintoja."""
    debug_menu_content = """
1 - Muuta polttoainetta
2 - Muuta sotapisteitä
3 - Avaa kauppa
4 - Aseta kaikki lentokentät Suomen hallintaan
"""
    debug_menu_panel = Panel(
        Align.center(debug_menu_content, vertical="middle"),
        title="🛠️ Debug-valikko 🛠️",
        border_style="bold green4",
        padding=(1, 2),
        width=80
    )
    console.print(debug_menu_panel, justify="center")
    


##-------------------------- PELIN KÄYNNISTYS (MAIN MENU) --------------------------##
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

    display_main_menu()  # Näytetään päävalikko

    choice = input("Valitse vaihtoehto: ")

    if choice == '1':
        display_airports_menu()  # Näytetään lentokenttien selausvalikko
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

    elif choice == '2':
        list_nearest_airports(player['location'])
        destination = input("\n🎯 Syötä hyökkäyskohteen ICAO-tunnus: ").upper()
        if destination != 'CANCEL':
            attack_airport(player_id, destination)

    elif choice == '3':
        display_inventory(player_id)  # Kutsutaan inventaarion näyttöfunktiota

    elif choice == '4':
        display_debug_menu()  # Näytetään debug-valikko
        debug_choice = input("Valitse debug-toiminto: ")

        if debug_choice == '1':
            new_fuel = input("🔧 Syötä uusi polttoainemäärä (km): ")
            if new_fuel.isdigit():
                set_player_fuel_debug(player_id, int(new_fuel))
                print(f"Polttoainemäärä päivitetty: {new_fuel} km")
            else:
                print("⚠️ Virheellinen arvo.")

        elif debug_choice == '2':
            new_war_points = input("🛡️ Syötä uusi sotapistemäärä: ")
            if new_war_points.isdigit():
                set_player_war_points_debug(player_id, int(new_war_points))
                print(f"Sotapisteet päivitetty: {new_war_points}")
            else:
                print("⚠️ Virheellinen arvo.")

        elif debug_choice == '3':
            print("🛠️ Debug: Avaamassa kauppa...")
            open_shop(player_id)

        elif debug_choice == '4':
            print("🛠️ Debug: Asetetaan kaikki lentokentät Suomen hallintaan...")
            set_all_airports_to_finland()
            print("Kaikki lentokentät ovat nyt Suomen hallinnassa!")

        else:
            print("⚠️ Virheellinen valinta, jatketaan...")


    wait_for_enter()  # Call wait_for_enter once at the end of each iteration jeeeeeeeeeeee
