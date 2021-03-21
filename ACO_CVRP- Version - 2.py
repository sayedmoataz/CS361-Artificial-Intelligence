from igraph import *
import math
import random
import numpy
from functools import reduce
alfa = 2
beta = 5
iterations = 10
ro = 0.8 #التبخر
vehicle = 22
sigm = 3 #Q capacity
th = 80
def generate_demand(vehicle_num,capacity_limit):
    demand = dict()
    for i in range(1,vehicle_num+1):
        r = random.randint(1,capacity_limit+1)
        demand[i]=r
    return demand

def generate_edges(graph_dict,depots_info):
    edges = dict()
    for depot,customers in depots_info["customers"].items():
        edges[int(depot)]=dict()
        for b in customers:
            d = numpy.sqrt((graph_dict[depot][0]-graph_dict[b][0])**2 + (graph_dict[depot][1]-graph_dict[b][1])**2)
            edges[int(depot)].update({(min(depot,b),max(depot,b)):d})

        for a in customers:
        
            for b in customers:
                if a==b:
                    #جذر ((x0-y0)+(x1-y1))^2 
                    edges[int(depot)].update({(a,b):0.0})
                else:
                    d = numpy.sqrt((graph_dict[a][0]-graph_dict[b][0])**2 + (graph_dict[a][1]-graph_dict[b][1])**2)
                    edges[int(depot)].update({(min(a,b),max(a,b)):d}) 
                                   
    return edges

def generate_pheromones(depots_info):
    pheromones=dict()
    for depot,customers in depots_info["customers"].items():
        pheromones[int(depot)] = dict()
        for b in customers:
                pheromones[int(depot)].update({(min(depot,b),max(depot,b)):1})
        for a in customers:
            for b in customers:
                if a != b:
                    pheromones[int(depot)].update({(min(a,b),max(a,b)):1})
    return pheromones
def generate_graph(vehicle_num):
    graph = dict()
    for i in range(1,vehicle_num+1):
        r1 = random.randint(1,300)
        r2 = random.randint(1,300)
        graph[i]=(r1,r2)
    return graph
def generate_vertices(vehicle_num):
    vertices=list()
    for i in range(2,vehicle_num+1):
        vertices.append(i)
    return vertices
def use_random_set():
    #dataset
    capacityLimit = random.randit(4000,8000)
    optimalValue="unknown"
    vehicle = random.randit(10,30)
    demand = generate_demand(vehicle,capacityLimit)
    #cities(x,y)
    graph = generate_graph(vehicle)
    #cities
    vertices = generate_vertices(vehicle)
    vertices.remove(1)
    #distances  ((x0-y0)+(x1-y1))^2
    edges = generate_edges(graph)
    
    #initialize pheromones between cities to 1
    pheromones = generate_pheromones(graph)
    
    return vertices, edges, capacityLimit, demand, pheromones, optimalValue
def use_dataset():
    #dataset
    capacityLimit = 6000
    optimalValue=375
    depots=[1,25]
    demand = {1: 0, 2: 1100, 3: 700, 4: 800, 5: 1800, 6: 2100, 7: 400, 8: 800, 9: 100, 10: 500, 11: 600, 12: 1200, 13: 1300, 14: 1300, 15: 300, 16: 900, 17: 2100, 18: 1000, 19: 900, 20: 2500, 21: 1800, 22: 700 , 23: 500, 24: 600, 25: 0, 26: 1300, 27: 1300, 28: 300, 29: 900, 30: 2100, 31: 1000, 32: 900, 33: 2500, 34: 1800}
    #cities(x,y)
    graph = {1: (145, 215), 2: (151, 264), 3: (159, 261), 4: (130, 254), 5: (128, 252), 6: (163, 247), 7: (146, 246), 8: (161, 242), 9: (142, 239), 10: (163, 236), 11: (148, 232), 12: (128, 231), 13: (156, 217), 14: (129, 214), 15: (146, 208), 16: (164, 208), 17: (141, 206), 18: (147, 193), 19: (164, 193), 20: (129, 189), 21: (155, 185), 22: (139, 182), 23: (148, 232), 24: (128, 231), 25: (156, 217), 26: (129, 214), 27: (146, 208), 28: (164, 208), 29: (141, 206), 30: (147, 193), 31: (164, 193), 32: (129, 189), 33: (155, 185), 34: (139, 182)}
    #customers
    #vertices = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22]
    depots_info = {}
    depots_info= {"customers" : {1:[2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22],25:[23,24,26,27,28,29,30,31,32,33,34]},
                    "vehicle" : {1:15,25:10}}

    #distances  ((x0-y0)+(x1-y1))^2
    edges = generate_edges(graph,depots_info)
    
    #initialize pheromones between cities to 1
    pheromones = generate_pheromones(depots_info)
    
    return edges, capacityLimit, demand, pheromones, optimalValue, depots_info

def depots_info(depots,graph):
    g_customers= list()
    dists=dict()
    depots_list=list()
    #calc distance between i(100,150) and x(200,100)
    for i in range(1,len(graph)+1):
        for x in depots:
            if x != i:
                c = float(numpy.sqrt((graph[i][0]-graph[x][0])**2 + (graph[i][1]-graph[x][1])**2))
                dists[(x,i)]=c

        keys = list(dists.keys())
        val = list(dists.values())
        key = val.index(min(dists))
        depots_list["customers"][key[0]].append(key[1])
    #generate number of vehicles to each depot
    for d in depots:
        depots_list["vehicle"][d] = random.randit(10,30)

    return depots_list

def solutionOfOneAnt(vertices, edges, capacityLimit, demand, pheromones):
    solution = list()
    while(len(vertices)!=0):
        #initi go to first city (randomly)
        path = list()
        city = numpy.random.choice(vertices)
        #demand: the original delivery quantity to customer
        #capacity Q : the capacity for each vehicle.
        capacity = capacityLimit - demand[city]
        
        path.append(city)
        vertices.remove(city)#visited
        while(len(vertices)!=0):
            #
            #calc probability
            probabilities= list()
            for x in vertices:
                r = float((pheromones[(min(x,city), max(x,city))])**alfa)*((1/edges[(min(x,city), max(x,city))])**beta)
                probabilities.append(r)
            probabilities = probabilities/numpy.sum(probabilities)
            #choose random city from remaining based on probability
            city = numpy.random.choice(vertices, p=probabilities)
            capacity = capacity - demand[city]

            if(capacity>0):
                path.append(city)
                vertices.remove(city)#visited
            else:
                break
        
        solution.append(path)

    return solution

def rateSolution(solution, edges, depot):
    sum = 0
    for i in solution:
        a = depot
        for j in i:
            b = j
            sum = sum + edges[(min(a,b), max(a,b))]
            a = b
        b = depot
        sum = sum + edges[(min(a,b), max(a,b))]
    return sum

def update_pheromone(pheromones, solutions, bestSolution):
    #print(solutions)
    
    Lavg = reduce(lambda x,y: x+y, (i[1] for i in solutions)) / len(solutions)
    #decreament
    pheromones = { k : (ro + th/Lavg)*v for (k,v) in pheromones.items() }
    solutions.sort(key = lambda x: x[1])
    if(bestSolution!=None):
        if(solutions[0][1] < bestSolution[1]):
            bestSolution = solutions[0]
        for path in bestSolution[0]:
            for i in range(len(path)-1):
                #print(pheromones)
                #print(pheromones[(8,9)])
                #print("**********************************")
                decrease = pheromones[(min(path[i],path[i+1]), max(path[i],path[i+1]))]
                increase = sigm/bestSolution[1]
                pheromones[(min(path[i],path[i+1]), max(path[i],path[i+1]))] =  decrease + increase
    else:
        bestSolution = solutions[0]
    #sigm go through the fisrt 3 solutions (not all solutions)
    for l in range(sigm):
        paths = solutions[l][0]
        L = solutions[l][1]
        for path in paths:
            for i in range(len(path)-1):
                decrease = pheromones[(min(path[i],path[i+1]), max(path[i],path[i+1]))]
                increase = (sigm-(l+1)/L**(l+1))
                pheromones[(min(path[i],path[i+1]), max(path[i],path[i+1]))] = increase + decrease

    return bestSolution
def main():
    bestSolution = None
    best_solutions = dict()
    
    edges, capacityLimit, demand, pheromones, optimalValue, depot_inf = use_dataset()

    
    for depot,customers in depot_inf["customers"].items():
        bestSolution = None
        #best_solutions[int(depot)] = list()
        vehicle_d = depot_inf["vehicle"][int(depot)]
        for i in range(iterations):
            solutions = list()
            for _ in range(vehicle_d):
                
                solution = solutionOfOneAnt(customers.copy(), edges[int(depot)], capacityLimit, demand, pheromones[int(depot)])#update ant
                
                solutions.append((solution, rateSolution(solution, edges[int(depot)],int(depot))))
            bestSolution = update_pheromone(pheromones[int(depot)], solutions, bestSolution)
        
        best_solutions[int(depot)]=bestSolution
    
    #graph
    G= Graph()
    length = 0
    f_path = list()
    for k,y in best_solutions.items():
        #print(y)
        for l in y[0]:
            length += len(l)   
        f_path.append(k)
    length += len(f_path)
    for y in range(1,length+1):
        G.add_vertex(y)
    #print(length)
    G.vs["label"]=[str(a) for a in range(1,length+2)]
    u = {m:"yellow" for m in range(1,length+2)}
    #w is 1D of all paths inside solutions 
    for f in f_path:
        u.update({f:"red"})
    G.vs["color"] = [u[int(p)] for p in G.vs["label"]]
    for depot,d in best_solutions.items():
        for e in d[0]:
            for i in range(len(e)):

                if i==0:
                    idx_n = e[i]-1
                    G.add_edges([(idx_n,depot-1)])

                
                idx_i = e[i]-1
                
                idx_n =0
                if i==len(e)-1:
                    idx_n = depot-1
                else:
                    idx_n = e[i+1]-1
                

                G.add_edges([(idx_i,idx_n)])
    layout= G.layout("KK")
    plot(G,layout=layout)
    return best_solutions

solution = main()


print("Solution: "+str(solution))
