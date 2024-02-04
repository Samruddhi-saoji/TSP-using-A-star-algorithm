from tsp import TSP
from A_star import A_star
import numpy as np
from random import random

####### creating a tsp ########
#randomly generate the cities
n = 12 #number of cities
cities = []
max_dist = 20000
for i in range(n) :
    tup = (max_dist*random(), max_dist*random(), i, i+1) #(x, y, index, name)
    cities.append(tup)

#the TSP problem
tsp = TSP(n, cities)

a_star = A_star(tsp)
route, dist = a_star.run()
print(route, dist)