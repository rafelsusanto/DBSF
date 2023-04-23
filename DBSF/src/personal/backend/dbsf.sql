-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: localhost
-- Generation Time: Apr 18, 2023 at 07:36 PM
-- Server version: 10.4.28-MariaDB
-- PHP Version: 8.1.17

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `dbsf`
--

-- --------------------------------------------------------

--
-- Table structure for table `Scan`
--

CREATE TABLE `Scan` (
  `ScanID` int(11) NOT NULL,
  `Name` varchar(255) NOT NULL,
  `IPAddress` varchar(255) NOT NULL,
  `PacketRequest` longtext DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `ScanResult`
--

CREATE TABLE `ScanResult` (
  `ResultID` int(11) NOT NULL,
  `ScanID` int(11) NOT NULL,
  `ScanType` int(11) NOT NULL,
  `FilePath` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `Scan`
--
ALTER TABLE `Scan`
  ADD PRIMARY KEY (`ScanID`);

--
-- Indexes for table `ScanResult`
--
ALTER TABLE `ScanResult`
  ADD PRIMARY KEY (`ResultID`),
  ADD KEY `ScanResult_FK` (`ScanID`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `Scan`
--
ALTER TABLE `Scan`
  MODIFY `ScanID` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `ScanResult`
--
ALTER TABLE `ScanResult`
  MODIFY `ResultID` int(11) NOT NULL AUTO_INCREMENT;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `ScanResult`
--
ALTER TABLE `ScanResult`
  ADD CONSTRAINT `ScanResult_FK` FOREIGN KEY (`ScanID`) REFERENCES `Scan` (`ScanID`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;