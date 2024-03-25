from graph import Node
from problem import Problem
from search_strategy import BFS, AStar
from graphviz import Digraph


p = Problem()
# n = p.random_generate_init()
n = Node([[6,7,8],[2,1,5],[0,4,3]])
print(n, "\n")

print("BFS: ")
bfs = BFS()
dot, cost, path = bfs.search(n)
print("Total cost: ", cost)
path_print = ""
for step in path:
    path_print += step + "->"
print("Path: ", path_print)

print("A*: ")
astar = AStar()
dot, cost, path = astar.search(n)
print("Total cost: ", cost)
path_print = ""
for step in path:
    path_print += step + "->"
print("Path: ", path_print)
