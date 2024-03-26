from game import Game

game = Game()
n = 1000
node_arr = game.random_multi_initial_state(n)
average_bfs = 0
average_astar = 0

for node in node_arr:
    bfs_game = Game(board=node, algorithm="bfs")
    astar_game = Game(board=node, algorithm="astar")
    _, bfs_cost, _ = bfs_game.solve_board()
    _, astar_cost, _ = astar_game.solve_board()
    average_bfs += bfs_cost
    average_astar += astar_cost

average_bfs /= n
average_astar /= n
