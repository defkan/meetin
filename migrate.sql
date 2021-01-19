
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

CREATE TABLE `university` (
  `universityId` integer unsigned NOT NULL AUTO_INCREMENT,
  `universityName` varchar(255),
  PRIMARY KEY (`universityId`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;

CREATE TABLE `user` (
  `userId` integer unsigned NOT NULL AUTO_INCREMENT,
  `username` varchar(255) NOT NULL UNIQUE,
  `email` varchar(255) NOT NULL UNIQUE,
  `password` varchar(255) NOT NULL,
  PRIMARY KEY (`userId`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8;

CREATE TABLE `userdetail` (
  `userDetailId` integer unsigned NOT NULL AUTO_INCREMENT,
  `userId` integer unsigned UNIQUE NOT NULL,
  `universityId` integer unsigned,
  'gender' varchar(255),
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

