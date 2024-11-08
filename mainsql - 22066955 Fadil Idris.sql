DROP SCHEMA IF EXISTS world_hotels;
CREATE DATABASE World_Hotels;

USE World_Hotels;

CREATE TABLE HotelInformation
(
	HotelInformationID INT NOT NULL AUTO_INCREMENT,
    PRIMARY KEY (HotelInformationID),
    City VARCHAR(40) NULL,
    Standared_Room_Capacity VARCHAR(20) NULL,
    Double_Room_Capacity VARCHAR(20)  NULL,
    Family_Room_Capacity VARCHAR(20) NULL,
    PeakSeasonPrice FLOAT NULL,
    OffSeasonPrice FLOAT NULL
);

CREATE TABLE Room
(
	RoomTableID INT NOT NULL AUTO_INCREMENT,
    PRIMARY KEY (RoomTableID),
    HotelID INT,
    RoomNumber VARCHAR(20),
    RoomType VARCHAR(20) NOT NULL,
    FOREIGN KEY (HotelID) REFERENCES HotelInformation (HotelInformationID)
);
CREATE TABLE Billings
(
	BillingsID INT NOT NULL AUTO_INCREMENT,
    PRIMARY KEY (BillingsID),
    ChargeRate VARCHAR(20) NOT NULL,
    TotalCharges VARCHAR(20) NOT NULL,
    PaymentStatus VARCHAR(20) NOT NULL
);

CREATE TABLE BookingTable
(
	BookingID INT NOT NULL AUTO_INCREMENT,
    PRIMARY KEY (BookingID),
    RoomTableID INT,
    CheckInDate date NOT NULL,
    CheckOutDate date NOT NULL,
    HotelInformationID INT NULL,
    BillingsID INT NULL,
    FOREIGN KEY (HotelInformationID)
		REFERENCES HotelInformation (HotelInformationID)
        ON DELETE SET NULL
        ON UPDATE CASCADE,
	FOREIGN KEY (RoomTableID)
		REFERENCES Room (RoomTableID)
        ON DELETE SET NULL
        ON UPDATE CASCADE,
	FOREIGN KEY (BillingsID)
		REFERENCES Billings (BillingsID)
        ON DELETE SET NULL
        ON UPDATE CASCADE
);

CREATE TABLE UserInformation
(
	UserInfoId INT NOT NULL AUTO_INCREMENT,
    PRIMARY KEY (UserInfoId),
    Name VARCHAR(30) NULL,
    Surname VARCHAR(30) NULL,
    Email VARCHAR(60) NULL UNIQUE,
    PhoneNumber VARCHAR(20) NULL,
    User_Password VARCHAR(90) NULL,
    BookingID INT NULL UNIQUE,
	Privilages VARCHAR(20) NULL DEFAULT 'Normal',
    FOREIGN KEY (BookingID)
		REFERENCES BookingTable (BookingID)
        ON DELETE SET NULL
        ON UPDATE CASCADE
);

insert into HotelInformation ( City, Standared_Room_Capacity, Double_Room_Capacity, Family_Room_Capacity, PeakSeasonPrice, OffSeasonPrice) 
VALUES ('Aberdeen',27,45,18,140,70),
('Belfast',24,40,116,130,70),
('Birminghham',33,55,22,150,75),
('Bristol',30,50,20,140,70),
('Cardiff',27,45,18,130,70),
('Edinburgh',36,60,24,160,80),
('Glasgow',42,70,28,150,75),
('London',48,80,32,200,100),
('Manchester',45,75,30,180,90),
('New Castle',27,45,18,120,70),
('Norwich',27,45,18,130,70),
('Nottingham',33,55,22,130,70),
('Oxford',27,45,18,180,90),
('Plymouth',24,40,16,180,90),
('Swansea',21,35,14,130,70),
('Bournemouth',27,45,18,130,70),
('Kent',30,50,20,140,80);

SELECT User_Password FROM UserInformation WHERE Email = 'fihabeeb006@gmail.com';
SELECT * FROM UserInformation;		
SELECT * FROM HotelInformation;	
-- SELECT customerinfoid FROM CustomerInfo ORDER BY CustomerInfoID DESC LIMIT 1;
-- INSERT INTO UserInformation (NAME, SURNAME, EMAIL, USER_PASSWORD) VALUES ("Fadil Idris", "Habeeb", "1234567", "121121");
