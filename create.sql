DROP TABLE IF EXISTS Categories;
DROP TABLE IF EXISTS Items;
DROP TABLE IF EXISTS Users;
DROP TABLE IF EXISTS Bids;

CREATE TABLE Users(
    UserID VARCHAR(256),
    Rating INT,
    Country VARCHAR(256),
    Location VARCHAR(256),
    Primary Key (UserID)
);

CREATE TABLE Items(
    ItemID INT,
    Name VARCHAR(256),
    Currently MONEY,
    Buy_Price MONEY,
    First_Bid MONEY,
    Number_of_Bids INT,
    Started DateTime,
    Ends DateTime,
    Seller VARCHAR(256),
    Description VARCHAR(256),
    Primary Key (ItemID),
    Foreign Key (Seller) references Users (UserID)
);


CREATE TABLE Categories(
    ItemID INT,
    CategoryName  VARCHAR(256),
    Primary key (ItemID, CategoryName),
    Foreign key (ItemID) references Items (ItemID)
);



CREATE TABLE Bids(
    BidID INT,
    ItemID INT,
    Bidder VARCHAR(256),
    Time DateTime,
    Amount MONEY,
    Primary key (BidID),
    Foreign key (Bidder) references Users (UserID),
    Foreign key (ItemID) references Items (ItemID)
);
