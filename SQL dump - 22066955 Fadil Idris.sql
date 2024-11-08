-- MySQL dump 10.13  Distrib 8.0.34, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: world_hotels
-- ------------------------------------------------------
-- Server version	8.2.0

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `billings`
--

DROP TABLE IF EXISTS `billings`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `billings` (
  `BillingsID` int NOT NULL AUTO_INCREMENT,
  `ChargeRate` varchar(20) NOT NULL,
  `TotalCharges` varchar(20) NOT NULL,
  `PaymentStatus` varchar(20) NOT NULL,
  `BookingID` int DEFAULT NULL,
  `PayementType` varchar(20) NOT NULL DEFAULT 'Hotel Payement',
  PRIMARY KEY (`BillingsID`),
  KEY `BookingID` (`BookingID`),
  CONSTRAINT `billings_ibfk_1` FOREIGN KEY (`BookingID`) REFERENCES `bookingtable` (`BookingID`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `billings`
--

LOCK TABLES `billings` WRITE;
/*!40000 ALTER TABLE `billings` DISABLE KEYS */;
INSERT INTO `billings` VALUES (1,'180.0','1800.0','Payed',1,'Hotel Payement'),(2,'N/A','1260.0','Extra Payement',1,'Hotel Payement'),(3,'210.0','630.0','Payed',2,'Hotel Payement'),(4,'130.01538461538462','1690.2','Payed',3,'Hotel Payement'),(5,'N/A','259.79999999999995','Extra Payement',3,'Hotel Payement');
/*!40000 ALTER TABLE `billings` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `bookingtable`
--

DROP TABLE IF EXISTS `bookingtable`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `bookingtable` (
  `BookingID` int NOT NULL AUTO_INCREMENT,
  `RoomTableID` int DEFAULT NULL,
  `CheckInDate` date NOT NULL,
  `CheckOutDate` date NOT NULL,
  `HotelInformationID` int DEFAULT NULL,
  `Status` varchar(20) DEFAULT 'Booked',
  `UserInformationID` int DEFAULT NULL,
  PRIMARY KEY (`BookingID`),
  KEY `HotelInformationID` (`HotelInformationID`),
  KEY `RoomTableID` (`RoomTableID`),
  KEY `UserInformationID` (`UserInformationID`),
  CONSTRAINT `bookingtable_ibfk_1` FOREIGN KEY (`HotelInformationID`) REFERENCES `hotelinformation` (`HotelInformationID`) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `bookingtable_ibfk_2` FOREIGN KEY (`RoomTableID`) REFERENCES `room` (`RoomTableID`) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `bookingtable_ibfk_3` FOREIGN KEY (`UserInformationID`) REFERENCES `userinformation` (`UserInfoId`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `bookingtable`
--

LOCK TABLES `bookingtable` WRITE;
/*!40000 ALTER TABLE `bookingtable` DISABLE KEYS */;
INSERT INTO `bookingtable` VALUES (1,NULL,'2024-04-30','2024-05-17',13,'Cancelled',1),(2,2,'2024-04-30','2024-05-03',1,'Booked',1),(3,3,'2024-05-03','2024-05-18',11,'Booked',4);
/*!40000 ALTER TABLE `bookingtable` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `hotelinformation`
--

DROP TABLE IF EXISTS `hotelinformation`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `hotelinformation` (
  `HotelInformationID` int NOT NULL AUTO_INCREMENT,
  `City` varchar(40) DEFAULT NULL,
  `Standared_Room_Capacity` varchar(20) DEFAULT NULL,
  `Double_Room_Capacity` varchar(20) DEFAULT NULL,
  `Family_Room_Capacity` varchar(20) DEFAULT NULL,
  `PeakSeasonPrice` float DEFAULT NULL,
  `OffSeasonPrice` float DEFAULT NULL,
  PRIMARY KEY (`HotelInformationID`)
) ENGINE=InnoDB AUTO_INCREMENT=20 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `hotelinformation`
--

LOCK TABLES `hotelinformation` WRITE;
/*!40000 ALTER TABLE `hotelinformation` DISABLE KEYS */;
INSERT INTO `hotelinformation` VALUES (1,'Aberdeen','50','45','18',140,200),(2,'Belfast','24','40','116',130,70),(3,'Birminghham','33','55','22',150,75),(4,'Bristol','30','50','20',140,70),(5,'Cardiff','27','45','18',130,70),(6,'Edinburgh','36','60','24',160,80),(7,'Glasgow','42','70','28',150,75),(8,'London','48','80','32',200,100),(9,'Manchester','45','75','30',180,90),(10,'New Castle','27','45','18',120,70),(11,'Norwich','27','45','18',130,70),(12,'Nottingham','33','55','22',130,70),(13,'Oxford','27','45','18',180,90),(14,'Plymouth','24','40','16',180,90),(15,'Swansea','21','35','14',130,70),(16,'Bournemouth','27','45','18',130,70),(17,'Kent','30','50','20',140,80);
/*!40000 ALTER TABLE `hotelinformation` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `room`
--

DROP TABLE IF EXISTS `room`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `room` (
  `RoomTableID` int NOT NULL AUTO_INCREMENT,
  `HotelID` int DEFAULT NULL,
  `RoomNumber` varchar(20) DEFAULT NULL,
  `RoomType` varchar(20) NOT NULL,
  PRIMARY KEY (`RoomTableID`),
  KEY `HotelID` (`HotelID`),
  CONSTRAINT `room_ibfk_1` FOREIGN KEY (`HotelID`) REFERENCES `hotelinformation` (`HotelInformationID`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `room`
--

LOCK TABLES `room` WRITE;
/*!40000 ALTER TABLE `room` DISABLE KEYS */;
INSERT INTO `room` VALUES (2,1,'Abefam1','family'),(3,11,'Nordou1','double');
/*!40000 ALTER TABLE `room` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `userinformation`
--

DROP TABLE IF EXISTS `userinformation`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `userinformation` (
  `UserInfoId` int NOT NULL AUTO_INCREMENT,
  `Name` varchar(30) DEFAULT NULL,
  `Surname` varchar(30) DEFAULT NULL,
  `Email` varchar(60) DEFAULT NULL,
  `PhoneNumber` varchar(20) DEFAULT NULL,
  `User_Password` varchar(90) DEFAULT NULL,
  `Privilages` varchar(20) DEFAULT 'standard',
  PRIMARY KEY (`UserInfoId`),
  UNIQUE KEY `Email` (`Email`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `userinformation`
--

LOCK TABLES `userinformation` WRITE;
/*!40000 ALTER TABLE `userinformation` DISABLE KEYS */;
INSERT INTO `userinformation` VALUES (1,'Fadil Idris','Habeeb','fihabeeb006@gmail.com',NULL,'$5$rounds=535000$kzaLMn3TbXxs2DJM$1OnKPioB3IrOeHVkZg01XBH6tDNQGBOkUI98UgFwGQ.','admin'),(2,'Jak','Dax','fihabeeb@gmail.com',NULL,'$5$rounds=535000$oSdsaKJta3THNB/L$UGvCKzJdbCi2lmjixr3T1Icj5bi5na2DWWg1rpQ/fj5','standard'),(4,'jack','daxter','jack@email.com',NULL,'$5$rounds=535000$6DN8.DrVKqlwcjFI$Yfd/GgmHIi1JbTmGw7U6.ap43gPfzPjfE7U2lZy8tTC','standard');
/*!40000 ALTER TABLE `userinformation` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-04-29 14:34:32
