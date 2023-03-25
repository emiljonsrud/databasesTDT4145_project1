/*
User input:
    :date_
    :start_station
    :end_station
    :time_
*/


SELECT DISTINCT TR.Name, TOc.RunDate, RS1.Station, RS1.TimeOfDay, RS2.Station, RS2.TimeOfDay
FROM TrainRoute AS TR
    INNER JOIN TrainOccurance AS TOc
        ON TR.Name = TOc.NameOfRoute
    INNER JOIN TrackSection AS TS
        ON TR.SectionName = TS.Name
    INNER JOIN RouteStop AS RS1
        ON TR.Name = RS1.NameOfRoute
    INNER JOIN RouteStop AS RS2
        ON TR.Name = RS2.NameOfRoute
    LEFT OUTER JOIN TrackSubSection AS TSS1
        ON RS1.Station = TSS1.StartsAt
    LEFT OUTER JOIN TrackSubSection AS TSS2
        ON RS1.Station = TSS2.StartsAt
WHERE 
    (
        (TR.SectionMainDirection = 1 AND TSS1.SubSectionNo > TSS2.SubSectionNo)
        OR (TR.SectionMainDirection = 0 AND TSS1.SubSectionNo > TSS2.SubSectionNo)
        OR (TR.SectionMainDirection = 0 AND TSS1.SubSectionNo IS NULL)
    )
    AND (RS1.Station = :start_station AND RS2.Station = :end_station)
    AND TOc.RunDate >= :date_
    AND RS1.TimeOfDay >= :time_



/*
SELECT DISTINCT TR.Name, RS.TimeOfDay, TOCC.RunDate ---TODO   after tidspunkt !!!!!!!
FROM 
    ((TrainOccurance AS TOCC INNER JOIN TrainRoute AS TR 
        ON (TOCC.NameOfRoute = TR.Name))
    INNER JOIN RouteStop AS RS 
        ON (TR.Name = RS.NameOfRoute)) 
    INNER JOIN RouteStop AS RS2 
        ON (RS.NameOfRoute = RS2.NameOfRoute)
    INNER JOIN TrackSubSection AS TSS1
        ON (RS.Station = TSS1.StartsAt)
    INNER JOIN TrackSubSection AS TSS2
        ON (RS2.Station = TSS2.EndsAt)
    WHERE
    RS.Station = :start_station AND RS2.Station = :end_station AND TOCC.RunDate = :date_ 
    AND   RS.TimeOfDay >= :time_  AND  TSS1.SubSectionNo <= TSS2.SubSectionNo
    --ORDER BY TOCC.Rundate ASC, RS.TimeOfDay ASC

UNION

    
SELECT DISTINCT TR.Name, RS.TimeOfDay, TOCC.RunDate
FROM 
    ((TrainOccurance AS TOCC INNER JOIN TrainRoute AS TR 
        ON (TOCC.NameOfRoute = TR.Name))
    INNER JOIN RouteStop AS RS 
        ON (TR.Name = RS.NameOfRoute)) 
    INNER JOIN RouteStop AS RS2 
        ON (RS.NameOfRoute = RS2.NameOfRoute)
    INNER JOIN TrackSubSection AS TSS1
        ON (RS.Station = TSS1.StartsAt)
    INNER JOIN TrackSubSection AS TSS2
        ON (RS2.Station = TSS2.EndsAt)    
    WHERE
    RS.Station = :start_station AND RS2.Station = :end_station AND TOCC.RunDate = (SELECT DATE(:date_, '+1 day'))
    AND  TSS1.SubSectionNo <= TSS2.SubSectionNo
    ORDER BY TOCC.Rundate ASC, RS.TimeOfDay ASC;

*/


/*

SELECT DISTINCT TR.Name 
FROM 
    ((TrainOccurance AS TOCC INNER JOIN TrainRoute AS TR 
    ON (TOCC.NameOfRoute = TR.Name))
    INNER JOIN RouteStop AS RS 
    ON (TR.Name = RS.NameOfRoute))
    WHERE RS.Station = :start_station AND (TOCC.RunDate = :dato --AND RS.Station = :end_station;

INTERSECT

SELECT DISTINCT TR.Name
FROM 
    ((TrainOccurance AS TOCC INNER JOIN TrainRoute AS TR 
    ON (TOCC.NameOfRoute = TR.Name))
    INNER JOIN RouteStop AS RS 
    ON (TR.Name = RS.NameOfRoute))
    WHERE RS.Station = :end_station AND TOCC.RunDate = :dato; --AND RS.Station = :end_station;*/

    --ON (RS.Station = :start_station AND RS.Station = :end_station) 

--WHERE TOCC.RunDate = :dat, "end_station": "Mosjøen"o;
--ORDER BY TO.TIME;


--UNION --Sorting?
