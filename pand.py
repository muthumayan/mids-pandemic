#! /usr/bin/python3

debug = 0

LEFT = 0
RIGHT = 1

class Board:
   def __init__(self, size, epicenterCity):
       if epicenterCity > size:
           print('Epicenter ', epicenterCity, ' cannot exceed total cities ', size)
           return 
       self.size = size
       self.caseload = {}
       self.caseload[epicenterCity] = 1

       if debug:
           print('Old:')
           for i in sorted(self.caseload):
               print(self.caseload[i], end='')
               print()

   def move(self, cityid):
       if cityid in self.caseload:
           currcaseload = self.caseload[cityid]
       else:
           currcaseload = 0

       newnbrs = []
       for k, v in self.caseload.items():
           if v == 1:
               # keep track of keys with value 1, we need to
               # create new neighbors
               newnbrs.append(k)
           self.caseload[k] = v+1

       for nbr in newnbrs:
           if nbr-1 not in self.caseload and nbr-1 >= 0:
               self.caseload[nbr-1] = 1
           if nbr+1 not in self.caseload and nbr+1 <= self.size:
               self.caseload[nbr+1] = 1

       if debug:
           print('Checking location ' + str(cityid) + ", Value: ", str(currcaseload))
           print('New:')
           for i in sorted(self.caseload):
               print(i, ':', self.caseload[i], ' ', end='')
           print()

       return(currcaseload)



class Solver:
    def __init__(self, board):
        self.board = board

    def solve(self):
        '''
            This method works with both a manipulated board and a clean slate board.
            A manipulated board is one where the 'move' method has been invoked 
            outside of the solve method. A clean board starts with a clean board with
            no 'moves'. 
        '''
        epicenter = 0
        num_cities = self.board.size

        # divide the entire space into partitions. If the number of cities is very
        # small, then each each city becomes a partition
        if num_cities > 10:
            num_partitions = 10
        else:
            num_partitions = num_cities

        # compute each partition size
        part_size = int(num_cities/num_partitions)

        # expected spread in the epicenter
        exp_spread_in_epicenter = 1
        city = 0

        # The progresssion of these for loops below is as follows:
        # Assunming a partition size of 100 and 10 partitions (for a 1000 cities):
        # The scan goes:
        #     0, 100, 200, 300, ...
        #     1, 101, 201, 301, ...
        for i in range(0,part_size):
            for j in range(num_partitions):
                city = (j * part_size) + i

                spread = self.board.move(city)
                exp_spread_in_epicenter += 1

                if debug:
                    print('Tested city ', city, 'return val: ', spread)

                # So long as the spread is zero, we need to continue scanning
                if spread == 0:
                    continue
                else:
                    # the first non-zero spread encountered. Let's see if the 
                    # path towards the epicenter is on the lhs or rhs or is this
                    # the center. To ascertain, we need to get a reading on the
                    # left and right of the current city.

                    reference_spread = spread

                    if city - 1 < 0:
                        # We are at the left edge, so the only way to go is
                        # right side
                        direction = RIGHT
                    elif city + 1 > num_cities:
                        # We are at the right edge, so the only way to go is
                        # left side
                        direction = LEFT
                    else:
                        lhs = self.board.move(city-1)
                        exp_spread_in_epicenter += 1
                    
                        rhs = self.board.move(city+1)
                        exp_spread_in_epicenter += 1
 
                        if lhs < reference_spread+1 and rhs > reference_spread+2:
                            direction = RIGHT
                        elif lhs > reference_spread+1 and rhs < reference_spread+2:
                            direction = LEFT
                        elif lhs < reference_spread+1 and rhs < reference_spread+2:
                            # both lhs and rhs sides are smaller. So, this must be 
                            # the epicenter
                            return(city)
                        else:
                            print('Wrong result')

                        # since we have tested two times already
                        # we add one more to reflect the actual in-mem value
                        reference_spread += 3

                        if direction == LEFT:
                            # move by exp_spread_in_epicenter to left
                            for i in range(1,num_cities):
                                ## check_city = city - exp_spread_in_epicenter - i
                                check_city = city - i
                                lhs = self.board.move(check_city)
                                exp_spread_in_epicenter += 1
                                if lhs <= reference_spread:
                                    print('LEFT ', check_city+1)
                                    return(check_city+1)
                                else:
                                    reference_spread = lhs
                        if direction == RIGHT:
                            # move by exp_spread_in_epicenter to right
                            for i in range(1,num_cities):
                                # check_city = city + exp_spread_in_epicenter + i
                                check_city = city + i
                                rhs = self.board.move(check_city)
                                exp_spread_in_epicenter += 1
                                if rhs <= reference_spread:
                                    print('RIGHT ', check_city+1)
                                    return(check_city-1)
                                else:
                                    reference_spread = rhs



