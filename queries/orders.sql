/*
Input: customer_id
*/

-- TODO Only show FUTURE orders! need current time


SELECT  DISTINCT C1.CustomerID, RS1.Station , 
                 T1.EndStation, RS1.TimeOfDay, 
                 sub_query.TimeOfDay, P.PlaceNo,
                 CarInTrain.CarNo, TR1.Name


FROM Customer as C1 
    INNER JOIN CustomerOrder AS CO1 
        ON C1.CustomerID = CO1.CustomerID
    INNER JOIN Ticket AS T1
        ON CO1.OrderID = T1.OrderID

    /*
    INNER JOIN TicketOnSection AS TOS1
        ON T1.TicketNo = TOS1.TicketNo
        */

    INNER JOIN TrainOccurance AS TO1 
        ON T1.NameOfRoute = TO1.NameOfRoute AND  T1.RunDate = TO1.RunDate --ENDRET!! ta med lenger opp
    INNER JOIN TrainRoute AS TR1
        ON TO1.NameOfRoute = TR1.Name
   INNER JOIN RouteStop AS RS1
        ON TR1.Name = RS1.NameOfRoute       
    INNER JOIN Placement AS P 
        ON T1.PlaceNo = P.PlaceNo
    INNER JOIN CarInTrain
        ON P.CarID = CarInTrain.CarID

    INNER JOIN

    (SELECT RS2.TimeOfDay, T2.OrderID  -- Finding EndStop Arrival Time   --Join on OrderID
    FROM Customer as C2 
        INNER JOIN CustomerOrder AS CO2 
                ON C2.CustomerID = CO2.CustomerID
            INNER JOIN Ticket AS T2
                ON CO2.OrderID = T2.OrderID
                /*
            INNER JOIN TicketOnSection AS TOS2
                ON T2.TicketNo = TOS2.TicketNo
                */
            INNER JOIN TrainOccurance AS TO2 
                ON T2.NameOfRoute = TO2.NameOfRoute AND  T2.RunDate = TO2.RunDate
            INNER JOIN TrainRoute AS TR2
                ON TO2.NameOfRoute = TR2.Name
            INNER JOIN RouteStop AS RS2
                ON TR2.Name = RS2.NameOfRoute
    WHERE 
        --RS2.Station =  T2.EndStation --TOS2.EndStation 
         C2.CustomerID = :customer_id) sub_query

    ON (sub_query.OrderID = T1.OrderID)

 WHERE 
         RS1.Station = T1.StartStation--TOS1.StartStation 
        AND
        C1.CustomerID = :customer_id
        AND
        TO1.RunDate >=  DATE()


