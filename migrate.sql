

set FOREIGN_KEY_CHECKS=0;
DROP TABLE IF EXISTS `interest`;
DROP TABLE IF EXISTS `interestlist`;
DROP TABLE IF EXISTS category;
DROP TABLE IF EXISTS `university`;
DROP TABLE IF EXISTS `user`;
DROP TABLE IF EXISTS `userdetail`;
DROP TABLE IF EXISTS `enrollment`;
DROP TABLE IF EXISTS `event`;
set FOREIGN_KEY_CHECKS=1;

CREATE TABLE category (
  categoryId integer unsigned NOT NULL AUTO_INCREMENT,
  categoryName varchar(255) UNIQUE NOT NULL,
  PRIMARY KEY (categoryId)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8;

--
-- Dumping data for table `category`
--

LOCK TABLES `category` WRITE;
/*!40000 ALTER TABLE `category` DISABLE KEYS */;
INSERT INTO `category` VALUES (1,'futbol'),(2,'Education'),(3,'PR'),(4,'FR'),(5,'Design');
/*!40000 ALTER TABLE `category` ENABLE KEYS */;
UNLOCK TABLES;




/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `university` (
  `universityId` integer unsigned NOT NULL AUTO_INCREMENT,
  `universityName` varchar(255),
  PRIMARY KEY (`universityId`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `university`
--

LOCK TABLES `university` WRITE;
/*!40000 ALTER TABLE `university` DISABLE KEYS */;
INSERT INTO `university` VALUES (1,'not selected');
/*!40000 ALTER TABLE `university` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user`
--

/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user` (
  `userId` integer unsigned NOT NULL AUTO_INCREMENT,
  `username` varchar(255) NOT NULL UNIQUE,
  `email` varchar(255) NOT NULL UNIQUE,
  `password` varchar(255) NOT NULL,
  PRIMARY KEY (`userId`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES (2,'a','cakirverda@gmail.com','e982fe702894da150c5f8e90708fc830'),(3,'lalverda','lalverdac@gmail.com','e982fe702894da150c5f8e90708fc830'),(4,'elaa','elaa@gmail.com','e982fe702894da150c5f8e90708fc830'),(11,'abcabc','abc@gmail.com','97ac82a5b825239e782d0339e2d7b910'),(13,'bugra','bugra@gmail.com','25d55ad283aa400af464c76d713c07ad');
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `userdetail`
--


/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `userdetail` (
  `userDetailId` integer unsigned NOT NULL AUTO_INCREMENT,
  `userId` integer unsigned UNIQUE NOT NULL,
  `universityId` integer unsigned,
  `photoUrl` varchar(255),
  `birthDate` date,
  `bio` varchar(255),
  `urlInstagram` varchar(255),
  `urlTwitter` varchar(255) ,
  `urlFacebook` varchar(255) ,
  `occupation` varchar(255) ,
  PRIMARY KEY (`userDetailId`),
  CONSTRAINT `userdetail_ibfk_1` FOREIGN KEY (`userId`) REFERENCES `user` (`userId`) ON DELETE CASCADE,
  CONSTRAINT `userdetail_ibfk_2` FOREIGN KEY (`universityId`) REFERENCES `university` (`universityId`) ON DELETE SET NULL
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `userdetail`
--

LOCK TABLES `userdetail` WRITE;
/*!40000 ALTER TABLE `userdetail` DISABLE KEYS */;
INSERT INTO `userdetail` VALUES (4,11,1,'img/profile/dummy.png',NULL,'','instagram','twitter','facebook',''),(5,13,1,'img/profile/dummy.png',NULL,'jjugguşjmşg','instagram','twitter','facebook','');
/*!40000 ALTER TABLE `userdetail` ENABLE KEYS */;
UNLOCK TABLES;




/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `event` (
  `eventId` integer unsigned NOT NULL AUTO_INCREMENT,
  `adminId` integer unsigned NOT NULL,
  `categoryId` integer unsigned,
  `eventName` varchar(255),
  `description` varchar(255),
  `eventLink` varchar(255),
  `eventdate` date,
  `eventPhotoUrl` varchar(255) DEFAULT 'img/event_photo/dummy.jpg',
  PRIMARY KEY (`eventId`),
  CONSTRAINT `event_ibfk_1` FOREIGN KEY (`adminId`) REFERENCES `user` (`userId`) ON DELETE CASCADE,
  CONSTRAINT `event_ibfk_2` FOREIGN KEY (`categoryId`) REFERENCES `category` (`categoryId`) ON DELETE SET NULL
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `event`
--

LOCK TABLES `event` WRITE;
/*!40000 ALTER TABLE `event` DISABLE KEYS */;
INSERT INTO `event` VALUES (1,11,1,'Denem','Deneme','','2020-03-03','img/event_photo/dummy.jpg'),(2,11,2,'wferwfe','efwfewf','ewfewfe','2020-01-01','img/event_photo/dummy.jpg'),(3,11,2,'wferwfe','efwfewf','ewfewfe','2020-01-01','img/event_photo/dummy.jpg'),(4,11,2,'wferwfe','efwfewf','ewfewfe','2020-01-01','img/event_photo/dummy.jpg'),(5,11,1,'efewf','fewfew','efwfew','2020-01-01','img/event_photo/dummy.jpg'),(6,11,1,'fefe','fefe','fqeeq','2020-01-01','img/event_photo/dummy.jpg'),(7,11,1,'fefe','fefegrwgEWRGEWE','fqeeq','2020-01-01','img/event_photo/dummy.jpg');
/*!40000 ALTER TABLE `event` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `enrollment`
--


/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `enrollment` (
  `enrollmentId` integer unsigned NOT NULL AUTO_INCREMENT,
  `userId` integer unsigned NOT NULL,
  `eventId` integer unsigned NOT NULL,
  `reason` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`enrollmentId`),
  KEY `userId` (`userId`),
  KEY `eventId` (`eventId`),
  CONSTRAINT `enrollment_ibfk_1` FOREIGN KEY (`userId`) REFERENCES `user` (`userId`) ON DELETE CASCADE,
  CONSTRAINT `enrollment_ibfk_2` FOREIGN KEY (`eventId`) REFERENCES `event` (`eventId`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;


LOCK TABLES `enrollment` WRITE;
/*!40000 ALTER TABLE `enrollment` DISABLE KEYS */;
INSERT INTO `enrollment` VALUES (1,11,1,NULL),(4,13,2,'dsgdgedw');
/*!40000 ALTER TABLE `enrollment` ENABLE KEYS */;
UNLOCK TABLES;

