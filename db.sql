-- phpMyAdmin SQL Dump
-- version 4.0.4.1
-- http://www.phpmyadmin.net
--
-- Host: 127.0.0.1
-- Generation Time: Jan 10, 2014 at 11:00 PM
-- Server version: 5.5.32
-- PHP Version: 5.4.19

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Database: `db`
--
CREATE DATABASE IF NOT EXISTS `db` DEFAULT CHARACTER SET latin1 COLLATE latin1_swedish_ci;
USE `db`;

-- --------------------------------------------------------

--
-- Table structure for table `location`
--

CREATE TABLE IF NOT EXISTS `location` (
  `location_id` int(11) NOT NULL AUTO_INCREMENT,
  `location_country` varchar(45) NOT NULL,
  `location_subDivision` varchar(45) NOT NULL,
  `location_city` varchar(45) NOT NULL,
  PRIMARY KEY (`location_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=4 ;

--
-- Dumping data for table `location`
--

INSERT INTO `location` (`location_id`, `location_country`, `location_subDivision`, `location_city`) VALUES
(1, 'Canada', 'Lower Mainland', 'Vancouver'),
(2, 'Canada', 'Interior', 'Kamloops'),
(3, 'South Africa', 'Sowete', 'Johannosberg');

-- --------------------------------------------------------

--
-- Table structure for table `plan`
--

CREATE TABLE IF NOT EXISTS `plan` (
  `plan_id` int(10) NOT NULL AUTO_INCREMENT,
  `plan_name` varchar(45) DEFAULT NULL,
  `plan_usersMax` int(10) NOT NULL,
  PRIMARY KEY (`plan_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=3 ;

--
-- Dumping data for table `plan`
--

INSERT INTO `plan` (`plan_id`, `plan_name`, `plan_usersMax`) VALUES
(1, 'AwesomeApp', 10000),
(2, 'NotSoAwesomeApp', 5);

-- --------------------------------------------------------

--
-- Table structure for table `project`
--

CREATE TABLE IF NOT EXISTS `project` (
  `project_id` int(11) NOT NULL AUTO_INCREMENT,
  `project_name` varchar(45) DEFAULT NULL,
  `project_createDate` datetime DEFAULT NULL,
  `project_completionDate` datetime DEFAULT NULL,
  `project_lastActivityDate` datetime DEFAULT NULL,
  `Team_team_id` int(11) NOT NULL,
  PRIMARY KEY (`project_id`),
  KEY `Team_teamId` (`Team_team_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=4 ;

--
-- Dumping data for table `project`
--

INSERT INTO `project` (`project_id`, `project_name`, `project_createDate`, `project_completionDate`, `project_lastActivityDate`, `Team_team_id`) VALUES
(1, 'ISpyApp', '2013-12-19 06:22:13', '2013-12-23 06:22:07', '2013-12-22 12:14:16', 1),
(2, 'HistoryProject', '2013-12-20 07:06:14', '2013-12-22 15:00:00', '2013-12-22 00:00:00', 2),
(3, 'HelloWorld', '2014-01-02 05:27:00', NULL, '2014-01-04 08:11:17', 9);

-- --------------------------------------------------------

--
-- Table structure for table `session`
--

CREATE TABLE IF NOT EXISTS `session` (
  `session_id` int(45) NOT NULL AUTO_INCREMENT,
  `session_loginDate` datetime DEFAULT NULL,
  `session_logoutDate` datetime DEFAULT NULL,
  `session_ipAddress` varchar(40) NOT NULL,
  `Users_user_id` int(11) NOT NULL,
  `Location_location_id` int(11) NOT NULL,
  PRIMARY KEY (`session_id`),
  KEY `Users_userId` (`Users_user_id`),
  KEY `Location_location_id` (`Location_location_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=5 ;

--
-- Dumping data for table `session`
--

INSERT INTO `session` (`session_id`, `session_loginDate`, `session_logoutDate`, `session_ipAddress`, `Users_user_id`, `Location_location_id`) VALUES
(1, '2014-01-01 06:10:32', '2014-01-01 21:54:45', '123.456.789', 1, 1),
(2, '2014-01-01 03:04:07', '2014-01-01 08:10:14', '789.456.123', 2, 2),
(3, '2014-01-01 00:00:00', '2014-01-01 05:14:14', '123.456.789', 5, 1),
(4, '2014-01-04 05:16:10', '2014-01-04 07:00:00', '123.456.789', 5, 1);

-- --------------------------------------------------------

--
-- Table structure for table `team`
--

CREATE TABLE IF NOT EXISTS `team` (
  `team_id` int(10) NOT NULL AUTO_INCREMENT,
  `team_name` varchar(45) DEFAULT NULL,
  `team_createDate` date DEFAULT NULL,
  `Users_owner_id` int(10) NOT NULL,
  PRIMARY KEY (`team_id`),
  KEY `Users_ownerId` (`Users_owner_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=10 ;

--
-- Dumping data for table `team`
--

INSERT INTO `team` (`team_id`, `team_name`, `team_createDate`, `Users_owner_id`) VALUES
(1, 'Dragons', '2013-12-19', 1),
(2, 'Eagles', '2013-12-20', 3),
(3, 'Panthers', '2014-01-03', 5),
(4, 'Techies', '2014-01-02', 4),
(9, 'Aliens', '2014-01-01', 13);

--
-- Triggers `team`
--
DROP TRIGGER IF EXISTS `ownerMustBeOnTeamINSERT`;
DELIMITER //
CREATE TRIGGER `ownerMustBeOnTeamINSERT` AFTER INSERT ON `team`
 FOR EACH ROW INSERT INTO team_has_users
VALUES (NEW.Users_owner_id, NEW.team_id)
//
DELIMITER ;
DROP TRIGGER IF EXISTS `ownerMustBeOnTeamUPDATE`;
DELIMITER //
CREATE TRIGGER `ownerMustBeOnTeamUPDATE` AFTER UPDATE ON `team`
 FOR EACH ROW INSERT INTO team_has_users
VALUES (NEW.Users_owner_id, NEW.team_id)
//
DELIMITER ;

-- --------------------------------------------------------

--
-- Table structure for table `team_has_users`
--

CREATE TABLE IF NOT EXISTS `team_has_users` (
  `Users_user_id` int(10) NOT NULL,
  `Team_team_id` int(10) NOT NULL,
  PRIMARY KEY (`Users_user_id`,`Team_team_id`),
  UNIQUE KEY `Users_user_id` (`Users_user_id`),
  KEY `Team_team_id` (`Team_team_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `team_has_users`
--

INSERT INTO `team_has_users` (`Users_user_id`, `Team_team_id`) VALUES
(1, 1),
(2, 1),
(3, 2),
(4, 4),
(5, 3),
(6, 2),
(7, 2),
(8, 3),
(9, 3),
(10, 3),
(11, 3),
(12, 4),
(13, 9);

--
-- Triggers `team_has_users`
--
DROP TRIGGER IF EXISTS `maxSizeLimitINSERT`;
DELIMITER //
CREATE TRIGGER `maxSizeLimitINSERT` BEFORE INSERT ON `team_has_users`
 FOR EACH ROW BEGIN


DECLARE total INT;
DECLARE maximum INT;

SELECT COUNT(DISTINCT u.user_id) 
FROM team t 
	JOIN team_has_users x ON t.team_id = x.Team_team_id
	JOIN users u ON u.user_id = x.Users_user_id
	JOIN plan p ON u.Plan_plan_id = p.plan_id
WHERE t.team_id = NEW.Team_team_id
INTO total;

SELECT p.plan_usersMax
FROM team t 
	JOIN users u ON t.Users_owner_id = u.user_id
	JOIN plan p ON u.Plan_plan_id = p.plan_id
WHERE team_id = NEW.Team_team_id
INTO maximum;


IF total >= maximum
THEN SIGNAL SQLSTATE '45000'
		SET MESSAGE_TEXT = 'Error, team size limit exceeded. Size determined by team owner plan type';
END IF;

END
//
DELIMITER ;
DROP TRIGGER IF EXISTS `maxSizeLimitUPDATE`;
DELIMITER //
CREATE TRIGGER `maxSizeLimitUPDATE` BEFORE UPDATE ON `team_has_users`
 FOR EACH ROW BEGIN


DECLARE total INT;
DECLARE maximum INT;

SELECT COUNT(DISTINCT u.user_id) 
FROM team t 
	JOIN team_has_users x ON t.team_id = x.Team_team_id
	JOIN users u ON u.user_id = x.Users_user_id
	JOIN plan p ON u.Plan_plan_id = p.plan_id
WHERE t.team_id = NEW.Team_team_id
INTO total;

SELECT p.plan_usersMax
FROM team t 
	JOIN users u ON t.Users_owner_id = u.user_id
	JOIN plan p ON u.Plan_plan_id = p.plan_id
WHERE team_id = NEW.Team_team_id
INTO maximum;


IF total >= maximum
THEN SIGNAL SQLSTATE '45000'
		SET MESSAGE_TEXT = 'Error, team size limit exceeded. Size determined by team owner plan type';
END IF;

END
//
DELIMITER ;

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE IF NOT EXISTS `users` (
  `user_id` int(8) NOT NULL AUTO_INCREMENT,
  `user_FName` varchar(45) NOT NULL,
  `user_LName` varchar(45) NOT NULL,
  `user_email` varchar(45) NOT NULL,
  `user_gender` varchar(1) NOT NULL,
  `user_dateBirth` date NOT NULL,
  `user_createDate` date NOT NULL,
  `user_upgradeDate` date DEFAULT NULL,
  `Plan_plan_id` int(10) NOT NULL,
  PRIMARY KEY (`user_id`),
  KEY `Plan_planId` (`Plan_plan_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=14 ;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`user_id`, `user_FName`, `user_LName`, `user_email`, `user_gender`, `user_dateBirth`, `user_createDate`, `user_upgradeDate`, `Plan_plan_id`) VALUES
(1, 'Parker', 'Ferguson', 'parker_ferguson@hotmail.com', 'M', '1984-01-11', '2013-12-19', NULL, 1),
(2, 'Jessica', 'Turner', 'jessica_turner@hotmail.com', 'F', '1988-02-02', '2013-12-19', '2014-01-01', 2),
(3, 'Mark', 'Jacobs', 'mark_jacobs@hotmail.com', 'M', '1977-12-03', '2013-12-19', NULL, 1),
(4, 'Max', 'Powers', 'max_powers@hotmail.com', 'M', '1980-11-04', '2013-12-29', '2014-01-01', 2),
(5, 'Homer', 'Simpson', 'homer_simpson@hotmail.com', 'M', '1976-09-01', '2013-12-29', '2014-01-03', 2),
(6, 'Ernest', 'Hemmingway', 'ernest_hemmingway@hotmail.com', 'm', '1978-09-11', '2013-12-29', '2014-01-01', 2),
(7, 'Pablo', 'Picasso', 'pablo_picasso@hotmail.com', 'M', '1956-08-12', '2013-12-29', '2013-12-29', 2),
(8, 'Emily', 'Carr', 'emily_carr@hotmail.com', 'F', '1980-03-12', '2013-12-29', '2014-01-01', 2),
(9, 'Mel', 'Gibson', 'mel_gibson@hotmail.com', 'M', '1975-12-01', '2013-12-09', '2013-12-16', 2),
(10, 'Elizabeth', 'Schuh', 'elizabeth_schuh@gmail.com', 'F', '1990-01-31', '2013-12-24', '2014-01-13', 2),
(11, 'Tom', 'Cruise', 'tom_cruise@gmail.com', 'M', '1975-10-09', '2014-01-01', NULL, 1),
(12, 'Walt', 'Disney', 'walt_disney@gmail.com', 'M', '1954-09-16', '2014-01-01', NULL, 1),
(13, 'Emilio', 'Estevez', 'emilio_estevez@hotmail.com', 'M', '1976-03-13', '2014-01-02', NULL, 1);

--
-- Triggers `users`
--
DROP TRIGGER IF EXISTS `userGenderINSERT`;
DELIMITER //
CREATE TRIGGER `userGenderINSERT` BEFORE INSERT ON `users`
 FOR EACH ROW BEGIN

IF NEW.user_gender != 'M' AND New.user_gender != 'F'

THEN SIGNAL SQLSTATE '45000'
		SET MESSAGE_TEXT = 'Error, gender must be M or F';
END IF;

END
//
DELIMITER ;
DROP TRIGGER IF EXISTS `userGenderUPDATE`;
DELIMITER //
CREATE TRIGGER `userGenderUPDATE` BEFORE UPDATE ON `users`
 FOR EACH ROW BEGIN

IF NEW.user_gender != 'M' AND New.user_gender != 'F'

THEN SIGNAL SQLSTATE '45000'
		SET MESSAGE_TEXT = 'Error, gender must be M or F';
END IF;

END
//
DELIMITER ;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `project`
--
ALTER TABLE `project`
  ADD CONSTRAINT `project_ibfk_1` FOREIGN KEY (`Team_team_id`) REFERENCES `team` (`team_id`) ON UPDATE CASCADE;

--
-- Constraints for table `session`
--
ALTER TABLE `session`
  ADD CONSTRAINT `session_ibfk_1` FOREIGN KEY (`Users_user_id`) REFERENCES `users` (`user_id`) ON UPDATE CASCADE,
  ADD CONSTRAINT `session_ibfk_2` FOREIGN KEY (`Location_location_id`) REFERENCES `location` (`location_id`) ON UPDATE CASCADE;

--
-- Constraints for table `team`
--
ALTER TABLE `team`
  ADD CONSTRAINT `team_ibfk_1` FOREIGN KEY (`Users_owner_id`) REFERENCES `users` (`user_id`) ON UPDATE CASCADE;

--
-- Constraints for table `team_has_users`
--
ALTER TABLE `team_has_users`
  ADD CONSTRAINT `team_has_users_ibfk_1` FOREIGN KEY (`Users_user_id`) REFERENCES `users` (`user_id`) ON UPDATE CASCADE,
  ADD CONSTRAINT `team_has_users_ibfk_2` FOREIGN KEY (`Team_team_id`) REFERENCES `team` (`team_id`) ON UPDATE CASCADE;

--
-- Constraints for table `users`
--
ALTER TABLE `users`
  ADD CONSTRAINT `users_ibfk_1` FOREIGN KEY (`Plan_plan_id`) REFERENCES `plan` (`plan_id`) ON UPDATE CASCADE;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
