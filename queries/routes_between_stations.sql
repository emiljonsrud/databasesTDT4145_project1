/*
User input:
    dato
    start_stationSELECT TR.Name
FROM 
    (TrainOccurance AS TOCC INNER JOIN TrainRoute AS TR 
    ON (TOCC.NameOfRoute = TR.Name))
    INNER JOIN RouteStop AS RS 
    ON (:start_station = RS.NameOfRoute AND :end_station = RS.NameOfRoute)
WHERE TOCC.RunDate = :dato;
    end_station
*/



SELECT DISTINCT TR.Name, RS.TimeOfDay, TOCC.RunDate
FROM 
    ((TrainOccurance AS TOCC INNER JOIN TrainRoute AS TR 
    ON (TOCC.NameOfRoute = TR.Name))
    INNER JOIN RouteStop AS RS 
    ON (TR.Name = RS.NameOfRoute)) 
    INNER JOIN RouteStop AS RS2 ON (RS.NameOfRoute = RS2.NameOfRoute)
    WHERE
    RS.Station = :start_station AND RS2.Station = :end_station AND (TOCC.RunDate = :dato OR TOCC.RunDate = :dato +1)
    ORDER BY TOCC.Rundate ASC, RS.TimeOfDay ASC;





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