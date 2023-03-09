# TDT4145 - databases project
Semester project for the courese TDT4145 Data Modelling and Database Systems offered at NTNU Trondheim.


Forslag til ER-diagram tegner:
- https://dbdiagram.io/home?utm_referrer=https%3A%2F%2Fwww.google.com%2F
- https://drawsql.app/teams/anonyme-funksjonelt-avhengige/diagrams/databaser-prosjekt
- https://www.quickdatabasediagrams.com/?utm_referrer=https%3A%2F%2Fwww.google.com%2F


## Condenced problem description:

`Entity`, **attribute**

### TrackSection

- Starts at a `RailwayStation`
- Passes through a number of `RailwayStation`s
- Ends at a `RailwayStation`
- Has a **Name**
- Equiped for a driving energy (either diesel or electric)
- Consist of a number of `SubSection`s
- `TrainRoute`s run on track sections, they either run in the sections main
  direction or opposite
- A `TrainRoute` can run the entire track section or only parts of it


### SubSection

- A number of subsections build a `TrackSection`
- Runs between two `RailwayStation`s 
- Has **Length** in km
- Track specification (either single- or double track)

### RailwayStation

- Is the start and end of `TrackSection`s
  - ^ Same, but with `TrainRoute` aswell
- Passed through by `TrackSection`s
  - ^ Same, but with `TrainRoute` aswell
  - Has an arrival/departure time for each stop in a `TrainRoute` instance
- Is the endpoints of a `SubSection`
- Has a unique **Name**
- Has the **Altitude** of the station (mals - meters above sea level)
- A ticket reserves a space from one station to another on a `TrainRoute`


### TrainRoute

- Runs on `TrackSection`s, may run in the main direction or opposite
- Can run the entire `TrackSection` or parts of it
- Has a start - and end `RailwayStation`






