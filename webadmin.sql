-- --------------------------------------------------------
-- Servidor:                     127.0.0.1
-- Versão do servidor:           10.9.2-MariaDB - mariadb.org binary distribution
-- OS do Servidor:               Win64
-- HeidiSQL Versão:              11.3.0.6295
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


-- Copiando estrutura do banco de dados para webadmin
CREATE DATABASE IF NOT EXISTS `webadmin` /*!40100 DEFAULT CHARACTER SET latin1 */;
USE `webadmin`;

-- Copiando estrutura para tabela webadmin.license
CREATE TABLE IF NOT EXISTS `license` (
  `login` text DEFAULT NULL,
  `token` text DEFAULT NULL,
  `date` text DEFAULT NULL,
  `enddate` text DEFAULT NULL,
  `game` text DEFAULT NULL,
  `IP` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- Exportação de dados foi desmarcado.

-- Copiando estrutura para tabela webadmin.payment
CREATE TABLE IF NOT EXISTS `payment` (
  `Login` text DEFAULT NULL,
  `payment_id` text DEFAULT NULL,
  `payment_method` text DEFAULT NULL,
  `status` text DEFAULT NULL,
  `date` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- Exportação de dados foi desmarcado.

-- Copiando estrutura para tabela webadmin.users
CREATE TABLE IF NOT EXISTS `users` (
  `Login` text DEFAULT NULL,
  `Password` text DEFAULT NULL,
  `Email` text DEFAULT NULL,
  `IP` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- Exportação de dados foi desmarcado.

/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;
