-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jun 18, 2024 at 06:39 PM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `db_restoran`
--

-- --------------------------------------------------------

--
-- Table structure for table `customers`
--

CREATE TABLE `customers` (
  `CustomerID` int(11) NOT NULL,
  `CustomerName` varchar(50) DEFAULT NULL,
  `Email` varchar(100) DEFAULT NULL,
  `PhoneNumber` varchar(15) DEFAULT NULL,
  `CreatedAt` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `customers`
--

INSERT INTO `customers` (`CustomerID`, `CustomerName`, `Email`, `PhoneNumber`, `CreatedAt`) VALUES
(1, 'John Doe', 'john.doe@example.com', '123-456-7890', '2024-06-12 16:22:04'),
(2, 'Jane Smith', 'jane.smith@example.com', '098-765-4321', '2024-06-12 16:22:04'),
(3, 'Nia', 'nia8@gmail.com', '625874135', '2024-06-02 16:46:54');

-- --------------------------------------------------------

--
-- Table structure for table `menuitems`
--

CREATE TABLE `menuitems` (
  `img_url` varchar(255) DEFAULT NULL,
  `MenuItemID` int(11) NOT NULL,
  `Name` varchar(100) DEFAULT NULL,
  `Description` text DEFAULT NULL,
  `Price` decimal(10,2) DEFAULT NULL,
  `Category` varchar(50) DEFAULT NULL,
  `CreatedAt` timestamp NOT NULL DEFAULT current_timestamp(),
  `Quantity` int(11) DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `menuitems`
--

INSERT INTO `menuitems` (`img_url`, `MenuItemID`, `Name`, `Description`, `Price`, `Category`, `CreatedAt`, `Quantity`) VALUES
('https://media-cdn.tripadvisor.com/media/photo-s/1a/6c/6f/d9/gemeos-ou-criado-pela.jpg', 1, 'Burger', 'Juicy, grilled beef patty, crisp lettuce, ripe tomato, pickles, and onions, all nestled in a toasted sesame seed bun.', 8.99, 'Main Course', '2024-06-12 16:20:31', 24),
('https://www.astronauts.id/blog/wp-content/uploads/2022/10/Sudah-Pasti-Lezat-Ini-Resep-Salad-Sayur-Diet-Untuk-Kamu-1024x683.jpg', 2, 'Salad', 'Crisp mixed greens tossed with juicy cherry tomatoes, cucumbers, and shredded carrots, topped with crunchy croutons and a sprinkle of feta cheese.', 5.99, 'Appetizer', '2024-06-12 16:20:31', 28),
('https://asset.kompas.com/crops/SzncWf6hbXuh5Konwvck0awlG-A=/0x0:1000x667/750x500/data/photo/2020/06/29/5ef9b1e9e2875.jpg', 3, 'Bruschetta', 'Sliced rustic bread grilled to perfection, topped with a savory blend of diced ripe tomatoes, garlic, and fresh basil, finished with a generous drizzle of extra virgin olive oil.', 9.99, 'Dessert', '2024-06-12 17:15:10', 8),
('https://www.allrecipes.com/thmb/mXZ0Tulwn3x9_YB_ZbkiTveDYFE=/1500x0/filters:no_upscale():max_bytes(150000):strip_icc()/229063-Classic-Restaurant-Caesar-Salad-ddmfs-4x3-231-89bafa5e54dd4a8c933cf2a5f9f12a6f.jpg', 4, 'Caesar Salad', 'Crisp romaine lettuce topped with grilled chicken breast, Parmesan cheese, croutons, and Caesar dressing.', 11.99, 'Salad', '2024-06-12 17:15:10', 10),
('https://assets.promediateknologi.id/crop/0x0:0x0/750x500/webp/photo/2023/07/26/Salinan-dari-foto-content-75-Fisqiyyah-Awawin-4192925078.png', 5, 'Margarita Pizza', 'Classic pizza topped with tomato sauce, fresh mozzarella cheese, basil, and a drizzle of olive oil.', 12.99, 'Pizza', '2024-06-12 17:15:10', 9),
('https://food.fnr.sndimg.com/content/dam/images/food/fullset/2021/12/15/0/FNM_010122-Dark-Chocolate-Brownie-Sundae_s4x3.jpg.rend.hgtvcom.616.462.suffix/1639586951781.jpeg', 6, 'Chocolate Brownie Sundae', 'Warm chocolate brownie topped with vanilla ice cream, whipped cream, chocolate syrup, and a cherry.', 6.99, 'Dessert', '2024-06-12 17:15:10', 4),
('https://www.thecandidcooks.com/wp-content/uploads/2023/04/bbq-chicken-pizza-feature.jpg', 7, 'BBQ Chicken Pizza', 'Pizza with BBQ sauce, grilled chicken, red onions, and cilantro.', 12.99, 'Pizza', '2024-06-17 16:25:22', 20),
('https://www.foodandwine.com/thmb/DTkNucHOU-YwpbJCtGQsflDQEs0=/1500x0/filters:no_upscale():max_bytes(150000):strip_icc()/Best-Spaghetti-Carbonara-Youll-Ever-Eat-Takes-Just-30-Minutes-To-Make-FT-RECIPE-0224_Lead-2caa6dc8f3ef4947bda5fa12c27e1a75.jpg', 8, 'Spaghetti Carbonara', 'Pasta with a creamy sauce made from eggs, cheese, pancetta, and pepper.', 11.99, 'Pasta', '2024-06-17 16:25:22', 15),
('https://www.thespruceeats.com/thmb/w2zenmawqCKTG__6NPiqITjeRNc=/1500x0/filters:no_upscale():max_bytes(150000):strip_icc()/simple-grilled-salmon-1300707-hero-01-48c84abce23d4a37a72ef15d8601219e.JPG', 9, 'Grilled Salmon', 'Fresh salmon fillet grilled to perfection and served with lemon butter sauce.', 18.99, 'Entree', '2024-06-17 16:25:22', 10),
('https://iamhomesteader.com/wp-content/uploads/2022/04/birria-taco-2.jpg', 10, 'Beef Tacos', 'Soft tortillas filled with seasoned beef, lettuce, cheese, and salsa.', 9.99, 'Mexican', '2024-06-17 16:25:22', 30),
('https://www.allrecipes.com/thmb/dcJLnSZrqStUxwGsc87idivCylE=/1500x0/filters:no_upscale():max_bytes(150000):strip_icc()/24712-ginger-veggie-stir-fry-DDMFS-4X3-3f25aaf303e04c849a71cc1e448dae6d.jpg', 11, 'Vegetable Stir Fry', 'Mixed vegetables stir-fried with soy sauce and served with rice.', 10.99, 'Asian', '2024-06-17 16:25:22', 25),
('https://hips.hearstapps.com/hmg-prod/images/chicken-alfredo-index-64ee1026c82a9.jpg?crop=0.9994472084024323xw:1xh;center,top&resize=1200:*', 12, 'Chicken Alfredo', 'Fettuccine pasta with creamy Alfredo sauce and grilled chicken.', 13.99, 'Pasta', '2024-06-17 16:25:22', 20),
('https://www.mediterraneanliving.com/wp-content/uploads/2018/02/Authentic-Greek-Salad-3-scaled.jpg', 13, 'Greek Salad', 'Salad with tomatoes, cucumbers, red onions, olives, feta cheese, and olive oil.', 8.99, 'Salad', '2024-06-17 16:25:22', 15),
('https://hips.hearstapps.com/hmg-prod/images/shrimp-scampi-index-644c0ade03d01.jpg?crop=0.8886420438767009xw:1xh;center,top&resize=1200:*', 14, 'Shrimp Scampi', 'Shrimp cooked in garlic, white wine, and butter sauce, served with pasta.', 17.99, 'Seafood', '2024-06-17 16:25:22', 12),
('https://mccormick.widen.net/content/gbdgjvbgvd/webp/Franks%20Original%20Buffalo%20Chicken%20Wings-1376x774.webp', 15, 'Buffalo Wings', 'Crispy chicken wings tossed in spicy buffalo sauce, served with blue cheese dip.', 10.99, 'Appetizer', '2024-06-17 16:25:22', 25);

-- --------------------------------------------------------

--
-- Table structure for table `orderitems`
--

CREATE TABLE `orderitems` (
  `ItemID` int(11) NOT NULL,
  `OrderID` int(11) DEFAULT NULL,
  `ItemName` varchar(100) NOT NULL,
  `Quantity` int(11) NOT NULL,
  `Price` decimal(10,2) NOT NULL,
  `Total` decimal(10,2) GENERATED ALWAYS AS (`Quantity` * `Price`) STORED
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `orderitems`
--

INSERT INTO `orderitems` (`ItemID`, `OrderID`, `ItemName`, `Quantity`, `Price`) VALUES
(1, 1, 'Caesar Salad', 2, 8.99),
(2, 1, 'Grilled Salmon', 1, 18.99),
(3, 1, 'Chocolate Lava Cake', 1, 6.99),
(4, 2, 'Caesar Salad', 1, 8.99),
(5, 2, 'Chocolate Lava Cake', 3, 6.99);

-- --------------------------------------------------------

--
-- Table structure for table `orders`
--

CREATE TABLE `orders` (
  `OrderID` int(11) NOT NULL,
  `OrderDate` date NOT NULL,
  `CustomerName` varchar(100) NOT NULL,
  `Location` varchar(255) NOT NULL,
  `Status` varchar(20) DEFAULT 'Pending',
  `Amount` decimal(10,2) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `orders`
--

INSERT INTO `orders` (`OrderID`, `OrderDate`, `CustomerName`, `Location`, `Status`, `Amount`) VALUES
(1, '2024-06-17', 'Jane Doe', '123 Street', 'Reject', 19.70),
(2, '2024-06-17', 'John Doe', '123 Main St', 'Accept', 20.00),
(3, '2024-06-18', 'Jane Smith', '456 Elm St', 'Reject', 21.00);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `customers`
--
ALTER TABLE `customers`
  ADD PRIMARY KEY (`CustomerID`),
  ADD KEY `idx_CustomerName` (`CustomerName`);

--
-- Indexes for table `menuitems`
--
ALTER TABLE `menuitems`
  ADD PRIMARY KEY (`MenuItemID`);

--
-- Indexes for table `orderitems`
--
ALTER TABLE `orderitems`
  ADD PRIMARY KEY (`ItemID`),
  ADD KEY `OrderID` (`OrderID`);

--
-- Indexes for table `orders`
--
ALTER TABLE `orders`
  ADD PRIMARY KEY (`OrderID`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `customers`
--
ALTER TABLE `customers`
  MODIFY `CustomerID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `menuitems`
--
ALTER TABLE `menuitems`
  MODIFY `MenuItemID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=17;

--
-- AUTO_INCREMENT for table `orderitems`
--
ALTER TABLE `orderitems`
  MODIFY `ItemID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `orders`
--
ALTER TABLE `orders`
  MODIFY `OrderID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `orderitems`
--
ALTER TABLE `orderitems`
  ADD CONSTRAINT `orderitems_ibfk_1` FOREIGN KEY (`OrderID`) REFERENCES `orders` (`OrderID`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
