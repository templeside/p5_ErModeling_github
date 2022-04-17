DROP TABLE IF EXISTS Categories;
DROP TABLE IF EXISTS Items;
DROP TABLE IF EXISTS Users;
DROP TABLE IF EXISTS Bids;

CREATE TABLE Users(
    UserID varchar(256),
    Rating INT,
    Country varchar(256),
    Location varchar(256),
    Primary key (UserID)
);

CREATE TABLE Items(
    ItemID varchar(256),
    Name varchar(256),
    Currently money,
    Buy_Price money,
    First_Bid money,
    Number_of_Bids INT,
    Started datetime,
    Ends datetime,
    Seller varchar(256),
    Description varchar(256),
    Primary key (ItemID),
    Foreign key (Seller) references Users (UserID)
);


CREATE TABLE Categories(
    ItemID   INT,
    CategoryName  varchar(256),
    Primary key (ItemID, CategoryName),
    Foreign key (ItemID) references Items (ItemID)
);



CREATE TABLE Bids(
    BidID INT,
    ItemID   INT,
    Bidder  varchar(256),
    Time datetime,
    Amount money,
    Primary key (BidID),
    Foreign key (Bidder) references Users (UserID),
    Foreign key (ItemID) references Items (ItemID)
);
