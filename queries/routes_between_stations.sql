/*
User input:
    date_
    start_station
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
    RS.Station = :start_station AND RS2.Station = :end_station AND TOCC.RunDate = :date_
    --ORDER BY TOCC.Rundate ASC, RS.TimeOfDay ASC

UNION

SELECT DISTINCT TR.Name, RS.TimeOfDay, TOCC.RunDate
FROM 
    ((TrainOccurance AS TOCC INNER JOIN TrainRoute AS TR 
    ON (TOCC.NameOfRoute = TR.Name))
    INNER JOIN RouteStop AS RS 
    ON (TR.Name = RS.NameOfRoute)) 
    INNER JOIN RouteStop AS RS2 ON (RS.NameOfRoute = RS2.NameOfRoute)
    WHERE
    RS.Station = :start_station AND RS2.Station = :end_station AND TOCC.RunDate = (SELECT DATE(:date_, '+1 day'))
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
