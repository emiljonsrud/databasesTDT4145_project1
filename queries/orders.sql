/*
Input: customer_id
*/

SELECT DISTINCT 
    T1.RunDate, 
    TrainRoute.Name, 
    CarInTrain.CarNo, 
    T1.PlaceNo, 
    RS1.Station, 
    RS2.Station, 
    RS1.TimeOfDay, 
    RS2.TimeOfDay
FROM CustomerOrder 
    INNER JOIN Ticket AS T1
        ON (CustomerOrder.OrderID = T1.OrderID)
    INNER JOIN TrainOccurance AS TOC 
        ON T1.NameOfRoute = TOC.NameOfRoute AND  T1.RunDate = TOC.RunDate 
    INNER JOIN TrainRoute 
        ON TrainRoute.Name = TOC.NameOfRoute
    INNER JOIN RouteStop AS RS1 
        ON  RS1.NameOfRoute = TrainRoute.Name
    INNER JOIN RouteStop AS RS2 
        ON RS2.NameOfRoute= TrainRoute.Name
    INNER JOIN CarInTrain
        ON T1.CarID = CarInTrain.CarID

WHERE CustomerOrder.CustomerID = :customer_id
AND RS1.Station = T1.StartStation
AND RS2.Station = T1.EndStation
AND TOC.RunDate >=  DATE();