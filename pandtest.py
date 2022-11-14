#! /usr/bin/python3
from pand import Board
from pand import Solver
import time

debug = 0


def main():
   print('Enter number of cities: ', end = "")
   cities = input()
   cities = int(cities)

   print('Enter epicenter : ', end = "")
   epi = input()
   epi = int(epi)
   if epi > cities:
       print('Cannot have epicenter larger than the number of cities')
       exit

   myboard = Board(cities, epi)
   #myboard.move(0)
   #myboard.move(1)
   #myboard.move(1)

   solver = Solver(myboard)
   start = time.time()
   loc = solver.solve()
   end = time.time()
   print('Epicenter is: ', loc, 'Elapsed Time: ', (end-start))

if __name__ == "__main__":
    main()



