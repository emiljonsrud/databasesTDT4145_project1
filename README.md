# TDT4145 - databases project
Semester project for the courese TDT4145 Data Modelling and Database Systems offered at NTNU Trondheim.



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
- Has a start - and end `RailwayStation` "usually stops inbetween"
  - For each `RailwayStation` we have arrival/departure time
- Runs *at most* once per day, it must be recorded on which days of the week the
  route runs from the start `RailwayStation`
- Operated by an `Operator`
- Has a fixed `CarArrangement` made up of available `Car` types
- Has a fixed `Timetable` with **departure/arrival** times for each
  `RailwayStation` on the route
- Has a `Train` occurrence for each day the route is operated
- To travel a route, a `Customer` buys a `Ticket` for one or more
  seats in a `Train` occurrence
  - A `Ticket` reserves a space from one `RailwayStation` on the route to another
  - If someone has a `Ticket` for one or more beds on part of the route, we do not
    sell the seats in the compartment to others


### Operator

- Operates a `TrainRoute`
- Has a number of `Car` types
- All operators have a common `CustomerRegistry`


### Customer

- Can buy `Ticket`s to one or more seats in a `Train` occurance
- Has unique **CustomerID**
- Has **Name**, **EmailAddress** and **MobileNo**
- Can buy one or two places in a sleeping compartment (in `Car`)


### CarArrangement

- `TrainRoute` has fixed car arrangement
- Made up of available `Car` types
- The `Cars` are numbered from the fromnt to the back of the `Train`

### Train

- Occures each day the `TrainRoute` is operated
- To travel a `TrainRoute` a `Customer` buys a `Ticket` for
  one or more seats in the train occurance

### Ticket

- A `Customer` buys a ticket for one or more seats in the `Train` occurance
- To purchase tickets, one must be registered as a customer in the operators' 
  common `CustomerRegistry`
- Applies to either a seat in a cair `Car` or bed in sleep `Car` and reserves the
  space from one `RailwayStation` to another on the `TrainRoute`
- Is organized into a `CustomerOreder` (?) that has a unique **OrderNumber**
  **Day** and **Time** of purchase, and a number of ticket purchases in the Same
  `Train` occurance
- Not possivle to buy tickes to seats that are sold (on the same route intervall)

### 


