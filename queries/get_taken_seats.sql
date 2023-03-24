/*
Input:  run_date, 
        name_of_route, 
        car_id, 
        start_sec_no, (the start-subsection-number for the booking start_station)
        end_sec_no (the end-subsection-number for the booking end_station)
*/

/* Old attempt
SELECT Placement.PlaceNo
FROM
    Ticket INNER JOIN TicketOnSection
        ON (Ticket.TicketNo = TicketOnSection.TicketNo)
    INNER JOIN Placement 
        ON (Ticket.PlaceNo = Placement.PlaceNo 
        AND Ticket.CarID = Placement.CarID )
WHERE Placement.CarID = :car_id AND TicketOnSection.StartStation = :start_station
    AND TicketOnSection.EndStation = :end_station AND Ticket.RunDate = :run_date
    AND Ticket.NameOfRoute = :name_of_route;
*/

SELECT T.PlaceNo
FROM Ticket AS T
    INNER JOIN TrackSubSection AS TSS1
        ON T.StartStation = TSS1.StartsAt
    INNER JOIN TrackSubSection AS TSS2
        ON T.EndStation = TSS2.EndsAt
WHERE ((TSS1.SubSectionNo <= :start_sec_no AND TSS2.SubSectionNo >= :start_sec_no)
        OR (TSS1.SubSectionNo <= :end_sec_no AND TSS2.SubSectionNo >= :end_sec_no))
    AND T.RunDate = :run_date
    AND T.NameOfRoute = :name_of_route
    AND T.CarID = :car_id
