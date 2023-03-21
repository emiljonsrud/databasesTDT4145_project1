/* User arguments:
  :weekday (WeekDay.Name)
  :station (RailwayStation.Name)
*/
SELECT DISTINCT TR.Name 
FROM RailwayStation AS RS 
  INNER JOIN TrackSubSection AS TSS 
    ON (RS.Name = TSS.StartsAt OR RS.Name = TSS.EndsAt)
  INNER JOIN TrackSection AS TS 
    ON (TSS.SectionName = TS.Name)
  INNER JOIN TrainRoute AS TR 
    ON (TS.Name = TR.SectionName)
  INNER JOIN DayOfRoute AS DOR
    ON (TR.Name = DOR.NameOfRoute)
  INNER JOIN WeekDay AS WD
    ON (DOR.NameOfDay = WD.Name)
WHERE WD.Name = :weekday 
  AND RS.Name = :station;
