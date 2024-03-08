class State:
    def __init__(self, pacman_position, food_points, parent_state=None, parent_action=None, cost=0):
        self.pacman_position = pacman_position
        self.food_points = food_points
        self.parent_state = parent_state
        self.parent_action = parent_action
        self.cost = cost  # Initialize cost attribute

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

    def load_layout(self, layout_file):
        with open(layout_file, 'r') as file:
            layout = [line.strip() for line in file]
        return layout

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

import heapq

class UCS:  
    def __init__(self, maze):
        self.maze = maze

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

        return None, float('inf')  # No solution found

    def is_goal_state(self, state):
        # Check if all food points have been collected and all corners visited
        return not state.food_points

    def get_successors(self, state):
        successors = []
        x, y = state.pacman_position

        # Define actions and their effects
        actions = [(0, 1, 'East'), (0, -1, 'West'), (1, 0, 'South'), (-1, 0, 'North'), (0, 0, 'Stop')]
        for dx, dy, action in actions:
            new_x, new_y = x + dx, y + dy
            if self.is_valid_position(new_x, new_y):
                next_state = self.get_next_state(state, (new_x, new_y), action)  # Pass action
                step_cost = 1  # Uniform cost for all actions
                successors.append((action, next_state, step_cost))

        return successors

    def is_valid_position(self, x, y):
        return 0 <= x < self.maze.rows and 0 <= y < self.maze.cols and self.maze.layout[x][y] != '%'

    def get_next_state(self, state, next_position, action):
        pacman_position = next_position
        food_points = [point for point in state.food_points if point != next_position]
        cost = state.cost + 1  # Update cost
        return State(pacman_position, food_points, state, action, cost)  # Update parent_action with action

    def extract_actions(self, final_state):
        # Trace back actions from final state to initial state
        actions = []
        current_state = final_state
        while current_state.parent_action:
            actions.append(current_state.parent_action)
            current_state = current_state.parent_state
        return actions[::-1]

import heapq

class AStar:
    def __init__(self, maze, heuristic):
        self.maze = maze
        self.heuristic = heuristic

    def search(self, initial_state):
        frontier = [(self.heuristic(initial_state), 0, initial_state)]
        explored = set()

        while frontier:
            _, cost, current_state = heapq.heappop(frontier)
            if self.is_goal_state(current_state):
                return self.extract_actions(current_state), cost

            if hash(current_state) not in explored:
                explored.add(hash(current_state))
                for action, next_state, step_cost in self.get_successors(current_state):
                    new_cost = cost + step_cost
                    priority = new_cost + self.heuristic(next_state)
                    heapq.heappush(frontier, (priority, new_cost, next_state))

        return None, float('inf')  # No solution found
    
    def is_goal_state(self, state):
        # Check if all food points have been collected and all corners visited
        return not state.food_points

    def get_successors(self, state):
        successors = []
        x, y = state.pacman_position

        # Define actions and their effects
        actions = [(0, 1, 'East'), (0, -1, 'West'), (1, 0, 'South'), (-1, 0, 'North'), (0, 0, 'Stop')]
        for dx, dy, action in actions:
            new_x, new_y = x + dx, y + dy
            if self.is_valid_position(new_x, new_y):
                next_state = self.get_next_state(state, (new_x, new_y), action)  # Pass action
                step_cost = 1  # Uniform cost for all actions
                successors.append((action, next_state, step_cost))

        return successors

    def is_valid_position(self, x, y):
        return 0 <= x < self.maze.rows and 0 <= y < self.maze.cols and self.maze.layout[x][y] != '%'

    def get_next_state(self, state, next_position, action):
        pacman_position = next_position
        food_points = [point for point in state.food_points if point != next_position]
        cost = state.cost + 1  # Update cost
        return State(pacman_position, food_points, state, action, cost)  # Update parent_action with action

    def extract_actions(self, final_state):
        # Trace back actions from final state to initial state then print it
        actions = []
        current_state = final_state
        while current_state.parent_action:
            actions.append(current_state.parent_action)
            current_state = current_state.parent_state
        return actions[::-1]
    


import os
import time

'''
print the steps to achieve the goal, such as: north, north, south, west, east, east
'''
def visualize(maze, actions):
    if not actions:
        print("No solution found.")
        return

    current_state = maze.get_initial_state()
    for action in actions:
        print(action)
        if current_state.parent_state is not None:  # Add this condition
            current_state = current_state.parent_state

    print("Goal reached.")

def print_maze(maze, action):
    pacman_x, pacman_y = maze.pacman_position
    maze_layout = maze.layout.copy()

    # Update Pacman position based on action
    if action == 'North':
        pacman_x -= 1
    elif action == 'East':
        pacman_y += 1
    elif action == 'South':
        pacman_x += 1
    elif action == 'West':
        pacman_y -= 1

    # Update maze layout with Pacman's new position
    maze_layout[pacman_x] = maze_layout[pacman_x][:pacman_y] + 'P' + maze_layout[pacman_x][pacman_y + 1:]

    # Print the updated maze layout
    # for row in maze_layout:
    #     print(row)

def manhattan_distance(point1, point2):
    return abs(point1[0] - point2[0]) + abs(point1[1] - point2[1])

def nearest_food_heuristic(state):
    pacman_position = state.pacman_position
    remaining_food_points = state.food_points
    if not remaining_food_points:
        return 0  # If no food points remaining, heuristic value is 0
    return min(manhattan_distance(pacman_position, food_point) for food_point in remaining_food_points)


def main(layout_file, algorithm):
    maze = Maze(layout_file)
    initial_state = maze.get_initial_state()

    if algorithm == 'UCS':
        search_algorithm = UCS(maze)
    elif algorithm == 'A*':
        heuristic = nearest_food_heuristic
        search_algorithm = AStar(maze, heuristic)
    else:
        print("Invalid algorithm specified.")
        return

    actions, total_cost = search_algorithm.search(initial_state)
    visualize(maze, actions)
    print("Total cost:", total_cost)

if __name__ == "__main__":
    layout_file = "D:\\UniBachelor\\232\\AI\\BTL1\\pacman_layouts\\pacman_layouts\\bigMaze.lay"
    algorithm = "A*"  # or "UCS"
    main(layout_file, algorithm)
