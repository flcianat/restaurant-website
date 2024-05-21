-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: May 21, 2024 at 10:25 AM
-- Server version: 10.4.25-MariaDB
-- PHP Version: 7.4.30

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `db_perpus`
--

-- --------------------------------------------------------

--
-- Table structure for table `anggota`
--

CREATE TABLE `anggota` (
  `id` int(100) NOT NULL,
  `fullname` varchar(100) NOT NULL,
  `email` varchar(100) NOT NULL,
  `password` varchar(255) NOT NULL,
  `born` date NOT NULL,
  `phonenumber` varchar(20) NOT NULL,
  `status` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `anggota`
--

INSERT INTO `anggota` (`id`, `fullname`, `email`, `password`, `born`, `phonenumber`, `status`) VALUES
(1, 'John Doe', 'john@example.com', 'password123', '1990-05-15', '1234567890', 'Tidak Aktif'),
(2, 'Jane Smith', 'jane@example.com', 'securepassword', '1985-09-20', '9876543210', 'Aktif'),
(4, 'Bob Brown', 'bob@example.com', 'pass123', '1980-11-25', '1112223333', 'Aktif'),
(5, 'Eve Taylor', 'eve@example.com', 'password321', '1998-07-30', '4445556666', 'Aktif');

-- --------------------------------------------------------

--
-- Table structure for table `buku`
--

CREATE TABLE `buku` (
  `id` int(100) NOT NULL,
  `judul` varchar(200) NOT NULL,
  `penulis` varchar(100) NOT NULL,
  `tahun` year(4) NOT NULL,
  `status` varchar(100) NOT NULL,
  `stok` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `buku`
--

INSERT INTO `buku` (`id`, `judul`, `penulis`, `tahun`, `status`, `stok`) VALUES
(3, 'To Kill a Mockingbird', 'Harper Lee', 1960, 'Tidak Tersedia', 8),
(4, '1984', 'George Orwell', 1949, 'Tersedia', 5),
(5, 'Sapiens: A Brief History of Humankind', 'Yuval Noah Harari', 2011, 'Tersedia', 15),
(6, 'The Origin of Species', 'Charles Darwin', 0000, 'Tersedia', 3);

-- --------------------------------------------------------

--
-- Table structure for table `koleksi_saya`
--

CREATE TABLE `koleksi_saya` (
  `judulbuku` varchar(100) NOT NULL,
  `durasipeminjaman` varchar(10) NOT NULL,
  `deskripsi` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `koleksi_saya`
--

INSERT INTO `koleksi_saya` (`judulbuku`, `durasipeminjaman`, `deskripsi`) VALUES
('The Great Gatsby', '10 Hari', 'Jay Gatsby, seorang pemuda yang tinggal dalam kemewahan di sebuah rumah besar di West Egg, Long Island. Gatsby terobsesi dengan Daisy Buchanan, seorang wanita yang menjadi lambang kekayaan dan kesuksesan baginya.\r\n');

-- --------------------------------------------------------

--
-- Table structure for table `transaksi`
--

CREATE TABLE `transaksi` (
  `idtransaksi` int(100) NOT NULL,
  `judulbuku` varchar(200) NOT NULL,
  `namapeminjam` varchar(100) NOT NULL,
  `tanggalpeminjaman` date NOT NULL,
  `tanggalpengembalian` date NOT NULL,
  `status` varchar(100) NOT NULL,
  `statusdenda` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `transaksi`
--

INSERT INTO `transaksi` (`idtransaksi`, `judulbuku`, `namapeminjam`, `tanggalpeminjaman`, `tanggalpengembalian`, `status`, `statusdenda`) VALUES
(1, 'The Great Gatsby', 'Jane Smith', '2024-05-14', '2024-05-31', 'Dipinjam', 'Denda'),
(2, 'Buku 2', 'Peminjam 2', '2024-05-09', '2024-05-31', 'Dipinjam', '');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `anggota`
--
ALTER TABLE `anggota`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `buku`
--
ALTER TABLE `buku`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `koleksi_saya`
--
ALTER TABLE `koleksi_saya`
  ADD PRIMARY KEY (`judulbuku`);

--
-- Indexes for table `transaksi`
--
ALTER TABLE `transaksi`
  ADD PRIMARY KEY (`idtransaksi`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `anggota`
--
ALTER TABLE `anggota`
  MODIFY `id` int(100) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `buku`
--
ALTER TABLE `buku`
  MODIFY `id` int(100) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT for table `transaksi`
--
ALTER TABLE `transaksi`
  MODIFY `idtransaksi` int(100) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
