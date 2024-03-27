from game import Game
import matplotlib.pyplot as plt

game = Game()
n = 10
node_arr = game.random_multi_initial_state(n)
average_bfs = 0
average_astar = 0
bfs_cost_arr = []
astar_cost_arr = []

for node in node_arr:
    bfs_game = Game(board=node, algorithm="bfs")
    astar_game = Game(board=node, algorithm="astar")
    _, bfs_cost, _ = bfs_game.solve_board()
    _, astar_cost, _ = astar_game.solve_board()
    average_bfs += bfs_cost
    average_astar += astar_cost
    bfs_cost_arr.append(bfs_cost)
    astar_cost_arr.append(astar_cost)
    # bfs_cost_arr.append(node.state[0][0])
    # astar_cost_arr.append(node.state[0][1])


average_bfs /= n
average_astar /= n

print("Result")
print("Average cost: ")
print("1. BFS: ", average_bfs)
print("2. A Star: ", average_astar)

print("Array BFS: ", bfs_cost_arr)
print("Array A Star: ", astar_cost_arr)

plt.plot(bfs_cost_arr, label='BFS cost')
plt.plot(astar_cost_arr, label='A* cost')
plt.xlabel('Index')
plt.ylabel('Cost')
plt.legend()
plt.show()