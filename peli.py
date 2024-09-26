import mysql.connector
import os

def create_connection():
    #LAITA TÄHÄN OMAT USER JA PASSWORD JA DB NIMI JOS SULA ERI 
        #LAITA TÄHÄN OMAT USER JA PASSWORD JA DB NIMI JOS SULA ERI 
        #LAITA TÄHÄN OMAT USER JA PASSWORD JA DB NIMI JOS SULA ERI 
        #LAITA TÄHÄN OMAT USER JA PASSWORD JA DB NIMI JOS SULA ERI 
    try:
        conn = mysql.connector.connect(
            host='127.0.0.1',  
            port=3306,  
            database='flight_game', 
            user='vennilim',  
            password='kappa',  
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

def get_player_status(player_id):
   #Hakee pelaajan statsit tietokannasta
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


 #Pelaajan nykyiset statsit
def display_player_status(player, remaining_airports):
    print("Muista sotilas! Olet meidän ainoa toivo!")
    term_size = os.get_terminal_size()
    print('=' * term_size.columns)
    print(f"Nykyinen sijaintisi: {player['location']}")
    print(f"Polttoainetta: {player['fuel']} km")
    print(f"Vapauttamattomia kenttiä: {remaining_airports}")
    print(f"Sotapisteet: {player['war_points']}")
    print('=' * term_size.columns)

def wait_for_enter():
    #enter input
    input("Paina enter jatkaaksesi...")

def display_story():
    #tarina ja odottaa enter key
    tarina = [
        "Olet kokenut lentäjä, jolla on aina ollut vahva rakkaus kotimaatasi kohtaan. "
        "Viime vuosina Suomen hallitus on tehnyt päätöksiä, jotka ovat rapauttaneet maan puolustuskykyä. "
        "Tämä on ollut täydellinen tilaisuus Venäjälle, joka on pitkään suunnitellut hyökkäystä. "
        "Lopulta, koittaessa hetken, jota pelättiin, Venäjä hyökkää Suomeen.",
        
        "Ensimmäisenä Venäjä iskee Suomen lentokenttiin. Yöllä, salaisen operaation aikana, suurin osa maan lentokentistä vallataan hetkessä. "
        "Sinä, lentäjä, heräät uutiseen, että kotimaan ilmatila on menetetty, ja kentät ovat vihollisen hallussa. "
        "On selvää, että toimintaasi tarvitaan – sinut kutsutaan operaatioon vapauttamaan Suomi pala palalta.",
        
        "Matkasi on vaarallinen. Jokainen lentokenttä on strategisesti tärkeä, ja jokainen liike on elintärkeä. "
        "Tavoitteenasi on saavuttaa tärkeät kentät ennen kuin vihollisen vahvistukset ehtivät paikalle.",
        
        "Matkasi varrella voit avata huoltolaitteita, jotka auttavat sinua, mutta samalla on riski, että törmäät vihollisen ryhmityksiin.",
        
        "Lopulta sinun on päästävä Suomen tärkeimmille lentokentille ja vapautettava ne. Vain sinä voit estää Suomen joutumasta täysin vihollisen hallintaan. "
        "Taistele nopeudella ja älyllä, hallitse resurssejasi ja estä vihollisen vastaiskut. Kun olet vapauttanut viimeisenkin kentän ja Venäjä on lyöty, "
        "voit ylpeänä palata takaisin ensimmäiselle vapautetulle kentälle. Olet voittanut taistelun ja pelastanut Suomen."
    ]

    for osa in tarina:
        os.system('cls' if os.name == 'nt' else 'clear')  # os system clear = poistaa tekstin terminalist
        print(osa)
        wait_for_enter()

if __name__ == "__main__":
    display_story()
    
    # tarina loppuessa pelaajan perusnäyttö eli statsit näkyviin
    os.system('cls' if os.name == 'nt' else 'clear') # os system clear taas 
    print("Tarinan loppu. Paina enter aloittaaksesi seikkailun...")
    wait_for_enter()
    os.system('cls' if os.name == 'nt' else 'clear')
    
    player_id = '1'  # pelaajan id 
    player, remaining_airports = get_player_status(player_id)
    if player:
        display_player_status(player, remaining_airports)
    else:
        print("Pelaajan tietojen haku epäonnistui.")
