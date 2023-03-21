
/*
This file is only for testing!
*/

INSERT INTO TrainRoute(Name, Operator, SectionName)
VALUES
    ("Nr1", "SJ", "NordlandsBanen" ),
    ("Nr2", "SJ", "NordlandsBanen");

INSERT INTO RouteStop(Station, NameOfRoute, TimeOfDay)
VALUES
    ("Steinkjer", "Nr1", '02:00'),
    ("Mosjøen", "Nr1", '03:00'),
    ("Steinkjer", "Nr2", '02:30'),
    ("Mosjøen", "Nr2", '05:00'),
    ("Mo i Rana", "Nr2", '06:00');


INSERT INTO TrainOccurance(RunDate, NameOfRoute)
VALUES
    ('2023-03-04', "Nr1"),
    ('2023-03-05', "Nr1"),
    ('2023-03-04', "Nr2"),
    ('2023-03-05', "Nr2");