import heapq
import numpy as np

class Node:
    def __init__(self, state, n, parent, current):
        self.state = state #list of cities visited yet
        self.dist = 0 #distance coveres yet
        self.h = 0 # H(x) value
        self.n = n #no of cities visited yet
        self.parent = parent
        self.current = current #last visited city
        self.f = 0 # f(x) value

    def __lt__(self, other):
        return self.f < other.f


class A_star:
    def __init__(self, tsp):
        self.tsp = tsp


    #returns distance between 2 cities
    def distance_btw(self, c1, c2):
        return self.tsp.distance_btw(c1, c2)


    def calculate_f(self, node):
        node.f = node.dist - node.h


    # g(x) = distance covered
    def calculate_g(self, node):
        parent = node.parent 
        last = parent.current #last visited city
        new = node.current #the newly visited city

        #New path added in route is the edge btw 'last' and 'new'
        node.dist = parent.dist + self.tsp.distance_btw(new, last)


    # H(x) 
    def calculate_h(self, node):
        parent = node.parent
        new = node.current #the new city added to the route

        dist_eli = 0 #tot distance eliminated by adding 'new' city to the route

        for i in range(node.n - 1):
            city = node.state[i] #ith city in the route

            #add dist btw new city and ith city to eliminated distance
            dist_eli += self.tsp.distance_btw(city, new) 
        node.h = parent.h + dist_eli


    ############################ solve TSP #######################
    #returns route, dist pair
    def run(self, epochs):
        solutions = [] #(route, dist) pairs
            #solution when starting from the ith city

        e = 0 #iterations
        for i in range(self.tsp.n):
            #start from the city with the least no of neighbours
            start_city = self.tsp.cities[i]
            root = Node([start_city], 1, None, start_city)

            #priority queue (aka open list)
            queue = []
            heapq.heappush(queue, (root.f, root))

            # visit one city at atime
            while queue and e<epochs:
                #get the node with the lowest f value
                front = heapq.heappop(queue)[1]

                # if all cities have been visited, then tour is complete
                if front.n == self.tsp.n:
                    #revisit the starting city
                    front.state.append(start_city)
                    front.dist += self.distance_btw(front.current, start_city)

                    solutions.append((front.state, front.dist))
                    break 

                # Which cities can be visited next?
                current_city = front.current #last visited city in the current state
                neighbours = [c for c in self.tsp.cities if c not in front.state]
                m = len(neighbours)

                #if the current city has no neighbours, then this node is a deadend
                if m == 0:
                    continue

                #create 'm' child nodes, each visiting one neighbour
                for i in range(m):
                    next_city = neighbours[i]

                    #generate child node
                    temp = Node(front.state + [next_city], front.n + 1, front, next_city)

                    #calculate f, g, h for child node
                    self.calculate_g(temp)
                    self.calculate_h(temp)
                    self.calculate_f(temp)

                    #push child node to queue
                    heapq.heappush(queue, (temp.f, temp))

                    #increment iteration number
                    e = e + 1

        # check the best route found
        print("No of full routes complted = ", len(solutions))
        
        min_dist = solutions[0][1]
        min_route = solutions[0][0]

        for sol in solutions: #sol = (state, dist)
            if sol[1] < min_dist:
                #update
                min_dist = sol[1]
                min_route = sol[0]
        
        return min_route, min_dist