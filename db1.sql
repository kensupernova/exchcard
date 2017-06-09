-- MySQL dump 10.13  Distrib 5.7.11, for osx10.9 (x86_64)
--
-- Host: localhost    Database: exchcard
-- ------------------------------------------------------
-- Server version	5.7.11

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
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(80) CHARACTER SET latin1 NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_group_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `group_id` (`group_id`,`permission_id`),
  KEY `auth_group__permission_id_1f49ccbbdc69d2fc_fk_auth_permission_id` (`permission_id`),
  CONSTRAINT `auth_group__permission_id_1f49ccbbdc69d2fc_fk_auth_permission_id` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permission_group_id_689710a9a73b7457_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) CHARACTER SET latin1 DEFAULT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) CHARACTER SET latin1 NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `content_type_id` (`content_type_id`,`codename`),
  CONSTRAINT `auth__content_type_id_508cf46651277a81_fk_django_content_type_id` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=73 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add permission',1,'add_permission'),(2,'Can change permission',1,'change_permission'),(3,'Can delete permission',1,'delete_permission'),(4,'Can add group',2,'add_group'),(5,'Can change group',2,'change_group'),(6,'Can delete group',2,'delete_group'),(7,'Can add user',3,'add_user'),(8,'Can change user',3,'change_user'),(9,'Can delete user',3,'delete_user'),(10,'Can add content type',4,'add_contenttype'),(11,'Can change content type',4,'change_contenttype'),(12,'Can delete content type',4,'delete_contenttype'),(13,'Can add session',5,'add_session'),(14,'Can change session',5,'change_session'),(15,'Can delete session',5,'delete_session'),(16,'Can add site',6,'add_site'),(17,'Can change site',6,'change_site'),(18,'Can delete site',6,'delete_site'),(19,'Can add log entry',7,'add_logentry'),(20,'Can change log entry',7,'change_logentry'),(21,'Can delete log entry',7,'delete_logentry'),(22,'Can add address',8,'add_address'),(23,'Can change address',8,'change_address'),(24,'Can delete address',8,'delete_address'),(25,'Can add profile',9,'add_profile'),(26,'Can change profile',9,'change_profile'),(27,'Can delete profile',9,'delete_profile'),(28,'Can add detailed address',10,'add_detailedaddress'),(29,'Can change detailed address',10,'change_detailedaddress'),(30,'Can delete detailed address',10,'delete_detailedaddress'),(31,'Can add card',11,'add_card'),(32,'Can change card',11,'change_card'),(33,'Can delete card',11,'delete_card'),(34,'Can add avatar photo',12,'add_avatarphoto'),(35,'Can change avatar photo',12,'change_avatarphoto'),(36,'Can delete avatar photo',12,'delete_avatarphoto'),(37,'Can add card photo',13,'add_cardphoto'),(38,'Can change card photo',13,'change_cardphoto'),(39,'Can delete card photo',13,'delete_cardphoto'),(40,'Can add dian zan',14,'add_dianzan'),(41,'Can change dian zan',14,'change_dianzan'),(42,'Can delete dian zan',14,'delete_dianzan'),(43,'Can add verse',15,'add_verse'),(44,'Can change verse',15,'change_verse'),(45,'Can delete verse',15,'delete_verse'),(46,'Can add gcm register',16,'add_gcmregister'),(47,'Can change gcm register',16,'change_gcmregister'),(48,'Can delete gcm register',16,'delete_gcmregister'),(49,'Can add secret',17,'add_secret'),(50,'Can change secret',17,'change_secret'),(51,'Can delete secret',17,'delete_secret'),(52,'Can add address',18,'add_address'),(53,'Can change address',18,'change_address'),(54,'Can delete address',18,'delete_address'),(55,'Can add detailed address',19,'add_detailedaddress'),(56,'Can change detailed address',19,'change_detailedaddress'),(57,'Can delete detailed address',19,'delete_detailedaddress'),(58,'Can add profile',20,'add_profile'),(59,'Can change profile',20,'change_profile'),(60,'Can delete profile',20,'delete_profile'),(61,'Can add card',21,'add_card'),(62,'Can change card',21,'change_card'),(63,'Can delete card',21,'delete_card'),(64,'Can add avatar photo',22,'add_avatarphoto'),(65,'Can change avatar photo',22,'change_avatarphoto'),(66,'Can delete avatar photo',22,'delete_avatarphoto'),(67,'Can add card photo',23,'add_cardphoto'),(68,'Can change card photo',23,'change_cardphoto'),(69,'Can delete card photo',23,'delete_cardphoto'),(70,'Can add dian zan',24,'add_dianzan'),(71,'Can change dian zan',24,'change_dianzan'),(72,'Can delete dian zan',24,'delete_dianzan');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user`
--

DROP TABLE IF EXISTS `auth_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `password` varchar(128) CHARACTER SET latin1 NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(30) CHARACTER SET latin1 NOT NULL,
  `first_name` varchar(30) CHARACTER SET latin1 NOT NULL,
  `last_name` varchar(30) CHARACTER SET latin1 NOT NULL,
  `email` varchar(254) CHARACTER SET latin1 DEFAULT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=23 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user`
--

LOCK TABLES `auth_user` WRITE;
/*!40000 ALTER TABLE `auth_user` DISABLE KEYS */;
INSERT INTO `auth_user` VALUES (10,'pbkdf2_sha256$20000$wrpo4u9Qgx2N$M2EWXBc9VZfE123tqXCXDYdT463BTBHA8f0eVShLQFs=','2017-05-09 18:07:00.927179',1,'ken','','','kencan2009@sina.com',1,1,'2017-05-09 17:48:40.773948'),(12,'pbkdf2_sha256$20000$x7A3yFeE1RQr$WTS6GBmAAuKl3NFzD0e5DiV1WXMiQ3un+h+Edo6QksA=','2017-05-09 18:23:10.361287',1,'zgh','','','kencan2009@sina.com',1,1,'2017-05-09 18:07:34.432360'),(13,'pbkdf2_sha256$20000$DQdu3o36eray$z4lXn4zK9vZBpW9D0x0V43TnacKvj9kpNgjx/UD/Kk4=','2017-05-14 07:10:21.008655',1,'admin','','','admin@126.com',1,1,'2017-05-09 18:23:57.930518'),(15,'pbkdf2_sha256$20000$Qj7f3xiQcZl5$0nq340ebuU//rKhqyWqoVUejxUJXYC6Z4P4xjIcUC2c=','2017-05-10 06:05:26.549795',0,'dbd7989949746e3c','','','zgh4@126.com',0,1,'2017-05-10 01:25:08.258800'),(16,'pbkdf2_sha256$20000$sc6pLODakLQx$D+fa0DMGjSYvV+ao3j4PSh+7rQD5wE8DM/v60FwWgIs=','2017-05-10 05:50:47.303958',0,'40158c82753e3145','','','zgh1@126.com',0,1,'2017-05-10 02:59:45.746913'),(17,'pbkdf2_sha256$20000$aue1qrog8MDO$3oS3YWLguvBNFt3kP1P4XAWj0wiI+5wbNhbi0CbyvHM=','2017-05-10 03:22:52.026419',0,'64230921c9a4c468','','','zgh2@126.com',0,1,'2017-05-10 03:18:57.875828'),(18,'pbkdf2_sha256$20000$Elo6if199YyU$gdyzLD3wRVpZ1YEKLun+0jaCk7rhgT7uoreQJJQa+S4=',NULL,0,'6bd90b4a5f8ff803','','','zgh3@126.com',0,1,'2017-05-10 03:35:35.816325'),(19,'pbkdf2_sha256$20000$59TKFyWneZKd$7QgGG8w/Zns8MYrHC1jx7nOBuvyD31lHbuZ0Czqe0ws=',NULL,0,'b289f0e14691fb12','','','zgh5@126.com',0,1,'2017-05-10 03:38:51.041656'),(20,'pbkdf2_sha256$20000$S07iWW00Dh5p$UXxMcHCRB8mYBH2YaHzmrITchgswnujyJzAwGFXqvsg=','2017-05-10 03:42:24.068541',0,'0ab8ffb991ac8cb3','','','zgh6@126.com',0,1,'2017-05-10 03:42:23.588847'),(21,'pbkdf2_sha256$20000$UQFENtz4IAl0$QeUX5H+b93OXZF8pRtIGqEu95+GLX1AKRHBTyU3+km0=','2017-05-10 04:02:34.198565',0,'a0a4db994046b493','','','zgh7@126.com',0,1,'2017-05-10 04:02:33.955392'),(22,'pbkdf2_sha256$20000$KWDb0CZmW0PV$oMZS/ynVmAoKALg48B4OqwR76ujuyDHoe93dFsG/x3k=','2017-05-16 05:12:11.814324',0,'d9fa5c2705fb01d5','','','zgh8@126.com',0,1,'2017-05-10 04:05:25.139956');
/*!40000 ALTER TABLE `auth_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_groups`
--

DROP TABLE IF EXISTS `auth_user_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user_groups` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`,`group_id`),
  KEY `auth_user_groups_group_id_33ac548dcf5f8e37_fk_auth_group_id` (`group_id`),
  CONSTRAINT `auth_user_groups_group_id_33ac548dcf5f8e37_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `auth_user_groups_user_id_4b5ed4ffdb8fd9b0_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_groups`
--

LOCK TABLES `auth_user_groups` WRITE;
/*!40000 ALTER TABLE `auth_user_groups` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_user_permissions`
--

DROP TABLE IF EXISTS `auth_user_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user_user_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`,`permission_id`),
  KEY `auth_user_u_permission_id_384b62483d7071f0_fk_auth_permission_id` (`permission_id`),
  CONSTRAINT `auth_user_u_permission_id_384b62483d7071f0_fk_auth_permission_id` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_user_user_permissi_user_id_7f0938558328534a_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_user_permissions`
--

LOCK TABLES `auth_user_user_permissions` WRITE;
/*!40000 ALTER TABLE `auth_user_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `djang_content_type_id_697914295151027a_fk_django_content_type_id` (`content_type_id`),
  KEY `django_admin_log_user_id_52fdd58701c5f563_fk_auth_user_id` (`user_id`),
  CONSTRAINT `djang_content_type_id_697914295151027a_fk_django_content_type_id` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_52fdd58701c5f563_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=20 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
INSERT INTO `django_admin_log` VALUES (4,'2017-05-09 18:04:04.149593','5','zgh2',3,'',3,10),(5,'2017-05-09 18:04:04.159709','2','zgm',3,'',3,10),(6,'2017-05-09 18:04:31.352072','1','zgh',3,'',3,10),(7,'2017-05-09 18:04:51.677701','6','zgh2@126.com',3,'',3,10),(8,'2017-05-09 18:09:17.835411','4','dummy',3,'',3,10),(9,'2017-05-09 18:11:08.132413','1','zgh, ohenldv, fafa',3,'',8,10),(10,'2017-05-09 18:23:23.806951','3','admin',3,'',3,12),(11,'2017-05-09 18:25:24.175209','9','guanghui',3,'',3,12),(12,'2017-05-09 18:33:46.819249','7','zgh, iamaddress1, 111111',1,'',8,13),(13,'2017-05-09 18:34:38.581345','3','zgh1@126.com',3,'',9,13),(14,'2017-05-09 18:34:50.002110','6','zgh1@126.com',1,'',9,13),(15,'2017-05-10 01:24:22.951725','14','194827999b6d39d',3,'',3,13),(16,'2017-05-10 01:24:41.228884','8','zgh, iamaddress4, 123445',3,'',8,13),(17,'2017-05-10 02:56:12.992981','7','zgh1@126.com',3,'',3,13),(18,'2017-05-10 02:56:13.002278','11','zgh2@126.com',3,'',3,13),(19,'2017-05-10 02:56:13.003576','8','zgh3@126.com',3,'',3,13);
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) CHARACTER SET latin1 NOT NULL,
  `model` varchar(100) CHARACTER SET latin1 NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_45f3b1d93ec8c61c_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=26 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (7,'admin','logentry'),(18,'api-exchcard','address'),(22,'api-exchcard','avatarphoto'),(21,'api-exchcard','card'),(23,'api-exchcard','cardphoto'),(19,'api-exchcard','detailedaddress'),(24,'api-exchcard','dianzan'),(20,'api-exchcard','profile'),(2,'auth','group'),(1,'auth','permission'),(3,'auth','user'),(4,'contenttypes','contenttype'),(8,'exchcard','address'),(12,'exchcard','avatarphoto'),(11,'exchcard','card'),(13,'exchcard','cardphoto'),(10,'exchcard','detailedaddress'),(14,'exchcard','dianzan'),(9,'exchcard','profile'),(25,'exchcard','xuser'),(16,'oneverse','gcmregister'),(17,'oneverse','secret'),(15,'oneverse','verse'),(5,'sessions','session'),(6,'sites','site');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_migrations` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app` varchar(255) CHARACTER SET latin1 NOT NULL,
  `name` varchar(255) CHARACTER SET latin1 NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=32 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2016-11-02 06:48:05.602849'),(2,'auth','0001_initial','2016-11-02 06:48:05.836556'),(3,'admin','0001_initial','2016-11-02 06:48:05.894656'),(4,'contenttypes','0002_remove_content_type_name','2016-11-02 06:48:06.026943'),(5,'auth','0002_alter_permission_name_max_length','2016-11-02 06:48:06.059665'),(6,'auth','0003_alter_user_email_max_length','2016-11-02 06:48:06.100645'),(7,'auth','0004_alter_user_username_opts','2016-11-02 06:48:06.129791'),(8,'auth','0005_alter_user_last_login_null','2016-11-02 06:48:06.174777'),(9,'auth','0006_require_contenttypes_0002','2016-11-02 06:48:06.177073'),(10,'exchcard','0001_initial','2016-11-02 06:48:06.515741'),(11,'exchcard','0002_auto_20160313_0000','2016-11-02 06:48:06.706763'),(12,'exchcard','0004_auto_20160318_2315','2016-11-02 06:48:06.761330'),(13,'exchcard','0005_avatarphoto','2016-11-02 06:48:06.802318'),(14,'exchcard','0006_auto_20160529_2126','2016-11-02 06:48:07.031897'),(15,'oneverse','0001_initial','2016-11-02 06:48:07.056002'),(16,'oneverse','0002_auto_20160319_2314','2016-11-02 06:48:07.098156'),(17,'oneverse','0003_verse_push_date','2016-11-02 06:48:07.123751'),(18,'oneverse','0004_auto_20160319_2318','2016-11-02 06:48:07.151336'),(19,'oneverse','0005_auto_20160324_0932','2016-11-02 06:48:07.202107'),(20,'oneverse','0006_gcmregister','2016-11-02 06:48:07.229664'),(21,'oneverse','0007_serect','2016-11-02 06:48:07.255618'),(22,'sessions','0001_initial','2016-11-02 06:48:07.289588'),(23,'sites','0001_initial','2016-11-02 06:48:07.317098'),(24,'exchcard','0007_auto_20161102_1449','2016-11-02 06:51:10.146157'),(25,'oneverse','0008_auto_20161102_1449','2016-12-17 12:16:35.731529'),(26,'api-exchcard','0001_initial','2016-12-18 15:57:06.655886'),(27,'api-exchcard','0002_auto_20160313_0000','2016-12-18 15:57:06.839538'),(28,'api-exchcard','0004_auto_20160318_2315','2016-12-18 15:57:06.880940'),(29,'api-exchcard','0005_avatarphoto','2016-12-18 15:57:06.919664'),(30,'api-exchcard','0006_auto_20160529_2126','2016-12-18 15:57:07.128784'),(31,'api-exchcard','0007_auto_20161102_1449','2016-12-18 15:57:07.221522');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) CHARACTER SET latin1 NOT NULL,
  `session_data` longtext CHARACTER SET latin1 NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_de54fa62` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
INSERT INTO `django_session` VALUES ('011shu84sj5r6xxaixfoeaamc46uj4fg','NmM4YjM2NzQwMjBiNmZlOGFlODQ2N2NiZTUwZjgwMzAxNTc5ZjIxNDp7Il9hdXRoX3VzZXJfaGFzaCI6ImFlMDM5NGY0NDNlYWU2NjIyNzlhMTVkODkwOTczY2Y2ZjYwYmVkY2UiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCIsIl9hdXRoX3VzZXJfaWQiOiIxIn0=','2016-11-28 15:37:03.013301'),('3jjtq398tludmszotmo8r8mz4uicf4b6','YTkxODM0ZDFlYTBmZmQ5NTIxMzExNGE1NGQxZGJhMjVhMDVmMGJiNDp7Il9hdXRoX3VzZXJfaGFzaCI6ImI0OTc1NTgxZjk3NGQ4OWFjNTZkY2FjMGU5ZmM5Mjg1ZjliODhiNmQiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCIsIl9hdXRoX3VzZXJfaWQiOiIyMiJ9','2017-05-25 02:13:16.792940'),('4x6f6io7rd9n9qy344dzuwbem0zpin1r','ZDUxZmQ3MjMzNDRkZDQyYWVhM2RiMDllNmMwYWRkNzEwMDI3YThiZjp7Il9hdXRoX3VzZXJfaGFzaCI6ImYzNjQ3YWY3MDI4MmUyMjRmZDg5MWI5MjQzYzAwNzM5ZDI4MmEwMjkiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCIsIl9hdXRoX3VzZXJfaWQiOiI1In0=','2017-05-31 08:23:52.562371'),('5qcq1fv1f9p37ms9cpvez0j450jdxkxv','ODQyMjljNTYyNjU2ZmIwZWE3YmVkYWEwN2EzZjc2NjU4ZTk3Y2NlMDp7Il9hdXRoX3VzZXJfaGFzaCI6IjY1MWRhZjhjODg2NWM4YWU4MmI5ODU0ZGEyZWY5NDQwNGUzOWM0NzIiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCIsIl9hdXRoX3VzZXJfaWQiOiI3In0=','2017-01-25 12:15:28.307212'),('89likrsuhx01sk4koya5fq62qllkxl67','NmJkOTU3ZjRkM2M3Nzg0YzAwYjNkMjdjOGU3ZGQwNThmOWE5ZTkxMTp7Il9hdXRoX3VzZXJfaGFzaCI6IjMyOGFjYjg1ZjQxNDkyM2NkNzAwZjYzNzY1ZTNhM2ZjMjYwMGUxODEiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCIsIl9hdXRoX3VzZXJfaWQiOiIzIn0=','2017-06-23 02:58:31.630005'),('bp4063iussau8juld5zhur5ahbbcxoi6','ZjI3MjI3NzEzYWRkODdlYjgyYzJiYTYwNWU5MDU4NmFmMDdjY2YzOTp7Il9hdXRoX3VzZXJfaGFzaCI6IjlmMWNmYTkwYzk2ZjE5ODEzZmE3NTk2N2UyOWYzNzkwYTM0MzA1YjMiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCIsIl9hdXRoX3VzZXJfaWQiOiI0In0=','2017-05-31 08:16:43.730872'),('dlivk413yej9lc23r3uvamvaxfq3f97g','N2JiZTdkYTYzOGIzZWY4NGYwMjc5NmE4NmEyZDM0NzI0NjZkMGUxODp7Il9hdXRoX3VzZXJfaGFzaCI6ImI5MzA0NzE4YzYwN2ZmOGE2ZWU2YzA3NzllZWYyYjA1NGE5NDNlMzYiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCIsIl9hdXRoX3VzZXJfaWQiOiI3In0=','2017-05-31 08:32:10.730225'),('fqqterc7022d2kvirdc0madauyuocw4c','ZjI3MjI3NzEzYWRkODdlYjgyYzJiYTYwNWU5MDU4NmFmMDdjY2YzOTp7Il9hdXRoX3VzZXJfaGFzaCI6IjlmMWNmYTkwYzk2ZjE5ODEzZmE3NTk2N2UyOWYzNzkwYTM0MzA1YjMiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCIsIl9hdXRoX3VzZXJfaWQiOiI0In0=','2017-06-03 22:52:24.405178'),('lul6jg23gcbyl997bqzi5bp8m0yc648n','NmM4YjM2NzQwMjBiNmZlOGFlODQ2N2NiZTUwZjgwMzAxNTc5ZjIxNDp7Il9hdXRoX3VzZXJfaGFzaCI6ImFlMDM5NGY0NDNlYWU2NjIyNzlhMTVkODkwOTczY2Y2ZjYwYmVkY2UiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCIsIl9hdXRoX3VzZXJfaWQiOiIxIn0=','2016-11-17 13:38:15.133251'),('tb1c7wimjivaoyd3v4v476jismeutdbc','YzRiOTFlYzI4ZDM4MDE1OWFiZTg1OTM1YjZkNzU3MjBhZTMwN2QxZDp7Il9hdXRoX3VzZXJfaGFzaCI6IjNkZmUzZGFlZjNhZGYyYTM0MjRhOGYyZDE5NzAzOTg1MmI5NWEyNjEiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCIsIl9hdXRoX3VzZXJfaWQiOiI4In0=','2017-05-31 08:35:18.138822'),('uowfy1b8qkw5jx1fzkz7lyrqmqfbsw6z','NmUwOWQ1YTkzZjEyZGMyMjRjZjliMDk3NmJjMTkwMDhjODg4Mjg0YTp7Il9hdXRoX3VzZXJfaGFzaCI6ImM1YzJiZWRiNzJkMTE4MmMzOWRlMjEwMDg2Y2VkZWEyOTg5YjY5ZDUiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCIsIl9hdXRoX3VzZXJfaWQiOiI2In0=','2017-05-31 08:26:38.569109'),('yhj6l193dmohpi7uyua09aimrjx6h164','ZTU2NWI1MDI5ODY3YzBjY2MzZTAxOTQ1MzIwMGIyYjc2NTllZmRlYzp7Il9hdXRoX3VzZXJfaGFzaCI6IjM0ZWIwZGE2NTM1ZDQxYmU1NGNmNjM2MWFkMGY5ZDA3NzRlYWI1NmIiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCIsIl9hdXRoX3VzZXJfaWQiOiIyMCJ9','2017-05-24 03:42:24.071088');
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_site`
--

DROP TABLE IF EXISTS `django_site`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_site` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `domain` varchar(100) CHARACTER SET latin1 NOT NULL,
  `name` varchar(50) CHARACTER SET latin1 NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_site`
--

LOCK TABLES `django_site` WRITE;
/*!40000 ALTER TABLE `django_site` DISABLE KEYS */;
INSERT INTO `django_site` VALUES (1,'example.com','example.com');
/*!40000 ALTER TABLE `django_site` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `exchcard_activity`
--

DROP TABLE IF EXISTS `exchcard_activity`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `exchcard_activity` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `created` datetime(6) NOT NULL,
  `type` varchar(50) NOT NULL,
  `short_name` varchar(20) NOT NULL,
  `short_name_zh` varchar(20) DEFAULT NULL,
  `description` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `exchcard_activity`
--

LOCK TABLES `exchcard_activity` WRITE;
/*!40000 ALTER TABLE `exchcard_activity` DISABLE KEYS */;
/*!40000 ALTER TABLE `exchcard_activity` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `exchcard_address`
--

DROP TABLE IF EXISTS `exchcard_address`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `exchcard_address` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `created` datetime(6) NOT NULL,
  `name` varchar(255) NOT NULL,
  `address` varchar(255) NOT NULL,
  `postcode` varchar(100) NOT NULL,
  `city` varchar(50) DEFAULT NULL,
  `country` varchar(50) DEFAULT NULL,
  `full_text_address` varchar(510) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `exchcard_address`
--

LOCK TABLES `exchcard_address` WRITE;
/*!40000 ALTER TABLE `exchcard_address` DISABLE KEYS */;
INSERT INTO `exchcard_address` VALUES (1,'2017-05-17 07:25:26.763047','Zhang Guanghui','Saint Street 6, Chengdu, Sichuan, China','610254','Chengdu','China',NULL),(2,'2017-05-17 07:25:31.760204','zgh','I am address 6, Chengdu, China','610234','Chengdu','China',NULL),(3,'2017-05-17 07:38:10.686008','zgh','I am address 6, Chengdu, China','610234','Chengdu','China',NULL),(4,'2017-05-17 07:38:13.624791','zgh','I am address 6, Chengdu, China','610234','Chengdu','China',NULL),(5,'2017-05-17 08:56:48.516054','zgh7','address street 1, Chengdu, China','610234','Chengdu','China',NULL),(6,'2017-05-17 08:59:49.191151','zgh7','address street 1, Chengdu, China','610234','Chengdu','China',NULL),(7,'2017-05-17 09:12:17.566209','zgh8','address street 1, Chengdu, \nSichuan, China','610234','Chengdu','China',NULL),(8,'2017-05-18 23:10:47.066059','good man','Block 34#3-1, Angle Street 1, Chengdu, Sichuan, China','323455','Chengdu','China',NULL),(9,'2017-05-20 10:43:45.348977','zgh 2','street 2, cd, cn','789654','Chengdu','China',NULL),(10,'2017-05-20 11:35:09.449084','zgh3','Angle Street 1, Chengdu','431343','Chengdu','China',NULL),(11,'2017-05-21 01:29:22.668239','Admin','Admin Street 1, Chengdu, Sichuan','123311','Chengdu','China',NULL),(12,'2017-05-28 11:51:48.051898','ZGH 21','Agle Sre Street, Chengdu, SC','342674',NULL,NULL,NULL),(13,'2017-06-03 11:30:01.714924','zgh10','address street 1, Chengdu, China','610234',NULL,NULL,NULL);
/*!40000 ALTER TABLE `exchcard_address` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `exchcard_avatarphoto`
--

DROP TABLE IF EXISTS `exchcard_avatarphoto`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `exchcard_avatarphoto` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `created` datetime(6) NOT NULL,
  `avatar` varchar(100) NOT NULL,
  `owner_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `exchcard_avatarphoto_5e7b1936` (`owner_id`),
  CONSTRAINT `exchcard_avatar_owner_id_6b10e28c0d84e8a6_fk_exchcard_profile_id` FOREIGN KEY (`owner_id`) REFERENCES `exchcard_profile` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=28 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `exchcard_avatarphoto`
--

LOCK TABLES `exchcard_avatarphoto` WRITE;
/*!40000 ALTER TABLE `exchcard_avatarphoto` DISABLE KEYS */;
INSERT INTO `exchcard_avatarphoto` VALUES (19,'2017-05-22 10:07:45.924005','avatar_photos/2017-5-22-18-7-45-923540.jpg',8),(20,'2017-05-22 10:11:03.377414','avatar_photos/2017-5-22-18-11-3-376397.jpeg',8),(21,'2017-05-29 09:39:32.913615','avatar_photos/2017529173932913259.jpg',8),(22,'2017-05-29 09:39:37.207990','avatar_photos/2017529173937207218.jpg',8),(23,'2017-05-29 09:41:02.746164','avatar_photos/201752917412745730.jpg',8),(24,'2017-05-29 09:52:16.417856','avatar_photos/2017529175216417342.jpg',8),(25,'2017-05-29 09:52:33.395070','avatar_photos/2017529175233394583.jpeg',8),(26,'2017-05-29 09:58:13.504423','avatar_photos/2017529175813503998.jpeg',8),(27,'2017-05-29 09:58:35.947356','avatar_photos/2017529175835946812.jpg',8);
/*!40000 ALTER TABLE `exchcard_avatarphoto` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `exchcard_card`
--

DROP TABLE IF EXISTS `exchcard_card`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `exchcard_card` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `created` datetime(6) NOT NULL,
  `card_name` varchar(50) NOT NULL,
  `sent_time` bigint(20) NOT NULL,
  `sent_date` datetime(6) NOT NULL,
  `arrived_time` bigint(20) DEFAULT NULL,
  `arrived_date` datetime(6) DEFAULT NULL,
  `has_arrived` tinyint(1) NOT NULL,
  `fromsender_id` int(11) NOT NULL,
  `torecipient_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `exchcard_card_564ba11d` (`fromsender_id`),
  KEY `exchcard_card_e5b1566a` (`torecipient_id`),
  CONSTRAINT `exchcard_c_fromsender_id_69bb6e43d7211c69_fk_exchcard_profile_id` FOREIGN KEY (`fromsender_id`) REFERENCES `exchcard_profile` (`id`),
  CONSTRAINT `exchcard_c_torecipient_id_d811557eafd4a39_fk_exchcard_profile_id` FOREIGN KEY (`torecipient_id`) REFERENCES `exchcard_profile` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=102 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `exchcard_card`
--

LOCK TABLES `exchcard_card` WRITE;
/*!40000 ALTER TABLE `exchcard_card` DISABLE KEYS */;
INSERT INTO `exchcard_card` VALUES (1,'2017-05-17 09:15:49.955908','POST533984',1495011575685,'2017-05-17 09:15:49.956011',NULL,NULL,0,7,1),(2,'2017-05-17 09:16:05.366483','POST315216',1495011575685,'2017-05-17 09:16:05.366563',NULL,NULL,0,7,7),(3,'2017-05-19 00:22:55.043472','POST766200',1495153341902,'2017-05-19 00:22:55.043543',1495687717496,'2017-05-25 04:48:37.496316',1,7,8),(4,'2017-05-19 12:43:12.062340','POST602175',1495196834526,'2017-05-19 12:43:12.062420',1495504318887,'2017-05-23 01:51:58.887349',1,8,8),(5,'2017-05-21 11:34:22.812270','POST839156',1495365725093,'2017-05-21 11:34:22.812351',NULL,NULL,0,8,1),(6,'2017-05-22 16:14:51.245024','POST83688',1495469643820,'2017-05-22 16:14:51.245105',NULL,NULL,0,8,11),(7,'2017-05-23 01:52:16.339496','POST251687',1495494789509,'2017-05-23 01:52:16.339577',NULL,NULL,0,8,10),(8,'2017-05-23 01:52:48.791133','POST989403',1495494789509,'2017-05-23 01:52:48.791208',NULL,NULL,0,8,11),(9,'2017-05-23 01:52:54.631304','POST76808',1495494789509,'2017-05-23 01:52:54.631385',NULL,NULL,0,8,11),(10,'2017-05-23 01:52:59.691485','POST11038',1495494789509,'2017-05-23 01:52:59.691693',NULL,NULL,0,8,7),(11,'2017-05-23 01:53:08.651026','POST274547',1495494789509,'2017-05-23 01:53:08.651091',NULL,NULL,0,8,9),(12,'2017-05-26 02:48:56.092238','POST578848',1495766929529,'2017-05-26 02:48:56.092316',NULL,NULL,0,8,9),(13,'2017-05-26 02:50:24.021047','POST153393',1495767013430,'2017-05-26 02:50:24.021171',NULL,NULL,0,8,9),(14,'2017-05-26 02:59:47.365464','POST609901',1495767573954,'2017-05-26 02:59:47.365543',NULL,NULL,0,8,10),(15,'2017-05-26 03:01:09.672055','POST298325',1495767655066,'2017-05-26 03:01:09.672123',1496045046862,'2017-05-29 08:04:06.862262',1,8,8),(16,'2017-05-26 03:01:31.554289','POST983174',1495767655066,'2017-05-26 03:01:31.554355',NULL,NULL,0,8,7),(17,'2017-05-26 03:05:32.003137','POST965010',1495767655066,'2017-05-26 03:05:32.003213',NULL,NULL,0,8,5),(18,'2017-05-26 03:17:39.218498','POST857410',1495768064854,'2017-05-26 03:17:39.218577',1496047851089,'2017-05-29 08:50:51.088890',1,8,8),(19,'2017-05-26 03:28:11.247494','POST815857',1495768064854,'2017-05-26 03:28:11.247572',NULL,NULL,0,8,1),(20,'2017-05-26 03:30:05.579639','POST531538',1495768064854,'2017-05-26 03:30:05.579720',NULL,NULL,0,8,10),(21,'2017-05-26 03:32:37.733476','POST81082',1495768064854,'2017-05-26 03:32:37.733559',NULL,NULL,0,8,9),(22,'2017-05-26 04:59:08.773775','POST174857',1495768064854,'2017-05-26 04:59:08.773977',1496047999248,'2017-05-29 08:53:19.248088',1,8,8),(23,'2017-05-26 05:00:25.734419','POST707361',1495768064854,'2017-05-26 05:00:25.734600',NULL,NULL,0,8,10),(24,'2017-05-26 05:08:27.150853','POST844197',1495768064854,'2017-05-26 05:08:27.150931',NULL,NULL,0,8,5),(25,'2017-05-26 05:08:29.489913','POST306085',1495768064854,'2017-05-26 05:08:29.489990',NULL,NULL,0,8,1),(26,'2017-05-26 06:30:51.980142','POST647374',1495780233139,'2017-05-26 06:30:51.980314',1496048051221,'2017-05-29 08:54:11.221138',1,8,8),(27,'2017-05-26 06:31:28.881881','POST618822',1495780233139,'2017-05-26 06:31:28.881949',NULL,NULL,0,8,9),(28,'2017-05-26 06:31:42.438004','POST542312',1495780233139,'2017-05-26 06:31:42.438071',NULL,NULL,0,8,1),(29,'2017-05-26 06:33:59.999874','POST225862',1495780233139,'2017-05-26 06:33:59.999939',NULL,NULL,0,8,7),(30,'2017-05-26 06:35:16.353452','POST175683',1495780233139,'2017-05-26 06:35:16.353518',NULL,NULL,0,8,5),(31,'2017-05-26 06:39:10.458118','POST727387',1495780233139,'2017-05-26 06:39:10.458184',NULL,NULL,0,8,9),(32,'2017-05-26 06:39:15.218580','POST769593',1495780233139,'2017-05-26 06:39:15.218651',1496062233494,'2017-05-29 12:50:33.493672',1,8,8),(33,'2017-05-26 06:39:38.324693','POST929934',1495780233139,'2017-05-26 06:39:38.324759',1496217323111,'2017-05-31 07:55:23.111456',1,8,8),(34,'2017-05-26 06:45:12.713458','POST38523',1495780233139,'2017-05-26 06:45:12.713526',NULL,NULL,0,8,11),(35,'2017-05-26 06:45:44.143474','POST130317',1495780233139,'2017-05-26 06:45:44.143548',NULL,NULL,0,8,9),(36,'2017-05-26 06:46:41.384742','POST977174',1495780233139,'2017-05-26 06:46:41.384815',NULL,NULL,0,8,1),(37,'2017-05-26 06:48:26.067214','POST830876',1495780233139,'2017-05-26 06:48:26.067301',1496645791483,'2017-06-05 06:56:31.482827',1,8,8),(38,'2017-05-26 06:50:52.523307','POST364999',1495780233139,'2017-05-26 06:50:52.523383',NULL,NULL,0,8,5),(39,'2017-05-26 06:51:20.777819','POST728789',1495780233139,'2017-05-26 06:51:20.777882',NULL,NULL,0,8,7),(40,'2017-05-26 06:52:10.168513','POST1224',1495780233139,'2017-05-26 06:52:10.168596',1495938267351,'2017-05-28 02:24:27.350751',1,8,8),(41,'2017-05-27 13:20:14.660147','POST456123',1495891166762,'2017-05-27 13:20:14.660226',NULL,NULL,0,9,7),(42,'2017-05-27 13:27:24.336260','POST155405',1495891633979,'2017-05-27 13:27:24.336343',1496621325166,'2017-06-05 00:08:45.166243',1,9,8),(43,'2017-05-27 13:30:11.375203','POST584032',1495891802688,'2017-05-27 13:30:11.375292',NULL,NULL,0,9,9),(44,'2017-05-27 13:43:30.422395','POST911023',1495892601241,'2017-05-27 13:43:30.422486',1495938174908,'2017-05-28 02:22:54.907836',1,9,8),(45,'2017-05-27 13:44:49.813010','POST620053',1495892601241,'2017-05-27 13:44:49.813076',NULL,NULL,0,9,1),(46,'2017-05-27 13:44:55.515426','POST866364',1495892601241,'2017-05-27 13:44:55.515490',NULL,NULL,0,9,9),(47,'2017-05-28 00:52:21.749882','POST626976',1495932557552,'2017-05-28 00:52:21.749960',NULL,NULL,0,8,1),(48,'2017-05-28 00:53:54.894463','POST761253',1495932557552,'2017-05-28 00:53:54.894528',NULL,NULL,0,8,10),(49,'2017-05-28 00:54:28.251388','POST296779',1495932557552,'2017-05-28 00:54:28.251453',NULL,NULL,0,8,1),(50,'2017-05-28 01:24:52.000395','POST747109',1495932557552,'2017-05-28 01:24:52.000472',NULL,NULL,0,8,9),(51,'2017-05-28 01:28:04.156171','POST153908',1495932557552,'2017-05-28 01:28:04.156244',NULL,NULL,0,8,1),(52,'2017-05-28 01:28:54.416235','POST904781',1495932557552,'2017-05-28 01:28:54.416313',NULL,NULL,0,8,11),(53,'2017-05-28 01:31:38.353025','POST793683',1495932557552,'2017-05-28 01:31:38.353087',NULL,NULL,0,8,10),(54,'2017-05-28 01:38:39.654353','POST84415',1495935290809,'2017-05-28 01:38:39.654419',NULL,NULL,0,8,1),(55,'2017-05-28 02:05:36.669928','POST98783',1495936183620,'2017-05-28 02:05:36.670004',NULL,NULL,0,8,1),(56,'2017-05-29 00:23:41.673811','POST225921',1496016005267,'2017-05-29 00:23:41.673983',NULL,NULL,0,8,7),(57,'2017-05-31 07:35:29.887946','POST707620',1496215854031,'2017-05-31 07:35:29.888028',NULL,NULL,0,8,11),(58,'2017-06-04 23:53:02.098329','POST571610',1496620370770,'2017-06-04 23:53:02.098402',NULL,NULL,0,8,1),(59,'2017-06-04 23:56:05.907973','POST321121',1496620370770,'2017-06-04 23:56:05.908037',NULL,NULL,0,8,7),(60,'2017-06-05 06:54:01.902461','POST268737',1496645133690,'2017-06-05 06:54:01.902527',NULL,NULL,0,8,10),(61,'2017-06-05 06:59:56.608292','POST245967',1496645133690,'2017-06-05 06:59:56.608375',NULL,NULL,0,8,9),(62,'2017-06-05 07:00:01.600978','POST929800',1496645133690,'2017-06-05 07:00:01.601044',NULL,NULL,0,8,12),(63,'2017-06-05 07:00:06.013418','POST68491',1496645133690,'2017-06-05 07:00:06.013488',NULL,NULL,0,8,13),(64,'2017-06-05 07:00:10.095541','POST200841',1496645133690,'2017-06-05 07:00:10.095625',NULL,NULL,0,8,11),(65,'2017-06-05 07:00:14.517000','POST325015',1496645133690,'2017-06-05 07:00:14.517073',NULL,NULL,0,8,5),(66,'2017-06-05 07:00:19.127704','POST424936',1496645133690,'2017-06-05 07:00:19.127770',NULL,NULL,0,8,10),(67,'2017-06-05 07:00:23.561340','POST382838',1496645133690,'2017-06-05 07:00:23.561406',NULL,NULL,0,8,1),(68,'2017-06-05 07:00:29.230021','POST769543',1496645133690,'2017-06-05 07:00:29.230085',NULL,NULL,0,8,5),(69,'2017-06-05 07:01:44.449632','POST250652',1496646094089,'2017-06-05 07:01:44.449704',NULL,NULL,0,8,13),(70,'2017-06-05 07:01:53.195847','POST637197',1496646094089,'2017-06-05 07:01:53.196055',NULL,NULL,0,8,5),(71,'2017-06-05 07:02:48.528614','POST5561',1496646165758,'2017-06-05 07:02:48.528686',NULL,NULL,0,8,13),(72,'2017-06-05 07:02:57.125118','POST140432',1496646165758,'2017-06-05 07:02:57.125181',NULL,NULL,0,8,10),(73,'2017-06-05 07:03:08.015864','POST565783',1496646165758,'2017-06-05 07:03:08.015928',NULL,NULL,0,8,12),(74,'2017-06-05 07:03:19.308777','POST480421',1496646165758,'2017-06-05 07:03:19.308936',NULL,NULL,0,8,5),(75,'2017-06-05 07:03:51.858074','POST475277',1496646165758,'2017-06-05 07:03:51.858153',NULL,NULL,0,8,5),(76,'2017-06-05 07:06:43.194923','POST554029',1496646399245,'2017-06-05 07:06:43.195002',1496732321476,'2017-06-06 06:58:41.475744',1,8,8),(77,'2017-06-05 07:06:51.148585','POST198111',1496646399245,'2017-06-05 07:06:51.148652',1496732568574,'2017-06-06 07:02:48.573642',1,8,8),(78,'2017-06-05 07:06:57.877995','POST686014',1496646399245,'2017-06-05 07:06:57.878059',1496733253828,'2017-06-06 07:14:13.827900',1,8,8),(79,'2017-06-05 07:08:23.684742','POST792126',1496646470232,'2017-06-05 07:08:23.684829',1496646554525,'2017-06-05 07:09:14.524859',1,8,8),(80,'2017-06-05 08:01:08.842758','POST511468',1496649656455,'2017-06-05 08:01:08.842829',1496736207155,'2017-06-06 08:03:27.154983',1,8,8),(81,'2017-06-06 00:02:04.778733','POST603837',1496707316931,'2017-06-06 00:02:04.778802',1496736710461,'2017-06-06 08:11:50.460647',1,8,8),(82,'2017-06-06 00:02:37.712298','POST603837',1496707354782,'2017-06-06 00:02:37.712365',NULL,NULL,0,8,8),(83,'2017-06-06 00:10:35.306693','POST603837',1496707699689,'2017-06-06 00:10:35.306779',NULL,NULL,0,8,8),(84,'2017-06-06 00:12:11.416457','POST777678',1496707920316,'2017-06-06 00:12:11.416538',NULL,NULL,0,8,8),(85,'2017-06-06 00:19:23.463958','POST428746',1496707920316,'2017-06-06 00:19:23.464027',NULL,NULL,0,8,8),(86,'2017-06-06 00:25:06.822277','POST237183',1496708510385,'2017-06-06 00:25:06.822348',NULL,NULL,0,8,8),(87,'2017-06-06 00:42:51.989679','POST533596',1496709755080,'2017-06-06 00:42:51.989753',1496737123940,'2017-06-06 08:18:43.939844',1,8,8),(88,'2017-06-06 00:43:17.726174','POST533596',1496709755080,'2017-06-06 00:43:17.726257',NULL,NULL,0,8,8),(89,'2017-06-06 00:48:59.775966','POST533596',1496710010579,'2017-06-06 00:48:59.776074',NULL,NULL,0,8,8),(90,'2017-06-06 00:53:30.095372','POST533596',1496710399476,'2017-06-06 00:53:30.095446',NULL,NULL,0,8,8),(91,'2017-06-06 00:53:41.581096','POST533596',1496710399476,'2017-06-06 00:53:41.581176',NULL,NULL,0,8,8),(92,'2017-06-06 01:00:52.339907','POST533596',1496710805394,'2017-06-06 01:00:52.339984',NULL,NULL,0,8,8),(93,'2017-06-06 01:02:07.286979','POST533596',1496710805394,'2017-06-06 01:02:07.287051',NULL,NULL,0,8,8),(94,'2017-06-06 01:06:28.136541','POST233180',1496711138674,'2017-06-06 01:06:28.136619',NULL,NULL,0,8,8),(95,'2017-06-06 01:06:48.933009','POST233180',1496711138674,'2017-06-06 01:06:48.933078',NULL,NULL,0,8,8),(96,'2017-06-06 03:58:53.541965','POST546154',1496719718873,'2017-06-06 03:58:53.542040',NULL,NULL,0,8,8),(97,'2017-06-08 03:52:28.782587','POST620810',1496893790593,'2017-06-08 03:52:28.782831',1496894190121,'2017-06-08 03:56:30.120694',1,8,8),(98,'2017-06-08 05:32:22.715940','POST967213',1496899492279,'2017-06-08 05:32:22.716055',1496899997110,'2017-06-08 05:33:17.110259',1,8,8),(99,'2017-06-08 06:30:23.982655','POST471087',1496902441108,'2017-06-08 06:30:23.982860',1496903464585,'2017-06-08 06:31:04.585328',1,9,9),(100,'2017-06-08 06:32:51.833332','POST701446',1496903558928,'2017-06-08 06:32:51.833412',1496903976876,'2017-06-08 06:39:36.875879',1,9,1),(101,'2017-06-09 02:54:09.830441','POST182579',1496974977287,'2017-06-09 02:54:09.830509',1496976994651,'2017-06-09 02:56:34.651232',1,1,11);
/*!40000 ALTER TABLE `exchcard_card` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `exchcard_cardphoto`
--

DROP TABLE IF EXISTS `exchcard_cardphoto`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `exchcard_cardphoto` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `created` datetime(6) NOT NULL,
  `card_photo` varchar(100) NOT NULL,
  `card_host_id` int(11) NOT NULL,
  `owner_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `exchcard_cardp_card_host_id_53e64ae6cf14215b_fk_exchcard_card_id` (`card_host_id`),
  KEY `exchcard_cardphoto_5e7b1936` (`owner_id`),
  CONSTRAINT `exchcard_cardp_card_host_id_53e64ae6cf14215b_fk_exchcard_card_id` FOREIGN KEY (`card_host_id`) REFERENCES `exchcard_card` (`id`),
  CONSTRAINT `exchcard_cardph_owner_id_7c71dbd9c4f8ca93_fk_exchcard_profile_id` FOREIGN KEY (`owner_id`) REFERENCES `exchcard_profile` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=64 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `exchcard_cardphoto`
--

LOCK TABLES `exchcard_cardphoto` WRITE;
/*!40000 ALTER TABLE `exchcard_cardphoto` DISABLE KEYS */;
INSERT INTO `exchcard_cardphoto` VALUES (1,'2017-05-23 02:01:31.430397','C:\\fakepath\\4106444347.jpg',3,8),(2,'2017-05-29 05:21:47.085594','C:\\fakepath\\4106444347.jpg',15,8),(3,'2017-05-29 07:49:01.158179','C:\\fakepath\\4106444347.jpg',15,8),(4,'2017-05-29 08:54:11.239104','C:\\fakepath\\4106444347.jpg',26,8),(5,'2017-05-29 09:34:42.186498','C:\\fakepath\\4106444347.jpg',5,8),(6,'2017-05-29 09:37:43.481196','C:\\fakepath\\4106444347的副本 2.jpg',5,8),(7,'2017-05-29 11:06:36.049520','card_photos/4106444347的副本_3.jpg',5,8),(8,'2017-05-29 11:18:23.688338','card_photos/2017529191823679827.jpg',5,8),(9,'2017-05-29 12:02:33.815311','card_photos/201752920233806614.jpg',5,8),(10,'2017-05-29 12:03:23.678809','card_photos/201752920323673933.jpg',5,8),(11,'2017-05-29 12:03:54.566014','card_photos/201752920354561299.jpg',5,8),(12,'2017-05-29 12:25:49.648254','card_photos/2017529202549642346.jpg',5,8),(13,'2017-05-29 12:50:33.510140','card_photos/2017529205033491729.jpg',32,8),(14,'2017-05-31 07:35:52.535428','card_photos/2017531153552531433.jpg',57,8),(15,'2017-05-31 07:55:23.126328','card_photos/2017531155523109381.jpg',33,8),(16,'2017-06-04 13:42:22.515376','card_photos/201764214222511970.jpg',4,8),(17,'2017-06-05 00:24:46.102227','card_photos/2017658244698625.jpeg',3,8),(18,'2017-06-05 00:25:20.189285','card_photos/20176582520186123.jpeg',4,8),(19,'2017-06-05 02:10:34.653080','card_photos/201765101034648707.jpeg',5,8),(20,'2017-06-06 00:42:52.002036','card_photos/20176684251989112.jpeg',87,8),(21,'2017-06-06 00:43:17.739063','card_photos/20176684317725727.jpeg',88,8),(22,'2017-06-06 00:48:59.783356','card_photos/20176684859775218.jpeg',89,8),(23,'2017-06-06 00:53:30.109629','card_photos/2017668533094815.jpeg',90,8),(24,'2017-06-06 01:02:07.301105','card_photos/201766927286597.jpeg',93,8),(25,'2017-06-06 01:06:48.945213','card_photos/2017669648932549.jpeg',95,8),(26,'2017-06-06 04:13:15.924319','card_photos/201766121315919591.jpeg',96,8),(27,'2017-06-06 04:13:36.415433','card_photos/201766121336409903.jpeg',96,8),(28,'2017-06-06 04:15:03.611551','card_photos/20176612153605404.jpeg',96,8),(29,'2017-06-06 04:15:26.092020','card_photos/20176612152686127.jpeg',96,8),(30,'2017-06-06 05:43:14.531549','card_photos/201766134314526698.jpeg',96,8),(31,'2017-06-06 05:56:53.423435','card_photos/201766135653420606.jpeg',96,8),(32,'2017-06-06 05:58:19.767240','card_photos/201766135819763144.jpeg',5,8),(33,'2017-06-06 05:58:23.557803','card_photos/201766135823553495.jpeg',5,8),(34,'2017-06-06 07:02:48.586565','card_photos/20176615248571768.jpeg',77,8),(35,'2017-06-06 07:03:32.243466','card_photos/20176615332241201.jpeg',77,8),(36,'2017-06-06 07:13:46.523217','card_photos/201766151346520717.jpeg',78,8),(37,'2017-06-06 07:14:13.843049','card_photos/201766151413826067.jpeg',78,8),(38,'2017-06-06 08:11:50.476498','card_photos/201766161150456140.jpeg',81,8),(39,'2017-06-06 08:18:43.961238','card_photos/201766161843936523.jpeg',87,8),(40,'2017-06-06 08:52:44.474980','card_photos/201766165244472462.jpeg',4,8),(41,'2017-06-06 08:53:58.820650','card_photos/201766165358814648.jpeg',4,8),(42,'2017-06-06 08:56:13.879808','card_photos/201766165613877503.jpeg',4,8),(43,'2017-06-06 08:56:22.000714','card_photos/201766165621998133.jpeg',4,8),(44,'2017-06-06 08:56:54.289245','card_photos/201766165654287365.jpg',4,8),(45,'2017-06-06 08:58:05.625715','card_photos/20176616585623561.png',4,8),(46,'2017-06-06 08:59:37.335301','card_photos/201766165937332767.jpeg',4,8),(47,'2017-06-08 03:52:28.788491','card_photos/201768115228779089.jpeg',97,8),(48,'2017-06-08 03:52:43.158125','card_photos/201768115243155856.jpeg',97,8),(49,'2017-06-08 03:53:08.087347','card_photos/2017681153885069.jpeg',97,8),(50,'2017-06-08 03:56:30.121239','card_photos/201768115630117909.jpeg',97,8),(51,'2017-06-08 05:32:34.562829','card_photos/201768133234560756.jpeg',98,8),(52,'2017-06-08 05:32:58.761697','card_photos/201768133258759797.jpeg',98,8),(53,'2017-06-08 05:33:17.110644','card_photos/201768133317108245.jpeg',98,8),(54,'2017-06-08 06:30:23.994779','card_photos/201768143023980455.jpeg',99,9),(55,'2017-06-08 06:31:12.739873','card_photos/201768143112737739.jpeg',99,9),(56,'2017-06-08 06:33:04.667157','card_photos/20176814334664349.jpeg',100,9),(57,'2017-06-08 06:35:21.398312','card_photos/201768143521395505.jpeg',100,9),(58,'2017-06-08 06:35:34.900991','card_photos/201768143534898332.jpeg',100,9),(59,'2017-06-08 06:37:09.619799','card_photos/20176814379616838.jpeg',100,9),(60,'2017-06-08 06:39:36.876261','card_photos/201768143936873759.jpeg',100,1),(61,'2017-06-09 02:54:09.843612','card_photos/20176910549828639.jpeg',101,1),(62,'2017-06-09 02:54:38.493013','card_photos/201769105438490242.jpeg',101,1),(63,'2017-06-09 02:56:34.651769','card_photos/201769105634649088.jpeg',101,11);
/*!40000 ALTER TABLE `exchcard_cardphoto` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `exchcard_detailedaddress`
--

DROP TABLE IF EXISTS `exchcard_detailedaddress`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `exchcard_detailedaddress` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `address_first_line` varchar(255) NOT NULL,
  `address_second_line` varchar(255) NOT NULL,
  `address_third_line` varchar(255) NOT NULL,
  `city` varchar(255) NOT NULL,
  `state_province` varchar(255) NOT NULL,
  `country` varchar(255) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `exchcard_detailedaddress`
--

LOCK TABLES `exchcard_detailedaddress` WRITE;
/*!40000 ALTER TABLE `exchcard_detailedaddress` DISABLE KEYS */;
/*!40000 ALTER TABLE `exchcard_detailedaddress` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `exchcard_dianzan`
--

DROP TABLE IF EXISTS `exchcard_dianzan`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `exchcard_dianzan` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `created` datetime(6) NOT NULL,
  `card_by_dianzan_id` int(11) NOT NULL,
  `card_photo_by_dianzan_id` int(11) NOT NULL,
  `person_who_dianzan_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `exchcard_card_by_dianzan_id_1f57f52b314706b1_fk_exchcard_card_id` (`card_by_dianzan_id`),
  KEY `D04645c90040d9c736e9c1fdc8241898` (`card_photo_by_dianzan_id`),
  KEY `exchcard_dianzan_e4524cb6` (`person_who_dianzan_id`),
  CONSTRAINT `D04645c90040d9c736e9c1fdc8241898` FOREIGN KEY (`card_photo_by_dianzan_id`) REFERENCES `exchcard_cardphoto` (`id`),
  CONSTRAINT `ex_person_who_dianzan_id_703bfc829fc16eb6_fk_exchcard_profile_id` FOREIGN KEY (`person_who_dianzan_id`) REFERENCES `exchcard_xuser` (`id`),
  CONSTRAINT `exchcard_card_by_dianzan_id_1f57f52b314706b1_fk_exchcard_card_id` FOREIGN KEY (`card_by_dianzan_id`) REFERENCES `exchcard_card` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `exchcard_dianzan`
--

LOCK TABLES `exchcard_dianzan` WRITE;
/*!40000 ALTER TABLE `exchcard_dianzan` DISABLE KEYS */;
/*!40000 ALTER TABLE `exchcard_dianzan` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `exchcard_follow`
--

DROP TABLE IF EXISTS `exchcard_follow`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `exchcard_follow` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `created` datetime(6) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `user_being_followed_id` int(11) NOT NULL,
  `subject_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `e_object_being_followed_id_143863d6387f51f4_fk_exchcard_xuser_id` (`user_being_followed_id`),
  KEY `exchcard_follow_subject_id_3f171fce9dd50bd6_fk_exchcard_xuser_id` (`subject_id`),
  CONSTRAINT `e_object_being_followed_id_143863d6387f51f4_fk_exchcard_xuser_id` FOREIGN KEY (`user_being_followed_id`) REFERENCES `exchcard_xuser` (`id`),
  CONSTRAINT `exchcard_follow_subject_id_3f171fce9dd50bd6_fk_exchcard_xuser_id` FOREIGN KEY (`subject_id`) REFERENCES `exchcard_xuser` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `exchcard_follow`
--

LOCK TABLES `exchcard_follow` WRITE;
/*!40000 ALTER TABLE `exchcard_follow` DISABLE KEYS */;
INSERT INTO `exchcard_follow` VALUES (1,'2017-06-04 06:04:36.426846',1,3,4),(2,'2017-06-04 06:07:46.395439',1,3,4),(3,'2017-06-04 06:11:33.599384',1,3,4),(4,'2017-06-04 06:12:44.542817',1,3,4),(5,'2017-06-04 06:12:51.498741',1,3,4),(6,'2017-06-04 06:17:49.439546',1,3,4),(7,'2017-06-04 06:21:20.911623',1,3,4),(8,'2017-06-04 06:21:22.350894',1,3,4),(9,'2017-06-04 07:25:39.242622',1,11,4),(10,'2017-06-04 07:25:58.266814',1,10,4),(11,'2017-06-04 07:32:49.443787',1,12,4),(12,'2017-06-04 07:50:05.889746',1,4,4),(13,'2017-06-04 13:45:05.668607',1,6,4),(14,'2017-06-08 06:31:27.970791',1,4,5),(15,'2017-06-08 06:31:36.756104',1,10,5),(16,'2017-06-08 06:31:45.397218',1,11,5),(17,'2017-06-08 06:41:46.778038',1,5,3),(18,'2017-06-08 06:42:01.210747',1,4,3),(19,'2017-06-08 06:43:05.874401',1,3,5),(20,'2017-06-09 02:57:39.967580',1,3,12);
/*!40000 ALTER TABLE `exchcard_follow` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `exchcard_profile`
--

DROP TABLE IF EXISTS `exchcard_profile`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `exchcard_profile` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `created` datetime(6) NOT NULL,
  `profileaddress_id` int(11) NOT NULL,
  `profileuser_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `profileuser_id` (`profileuser_id`),
  UNIQUE KEY `profileaddress_id` (`profileaddress_id`),
  CONSTRAINT `exchca_profileaddress_id_64fb2886ce9ece4b_fk_exchcard_address_id` FOREIGN KEY (`profileaddress_id`) REFERENCES `exchcard_address` (`id`),
  CONSTRAINT `exchcard_profile_profileuser_id_3bbe5e47f6c89845_fk_xuser_id` FOREIGN KEY (`profileuser_id`) REFERENCES `exchcard_xuser` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `exchcard_profile`
--

LOCK TABLES `exchcard_profile` WRITE;
/*!40000 ALTER TABLE `exchcard_profile` DISABLE KEYS */;
INSERT INTO `exchcard_profile` VALUES (1,'2017-05-17 07:25:26.777439',1,3),(5,'2017-05-17 08:56:48.531037',5,10),(7,'2017-05-17 09:12:17.579037',7,11),(8,'2017-05-18 23:10:47.080993',8,4),(9,'2017-05-20 10:43:45.361782',9,5),(10,'2017-05-20 11:35:09.460219',10,6),(11,'2017-05-21 01:29:22.671033',11,12),(12,'2017-05-28 11:51:48.064490',12,13),(13,'2017-06-03 11:30:01.727322',13,2);
/*!40000 ALTER TABLE `exchcard_profile` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `exchcard_receivecardaction`
--

DROP TABLE IF EXISTS `exchcard_receivecardaction`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `exchcard_receivecardaction` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `created` datetime(6) NOT NULL,
  `card_received_id` int(11) NOT NULL,
  `subject_id` int(11) NOT NULL,
  `has_photo` tinyint(1) NOT NULL,
  `card_received_photo_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `card_received_id` (`card_received_id`),
  UNIQUE KEY `card_received_photo_id` (`card_received_photo_id`),
  KEY `exchcard_receiv_subject_id_656acba83f66ad75_fk_exchcard_xuser_id` (`subject_id`),
  CONSTRAINT `a2e5b04d5445fc324d44deb130f9d490` FOREIGN KEY (`card_received_photo_id`) REFERENCES `exchcard_cardphoto` (`id`),
  CONSTRAINT `exchcard_r_card_received_id_34f8b03aa87e8bd7_fk_exchcard_card_id` FOREIGN KEY (`card_received_id`) REFERENCES `exchcard_card` (`id`),
  CONSTRAINT `exchcard_receiv_subject_id_656acba83f66ad75_fk_exchcard_xuser_id` FOREIGN KEY (`subject_id`) REFERENCES `exchcard_xuser` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=23 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `exchcard_receivecardaction`
--

LOCK TABLES `exchcard_receivecardaction` WRITE;
/*!40000 ALTER TABLE `exchcard_receivecardaction` DISABLE KEYS */;
INSERT INTO `exchcard_receivecardaction` VALUES (1,'2017-05-28 02:22:54.909159',44,4,0,NULL),(2,'2017-05-28 02:24:27.353531',40,4,0,NULL),(3,'2017-05-29 08:04:06.864302',15,4,0,NULL),(4,'2017-05-29 08:50:51.091543',18,4,0,NULL),(5,'2017-05-29 08:53:19.250479',22,4,0,NULL),(6,'2017-05-29 08:54:11.225540',26,4,0,NULL),(7,'2017-05-29 12:50:33.495153',32,4,0,NULL),(8,'2017-05-31 07:55:23.112844',33,4,0,NULL),(9,'2017-06-05 00:08:45.168645',42,4,0,NULL),(10,'2017-06-05 06:56:31.484227',37,4,0,NULL),(11,'2017-06-05 07:09:14.526521',79,4,0,NULL),(12,'2017-06-06 06:58:41.477045',76,4,0,NULL),(13,'2017-06-06 07:02:48.575330',77,4,0,NULL),(14,'2017-06-06 07:14:13.829412',78,4,0,NULL),(15,'2017-06-06 08:03:27.156326',80,4,0,NULL),(16,'2017-06-06 08:11:50.462150',81,4,1,NULL),(17,'2017-06-06 08:18:43.942252',87,4,1,NULL),(18,'2017-06-08 03:56:30.132331',97,4,1,50),(19,'2017-06-08 05:33:17.122005',98,4,1,53),(20,'2017-06-08 06:31:04.586736',99,5,0,NULL),(21,'2017-06-08 06:39:36.887242',100,3,1,60),(22,'2017-06-09 02:56:34.664617',101,12,1,63);
/*!40000 ALTER TABLE `exchcard_receivecardaction` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `exchcard_sentcardaction`
--

DROP TABLE IF EXISTS `exchcard_sentcardaction`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `exchcard_sentcardaction` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `created` datetime(6) NOT NULL,
  `card_sent_id` int(11) NOT NULL,
  `subject_id` int(11) NOT NULL,
  `has_photo` tinyint(1) NOT NULL,
  `card_sent_photo_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `card_sent_id` (`card_sent_id`),
  UNIQUE KEY `card_sent_photo_id` (`card_sent_photo_id`),
  CONSTRAINT `exc_card_sent_photo_id_123e235a97864e49_fk_exchcard_cardphoto_id` FOREIGN KEY (`card_sent_photo_id`) REFERENCES `exchcard_cardphoto` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=85 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `exchcard_sentcardaction`
--

LOCK TABLES `exchcard_sentcardaction` WRITE;
/*!40000 ALTER TABLE `exchcard_sentcardaction` DISABLE KEYS */;
INSERT INTO `exchcard_sentcardaction` VALUES (1,'2017-05-26 02:59:47.377354',14,4,0,NULL),(2,'2017-05-26 03:01:09.685057',15,4,0,NULL),(3,'2017-05-26 03:01:31.567740',16,4,0,NULL),(4,'2017-05-26 03:05:32.014387',17,4,0,NULL),(5,'2017-05-26 03:17:39.230401',18,4,0,NULL),(6,'2017-05-26 03:28:11.259461',19,4,0,NULL),(7,'2017-05-26 03:30:05.592437',20,4,0,NULL),(8,'2017-05-26 03:32:37.744520',21,4,0,NULL),(9,'2017-05-26 04:59:08.787490',22,4,0,NULL),(10,'2017-05-26 05:00:25.747340',23,4,0,NULL),(11,'2017-05-26 05:08:27.164311',24,4,0,NULL),(12,'2017-05-26 05:08:29.501961',25,4,0,NULL),(13,'2017-05-26 06:30:51.994237',26,4,0,NULL),(14,'2017-05-26 06:31:28.894544',27,4,0,NULL),(15,'2017-05-26 06:31:42.451081',28,4,0,NULL),(16,'2017-05-26 06:34:00.011750',29,4,0,NULL),(17,'2017-05-26 06:35:16.364972',30,4,0,NULL),(18,'2017-05-26 06:39:10.470809',31,4,0,NULL),(19,'2017-05-26 06:39:15.231823',32,4,0,NULL),(20,'2017-05-26 06:39:38.336770',33,4,0,NULL),(21,'2017-05-26 06:45:12.725046',34,4,0,NULL),(22,'2017-05-26 06:45:44.157752',35,4,0,NULL),(23,'2017-05-26 06:46:41.396796',36,4,0,NULL),(24,'2017-05-26 06:48:26.080977',37,4,0,NULL),(25,'2017-05-26 06:50:52.534897',38,4,0,NULL),(26,'2017-05-26 06:51:20.789762',39,4,0,NULL),(27,'2017-05-26 06:52:10.181719',40,4,0,NULL),(28,'2017-05-27 13:43:30.435716',44,5,0,NULL),(29,'2017-05-27 13:44:49.824575',45,5,0,NULL),(30,'2017-05-27 13:44:55.526516',46,5,0,NULL),(31,'2017-05-28 00:52:21.758950',47,4,0,NULL),(32,'2017-05-28 00:53:54.906107',48,4,0,NULL),(33,'2017-05-28 00:54:28.263996',49,4,0,NULL),(34,'2017-05-28 01:24:52.013222',50,4,0,NULL),(35,'2017-05-28 01:28:04.167585',51,4,0,NULL),(36,'2017-05-28 01:28:54.429154',52,4,0,NULL),(37,'2017-05-28 01:31:38.364495',53,4,0,NULL),(38,'2017-05-28 01:38:39.666323',54,4,0,NULL),(39,'2017-05-28 02:05:36.682047',55,4,0,NULL),(40,'2017-05-29 00:23:41.677420',56,4,0,NULL),(41,'2017-05-31 07:35:29.891786',57,4,0,NULL),(42,'2017-06-04 23:53:02.121967',58,4,0,NULL),(43,'2017-06-04 23:56:05.919435',59,4,0,NULL),(44,'2017-06-05 06:54:01.914134',60,4,0,NULL),(45,'2017-06-05 06:59:56.621515',61,4,0,NULL),(46,'2017-06-05 07:00:01.611855',62,4,0,NULL),(47,'2017-06-05 07:00:06.025170',63,4,0,NULL),(48,'2017-06-05 07:00:10.098738',64,4,0,NULL),(49,'2017-06-05 07:00:14.530134',65,4,0,NULL),(50,'2017-06-05 07:00:19.139276',66,4,0,NULL),(51,'2017-06-05 07:00:23.572108',67,4,0,NULL),(52,'2017-06-05 07:00:29.241840',68,4,0,NULL),(53,'2017-06-05 07:01:44.461196',69,4,0,NULL),(54,'2017-06-05 07:01:53.209832',70,4,0,NULL),(55,'2017-06-05 07:02:48.541704',71,4,0,NULL),(56,'2017-06-05 07:02:57.136494',72,4,0,NULL),(57,'2017-06-05 07:03:08.027010',73,4,0,NULL),(58,'2017-06-05 07:03:19.319631',74,4,0,NULL),(59,'2017-06-05 07:03:51.869097',75,4,0,NULL),(60,'2017-06-05 07:06:43.228913',76,4,0,NULL),(61,'2017-06-05 07:06:51.160060',77,4,0,NULL),(62,'2017-06-05 07:06:57.891450',78,4,0,NULL),(63,'2017-06-05 07:08:23.698477',79,4,0,NULL),(64,'2017-06-05 08:01:08.853897',80,4,0,NULL),(65,'2017-06-06 00:02:37.723057',82,4,0,NULL),(66,'2017-06-06 00:10:35.310024',83,4,0,NULL),(67,'2017-06-06 00:12:11.430117',84,4,0,NULL),(68,'2017-06-06 00:19:23.475783',85,4,0,NULL),(69,'2017-06-06 00:25:06.834275',86,4,0,NULL),(70,'2017-06-06 00:42:52.000765',87,4,1,NULL),(71,'2017-06-06 00:43:17.737782',88,4,1,NULL),(72,'2017-06-06 00:48:59.780769',89,4,1,NULL),(73,'2017-06-06 00:53:30.108311',90,4,1,NULL),(74,'2017-06-06 00:53:41.591924',91,4,0,NULL),(75,'2017-06-06 01:00:52.343537',92,4,0,NULL),(76,'2017-06-06 01:02:07.299753',93,4,1,NULL),(77,'2017-06-06 01:06:28.148982',94,4,0,NULL),(78,'2017-06-06 01:06:48.944031',95,4,1,NULL),(79,'2017-06-06 03:58:53.557159',96,4,0,NULL),(80,'2017-06-08 03:52:28.792198',97,4,1,47),(81,'2017-06-08 05:32:22.728417',98,4,0,NULL),(82,'2017-06-08 06:30:23.999850',99,5,1,54),(83,'2017-06-08 06:32:51.846621',100,5,0,NULL),(84,'2017-06-09 02:54:09.852681',101,3,1,61);
/*!40000 ALTER TABLE `exchcard_sentcardaction` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `exchcard_uploadcardphotoaction`
--

DROP TABLE IF EXISTS `exchcard_uploadcardphotoaction`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `exchcard_uploadcardphotoaction` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `created` datetime(6) NOT NULL,
  `card_actioned_id` int(11) NOT NULL,
  `subject_id` int(11) NOT NULL,
  `card_photo_uploaded_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `card_photo_uploaded_id` (`card_photo_uploaded_id`),
  KEY `exchcard_uploa_card_host_id_317f0fa94a505eb4_fk_exchcard_card_id` (`card_actioned_id`),
  KEY `exchcard_upload_subject_id_621796ad83b6417b_fk_exchcard_xuser_id` (`subject_id`),
  CONSTRAINT `e_card_photo_uploaded_id_9a76a4683f8699_fk_exchcard_cardphoto_id` FOREIGN KEY (`card_photo_uploaded_id`) REFERENCES `exchcard_cardphoto` (`id`),
  CONSTRAINT `exchcard_uploa_card_host_id_317f0fa94a505eb4_fk_exchcard_card_id` FOREIGN KEY (`card_actioned_id`) REFERENCES `exchcard_card` (`id`),
  CONSTRAINT `exchcard_upload_subject_id_621796ad83b6417b_fk_exchcard_xuser_id` FOREIGN KEY (`subject_id`) REFERENCES `exchcard_xuser` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `exchcard_uploadcardphotoaction`
--

LOCK TABLES `exchcard_uploadcardphotoaction` WRITE;
/*!40000 ALTER TABLE `exchcard_uploadcardphotoaction` DISABLE KEYS */;
INSERT INTO `exchcard_uploadcardphotoaction` VALUES (1,'2017-06-06 08:53:58.833146',4,4,5),(2,'2017-06-06 08:56:13.889913',4,4,3),(3,'2017-06-06 08:56:22.010504',4,4,4),(7,'2017-06-08 03:52:43.160681',97,4,48),(8,'2017-06-08 03:53:08.096964',97,4,49),(9,'2017-06-08 05:32:34.572736',98,4,51),(10,'2017-06-08 05:32:58.771546',98,4,52),(11,'2017-06-08 06:31:12.749487',99,5,55),(12,'2017-06-08 06:33:04.676650',100,5,56),(13,'2017-06-08 06:35:21.407904',100,5,57),(14,'2017-06-08 06:35:34.910870',100,5,58),(15,'2017-06-08 06:37:09.629015',100,5,59),(16,'2017-06-09 02:54:38.503184',101,3,62);
/*!40000 ALTER TABLE `exchcard_uploadcardphotoaction` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `exchcard_xuser`
--

DROP TABLE IF EXISTS `exchcard_xuser`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `exchcard_xuser` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `email` varchar(255) NOT NULL,
  `username` varchar(50) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `is_admin` tinyint(1) NOT NULL,
  `type` int(11) NOT NULL,
  `sex` int(11) DEFAULT NULL,
  `weibo_uid` varchar(50) DEFAULT NULL,
  `weibo_access_token` varchar(100) DEFAULT NULL,
  `url` varchar(200) DEFAULT NULL,
  `desc` varchar(2000) DEFAULT NULL,
  `avatar` varchar(500) DEFAULT NULL,
  `created` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `exchcard_xuser`
--

LOCK TABLES `exchcard_xuser` WRITE;
/*!40000 ALTER TABLE `exchcard_xuser` DISABLE KEYS */;
INSERT INTO `exchcard_xuser` VALUES (1,'pbkdf2_sha256$20000$wI7AIT5mURE0$NpjddA8jPDT3WJmtrk0TsJe8ejpYZdAVDeXfIX8VjuQ=',NULL,'zgh9@126.com','dotgh9at126.com',1,0,0,1,NULL,NULL,NULL,NULL,NULL,'2017-05-17 06:09:31.775465'),(2,'pbkdf2_sha256$20000$yb3T20KHLU7y$nhj8dEU17ZFWhOeb8eeQcQOneoO83lpQtc81EbcWDJM=','2017-06-03 11:26:39.579215','zgh10@126.com','dotgh10at126.com',1,0,0,1,NULL,NULL,NULL,NULL,NULL,'2017-05-17 06:12:21.712708'),(3,'pbkdf2_sha256$20000$G5lxSM7EVDSI$4joBDrq00x5v3ZN0K+PjahPup+GBgobrw7jRdcghoR8=','2017-06-09 02:58:31.627960','zgh11@126.com','dotgh11at126.com',1,0,0,1,NULL,NULL,NULL,NULL,NULL,'2017-05-17 06:37:38.758611'),(4,'pbkdf2_sha256$20000$EqPL9EevkllY$JceIAg9NKy8Lr1RjtcOkTGo/v0RwgHRxTA2s+mmCaE0=','2017-06-09 02:27:24.115257','zgh1@126.com','zgh44466adot',1,0,0,1,NULL,NULL,NULL,NULL,NULL,'2017-05-17 08:16:40.459051'),(5,'pbkdf2_sha256$20000$KefnqWBdvPZV$KDGWH8QmUCLbiKUJnKTr4ObZ6DfxS2tFWKGaMUzbhpM=','2017-06-08 06:40:28.643664','zgh2@126.com','zgh2at126dotcom',1,0,0,1,NULL,NULL,NULL,NULL,NULL,'2017-05-17 08:23:49.199432'),(6,'pbkdf2_sha256$20000$g1qPbIDiM4Ca$oHgLibS1qrPxQUqhbTsNXsxwsdgWwMGfObG4HW/TlGM=','2017-05-20 11:34:45.429895','zgh3@126.com','zgh3at126dotcom',1,0,0,1,NULL,NULL,NULL,NULL,NULL,'2017-05-17 08:26:37.303031'),(7,'pbkdf2_sha256$20000$DpwMvn7rn9DT$oiYbTbQOHKPUSfxOITJCdqW918qCOvj2o/Lw6dHZaKU=','2017-05-17 08:32:10.702585','zgh4@126.com','zgh4at126dotcom',1,0,0,1,NULL,NULL,NULL,NULL,NULL,'2017-05-17 08:32:09.424922'),(8,'pbkdf2_sha256$20000$KSRpGwFLyg0V$dcAh17zY1pYJ/Cp/55+DJjEbcg0+/bhQDKZsgWjG7sE=','2017-05-17 08:35:18.136544','zgh5@126.com','zgh5at126dotcom',1,0,0,1,NULL,NULL,NULL,NULL,NULL,'2017-05-17 08:35:16.827935'),(9,'pbkdf2_sha256$20000$Ewwm6awcVN28$ZTefLanqQ/MQsKSaNm0CnKDVCu+qsuNwq1uD05m8USI=','2017-05-17 08:39:04.798567','zgh6@126.com','zgh6at126dotcom',1,0,0,1,NULL,NULL,NULL,NULL,NULL,'2017-05-17 08:39:04.545281'),(10,'pbkdf2_sha256$20000$s6bYUBu2IQzB$tLywIjPW0DSvPWXA8Af88yjOmSXoVN3ca16ToNW1v2k=','2017-05-17 09:04:08.623399','zgh7@126.com','zgh7at126dotcom',1,0,0,1,NULL,NULL,NULL,NULL,NULL,'2017-05-17 08:45:22.469843'),(11,'pbkdf2_sha256$20000$pR6rPww2EpvN$Jw0zhIoTOifwaC/kHF4uqsAbsBhhtKPvGpn7qUOb9Mc=','2017-05-19 02:06:53.334710','zgh8@126.com','zgh8at126dotcom',1,0,0,1,NULL,NULL,NULL,NULL,NULL,'2017-05-17 09:12:12.273095'),(12,'pbkdf2_sha256$20000$RxWMq2Ytpvqq$8kLAm7k/eBfQkP7JNwfcp3cPImuEAD+msjyVsCbUN+M=','2017-06-09 02:55:59.285388','admin@126.com','admin',1,1,0,1,NULL,NULL,NULL,NULL,NULL,'2017-05-21 00:37:50.606299'),(13,'pbkdf2_sha256$20000$coH9rfCmSKAR$n489FMbX1ZhwCr1+WoF7ArIAfx3E2P6yHKNxJHh0tUA=','2017-05-28 11:51:12.542021','zgh21@126.com','916e7efb72',1,0,0,1,NULL,NULL,NULL,NULL,NULL,'2017-05-28 11:51:12.290932');
/*!40000 ALTER TABLE `exchcard_xuser` ENABLE KEYS */;
UNLOCK TABLES;



-- Dump completed on 2017-06-09 11:10:19
