CREATE DATABASE IF NOT EXISTS `gttravel` /*!40100 DEFAULT CHARACTER SET utf8 */;
USE `gttravel`;-- MySQL dump 10.13  Distrib 5.7.12, for Win64 (x86_64)

--
-- Host: 127.0.0.1    Database: gttravel
-- ------------------------------------------------------
-- Server version	5.7.13-log

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `capitals`
--

DROP TABLE IF EXISTS `capitals`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `capitals` (
  `Capital` varchar(32) NOT NULL,
  `Country` varchar(32) NOT NULL,
  PRIMARY KEY (`Capital`,`Country`),
  CONSTRAINT `capitals_ibfk_1` FOREIGN KEY (`Capital`, `Country`) REFERENCES `city` (`City`, `Country`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `capitals`
--

LOCK TABLES `capitals` WRITE;
/*!40000 ALTER TABLE `capitals` DISABLE KEYS */;
INSERT INTO `capitals` VALUES ('Brussels','Belgium'),('Dublin','Ireland'),('Madrid','Spain'),('Monaco','Monaco'),('Paris','France');
/*!40000 ALTER TABLE `capitals` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `city`
--

DROP TABLE IF EXISTS `city`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `city` (
  `City` varchar(32) NOT NULL,
  `Country` varchar(32) NOT NULL,
  `latitude` varchar(7) NOT NULL,
  `longitude` varchar(7) NOT NULL,
  `population` int(11) NOT NULL,
  PRIMARY KEY (`City`,`Country`),
  KEY `Country` (`Country`),
  CONSTRAINT `city_ibfk_1` FOREIGN KEY (`Country`) REFERENCES `country` (`Name`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `city`
--

LOCK TABLES `city` WRITE;
/*!40000 ALTER TABLE `city` DISABLE KEYS */;
INSERT INTO `city` VALUES ('Barcelona','Spain','41 23 N','2 11 E',5375774),('Brussels','Belgium','50 51 N','4 21 E',1830000),('Dublin','Ireland','53 20 N','6 15 W',1801040),('Madrid','Spain','40 24 N','3 41 W',6489162),('Metz','France','30 23 N','32 31 E',23432),('Monaco','Monaco','43 43 N','7 25 E',37731),('Paris','France','48 52 N','2 20 E',12405426),('Valencia','Spain','39 28 N','0 23 W',2516818);
/*!40000 ALTER TABLE `city` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `city_language`
--

DROP TABLE IF EXISTS `city_language`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `city_language` (
  `City` varchar(32) NOT NULL,
  `Country` varchar(32) NOT NULL,
  `Language` varchar(16) NOT NULL,
  PRIMARY KEY (`City`,`Country`,`Language`),
  KEY `Language` (`Language`),
  CONSTRAINT `city_language_ibfk_1` FOREIGN KEY (`City`, `Country`) REFERENCES `city` (`City`, `Country`) ON UPDATE CASCADE,
  CONSTRAINT `city_language_ibfk_2` FOREIGN KEY (`Language`) REFERENCES `language` (`Language`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `city_language`
--

LOCK TABLES `city_language` WRITE;
/*!40000 ALTER TABLE `city_language` DISABLE KEYS */;
INSERT INTO `city_language` VALUES ('Barcelona','Spain','Catalan'),('Brussels','Belgium','Dutch'),('Dublin','Ireland','English'),('Brussels','Belgium','French'),('Metz','France','French'),('Monaco','Monaco','French'),('Paris','France','French'),('Dublin','Ireland','Gaelic'),('Barcelona','Spain','Spanish'),('Madrid','Spain','Spanish'),('Valencia','Spain','Spanish'),('Valencia','Spain','Valencian');
/*!40000 ALTER TABLE `city_language` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `city_review`
--

DROP TABLE IF EXISTS `city_review`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `city_review` (
  `Username` varchar(16) NOT NULL,
  `City` varchar(32) NOT NULL,
  `Country` varchar(32) NOT NULL,
  `Date` date NOT NULL,
  `Score` int(11) NOT NULL,
  `Description` varchar(5000) NOT NULL,
  PRIMARY KEY (`Username`,`City`,`Country`,`Date`),
  KEY `City` (`City`,`Country`),
  CONSTRAINT `city_review_ibfk_1` FOREIGN KEY (`Username`) REFERENCES `users` (`Username`),
  CONSTRAINT `city_review_ibfk_2` FOREIGN KEY (`City`, `Country`) REFERENCES `city` (`City`, `Country`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `city_review`
--

LOCK TABLES `city_review` WRITE;
/*!40000 ALTER TABLE `city_review` DISABLE KEYS */;
INSERT INTO `city_review` VALUES ('cole','Paris','France','2016-07-18',3,'Could do better'),('mehul','Monaco','Monaco','2016-07-19',2,'It was ok'),('nancy','Monaco','Monaco','2016-07-19',1,'It was ok'),('nancy','Paris','France','2016-07-12',5,'It was ok'),('varun','Metz','France','2016-07-19',3,'It is not nice'),('varun','Monaco','Monaco','2016-07-19',3,'It was ok');
/*!40000 ALTER TABLE `city_review` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Temporary view structure for view `city_scores`
--

DROP TABLE IF EXISTS `city_scores`;
/*!50001 DROP VIEW IF EXISTS `city_scores`*/;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
/*!50001 CREATE VIEW `city_scores` AS SELECT
 1 AS `City`,
 1 AS `Country`,
 1 AS `Average_score`*/;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `country`
--

DROP TABLE IF EXISTS `country`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `country` (
  `Name` varchar(32) NOT NULL,
  `Population` int(11) NOT NULL,
  PRIMARY KEY (`Name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `country`
--

LOCK TABLES `country` WRITE;
/*!40000 ALTER TABLE `country` DISABLE KEYS */;
INSERT INTO `country` VALUES ('Belgium',113239973),('France',66553766),('Ireland',4892305),('Monaco',37731),('Spain',48146134);
/*!40000 ALTER TABLE `country` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `country_language`
--

DROP TABLE IF EXISTS `country_language`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `country_language` (
  `Country` varchar(32) NOT NULL,
  `Language` varchar(16) NOT NULL,
  PRIMARY KEY (`Country`,`Language`),
  KEY `Language` (`Language`),
  CONSTRAINT `country_language_ibfk_1` FOREIGN KEY (`Country`) REFERENCES `country` (`Name`) ON UPDATE CASCADE,
  CONSTRAINT `country_language_ibfk_2` FOREIGN KEY (`Language`) REFERENCES `language` (`Language`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `country_language`
--

LOCK TABLES `country_language` WRITE;
/*!40000 ALTER TABLE `country_language` DISABLE KEYS */;
INSERT INTO `country_language` VALUES ('Belgium','Dutch'),('Ireland','English'),('Belgium','French'),('France','French'),('Monaco','French'),('Ireland','Gaelic'),('Belgium','German'),('Spain','Spanish');
/*!40000 ALTER TABLE `country_language` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `event`
--

DROP TABLE IF EXISTS `event`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `event` (
  `Name` varchar(50) NOT NULL,
  `Date` date NOT NULL,
  `Start_time` time NOT NULL,
  `Address` varchar(64) NOT NULL,
  `City` varchar(32) NOT NULL,
  `Country` varchar(32) NOT NULL,
  `Category` varchar(12) NOT NULL,
  `Description` varchar(1000) NOT NULL,
  `Std_discount` tinyint(1) NOT NULL,
  `End_time` time DEFAULT NULL,
  `Cost` decimal(10,2) NOT NULL,
  PRIMARY KEY (`Name`,`Date`,`Start_time`,`Address`,`City`,`Country`),
  KEY `Address` (`Address`,`City`,`Country`),
  KEY `Category` (`Category`),
  CONSTRAINT `event_ibfk_1` FOREIGN KEY (`Address`, `City`, `Country`) REFERENCES `location` (`Address`, `City`, `Country`) ON UPDATE CASCADE,
  CONSTRAINT `event_ibfk_2` FOREIGN KEY (`Category`) REFERENCES `event_categories` (`Category`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `event`
--

LOCK TABLES `event` WRITE;
/*!40000 ALTER TABLE `event` DISABLE KEYS */;
INSERT INTO `event` VALUES ('Animating Finding Dory','2016-08-01','19:30:00','109 Disney Way','Barcelona','Spain','presentation','Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.',0,NULL,0.00),('Beauty and the Beast Sing Along','2016-04-25','18:00:00','106 Disney Way','Barcelona','Spain','concert','Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.',1,'20:30:00',15.00),('Beauty and the Beast Sing Along','2016-07-01','20:00:00','106 Disney Way','Barcelona','Spain','concert','Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.',1,'22:30:00',15.00),('Brother Bear Live','2016-05-06','15:00:00','110 Disney Way','Barcelona','Spain','concert','Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.',0,'17:00:00',20.00),('Brother Bear Live','2016-06-01','15:00:00','114 Disney Way','Paris','France','concert','Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.',1,'17:00:00',20.00),('Disney Convention','2016-01-25','19:00:00','112 Disney Way','Paris','France','festival','Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.',0,'23:00:00',35.00),('Event 2','2016-12-01','13:00:00','118 Disney Way','Paris','France','concert','Description 2',0,NULL,0.00),('Olaf vs Sven','2016-07-03','20:00:00','107 Disney Way','Barcelona','Spain','sports match','Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.',0,'23:00:00',30.00),('Race to Defeat the Huns','2016-05-09','12:00:00','111 Disney Way','Paris','France','race','Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.',0,NULL,40.00),('Race to See the Floating Lanterns','2016-03-22','06:00:00','111 Disney Way','Paris','France','race','Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.',0,'12:00:00',50.00),('Why Jane Is A Boss','2016-06-09','17:30:00','109 Disney Way','Barcelona','Spain','presentation','Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.',1,NULL,5.00);
/*!40000 ALTER TABLE `event` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `event_categories`
--

DROP TABLE IF EXISTS `event_categories`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `event_categories` (
  `Category` varchar(12) NOT NULL,
  PRIMARY KEY (`Category`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `event_categories`
--

LOCK TABLES `event_categories` WRITE;
/*!40000 ALTER TABLE `event_categories` DISABLE KEYS */;
INSERT INTO `event_categories` VALUES ('concert'),('festival'),('presentation'),('race'),('sports match');
/*!40000 ALTER TABLE `event_categories` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `event_review`
--

DROP TABLE IF EXISTS `event_review`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `event_review` (
  `Username` varchar(16) NOT NULL,
  `Name` varchar(32) NOT NULL,
  `Date` date NOT NULL,
  `Start_time` time NOT NULL,
  `Address` varchar(64) NOT NULL,
  `City` varchar(32) NOT NULL,
  `Country` varchar(32) NOT NULL,
  `Review_date` date NOT NULL,
  `Score` int(11) NOT NULL,
  `Review` varchar(5000) NOT NULL,
  PRIMARY KEY (`Username`,`Name`,`Date`,`Start_time`,`Address`,`City`,`Country`,`Review_date`),
  KEY `Event_name` (`Name`,`Date`,`Start_time`,`Address`,`City`,`Country`),
  CONSTRAINT `event_review_ibfk_1` FOREIGN KEY (`Username`) REFERENCES `users` (`Username`),
  CONSTRAINT `event_review_ibfk_2` FOREIGN KEY (`Name`, `Date`, `Start_time`, `Address`, `City`, `Country`) REFERENCES `event` (`Name`, `Date`, `Start_time`, `Address`, `City`, `Country`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `event_review`
--

LOCK TABLES `event_review` WRITE;
/*!40000 ALTER TABLE `event_review` DISABLE KEYS */;
INSERT INTO `event_review` VALUES ('cole','Brother Bear Live','2016-05-06','15:00:00','110 Disney Way','Barcelona','Spain','2016-07-13',1,'Finding Dory is a treasure honestly.'),('cole','Brother Bear Live','2016-06-01','15:00:00','114 Disney Way','Paris','France','2016-07-13',1,'Finding Dory is a treasure honestly.'),('cole','Event 2','2016-12-01','13:00:00','118 Disney Way','Paris','France','2016-07-13',5,'It was ok'),('mehul','Brother Bear Live','2016-05-06','15:00:00','110 Disney Way','Barcelona','Spain','2016-07-13',2,'Finding Dory is a treasure honestly.'),('nancy','Animating Finding Dory','2016-08-01','19:30:00','109 Disney Way','Barcelona','Spain','2016-07-13',5,'Finding Dory is a treasure honestly.'),('varun','Animating Finding Dory','2016-08-01','19:30:00','109 Disney Way','Barcelona','Spain','2016-07-13',3,'Finding Dory is a treasure honestly.'),('varun','Brother Bear Live','2016-06-01','15:00:00','114 Disney Way','Paris','France','2016-07-13',2,'Finding Dory is a treasure honestly.');
/*!40000 ALTER TABLE `event_review` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Temporary view structure for view `event_scores`
--

DROP TABLE IF EXISTS `event_scores`;
/*!50001 DROP VIEW IF EXISTS `event_scores`*/;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
/*!50001 CREATE VIEW `event_scores` AS SELECT
 1 AS `Name`,
 1 AS `Date`,
 1 AS `Address`,
 1 AS `City`,
 1 AS `Country`,
 1 AS `Average_score`*/;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `language`
--

DROP TABLE IF EXISTS `language`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `language` (
  `Language` varchar(16) NOT NULL,
  PRIMARY KEY (`Language`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `language`
--

LOCK TABLES `language` WRITE;
/*!40000 ALTER TABLE `language` DISABLE KEYS */;
INSERT INTO `language` VALUES ('Basque (Euskara)'),('Catalan'),('Dutch'),('English'),('Flemish'),('French'),('Gaelic'),('Galician'),('German'),('Greek'),('Italian'),('Portuguese'),('Spanish'),('Valencian');
/*!40000 ALTER TABLE `language` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `location`
--

DROP TABLE IF EXISTS `location`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `location` (
  `Address` varchar(64) NOT NULL,
  `City` varchar(32) NOT NULL,
  `Country` varchar(32) NOT NULL,
  `Cost` decimal(10,2) NOT NULL,
  `Type` varchar(10) NOT NULL,
  `Std_discount` tinyint(1) NOT NULL,
  `Name` varchar(32) NOT NULL,
  PRIMARY KEY (`Address`,`City`,`Country`),
  KEY `City` (`City`,`Country`),
  KEY `Type` (`Type`),
  CONSTRAINT `location_ibfk_1` FOREIGN KEY (`City`, `Country`) REFERENCES `city` (`City`, `Country`) ON UPDATE CASCADE,
  CONSTRAINT `location_ibfk_2` FOREIGN KEY (`Type`) REFERENCES `location_types` (`Type`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `location`
--

LOCK TABLES `location` WRITE;
/*!40000 ALTER TABLE `location` DISABLE KEYS */;
INSERT INTO `location` VALUES ('101 Disney Way','Madrid','Spain',0.00,'park',0,'Retiro Park'),('102 Disney Way','Madrid','Spain',15.00,'museum',1,'The Prado'),('103 Disney Way','Madrid','Spain',13.00,'museum',1,'Royal Palace'),('104 Disney Way','Madrid','Spain',0.00,'other',0,'opera House'),('105 Disney Way','Madrid','Spain',17.00,'museum',1,'Reina Sofia'),('106 Disney Way','Barcelona','Spain',0.00,'other',0,'Arc d\'Triomf'),('107 Disney Way','Barcelona','Spain',0.00,'stadium',0,'Camp Nou'),('108 Disney Way','Barcelona','Spain',15.00,'church',1,'Sagrada Familia'),('109 Disney Way','Barcelona','Spain',8.00,'Park',0,'Parc Guell'),('110 Disney Way','Barcelona','Spain',0.00,'other',0,'Teatre Apolo'),('111 Disney Way','Paris','France',14.00,'other',1,'Eiffel Tower'),('112 Disney Way','Paris','France',25.00,'museum',1,'Louvre'),('113 Disney Way','Paris','France',0.00,'church',0,'Notre Dame'),('114 Disney Way','Paris','France',0.00,'restaurant',0,'Moulin Rouge'),('118 Disney Way','Paris','France',14.00,'church',0,'Church 2');
/*!40000 ALTER TABLE `location` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `location_review`
--

DROP TABLE IF EXISTS `location_review`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `location_review` (
  `Username` varchar(16) NOT NULL,
  `Address` varchar(64) NOT NULL,
  `City` varchar(32) NOT NULL,
  `Country` varchar(32) NOT NULL,
  `Date` date NOT NULL,
  `Score` int(11) NOT NULL,
  `Description` varchar(5000) NOT NULL,
  PRIMARY KEY (`Username`,`Address`,`City`,`Country`,`Date`),
  KEY `Address` (`Address`,`City`,`Country`),
  CONSTRAINT `location_review_ibfk_1` FOREIGN KEY (`Username`) REFERENCES `users` (`Username`),
  CONSTRAINT `location_review_ibfk_2` FOREIGN KEY (`Address`, `City`, `Country`) REFERENCES `location` (`Address`, `City`, `Country`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `location_review`
--

LOCK TABLES `location_review` WRITE;
/*!40000 ALTER TABLE `location_review` DISABLE KEYS */;
INSERT INTO `location_review` VALUES ('cole','118 Disney Way','Paris','France','2016-07-13',1,'It was ok'),('mehul','106 Disney Way','Barcelona','Spain','2016-07-19',2,'It was ok'),('nancy','106 Disney Way','Barcelona','Spain','2016-07-19',1,'It was ok'),('varun','110 Disney Way','Barcelona','Spain','2016-07-19',3,'It was ok');
/*!40000 ALTER TABLE `location_review` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Temporary view structure for view `location_scores`
--

DROP TABLE IF EXISTS `location_scores`;
/*!50001 DROP VIEW IF EXISTS `location_scores`*/;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
/*!50001 CREATE VIEW `location_scores` AS SELECT
 1 AS `Address`,
 1 AS `City`,
 1 AS `Country`,
 1 AS `Average_score`*/;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `location_types`
--

DROP TABLE IF EXISTS `location_types`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `location_types` (
  `Type` varchar(10) NOT NULL,
  PRIMARY KEY (`Type`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `location_types`
--

LOCK TABLES `location_types` WRITE;
/*!40000 ALTER TABLE `location_types` DISABLE KEYS */;
INSERT INTO `location_types` VALUES ('church'),('memorial'),('museum'),('other'),('park'),('plaza'),('restaurant'),('stadium');
/*!40000 ALTER TABLE `location_types` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `users` (
  `Username` varchar(16) NOT NULL,
  `Email` varchar(32) NOT NULL,
  `Password` varchar(20) NOT NULL,
  `Is_manager` tinyint(1) NOT NULL,
  PRIMARY KEY (`Username`),
  UNIQUE KEY `Email` (`Email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES ('cole','cole.a.bowers@gmail.com','password',0),('manager','thebossman@gttravel.com','password',1),('mehul','mehulm@gmail.com','password',0),('nancy','nancy.tao42@gmail.com','password',0),('varun','varungupt-a@gmail.com','password',0);
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Final view structure for view `city_scores`
--

/*!50001 DROP VIEW IF EXISTS `city_scores`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8 */;
/*!50001 SET character_set_results     = utf8 */;
/*!50001 SET collation_connection      = utf8_general_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `city_scores` AS (select `city`.`City` AS `City`,`city`.`Country` AS `Country`,avg(`city_review`.`Score`) AS `Average_score` from (`city` join `city_review` on(((`city`.`City` = `city_review`.`City`) and (`city`.`Country` = `city_review`.`Country`)))) group by `city`.`City`,`city`.`Country` order by `Average_score` desc) */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `event_scores`
--

/*!50001 DROP VIEW IF EXISTS `event_scores`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8 */;
/*!50001 SET character_set_results     = utf8 */;
/*!50001 SET collation_connection      = utf8_general_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `event_scores` AS (select `event`.`Name` AS `Name`,`event`.`Date` AS `Date`,`event`.`Address` AS `Address`,`event`.`City` AS `City`,`event`.`Country` AS `Country`,avg(`event_review`.`Score`) AS `Average_score` from (`event` join `event_review` on(((`event`.`Name` = `event_review`.`Name`) and (`event`.`Date` = `event_review`.`Date`) and (`event`.`Start_time` = `event_review`.`Start_time`) and (`event`.`Address` = `event_review`.`Address`) and (`event`.`City` = `event_review`.`City`) and (`event`.`Country` = `event_review`.`Country`)))) group by `event`.`Name`,`event`.`Date`,`event`.`Address`,`event`.`City`,`event`.`Country` order by `Average_score` desc) */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `location_scores`
--

/*!50001 DROP VIEW IF EXISTS `location_scores`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8 */;
/*!50001 SET character_set_results     = utf8 */;
/*!50001 SET collation_connection      = utf8_general_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `location_scores` AS (select `location`.`Address` AS `Address`,`location`.`City` AS `City`,`location`.`Country` AS `Country`,avg(`location_review`.`Score`) AS `Average_score` from (`location` join `location_review` on(((`location`.`Address` = `location_review`.`Address`) and (`location`.`City` = `location_review`.`City`) and (`location`.`Country` = `location_review`.`Country`)))) group by `location`.`Address`,`location`.`City`,`location`.`Country` order by `Average_score` desc) */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2016-07-21 10:33:26
