from game import Game
from test_program import TestProgram
import matplotlib.pyplot as plt
import time

###########
# GREETING
###########
print("Welcome to 8 puzzle game")
print("How do you want to process?")
print("1. Solve 1 case")
print("2. Compare algorithm by testing multiple cases")
choice = input("Your choice: ")
while choice != "1" and choice != "2":
    choice = input("Please enter 1 or 2: ")


######################
# START GAME NORMALLY
######################
if choice == "1":
    game = Game()
    game.create_board()
    game.select_algorithm()
    game.start_game()


###########################
# PERFORM TEST ON ALGORITHM
###########################
if choice == "2":

    # Input number of test cases
    n = int(input("How many case do you want to test: "))

    # Start program
    print("Program started...")
    test_program = TestProgram()
    game = Game()
    node_arr = game.random_multi_initial_state(n)

    # Get result for BFS
    bfs_start_timer = time.time()
    bfs_result = test_program.test_algorithm(n, game, node_arr, "bfs")
    bfs_end_timer = time.time()
    print("Time take: ", round(bfs_end_timer - bfs_start_timer, 2), " seconds")

    # Get result for A*
    astar_start_timer = time.time()
    astar_result = test_program.test_algorithm(n, game, node_arr, "astar")
    astar_end_timer = time.time()
    print("Time take: ", round(astar_end_timer - astar_start_timer, 2), " seconds")

    # Get AVERAGE cost
    bfs_average_cost = bfs_result.compute_average_cost()
    astar_average_cost = astar_result.compute_average_cost()

    # Plot graph
    algorithms = ["BFS","A*"]
    average_costs = [bfs_average_cost, astar_average_cost]
    plt.bar(algorithms, average_costs, width=0.4)
    for i in range(len(algorithms)):
        plt.text(i,average_costs[i],average_costs[i])
    plt.xlabel('Algorithm')
    plt.ylabel('Average cost')
    plt.show()


