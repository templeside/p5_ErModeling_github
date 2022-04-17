DROP TABLE IF EXISTS Categories;
DROP TABLE IF EXISTS Items;
DROP TABLE IF EXISTS Users;
DROP TABLE IF EXISTS Bids;

CREATE TABLE Items(
    Item varchar(256)
    Currently money,
    Buy_Price money,
    Forst_Bid money,
    Number_of_Bids INT,
    Starts datetime,
    Ends datetime,
    Description varchar(256)
    Primary key (ItemID),
    Foreign key (Seller) references Users (UserID)
);


CREATE TABLE Categories(
    ItemID   INT,
    CategoryNames  varchar(256)
    Primary key (ItemID, CategoryNames),
    Foreign key (ItemID) references Items (ItemID)
);

CREATE TABLE Users(
    Rating INT,
    Country varchar(256),
    User_Address varchar(256)
    Primary key (UserID)
);

CREATE TABLE Bids(
    ItemID   INT,
    Bidder  varchar(256),
    BidID INT,
    BidTime datetime,
    Amount money
    Primary key (BidID),
    Foreign key (Bidder) references Users (UserID),
    Foreign key (ItemID) references Items (ItemID)
);
