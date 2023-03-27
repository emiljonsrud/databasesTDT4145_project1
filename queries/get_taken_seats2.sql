/*
Input:  run_date, 
        name_of_route, 
        car_id, 
        start_station, (the start-subsection-number for the booking start_station)
        end_station (the end-subsection-number for the booking end_station)
*/

SELECT DISTINCT T.PlaceNo,  TssQueryStart.SubSectionNo, TssQueryEnd.SubSectionNo , TssTicketStart.SubSectionNo, TssTicketEnd.SubSectionNo
FROM TrainOccurance AS TOC 
    INNER JOIN TrainRoute AS TR
       ON TR.Name = TOC.NameOfRoute
    INNER JOIN Ticket AS T
        ON T.NameOfRoute = TOC.NameOfRoute AND  T.RunDate = TOC.RunDate 
    INNER JOIN Ticket AS T2
        ON T2.NameOfRoute = TOC.NameOfRoute AND  T2.RunDate = TOC.RunDate 

    
    LEFT OUTER JOIN TrackSubSection AS TssTicketStart
        ON TssTicketStart.StartsAt = T.StartStation 
    LEFT OUTER JOIN TrackSubSection AS TssTicketEnd
        ON TssTicketEnd.StartsAt = T.EndStation 

    LEFT OUTER JOIN TrackSubSection AS TssQueryStart
        ON TssQueryStart.StartsAt = T2.StartStation
        
    LEFT OUTER JOIN TrackSubSection AS TssQueryEnd
        ON TssQueryEnd.StartsAt = T2.EndStation
        

WHERE 
   (TR.SectionMainDirection = 1 AND TssTicketStart.SubSectionNo < TssQueryStart.SubSectionNo AND TssTicketEnd.SubSectionNo IS NULL)
   OR
    (TR.SectionMainDirection = 1 AND TssTicketStart.SubSectionNo < TssQueryStart.SubSectionNo AND TssTicketEnd.SubSectionNo > TssQueryStart.SubSectionNo)
       -- OR (TssTicketStart.SubSectionNo < TssQueryEnd.SubSectionNo AND TssTicketEnd.SubSectionNo > TssQueryEnd.SubSectionNo))
    AND 
    T.RunDate = :run_date
    AND
    T2.RunDate = :run_date
    AND T.NameOfRoute = :name_of_route
    AND T.CarID = :car_id
    AND T2.CarID = :car_id
    AND TssQueryStart.StartsAt = :start_station
    AND TssQueryEnd.StartsAt= :end_station;
   -- AND TrainRoute.Name

/*
SELECT DISTINCT T.PlaceNo
    FROM Ticket AS T
        INNER JOIN TrainRoute AS TR
            ON T.NameOfRoute = TR.Name
        LEFT OUTER JOIN TrackSubSection AS TssTicketStart
            ON T.StartStation = TssTicketStart.StartsAt
        LEFT OUTER JOIN TrackSubSection AS TssTicketEnd
            ON T.EndStation = TssTicketEnd.StartsAt
        INNER JOIN TrackSubSection AS TssQueryStart
            ON  TR.SectionName = TssQueryStart.SectionName
            AND ((TR.SectionMainDirection=1 AND TssQueryStart.StartsAt = :start_station)
                OR (TR.SectionMainDirection=0 AND TssQueryStart.EndsAt = :start_station))
        INNER JOIN TrackSubSection AS TssQueryEnd
            ON  TR.SectionName = TssQueryEnd.SectionName
            AND (TssQueryEnd.StartsAt = :end_station OR TssQueryEnd.EndsAt = :end_station)
    WHERE (TssQueryStart.SubSectionNo BETWEEN TssTicketStart.SubSectionNo AND TssTicketEnd.SubSectionNo)
        OR(TssQueryEnd.SubSectionNo BETWEEN TssTicketStart.SubSectionNo AND TssTicketEnd.SubSectionNo)

        AND TR.Name = :name_of_route
        AND T.CarID = :car_id
        AND T.RunDate = :run_date;
    /*
    WHERE (TssTicketStart.SubSectionNo NOT BETWEEN TssQueryStart.SubSectionNo AND TssQueryEnd.SubSectionNo)
            AND (TssTicketEnd.SubSectionNo NOT BETWEEN TssQueryStart.SubSectionNo AND TssQueryEnd.SubSectionNo);
    */
    /*
    WHERE (TssTicketStart.SubSectionNo > min(TssQueryStart.SubSectionNo, TssQueryEnd.SubSectionNo)
               AND TssTicketStart.SubSectionNo < max(TssQueryStart.SubSectionNo, TssQueryEnd.SubSectionNo))
        OR (TssTicketEnd.SubSectionNo > min(TssQueryStart.SubSectionNo, TssQueryEnd.SubSectionNo)
               AND TssTicketEnd.SubSectionNo < max(TssQueryStart.SubSectionNo, TssQueryEnd.SubSectionNo));
    */
        

/*
SELECT DISTINCT Ticket.PlaceNo
FROM Ticket
    INNER JOIN RouteStop AS RS1
        ON Ticket.NameOfRoute = RS1.NameOfRoute
    INNER JOIN RouteStop AS RS2
        ON Ticket.NameOfRoute = RS2.NameOfRoute
    INNER JOIN TrackSubSection AS TSS1
        ON RS1.Station = TSS1.StartsAt
           AND TSS1.StartsAt != :end_station
           AND TSS1.EndsAt BETWEEN :start_station AND :end_station
    INNER JOIN TrackSubSection AS TSS2
        ON RS2.Station = TSS2.StartsAt
           AND TSS2.StartsAt != :start_station
           AND TSS2.EndsAt BETWEEN :start_station AND :end_station
WHERE
    Ticket.NameOfRoute = :name_of_route
    AND Ticket.RunDate = :run_date
    AND Ticket.CarID = :car_id
    AND RS1.Station = :start_station
    AND RS2.Station = :end_station
    AND TSS1.SubSectionNo <= TSS2.SubSectionNo
    AND Ticket.PlaceNo NOT IN (
        SELECT DISTINCT Ticket.PlaceNo
        FROM Ticket
            INNER JOIN RouteStop AS RS1
                ON Ticket.NameOfRoute = RS1.NameOfRoute
            INNER JOIN RouteStop AS RS2
                ON Ticket.NameOfRoute = RS2.NameOfRoute
            INNER JOIN TrackSubSection AS TSS1
                ON RS1.Station = TSS1.StartsAt
                   AND TSS1.StartsAt != :end_station
                   AND TSS1.EndsAt BETWEEN :start_station AND :end_station
            INNER JOIN TrackSubSection AS TSS2
                ON RS2.Station = TSS2.StartsAt
                   AND TSS2.StartsAt != :start_station
                   AND TSS2.EndsAt BETWEEN :start_station AND :end_station
        WHERE
            Ticket.NameOfRoute = :name_of_route
            AND Ticket.RunDate = :run_date
            AND Ticket.CarID = :car_id
            AND RS1.Station = :start_station
            AND RS2.Station = :end_station
            AND TSS1.SubSectionNo <= TSS2.SubSectionNo
            AND (
                TSS1.EndsAt = :end_station
                OR TSS2.StartsAt = :start_station
            )
    );
*/