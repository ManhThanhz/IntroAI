import random
from graphviz import Digraph
from node import Node
from helper import Helper
from search_strategy import BFS, AStar


class Game():

    def __init__(self, board: Node = None, algorithm: str = "") -> None:
        self.helper = Helper()
        self.board = board
        self.algorithm = algorithm


    def set_board(self, board: Node):
        self.board = board

    def set_algorithm(self, algorithm: str):
        self.algorithm = algorithm

    def start_game(self):
        if self.board == None:
            self.create_board()
        if self.algorithm == "":
            self.select_algorithm()
        print("Initial board: \n", self.board)
        print("\nThe algorithm is running, please wait...")
        dot, cost, path = self.solve_board()
        print("The algorithm is done! Here is the result: ")
        print("Total cost: ", cost)
        print_path = ""
        for turn in path:
            print_path += turn + "->" 
        print_path = print_path[:-2]
        print("Path: ", print_path)
        print("Graph: ", dot)

    

    def create_board(self):
        print("\nHow do you like to create your board?")
        print("1. Generate random state")
        print("2. Enter custom state")
        choice = input("Your choice: ")
        while choice != "1" and choice != "2":
            choice = input("Please enter 1 or 2: ")

        if choice == "1":
            self.board = self.random_initial_state()

        game_state = ""
        if choice == "2":
            game_state = input("Enter game state, from top-left to right-bottom, 10 characters, e.g. \"012345678\"\n")
            check = False
            temp = []
            while not check:
                if not self.helper.check_input_string(game_state):
                    game_state = input("Invalid game state, please enter again\n")
                    continue
                temp = self.create_node(game_state)
                if not self.check_solvable_board(temp):
                    game_state = input("This board isn't solvable, please enter again\n")
                    continue
                check = True
            self.board = Node(temp)



    def select_algorithm(self):
        print("\nChoose your algorithm:")
        print("1. Breath First Search (BFS)")
        print("2. Best First Search (A*)")
        choice = input("Your choice: ")
        while choice != "1" and choice != "2":
            choice = input("Please enter 1 or 2: ")
        self.algorithm = "bfs" if choice == "1" else "astar"


    def solve_board(self) -> tuple:
        search = BFS() if self.algorithm == "bfs" else AStar()
        dot, cost, path = search.search(self.board)
        return dot, cost, path
    

    def check_solvable_board(self, state: list = None) -> bool:
        board_state = self.board.state if state == None else state
        flat_board = [tile for row in board_state for tile in row if tile != 0]
        inversions = 0
        for i in range(len(flat_board)):
            for j in range(i + 1, len(flat_board)):
                if flat_board[i] > flat_board[j]:
                    inversions += 1
        return (inversions % 2 == 0)
    

    def create_node(self, input_string: str) -> list:
        arr = []
        for i in range(3):
            row = []
            for j in range(3):
                index = i*3 + j
                row.append(int(input_string[index]))
            arr.append(row)
        return arr


    def random_initial_state(self) -> Node:
        random_shuffle = [0, 1, 2, 3, 4, 5, 6, 7, 8]
        random.shuffle(random_shuffle)
        arr = [[],[],[]]
        for i1 in range(3):
            for i2 in range(3):
                arr[i1].append(random_shuffle[i1*3 + i2])
        if self.check_solvable_board(arr):
            return Node(arr)
        return self.random_initial_state()
    

    def random_multi_initial_state(self, num: int) -> list[Node]:
        node_arr = []
        for i in range(num):
            node_arr.append(self.random_initial_state())
        return node_arr
