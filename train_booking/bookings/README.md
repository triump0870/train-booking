IRCTC
Search page - from station, to station, DOJ (flexible), number of seats
Train - train no, train name, time on from station, number of seats available

T1 - D1 - total 5 seats - A -> Z
Seat1 A->B C->Z
Seat2 A->B
Seat3 A->C
Seat4 A->C
Seat5 B->C

Want to book 1 seat from A->C: 0 seats T1-D1 should not come in the results
Want to book 3 seat from C->E: 4 seats T1-D1 should come in the results
Want to book 5 seat from C->E: 4 seats T1-D1 should not come in the results

1. id
2. DB


Trains = 50000
Stations = 50000
Train goes stations = 100
Seats in Train = 1000



# Installation Guide

1. clone the repo
2. Create a conda/python virtual env on python 3.8
3. pip install -r requirements/local.txt
4. ./manage.py migrate
5. ./manage.py loaddata data/fixture.json
6. ./manage.py runserver

admin user: demo
admin pass: demo@1234
