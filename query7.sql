SELECT COUNT(DISTINCT CategoryName) FROM Categories WHERE ItemID IN 
(SELECT DISTINCT ItemID FROM Bids WHERE Amount>100);