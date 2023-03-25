/*
User input:
    :date_
    :time_
    :start_station
    :end_station
*/


SELECT DISTINCT TR.Name , TOc.RunDate, RS1.Station, RS1.TimeOfDay, RS2.Station, RS2.TimeOfDay
FROM TrainRoute AS TR
    INNER JOIN TrainOccurance AS TOc
        ON TR.Name = TOc.NameOfRoute
    INNER JOIN RouteStop AS RS1
        ON TR.Name = RS1.NameOfRoute
    INNER JOIN RouteStop AS RS2
        ON TR.Name = RS2.NameOfRoute
    LEFT OUTER JOIN TrackSubSection AS TSS1
        ON RS1.Station = TSS1.StartsAt
    LEFT OUTER JOIN TrackSubSection AS TSS2
        ON RS2.Station = TSS2.StartsAt
WHERE 
    RS1.Station = :start_station AND RS2.Station = :end_station 
    AND (     
        (TR.SectionMainDirection = 1  AND TSS1.SubSectionNo < TSS2.SubSectionNo) 
        OR (TR.SectionMainDirection = 0 AND TSS1.SubSectionNo > TSS2.SubSectionNo)
        OR (TR.SectionMainDirection = 0 AND TSS1.SubSectionNo = NULL)
    ) 
    AND TOc.RunDate = :date_
    AND RS1.TimeOfDay >= :time_

UNION 

SELECT DISTINCT TR.Name , TOc.RunDate, RS1.Station, RS1.TimeOfDay, RS2.Station, RS2.TimeOfDay
FROM TrainRoute AS TR
    INNER JOIN TrainOccurance AS TOc
        ON TR.Name = TOc.NameOfRoute
    INNER JOIN RouteStop AS RS1
        ON TR.Name = RS1.NameOfRoute
    INNER JOIN RouteStop AS RS2
        ON TR.Name = RS2.NameOfRoute
    LEFT OUTER JOIN TrackSubSection AS TSS1
        ON RS1.Station = TSS1.StartsAt
    LEFT OUTER JOIN TrackSubSection AS TSS2
        ON RS2.Station = TSS2.StartsAt
WHERE 
    RS1.Station = :start_station AND RS2.Station = :end_station AND
    (     
    ( TR.SectionMainDirection = 1  AND TSS1.SubSectionNo < TSS2.SubSectionNo) 
     OR (TR.SectionMainDirection = 0 AND TSS1.SubSectionNo > TSS2.SubSectionNo)
     OR (TR.SectionMainDirection = 0 AND TSS1.SubSectionNo = NULL)
    ) 
    AND TOc.RunDate = (SELECT DATE(:date_, '+1 day'))
    ORDER BY TOc.Rundate ASC, RS1.TimeOfDay ASC;
