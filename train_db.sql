-- Track Section
CREATE TABLE TrackSection(
  Name VARCHAR(255) PRIMARY KEY NOT NULL,
  ElectricTracks BOOL,
  StartStation VARCHAR(255) NOT NULL, 
  EndStation VARCHAR(255) NOT NULL, 
  FOREIGN KEY(StartStation) REFERENCES RailwayStation(Name) ON UPDATE CASCADE ON DELETE CASCADE,
  FOREIGN KEY(EndStation) REFERENCES RailwayStation(name) ON UPDATE CASCADE ON DELETE CASCADE,
  INSERT INTO TrackSubSection VALUES(StartStation, )
);

 -- RailwayStation
CREATE TABLE RailwayStation(
  Name VARCHAR(255) PRIMARY KEY NOT NULL, 
  Height INT NOT NULL
); 

-- TrackSubSection
CREATE TABLE TrackSubSection(
  SectionNo INT, 
  TrackSection VARCHAR(255) NOT NULL, 
  Length INT, 
  DoubleTrack BOOL,  
  StartsAt VARCHAR(255) NOT NULL,
  EndsAt VARCHAR(255) NOT NULL, 
  FOREIGN KEY(StartsAt) REFERENCES Station(Name), 
  FOREIGN KEY(EndsAT) REFERENCES Station(Name), 
  FOREIGN KEY(TrackSection) REFERENCES TrackSection(name),  
  CONSTRAINT PK_TrackSubSection PRIMARY KEY (SectionNo, TrackSection)
);

--  TrainRoute    
CREATE TABLE TrainRoute(
  Name VARCHAR(255) PRIMARY KEY NOT NULL, 
  Operator VARCHAR(255), 
  TrackName VARCHAR(255) NOT NULL, 
  FOREIGN KEY(TrackName) REFERENCES TrackSection(Name)
);

-- WeekDay
CREATE TABLE WeekDay(
  Name VARCHAR(255) PRIMARY KEY NOT NULL,
);

-- Day of Route
CREATE TABLE DayOfRoute(
  WeekDay VARCHAR(255),
  TrainRoute VARCHAR(255),
  FOREIGN KEY WeekName REFERENCES WeekDay(Name),
  FOREIGN KEY TrainRoute REFERENCES TrainRoute(Name)
  CONSTRAINT PK_DayOfRoute PRIMARY KEY(WeekName, TrainRoute)
);

-- Ticket
CREATE TABLE Ticket(
  TicketNo INT AUTO_INCREMENT PRIMARY KEY NOT NULL,
  OrderID INT,
  CarID INT,
  PlaceNo INT,
  FOREIGN KEY(OrderID) REFERENCES CustomerOrder(OrderID),
  FOREIGN KEY(CarID, PlaceNo) REFERENCES  Placement(CarID, PlaceNo)
);

-- RouteStop
CREATE TABLE RouteStop( 
  RailwayStation VARCHAR(255), 
  TrainRoute VARCHAR(255), 
  FOREIGN KEY(RailwayStation) REFERENCES RailwayStation(name), 
  FOREIGN KEY(TrainRoute) REFERENCES TrainRoute(name), 
  CONSTRAINT PK_RouteStop PRIMARY KEY(RailwayStation, TrainRoute)
); 


-- TrainOccurance 
CREATE TABLE TrainOccurance(
  Date DATE NOT NULL, 
  TrainRoute VARCHAR(255) NOT NULL, 
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
  OrderDate DATE, 
  OrderTime INT, 
  CustomerID INT NOT NULL, 
  FOREIGN KEY(CustomerID) REFERENCES Customer(CustomerID)
);


-- Customer
CREATE TABLE Customer(
  CustomerID INT PRIMARY KEY NOT NULL, 
  Name VARCHAR(255), 
  Email VARCHAR(255), 
  PhoneNO INT, 
  RegistryID INT NOT NULL, 
  FOREIGN KEY(RegistryID) REFERENCES CustomerRegistry(RegistryID)
);

-- CustomerRegistry
CREATE TABLE CustomerRegistry(
  RegistryID INT PRIMARY KEY NOT NULL
);

