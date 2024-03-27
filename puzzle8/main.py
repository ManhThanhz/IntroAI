from game import Game
from test_program import TestProgram
import matplotlib.pyplot as plt


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
    results = test_program.compare_algorithm(n, ["bfs","astar"])

    # Get result for each algorithm
    bfs_result = results["bfs"]
    astar_result = results["astar"]

    # Get AVERAGE cost
    bfs_average_cost = bfs_result.compute_average_cost()
    astar_average_cost = astar_result.compute_average_cost()

    # Get HIGHEST cost
    bfs_highest_cost = bfs_result.get_highest_cost()
    astar_highest_cost = astar_result.get_highest_cost()
    highest_cost = bfs_highest_cost if bfs_highest_cost > astar_highest_cost else astar_highest_cost

    # Plot graph
    print(bfs_average_cost)
    print(astar_average_cost)
    plt.bar(["bfs","astar"], [bfs_average_cost, astar_average_cost], width=0.4)
    plt.xlabel('Algorithm')
    plt.ylabel('Average cost')
    plt.show()


