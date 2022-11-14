#! /usr/bin/python3

debug = 0

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
            This method assumes that the board has not been manipulated prior to
            calling this method, i.e. the board is created afresh with a certain
            number of cities and an epicenter.
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
                    # difference in spread count between epicenter and current city
                    # this is an estimate. 
                    diff = abs(exp_spread_in_epicenter - spread) - 1
                    if debug:
                        print('exp_spread: ', exp_spread_in_epicenter, ' ', 'spread: ', spread)
                        print('diff: ', diff, ' ', 'possible_epicenter(s): ', city-diff, city+diff)
                    if (city - diff < 0):
                        #print("Epicenter: ", city+diff)
                        return(city+diff)
                    elif (city + diff > num_cities):
                        #print("Epicenter: ", city-diff)
                        return(city-diff)
                    else:
                        lhs = self.board.move(city-diff)
                        exp_spread_in_epicenter += 1
                        rhs = self.board.move(city+diff)
                        exp_spread_in_epicenter += 1
                        if lhs > rhs:
                            #print('Epicenter: ', city-diff)
                            return(city-diff)
                        else:
                            #print('Epicenter: ', city+diff)
                            return(city+diff)


