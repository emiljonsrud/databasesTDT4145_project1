
-- SQL script for Nordlandsbanen
/* Tables that should exists:
    TrackSection
    RailwayStation
    TrackSubsection
*/

INSERT INTO RailwayStation (Name, Height)
VALUES 
    ("Bodø", 4.1),
    ("Fauske", 34.0),
    ("Mo i Rana", 3.5),
    ("Mosjøen", 6.8),
    ("Steinkjer", 3.6),
    ("Trondheim", 5.1);


INSERT INTO TrackSection (Name, StartStation, EndStation)
VALUES 
    ("Nordlandsbanen", "Trondheim", "Bodø");


INSERT INTO TrackSubSection(SubSectionNo, SectionName, Distance, StartsAt, EndsAt)
VALUES
    (1, "Nordlandsbanen", 120, "Trondheim", "Steinkjer"),
    (2, "Nordlandsbanen", 280, "Steinkjer", "Mosjøen"),
    (3, "Nordlandsbanen", 90, "Mosjøen", "Mo i Rana"),
    (4, "Nordlandsbanen", 120, "Mo i Rana", "Fauske"),
    (5, "Nordlandsbanen", 60, "Fauske", "Bodø");

