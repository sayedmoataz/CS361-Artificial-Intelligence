from igraph import *
import math
import random
import numpy
from functools import reduce
import sys
import getopt
import random
alfa = 2
beta = 5
iterations = 500
ro = 0.8 #التبخر
vehicle = 4
sigm = 3 #Q capacity
th = 80
depotcustomer=[2,1]
vertices = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22]
for i in depotcustomer:
    vertices.remove(i)
def generateGraph():
    #dataset
    capacityLimit = 6000
    optimalValue=375
    demand = {1: 0, 2: 1100, 3: 700, 4: 800, 5: 1400, 6: 2100, 7: 400, 8: 800, 9: 100, 10: 500, 11: 600, 12: 1200, 13: 1300, 14: 1300, 15: 300, 16: 900, 17: 2100, 18: 1000, 19: 900, 20: 2500, 21: 1800, 22: 700}
    #print(demand)
    #cities(x,y)
    graph = {1: (145, 215), 2: (151, 264), 3: (159, 261), 4: (130, 254), 5: (128, 252), 6: (163, 247), 7: (146, 246), 8: (161, 242), 9: (142, 239), 10: (163, 236), 11: (148, 232), 12: (128, 231), 13: (156, 217), 14: (129, 214), 15: (146, 208), 16: (164, 208), 17: (141, 206), 18: (147, 193), 19: (164, 193), 20: (129, 189), 21: (155, 185), 22: (139, 182)}
    #cities
    vertices = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22]
    for i in depotcustomer:
        vertices.remove(i)
    #vertices.remove(1)
    #for i in depotcustomer:
     #   vertices.remove(i)
        
    #distances  ((x0-y0)+(x1-y1))^2
    edges = { (min(a,b),max(a,b)) : numpy.sqrt((graph[a][0]-graph[b][0])**2 + (graph[a][1]-graph[b][1])**2) for a in graph.keys() for b in graph.keys()}
    #print (vertices)
    #initialize pheromones between cities to 1
    pheromones = { (min(a,b),max(a,b)) : 1 for a in graph.keys() for b in graph.keys() if a!=b }

    return vertices, edges, capacityLimit, demand, pheromones, optimalValue

def solutionOfOneAnt(vertices, edges, capacityLimit, demand, pheromones):
    solution = list()
    while(len(vertices)!=0):
        path = list()
        city = numpy.random.choice(vertices)
        #demand: the original delivery quantity to customer
        #capacity Q : the capacity for each vehicle.
        capacity = capacityLimit - demand[city]
        
        path.append(city)
        vertices.remove(city)#visited
        #print(str(vertices)+"/ city: "+str(city))
        while(len(vertices)!=0):
            probabilities = list(map(lambda x: ((pheromones[(min(x,city), max(x,city))])**alfa)*((1/edges[(min(x,city), max(x,city))])**beta), vertices))
            probabilities = probabilities/numpy.sum(probabilities)
            
            city = numpy.random.choice(vertices, p=probabilities)
            
            capacity = capacity - demand[city]

            if(capacity>0):
                path.append(city)
                vertices.remove(city)#visited
                #print(str(vertices)+"/ city: "+str(city))
            else:
                break
        
        solution.append(path)
    return solution

def rateSolution(solution, edges):
    sum = 0
    for i in solution:
        a = 1
        for j in i: 
            b = j 
            sum = sum + edges[(min(a,b), max(a,b))]
            a = b
        b = 1
        sum = sum + edges[(min(a,b), max(a,b))]
    return sum

def updateFeromone(pheromones, solutions, bestSolution):
    Lavg = reduce(lambda x,y: x+y, (i[1] for i in solutions)) / len(solutions)
    #decreament
    pheromones = { k : (ro + th/Lavg)*v for (k,v) in pheromones.items() }
    solutions.sort(key = lambda x: x[1])
    if(bestSolution!=None):
        if(solutions[0][1] < bestSolution[1]):
            bestSolution = solutions[0]
        for path in bestSolution[0]:
            for i in range(len(path)-1):
                #increament
                pheromones[(min(path[i],path[i+1]), max(path[i],path[i+1]))] = sigm/bestSolution[1] + pheromones[(min(path[i],path[i+1]), max(path[i],path[i+1]))]
    else:
        bestSolution = solutions[0]
    for l in range(sigm):
        paths = solutions[l][0]
        L = solutions[l][1]
        for path in paths:
            for i in range(len(path)-1):
                pheromones[(min(path[i],path[i+1]), max(path[i],path[i+1]))] = (sigm-(l+1)/L**(l+1)) + pheromones[(min(path[i],path[i+1]), max(path[i],path[i+1]))]
    return bestSolution

def main():
    bestSolution = None
    f_path =random.choice(depotcustomer)
    depotcustomer.remove(f_path)
    print ("number depot",f_path)
    vertices, edges, capacityLimit, demand, pheromones, optimalValue = generateGraph()
    for i in range(iterations):

        solutions = list()
        for _ in range(vehicle):
            solution = solutionOfOneAnt(vertices.copy(), edges, capacityLimit, demand, pheromones)#update ant
            solutions.append((solution, rateSolution(solution, edges)))
        bestSolution = updateFeromone(pheromones, solutions, bestSolution)
        print("i:"+str(i)+ " bestsolution:"+str(bestSolution[1]))
    #graph
    G= Graph()
    for y in range(1,len(vertices)+2): G.add_vertex(y)
    G.vs["label"]=[str(a) for a in range(1,len(vertices)+2)]
    u = {m:"blue" for m in range(1,len(vertices)+2)}
    #w is 1D of all paths inside solutions

   # f_path =random.randint(1,2)
    #print(type(f_path))
    #random.shuffle(f_path)
    #print("Depot:",f_path)
    u.update({f_path:"red"})
    G.vs["color"] = [u[int(p)] for p in G.vs["label"] ]
    for w in bestSolution[0]:
        for i in range(len(w)):
            if i==0:
                idx_n = int(w[i])-1
                G.add_edges([(idx_n,f_path-1)])
            n = i+1
            idx_i = int(w[i])-1
            idx_n = 0
            if i==len(w)-1:
                idx_n = f_path-1
            else:
                idx_n = int(w[n])-1
            G.add_edges([(idx_i,idx_n)])
    layout= G.layout("kk")
    plot(G,layout=layout)
    return bestSolution
for i in range(2):
    solution = main()
    print("Solution: "+str(solution))