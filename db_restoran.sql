-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jun 12, 2024 at 07:48 PM
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

INSERT INTO `menuitems` (`MenuItemID`, `Name`, `Description`, `Price`, `Category`, `CreatedAt`, `Quantity`) VALUES
(1, 'Burger', 'A delicious beef burger', 8.99, 'Main Course', '2024-06-12 16:20:31', 24),
(2, 'Salad', 'A fresh green salad', 5.99, 'Appetizer', '2024-06-12 16:20:31', 28),
(3, 'Cheeseburger', 'Juicy beef patty topped with melted cheese, lettuce, tomato, and pickles on a sesame seed bun.', 9.99, 'Main Course', '2024-06-12 17:15:10', 8),
(4, 'Caesar Salad', 'Crisp romaine lettuce topped with grilled chicken breast, Parmesan cheese, croutons, and Caesar dressing.', 11.99, 'Salad', '2024-06-12 17:15:10', 10),
(5, 'Margarita Pizza', 'Classic pizza topped with tomato sauce, fresh mozzarella cheese, basil, and a drizzle of olive oil.', 12.99, 'Pizza', '2024-06-12 17:15:10', 9),
(6, 'Chocolate Brownie Sundae', 'Warm chocolate brownie topped with vanilla ice cream, whipped cream, chocolate syrup, and a cherry.', 6.99, 'Dessert', '2024-06-12 17:15:10', 4);

-- --------------------------------------------------------

--
-- Table structure for table `orderitems`
--

CREATE TABLE `orderitems` (
  `OrderItemID` int(11) NOT NULL,
  `MenuItemID` int(11) DEFAULT NULL,
  `Quantity` int(11) DEFAULT NULL,
  `Price` decimal(10,2) DEFAULT NULL,
  `OrderDate` timestamp NOT NULL DEFAULT current_timestamp(),
  `TotalAmount` decimal(10,2) DEFAULT NULL,
  `Status` enum('Completed','Not Completed Yet') DEFAULT 'Not Completed Yet',
  `CustomerID` int(11) DEFAULT NULL,
  `CustomerName` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `orderitems`
--

INSERT INTO `orderitems` (`OrderItemID`, `MenuItemID`, `Quantity`, `Price`, `OrderDate`, `TotalAmount`, `Status`, `CustomerID`, `CustomerName`) VALUES
(1, 1, 1, 8.99, '2024-06-12 17:00:28', 14.98, 'Completed', 1, 'John Doe'),
(2, 2, 1, 5.99, '2024-06-12 17:00:28', 14.98, 'Completed', 2, 'Jane Smith'),
(3, 1, 1, 8.99, '2024-06-12 17:00:28', 14.98, 'Completed', 3, 'Nia');

--
-- Triggers `orderitems`
--
DELIMITER $$
CREATE TRIGGER `before_orderitems_insert` BEFORE INSERT ON `orderitems` FOR EACH ROW BEGIN
    DECLARE firstName VARCHAR(50);
    DECLARE lastName VARCHAR(50);
    DECLARE totalAmount DECIMAL(10, 2);
    DECLARE status VARCHAR(50);
    DECLARE orderDate TIMESTAMP;

    -- Get customer and order details based on CustomerID
    SELECT FirstName, LastName INTO firstName, lastName
    FROM Customers
    WHERE CustomerID = NEW.CustomerID;

    -- Set customer name in the new record
    SET NEW.CustomerName = Name;

    -- Optionally, you can also get order details if they are to be computed at order placement
    -- Set other order details in the new record (if they are dynamic and computed here)
    -- SET NEW.OrderDate = CURRENT_TIMESTAMP;
    -- SET NEW.TotalAmount = ... (computed value);
    -- SET NEW.Status = 'Pending';  -- or another status
END
$$
DELIMITER ;
DELIMITER $$
CREATE TRIGGER `update_menuitem_quantity` AFTER INSERT ON `orderitems` FOR EACH ROW BEGIN
    UPDATE MenuItems
    SET Quantity = Quantity - NEW.Quantity
    WHERE MenuItemID = NEW.MenuItemID;
END
$$
DELIMITER ;

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
  ADD PRIMARY KEY (`OrderItemID`),
  ADD KEY `MenuItemID` (`MenuItemID`),
  ADD KEY `fk_customer` (`CustomerID`),
  ADD KEY `fk_customer_name` (`CustomerName`);

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
  MODIFY `MenuItemID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT for table `orderitems`
--
ALTER TABLE `orderitems`
  MODIFY `OrderItemID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `orderitems`
--
ALTER TABLE `orderitems`
  ADD CONSTRAINT `fk_customer` FOREIGN KEY (`CustomerID`) REFERENCES `customers` (`CustomerID`),
  ADD CONSTRAINT `fk_customer_name` FOREIGN KEY (`CustomerName`) REFERENCES `customers` (`CustomerName`),
  ADD CONSTRAINT `orderitems_ibfk_2` FOREIGN KEY (`MenuItemID`) REFERENCES `menuitems` (`MenuItemID`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
