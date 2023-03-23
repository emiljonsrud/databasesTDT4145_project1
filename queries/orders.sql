/*
Input: customer_id
*/

SELECT C1.CustomerID, TOS1.StartStation, RS1.TimeOfDay, TOS2.EndStation, RS2.TimeOfDay
FROM 
    ((((((Customer as C1 INNER JOIN CustomerOrder AS CO1 
    ON (C1.CustomerID = CO1.CustomerID))
    INNER JOIN Ticket AS T1
    ON (CO1.OrderID = T1.OrderID))
    INNER JOIN TicketOnSection AS TOS1
    ON (T1.TicketNo = TOS1.TicketNo))
    INNER JOIN TrainOccurance AS TO1 
    ON (T1.NameOfRoute = TO1.NameOfRoute))
    INNER JOIN TrainRoute AS TR1
    ON (TO1.NameOfRoute = TR1.Name))
    INNER JOIN RouteStop AS RS1
    ON (TR1.Name = RS1.NameOfRoute))

    INNER JOIN 
    (
    SELECT  
        TR2.Name, TOS2.EndStation, RS2.TimeOfDay
    FROM
        (((((Customer as C2 INNER JOIN CustomerOrder AS CO2 
        ON (C2.CustomerID = CO2.CustomerID))
        INNER JOIN Ticket AS T2
        ON (CO2.OrderID = T2.OrderID))
        INNER JOIN TicketOnSection AS TOS2
        ON (T2.TicketNo = TOS2.TicketNo))
        INNER JOIN TrainOccurance AS TO2 
        ON (T2.NameOfRoute = TO2.NameOfRoute))
        INNER JOIN TrainRoute AS TR2
        ON (TO2.NameOfRoute = TR2.Name))
        INNER JOIN RouteStop AS RS2
        ON (TR2.Name = RS2.NameOfRoute)
    WHERE 
        RS2.Station = TOS2.EndStation AND
        C2.CustomerID = :customer_id
    )
    ON (TR1.Name = TR2.Name)

WHERE RS1.Station = TOS1.StartStation 
    AND C1.CustomerID = :customer_id;


