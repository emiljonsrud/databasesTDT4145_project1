/* 
  Fill dummy customer data
*/

INSERT INTO Customer (Name, PhoneNO, Email)
VALUES
  ("Ola Nordman", 47474747, "ola@norge.no"),
  ("Rolf Rolfsen", 9009100, "rullerolf@online.com"),
  ("Hermine Grange", 10020343, "hermgra@stud.galtvort.no");


INSERT INTO CustomerOrder(OrderID, OrderDate, OrderTime, CustomerID)
VALUES
  (1, '2023-02-02', '09:00', 1),
  (2, '2023-02-04', '08:00', 1);

 -- Test for 1 customer
INSERT INTO Ticket(OrderID, CarID, PlaceNo, NameOfRoute)
VALUES
  (1, 2000, 2, "Dagtog-Trondheim-Bodø"),
  (2, 2001, 4, "Dagtog-Trondheim-Bodø");

INSERT INTO TicketOnSection(TicketNo, StartStation, EndStation)
VALUES
  (1, "Trondheim", "Mosjøen"),
  (2, "Trondheim", "Fauske");


INSERT INTO Placement(PlaceNo, CarID)
VALUES
  (2, 2000),
  (4, 2001);


