/*
Input: run_date, name_of_route, car_id, 
       start_station, end_station
*/

SELECT Placement.PlaceNo
FROM
    Ticket INNER JOIN TicketOnSection
        ON (Ticket.TicketNo = TicketOnSection.TicketNo)
    INNER JOIN Placement 
        ON (Ticket.PlaceNo = Placement.PlaceNO)
WHERE Placement.CarID = :car_id AND TicketOnSection.StartStation = :start_station
    AND TicketOnSection.EndStation = :end_station AND Ticket.RunDate = :run_date
    AND Ticket.NameOfRoute = :name_of_route;


