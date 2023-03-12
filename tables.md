# Table overview
**Primary key**, *foreign key*

- Custumer(**CID**, Name, Email, PhoneNo)
    - CID ->> PhoneNo
    - CID ->> Name
    - CID ->> Emil
- Order(**OrderID**, OrderDate, OrderTime, NoOfTickets, *Custumer*)
    - OrderID -> OrderDate
    - OrderID -> OrderTime
    - OrderID -> NoOfTickets
    - ???
- Ticket(***Train***, ***Seat***, *Order*)
- Train(**Day**, *TrainRoute*)
- Seat(**SeatNo**, *Car*)
- CarInTrain(**CarNo**, *CarType*, *TrainRoute*)
