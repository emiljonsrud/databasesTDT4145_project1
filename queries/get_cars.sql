/* Paramaters
  :train_route
*/

SELECT CIT.CarID, CIT.CarNo, CC.NumOfRows, CC.SeatsPerRow, SC.NumOfCompartments
FROM CarInTrain AS CIT
  LEFT OUTER JOIN ChairCar AS CC
    ON CIT.CarID = CC.CarID
  LEFT OUTER JOIN SleepCar AS SC
    ON CIT.CarID = SC.CarID
WHERE CIT.NameOfRoute = :train_route;

