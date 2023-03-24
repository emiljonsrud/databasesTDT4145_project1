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
INSERT INTO Ticket(TicketNo, OrderID, CarID, PlaceNo, StartStation, EndStation, NameOfRoute, RunDate)
VALUES
  (1, 1, 2000, 2, "Trondheim", "Fauske", "Dagtog-Trondheim-Bodø",'2023-04-03' ),
  (2, 2, 2000, 4, "Trondheim", "Fauske", "Dagtog-Trondheim-Bodø", '2023-04-03');

INSERT INTO Placement(PlaceNo, CarID)
VALUES
  (2, 2000),
  (3, 2000);


