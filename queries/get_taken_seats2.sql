/*
Input:  run_date, 
        name_of_route, 
        car_id, 
        start_station, (the start-subsection-number for the booking start_station)
        end_station (the end-subsection-number for the booking end_station)
*/


SELECT DISTINCT
    T.PlaceNo,
    TR.SectionMainDirection AS mainDir,
    T.StartStation AS tStart,
    T.EndStation AS tEnd
FROM 
    Ticket AS T
    INNER JOIN TrainRoute AS TR ON T.NameOfRoute = TR.Name
    INNER JOIN TrackSection AS TS ON TR.SectionName = TS.Name
    LEFT OUTER JOIN SleepCar ON SleepCar.CarID = T.CarID
    -- All sections covered by a ticket
    LEFT OUTER JOIN TrackSubSection AS eSec1 ON TR.SectionName = eSec1.SectionName
        AND ((tStart = eSec1.StartsAt AND mainDir = 1)
            OR (tStart = eSec1.EndsAt AND mainDir = 0))
    LEFT OUTER JOIN TrackSubSection AS eSec2 ON TR.SectionName = eSec2.SectionName
        AND ((tEnd = eSec2.EndsAt AND mainDir = 1)
            OR (tEnd = eSec2.StartsAt AND mainDir = 0))
    INNER JOIN TrackSubSection AS tCoveredSec ON TR.SectionName = tCoveredSec.SectionName
        AND (tCoveredSec.SubSectionNo BETWEEN eSec1.SubSectionNo AND eSec2.SubSectionNo)
        OR (tCoveredSec.SubSectionNo BETWEEN eSec2.SubSectionNo AND eSec1.SubSectionNo)
        OR (SleepCar.CarID IS NOT NULL) -- Ticket is sleep-car => whole section is booked
    -- Sections covered by query
    INNER JOIN TrainRoute AS qTR ON T.NameOfRoute = qTR.Name
        AND qTR.Name = :name_of_route
    LEFT OUTER JOIN TrackSubSection AS qSec1 ON TR.SectionName = qSec1.SectionName
        AND ((:start_station = qSec1.StartsAt AND mainDir = 1)
            OR (:start_station = qSec1.EndsAt AND mainDir = 0))
    LEFT OUTER JOIN TrackSubSection AS qSec2 ON TR.SectionName = qSec2.SectionName
        AND ((:end_station = qSec2.EndsAt AND mainDir = 1)
            OR (:end_station = qSec2.StartsAt AND mainDir = 0))
    INNER JOIN TrackSubSection AS qCoveredSec ON TR.SectionName = qCoveredSec.SectionName
        AND (qCoveredSec.SubSectionNo BETWEEN qSec1.SubSectionNo AND qSec2.SubSectionNo)
        OR (qCoveredSec.SubSectionNo BETWEEN qSec2.SubSectionNo AND qSec1.SubSectionNo)
WHERE
    qCoveredSec.SubSectionNo = tCoveredSec.SubSectionNo
    AND T.RunDate = :run_date
    AND T.CarID = :car_id