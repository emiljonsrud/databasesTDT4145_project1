-- Track Section

CREATE TABLE TrackSection(
  Name TEXT PRIMARY KEY NOT NULL,
  StartStation TEXT NOT NULL, 
  EndStation TEXT NOT NULL, 
  ElectricTracks BOOL,
  FOREIGN KEY(StartStation) REFERENCES RaylwayStation(Name) ON UPDATE CASCADE ON DELETE CASCADE,
  FOREIGN KEY(EndStation) REFERENCES RailwayStation(name) ON UPDATE CASCADE ON DELETE CASCADE);


 -- RailwayStation

CREATE TABLE RailwayStation(Name TEXT PRIMARY KEY NOT NULL, 
Height INT NOT NULL) 

-- TrackSubSection
CREATE TABLE TrackSubSection(SectionNo INT, 
Length INT, 
DoubleTrack BOOL,  
StartsAt TEXT NOT NULL,
EndsAt TEXT NOT NULL, 
TrackSection TEXT NOT NULL, 
 FOREIGN KEY(StartsAt) REFERENCES Station(Name), FOREIGN KEY(EndsAT) REFERENCES Station(Name), 
FOREIGN KEY(TrackSection) REFERENCES TrackSection(name),  CONSTRAINT PK_TrackSubSection PRIMARY KEY (SectionNO, TrackSection));

--  TrainRoute    
CREATE TABLE TrainRoute(
  Name TEXT PRIMARY KEY NOT NULL, 
  Operator TEXT, 
  TrackSection TEXT NOT NULL, 
  FOREIGN KEY(TrackSection) REFERENCES TrackSection(Name)
)

-- Ticket
CREATE TABLE Ticket(
  TicketNo INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
  OrderID INT,
  CarID INT,
  PlaceNo INT,
  FOREIGN KEY(OrderID) REFERENCES CustomerOrder(OrderID),
  FOREIGN KEY(CarID, PlaceNo) REFERENCES  Placement(CarID, PlaceNo),
)

-- RouteStop
CREATE TABLE RouteStop( 
  RailwayStation TEXT, 
  TrainRoute TEXT, 
  FOREIGN KEY(RailwayStation) REFERENCES RailwayStation(name), 
  FOREIGN KEY(TrainRoute) REFERENCES TrainRoute(name), 
  CONSTRAINT PK_RouteStop PRIMARY KEY(RailwayStation, 
  TrainRoute
); 


-- TrainOccurance 
CREATE TABLE TrainOccurance(
  Date INT NOT NULL, 
  TrainRoute TEXT NOT NULL, 
  FOREIGN KEY(TrainRoute) REFERENCES TrainRoute(Name), 
  CONSTRAINT PK_TrainOccurance PRIMARY KEY(Date, TrainRoute) 
);

-- CarInTrain
CREATE TABLE CarInTrain(
  CarID INT PRIMARY KEY NOT NULL, 
  CarNo INT
);


-- ChairCar 
CREATE TABLE ChairCar(
  CarID INT PRIMARY KEY REFERENCES CarInTrain(CarID), 
  NumberOfRows INT, 
  SeatsPerRow INT
);


-- SleepCar 
CREATE TABLE SleepCar(
  CarID INT PRIMARY KEY REFERENCES CarInTrain(CarID), 
  CarNo INT, 
  NumOfCompartments INT
);


-- CustomerOrder
CREATE TABLE CustomerOrder(
  OrderID INT PRIMARY KEY NOT NULL, 
  OrderDate ???INT???, 
  OrderTime INT, 
  CustomerID INT NOT NULL, 
  FOREIGN KEY(CustomerID) REFERENCES Customer(CustomerID)
);


-- Customer
CREATE TABLE Customer(
  CustomerID INT PRIMARY KEY NOT NULL, 
  Name TEXT, 
  Email TEXT, 
  PhoneNO INT, 
  RegistryID INT NOT NULL, 
  FOREIGN KEY(RegistryID) REFERENCES CustomerRegistry(RegistryID)
);

-- CustomerRegistry
CREATE TABLE CustomerRegistry(
  RegistryID INT PRIMARY KEY NOT NULL
);


