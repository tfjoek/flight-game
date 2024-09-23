/*M!999999\- enable the sandbox mode */ 
-- MariaDB dump 10.19-11.5.2-MariaDB, for Win64 (AMD64)
--
-- Host: localhost    Database: flight_game
-- ------------------------------------------------------
-- Server version	11.5.2-MariaDB

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*M!100616 SET @OLD_NOTE_VERBOSITY=@@NOTE_VERBOSITY, NOTE_VERBOSITY=0 */;

--
-- Table structure for table `airport`
--

DROP TABLE IF EXISTS `airport`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `airport` (
  `id` int(11) NOT NULL,
  `ident` varchar(40) NOT NULL,
  `name` varchar(40) DEFAULT NULL,
  `latitude_deg` double DEFAULT NULL,
  `longitude_deg` double DEFAULT NULL,
  `difficulty` int(11) NOT NULL DEFAULT 1,
  PRIMARY KEY (`ident`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `airport`
--

LOCK TABLES `airport` WRITE;
/*!40000 ALTER TABLE `airport` DISABLE KEYS */;
INSERT INTO `airport` VALUES
(27245,'EFAA','Aavahelukka Airport',67.60359954833984,23.97170066833496,1),
(27246,'EFAH','Ahmosuo Airport',64.895302,25.752199,1),
(27247,'EFAL','Alavus Airfield',62.554699,23.573299,1),
(44025,'EFEJ','Jorvin Hospital Heliport',60.220833,24.68639,1),
(44032,'EFEK','Kilpisjärvi Heliport',69.0022201538086,20.89638900756836,1),
(2303,'EFET','Enontekio Airport',68.362602233887,23.424299240112,1),
(2304,'EFEU','Eura Airport',61.1161,22.201401,1),
(27248,'EFFO','Forssa Airfield',60.803683,23.650802,1),
(27249,'EFGE','Genböle Airport',60.086899,22.5219,1),
(2305,'EFHA','Halli Airport',61.856039,24.786686,1),
(43021,'EFHE','Hernesaari Heliport',60.147778,24.924444,1),
(2306,'EFHF','Helsinki Malmi Airport',60.254601,25.042801,1),
(44026,'EFHH','Kanta-Hämeen Central Hospital Heliport',60.991112,24.415277,1),
(29933,'EFHI','Haapamäki Airfield',62.255204,24.349478,1),
(27250,'EFHJ','Haapajärvi Airport',63.7122,25.395,1),
(2307,'EFHK','Helsinki Vantaa Airport',60.3172,24.963301,1),
(27252,'EFHL','Hailuoto Airfield',64.969553,24.704218,1),
(2308,'EFHM','Hämeenkyrö Airfield',61.689701,23.0737,1),
(2309,'EFHN','Hanko Airport',59.8489,23.083599,1),
(44038,'EFHO','Oulun University Hospital Heliport',65.003609,25.520279,1),
(27251,'EFHP','Haapavesi Airfield',64.113098,25.5042,1),
(44035,'EFHS','Seinäjoen Central Hospital Heliport',62.769919,22.822402,1),
(2310,'EFHV','Hyvinkää Airfield',60.6544,24.8811,1),
(44027,'EFHY','Meilahti Hospital Helipad',60.188909,24.907276,1),
(27253,'EFII','Iisalmi Airport',63.631901,27.1222,1),
(2311,'EFIK','Kiikala Airport',60.462502,23.6525,1),
(2312,'EFIM','Immola Airport',61.249199,28.9037,1),
(2313,'EFIT','Kitee Airport',62.1661,30.073601,1),
(2314,'EFIV','Ivalo Airport',68.607299804688,27.405300140381,1),
(44031,'EFJE','North Karelia Central Hospital Heliport',62.590832,29.777779,1),
(346797,'EFJI','Ilvesjoki UL',62.324167,22.694167,1),
(27254,'EFJM','Jämijärvi Airfield',61.778599,22.716101,1),
(2315,'EFJO','Joensuu Airport',62.662899,29.6075,1),
(29099,'EFJP','Jäkäläpä Airfield',68.711403,25.7528,1),
(44034,'EFJV','Central Finland Central Hospital Helipor',62.230361,25.71154,1),
(2316,'EFJY','Jyväskylä Airport',62.399502,25.678301,1),
(2317,'EFKA','Kauhava Airfield',63.127102,23.051399,1),
(2318,'EFKE','Kemi-Tornio Airport',65.778701782227,24.582099914551,1),
(27259,'EFKG','Kumlinge Airport',60.24689865112305,20.80470085144043,1),
(27258,'EFKH','Kuhmo Airfield',64.112503,29.438601,1),
(2319,'EFKI','Kajaani Airport',64.2855,27.6924,1),
(2320,'EFKJ','Kauhajoki Airfield',62.462502,22.393101,1),
(2321,'EFKK','Kokkola-Pietarsaari Airport',63.721199,23.143101,1),
(2322,'EFKM','Kemijärvi Airport',66.712898,27.156799,1),
(27255,'EFKN','Kannus Airfield',63.920601,24.0867,1),
(2323,'EFKO','Kalajoki Airfield',64.2286,23.826401,1),
(27261,'EFKR','Kärsämäki Airport',63.989201,25.743601,1),
(2324,'EFKS','Kuusamo Airport',65.987602,29.239401,1),
(2325,'EFKT','Kittilä Airport',67.700996398926,24.846799850464,1),
(2326,'EFKU','Kuopio Airport',63.007099,27.7978,1),
(27257,'EFKV','Kivijärvi Airfield',63.125301,25.124201,1),
(27260,'EFKY','Kymi Airfield',60.5714,26.896099,1),
(2327,'EFLA','Lahti Vesivehmaa Airport',61.144199,25.693501,1),
(27262,'EFLL','Lapinlahti Airfield',63.399399,27.478901,1),
(2328,'EFLN','Lieksa Nurmes Airfield',63.511902,29.6292,1),
(2329,'EFLP','Lappeenranta Airport',61.044601,28.144743,1),(2330,'EFMA','Mariehamn Airport',60.1222,19.898199,1),
(2331,'EFME','Menkijärvi Airfield',62.946701,23.5189,1),
(2332,'EFMI','Mikkeli Airport',61.6866,27.201799,1),
(310896,'EFML','Ii Airfield',65.301144,25.416226,1),
(27263,'EFMN','Mäntsälä Airport',60.572498,25.5089,1),
(29100,'EFMP','Martiniiskonpalo Airport',68.6603012084961,25.702899932861328,1),
(27270,'EFNS','Savikko Airfield',60.52,24.831699,1),
(2333,'EFNU','Nummela Airport',60.3339,24.2964,1),
(27264,'EFOP','Oripää Airfield',60.8764,22.744699,1),
(2334,'EFOU','Oulu Airport',64.930099,25.354601,1),
(27266,'EFPA','Pokka Airport',68.15022277832031,25.82937240600586,1),
(44029,'EFPE','Peijaksen Hospital Heliport',60.331112,25.060833,1),
(30308,'EFPH','Pyhäsalmi Airport',62.464699,30.035299,1),
(2335,'EFPI','Piikajärvi Airport',61.245602,22.193399,1),
(44030,'EFPJ','Kuopio University Hospital Heliport',62.897499,27.648333,1),
(27265,'EFPK','Pieksämäki Airfield',62.264702,27.0028,1),
(44028,'EFPL','Päijät-Hämeen Central Hospital Heliport',60.99177,25.569456,1),
(27267,'EFPN','Punkaharju Airfield',61.728901,29.3936,1),
(2336,'EFPO','Pori Airport',61.4617,21.799999,1),
(334942,'EFPR','Helsinki East-Redstone Airport',60.479167,26.593889,1),
(44036,'EFPT','Tampere University Hospital Heliport',61.50639,23.8125,1),
(2337,'EFPU','Pudasjärvi Airfield',65.402199,26.946899,1),
(2338,'EFPY','Pyhäjärvi Airfield',63.731899,25.9263,1),
(27269,'EFRA','Rautavaara Airfield',63.424198,28.124201,1),
(2339,'EFRH','Raahe Pattijoki Airfield',64.688103,24.695801,1),
(2340,'EFRN','Rantasalmi Airfield',62.065498,28.356501,1),
(2341,'EFRO','Rovaniemi Airport',66.564796447754,25.830400466919,1),
(27268,'EFRU','Ranua Airfield',65.973099,26.365299,1),
(27256,'EFRV','Kiuruvesi Airfield',63.705601,26.6164,1),
(2342,'EFRY','Räyskälä Airfield',60.744701,24.1078,1),
(2343,'EFSA','Savonlinna Airport',61.9431,28.945101,1),
(2344,'EFSE','Selänpää Airfield',61.062401,26.798901,1),
(2345,'EFSI','Seinäjoki Airport',62.692101,22.8323,1),
(30430,'EFSJ','Sonkajärvi-Jyrkkä Airfield',63.819401,27.7694,1),
(2346,'EFSO','Sodankylä Airport',67.3949966431,26.6191005707,1),
(27272,'EFSU','Suomussalmi Airfield',64.821899,28.7103,1),
(27273,'EFTO','Torbacka Airfield',60.079201,24.172199,1),
(2347,'EFTP','Tampere-Pirkkala Airport',61.414101,23.604401,1),
(2348,'EFTS','Teisko Airfield',61.7733,24.027,1),
(2349,'EFTU','Turku Airport',60.514099,22.2628,1),
(44037,'EFTV','Turku University Central Hospital Helipad',60.451111,22.290277,1),
(2350,'EFUT','Utti Air Base',60.8964,26.9384,1),
(2351,'EFVA','Vaasa Airport',63.050701,21.762199,1),
(30532,'EFVI','Viitasaari Airfield',63.122501,25.816099,1),
(27274,'EFVL','Vaala Airfield',64.5019,26.76,1),
(27275,'EFVP','Vampula Airfield',61.0397,22.5917,1),
(2352,'EFVR','Varkaus Airport',62.171101,27.868601,1),
(27271,'EFVT','Sulkaharju Airfield',63.3978,24.0306,1),
(29101,'EFVU','Vuotso Airfield',68.087196,27.123899,1),
(27276,'EFWB','Wredeby Airfield',60.663601,26.7458,1),
(2353,'EFYL','Ylivieska Airfield',64.054722,24.725278,1);
/*!40000 ALTER TABLE `airport` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `game`
--

DROP TABLE IF EXISTS `game`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `game` (
  `id` varchar(40) NOT NULL,
  `location` varchar(10) DEFAULT NULL,
  `screen_name` varchar(40) DEFAULT NULL,
  `fuel` int(11) NOT NULL DEFAULT 500,
  `war_points` int(11) NOT NULL DEFAULT 0,
  PRIMARY KEY (`id`),
  KEY `location` (`location`),
  CONSTRAINT `fk_location_airport` FOREIGN KEY (`location`) REFERENCES `airport` (`ident`),
  CONSTRAINT `game_ibfk_1` FOREIGN KEY (`location`) REFERENCES `airport` (`ident`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `game`
--

LOCK TABLES `game` WRITE;
/*!40000 ALTER TABLE `game` DISABLE KEYS */;
INSERT INTO `game` VALUES
('1','EFHK','Heini',500,0),
('2','EGCC','Vesa',500,0),
('3','EGKK','Ilkka',500,0);
/*!40000 ALTER TABLE `game` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `store`
--

DROP TABLE IF EXISTS `store`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `store` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `item` varchar(100) NOT NULL,
  `effect` varchar(255) NOT NULL,
  `price` int(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `store`
--

LOCK TABLES `store` WRITE;
/*!40000 ALTER TABLE `store` DISABLE KEYS */;
/*!40000 ALTER TABLE `store` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*M!100616 SET NOTE_VERBOSITY=@OLD_NOTE_VERBOSITY */;

-- Dump completed on 2024-09-22 14:14:18