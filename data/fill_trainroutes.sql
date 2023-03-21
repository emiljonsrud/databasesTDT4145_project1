-- SQL script for togruter
/*
    RouteStop
    TrainRoute
*/

INSERT INTO TrainRoute(Name, Operator, SectionName)
VALUES
    ("Dagtog-Trondheim-Bodø", "SJ", "Nordlandsbanen"),
    ("Nattog-Trondheim-Bodø", "SJ", "Nordlandsbanen"),
    ("Morgentog-Mo_i_Rana-Trondheim", "SJ", "Nordlandsbanen");

INSERT INTO RouteStop(Station, NameOfRoute, TimeOfDay)
VALUES
    ("Trondheim", "Dagtog-Trondheim-Bodø", '07:49'), --Eller Trondheim S?
    ("Steinkjer", "Dagtog-Trondheim-Bodø", '09:51'),
    ("Mosjøen", "Dagtog-Trondheim-Bodø", '13:20'),
    ("Mo i Rana", "Dagtog-Trondheim-Bodø", '14:31'),
    ("Fauske", "Dagtog-Trondheim-Bodø", '16:49'),
    ("Trondheim", "Nattog-Trondheim-Bodø", '23:05'),
    ("Steinkjer", "Nattog-Trondheim-Bodø", '00:57'),
    ("Mosjøen", "Nattog-Trondheim-Bodø", '04:41'),
    ("Mo i Rana", "Nattog-Trondheim-Bodø", '05:55'),
    ("Fauske", "Nattog-Trondheim-Bodø", '08:19'),
    ("Bodø", "Nattog-Trondheim-Bodø", '09:05'),
    ("Mo i Rana", "Morgentog-Mo_i_Rana-Trondheim", '08:11'),
    ("Mosjøen", "Morgentog-Mo_i_Rana-Trondheim", '09:14'),
    ("Steinkjer", "Morgentog-Mo_i_Rana-Trondheim", '12:31'),
    ("Trondheim", "Morgentog-Mo_i_Rana-Trondheim", '14:13');

    