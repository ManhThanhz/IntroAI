import heapq
import os
import time

class State:
    def __init__(self, pacman_position, food_points, parent_state=None, parent_action=None, cost=0):
        self.pacman_position = pacman_position
        self.food_points = food_points
        self.parent_state = parent_state
        self.parent_action = parent_action
        self.cost = cost

    def __lt__(self, other):
        return self.cost < other.cost

    def __eq__(self, other):
        return isinstance(other, State) and \
               self.pacman_position == other.pacman_position and \
               self.food_points == other.food_points

    def __hash__(self):
        return hash((self.pacman_position, tuple(sorted(self.food_points))))

class Maze:
    def __init__(self, layout_file):
        self.layout = self.load_layout(layout_file)
        self.rows = len(self.layout)
        self.cols = len(self.layout[0])
        self.set_corners_as_food()
        self.initial_food_points = self.get_initial_food_points()

    def load_layout(self, layout_file):
        with open(layout_file, 'r') as file:
            layout = [list(line.strip()) for line in file]
        return layout

    def get_initial_food_points(self):
        return [(i, j) for i in range(self.rows) for j in range(self.cols) if self.layout[i][j] == '.']

    def set_corners_as_food(self):
        for i in (1, self.rows - 2):
            for j in (1, self.cols - 2):
                if self.layout[i][j] == '.':
                    continue
                if self.layout[i][j] == ' ':
                    self.layout[i][j] = '.'
        

    def get_initial_state(self):
        pacman_position = None
        food_points = []

        for i in range(self.rows):
            for j in range(self.cols):
                if self.layout[i][j] == 'P':
                    pacman_position = (i, j)
                elif self.layout[i][j] == '.':
                    food_points.append((i, j))

        return State(pacman_position, food_points)

    def print_maze(self, pacman_position, food_positions):
        for i in range(self.rows):
            for j in range(self.cols):
                if (i, j) == pacman_position:
                    print('P', end='')
                
                elif ((i, j) in self.initial_food_points) and ((i, j) in food_positions) and (not ((i, j) in [(1, 1), (1, self.cols - 2), (self.rows - 2, 1), (self.rows - 2, self.cols - 2)])):
                    print('.', end='')
                elif self.layout[i][j] == 'P' or self.layout[i][j] == '.':
                    print(' ', end='')
                else:
                    print(self.layout[i][j], end='')
            print()

class SearchAlgorithm:
    def __init__(self, maze):
        self.maze = maze

    def search(self, initial_state):
        raise NotImplementedError("Subclasses must implement search method.")

    def is_goal_state(self, state):
        return not state.food_points

    def get_successors(self, state):
        raise NotImplementedError("Subclasses must implement get_successors method.")

    def is_valid_position(self, x, y):
        return 0 <= x < self.maze.rows and 0 <= y < self.maze.cols and self.maze.layout[x][y] != '%'

    def get_next_state(self, state, next_position, action):
        pacman_position = next_position
        food_points = [point for point in state.food_points if point != next_position]
        cost = state.cost + 1
        return State(pacman_position, food_points, state, action, cost)

    def get_successors(self, state):
        successors = []
        x, y = state.pacman_position

        actions = [(0, 1, 'East'), (0, -1, 'West'), (1, 0, 'South'), (-1, 0, 'North'), (0, 0, 'Stop')]
        for dx, dy, action in actions:
            new_x, new_y = x + dx, y + dy
            if self.is_valid_position(new_x, new_y):
                next_state = self.get_next_state(state, (new_x, new_y), action)
                step_cost = 1
                successors.append((action, next_state, step_cost))

        return successors

    def extract_actions(self, final_state):
        actions = []
        current_state = final_state
        while current_state.parent_action:
            actions.append(current_state.parent_action)
            current_state = current_state.parent_state
        return actions[::-1]

class UCS(SearchAlgorithm):
    def search(self, initial_state):
        frontier = [(0, initial_state)]
        explored = set()

        while frontier:
            cost, current_state = heapq.heappop(frontier)
            if self.is_goal_state(current_state):
                return self.extract_actions(current_state), cost

            if hash(current_state) not in explored:
                explored.add(hash(current_state))
                for action, next_state, step_cost in self.get_successors(current_state):
                    new_cost = cost + step_cost
                    heapq.heappush(frontier, (new_cost, next_state))

        return None, float('inf')

class AStar(SearchAlgorithm):
    def __init__(self, maze, heuristic):
        super().__init__(maze)
        self.heuristic = heuristic

    def search(self, initial_state):
        frontier = [(0, initial_state)]
        explored = set()

        while frontier:
            cost, current_state = heapq.heappop(frontier)
            if self.is_goal_state(current_state):
                return self.extract_actions(current_state), cost

            if hash(current_state) not in explored:
                explored.add(hash(current_state))
                for action, next_state, step_cost in self.get_successors(current_state):
                    new_cost = current_state.cost + step_cost
                    heuristic_cost = self.heuristic(next_state)
                    heapq.heappush(frontier, (new_cost + heuristic_cost, next_state))

        return None, float('inf')
    
    

class Visualizer:
    def __init__(self, search_algorithm):
        self.search_algorithm = search_algorithm

    def visualize(search_algorithm, actions):
        if not actions:
            print("No solution found.")
            return

        current_state = search_algorithm.maze.get_initial_state()
        for action in actions:
            os.system('cls' if os.name == 'nt' else 'clear')  # Clear terminal
            search_algorithm.maze.print_maze(current_state.pacman_position, current_state.food_points)
            for dx, dy, action_name in [(0, 1, 'East'), (0, -1, 'West'), (1, 0, 'South'), (-1, 0, 'North'), (0, 0, 'Stop')]:
                if action_name == action:
                    new_x, new_y = current_state.pacman_position[0] + dx, current_state.pacman_position[1] + dy
                    if search_algorithm.is_valid_position(new_x, new_y):
                        current_state = State((new_x, new_y), [point for point in current_state.food_points if point != (new_x, new_y)], current_state, action, current_state.cost + 1)
                        break
            time.sleep(0.2)
        os.system('cls' if os.name == 'nt' else 'clear')  # Clear terminal
        print("List of actions:")
        print(", ".join(actions))
        print("Goal reached.")

def manhattan_distance(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

def nearest_food_heuristic(state):
    pacman_position = state.pacman_position
    if not state.food_points:
        return 0
    return min(manhattan_distance(pacman_position, food_point) for food_point in state.food_points)

def main(layout_file, algorithm):
    maze = Maze(layout_file)
    initial_state = maze.get_initial_state()

    if algorithm == "UCS":
        search_algorithm = UCS(maze)
    elif algorithm == "A*":
        search_algorithm = AStar(maze, nearest_food_heuristic)
    else:
        raise ValueError("Invalid algorithm.")

    actions, cost = search_algorithm.search(initial_state)
    Visualizer.visualize(search_algorithm, actions)
    print("Total cost:", cost)


if __name__ == "__main__":
    layout_file = "pacman_layouts\\pacman_layouts\\smallMaze.lay"
    algorithm = "UCS" 
    main(layout_file, algorithm)