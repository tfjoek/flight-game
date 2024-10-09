-- --------------------------------------------------------
-- Host:                         127.0.0.1
-- Server version:               11.5.2-MariaDB - mariadb.org binary distribution
-- Server OS:                    Win64
-- HeidiSQL Version:             12.6.0.6765
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


-- Dumping database structure for flight_game
CREATE DATABASE IF NOT EXISTS `flight_game` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_uca1400_ai_ci */;
USE `flight_game`;

-- Dumping structure for table flight_game.airport
CREATE TABLE IF NOT EXISTS `airport` (
  `id` int(11) NOT NULL,
  `ident` varchar(40) NOT NULL,
  `name` varchar(40) DEFAULT NULL,
  `latitude_deg` double DEFAULT NULL,
  `longitude_deg` double DEFAULT NULL,
  `difficulty` int(11) NOT NULL DEFAULT 1,
  `owner` varchar(10) DEFAULT NULL,
  PRIMARY KEY (`ident`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Dumping data for table flight_game.airport: ~18 rows (approximately)
REPLACE INTO `airport` (`id`, `ident`, `name`, `latitude_deg`, `longitude_deg`, `difficulty`, `owner`) VALUES
	(2307, 'EFHK', 'Helsinki Vantaa Airport', 60.3172, 24.963301, 5, 'Russia'),
	(2314, 'EFIV', 'Ivalo Airport', 68.607299804688, 27.405300140381, 3, 'Russia'),
	(2315, 'EFJO', 'Joensuu Airport', 62.662899, 29.6075, 2, 'Russia'),
	(2316, 'EFJY', 'Jyväskylä Airport', 62.399502, 25.678301, 1, 'Russia'),
	(2318, 'EFKE', 'Kemi-Tornio Airport', 65.778701782227, 24.582099914551, 1, 'Russia'),
	(2319, 'EFKI', 'Kajaani Airport', 64.2855, 27.6924, 2, 'Russia'),
	(2321, 'EFKK', 'Kokkola-Pietarsaari Airport', 63.721199, 23.143101, 2, 'Russia'),
	(2324, 'EFKS', 'Kuusamo Airport', 65.987602, 29.239401, 1, 'Russia'),
	(2325, 'EFKT', 'Kittilä Airport', 67.700996398926, 24.846799850464, 1, 'Russia'),
	(2326, 'EFKU', 'Kuopio Airport', 63.007099, 27.7978, 2, 'Russia'),
	(2330, 'EFMA', 'Mariehamn Airport', 60.1222, 19.898199, 1, 'Russia'),
	(2334, 'EFOU', 'Oulu Airport', 64.930099, 25.354601, 4, 'Russia'),
	(2336, 'EFPO', 'Pori Airport', 61.4617, 21.799999, 1, 'Russia'),
	(2341, 'EFRO', 'Rovaniemi Airport', 66.564796447754, 25.830400466919, 3, 'Russia'),
	(2343, 'EFSA', 'Savonlinna Airport', 61.9431, 28.945101, 1, 'Russia'),
	(2347, 'EFTP', 'Tampere-Pirkkala Airport', 61.414101, 23.604401, 3, 'Finland'),
	(2349, 'EFTU', 'Turku Airport', 60.514099, 22.2628, 4, 'Russia'),
	(2351, 'EFVA', 'Vaasa Airport', 63.050701, 21.762199, 1, 'Russia');

-- Dumping structure for table flight_game.game
CREATE TABLE IF NOT EXISTS `game` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `location` varchar(40) NOT NULL,
  `screen_name` varchar(40) DEFAULT NULL,
  `fuel` int(11) DEFAULT 500,
  `war_points` int(11) DEFAULT 0,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

-- Dumping data for table flight_game.game: ~1 rows (approximately)
REPLACE INTO `game` (`id`, `location`, `screen_name`, `fuel`, `war_points`) VALUES
	(1, 'EFTP', 'Pelaaja', 100, 0);

-- Dumping structure for table flight_game.inventory
CREATE TABLE IF NOT EXISTS `inventory` (
  `player_id` int(11) NOT NULL,
  `item_id` int(11) NOT NULL,
  `quantity` int(11) DEFAULT 1,
  PRIMARY KEY (`player_id`,`item_id`),
  KEY `item_id` (`item_id`),
  CONSTRAINT `inventory_ibfk_1` FOREIGN KEY (`player_id`) REFERENCES `game` (`id`),
  CONSTRAINT `inventory_ibfk_2` FOREIGN KEY (`item_id`) REFERENCES `item` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

-- Dumping data for table flight_game.inventory: ~1 rows (approximately)

-- Dumping structure for table flight_game.item
CREATE TABLE IF NOT EXISTS `item` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  `description` varchar(255) DEFAULT NULL,
  `effect` varchar(100) DEFAULT NULL,
  `price` int(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

-- Dumping data for table flight_game.item: ~5 rows (approximately)
REPLACE INTO `item` (`id`, `name`, `description`, `effect`, `price`) VALUES
	(1, 'Mini Aviation Turbofan Engine', '10% efficient fuel usage', 'reduce_fuel_usage_10', 100),
	(2, 'Attack Booster', 'Parantaa hyökkäysten onnistumistodennäköisyyttä 5 %', 'attack_booster', 50),
	(3, 'DEBUG ATTACK BOOSTER', 'Täydellinen onnistumisprosentti hyökkäyksissä', 'debug_attack_booster', 10),
	(4, 'Fuel Booster', 'Vähentää polttoaineenkulutusta hyökkäyksissä 10%', 'fuel_booster', 20),
	(5, 'Debug Fuel Saver', 'Reduces fuel consumption by 90%', 'debug_fuel_saver', 0);

-- Dumping structure for table flight_game.store
CREATE TABLE IF NOT EXISTS `store` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `item` varchar(100) NOT NULL,
  `effect` varchar(255) NOT NULL,
  `price` int(11) NOT NULL,
  `bought` tinyint(1) DEFAULT 0,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Dumping data for table flight_game.store: ~3 rows (approximately)
REPLACE INTO `store` (`id`, `item`, `effect`, `price`, `bought`) VALUES
	(1, 'moottori', 'Tekee bensan käytöstä tehokkaampaa', 1000, 0),
	(2, 'moottori prime', 'Tekee bensan käytöstä vielä tehokkaampaa', 2000, 0),
	(3, 'bensa', '10 fuel lisää', 10, 0);

/*!40103 SET TIME_ZONE=IFNULL(@OLD_TIME_ZONE, 'system') */;
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;
