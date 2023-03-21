/* Paramaters
  :car_id
*/
SELECT * 
FROM CarInTrain
  RIGHT OUTER JOIN ChairCar
    ON CarID
  RIGHT OUTER JOIN SleepCar
    ON CarID
WHERE CarID = :car_id;

