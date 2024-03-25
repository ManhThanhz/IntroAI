from graphviz import Digraph
from heapq import heappop, heappush
from graph import Node
import time


class SearchStrategy:
  def __init__(self) -> None:
     self.i = 0
  
  def search(self, node: Node) -> tuple:
    return (0,0)
  
  def check_goal(self, state: Node):
    goal1 = [[1, 2, 3],[4, 5, 6],[7, 8, 0]]
    goal2 = [[0, 1, 2],[3, 4, 5],[6, 7, 8]]
    if str(state) == str(Node(goal1)) or str(state) == str(Node(goal2)):
      return True
    return False

  def find_cost_and_path(self, current_state: Node, initial_state: Node):
    if current_state.parent == initial_state:
      print(current_state.action)
      return 1, current_state.action
    else:
      extra_cost, extra_path = self.find_cost_and_path(current_state.parent, initial_state)
      cost = extra_cost + 1
      path = extra_path + current_state.action
      print(current_state.action)
      return cost, path



class BFS(SearchStrategy):
  def search(self, node: Node) -> tuple[Digraph, int, list]:
    dot = Digraph()
    frontier = list()
    explored = set()
    frontier.append(node)

    while len(frontier) > 0:
      if frontier[0] not in explored:
        explored.add(str(frontier[0]))
        successors = frontier[0].get_successors()
        frontier.pop(0)
        for successor in successors:
          if str(successor) not in explored:
            self.i += 1
            print(self.i)

            frontier.append(successor)
            explored.add(str(successor))
            successor.draw(dot)
            if self.check_goal(successor):
              cost, path = self.find_cost_and_path(successor, node)
              return dot, cost, path

    return dot, 0, []


  
class AStar(SearchStrategy):
  def search(self, node: Node) -> tuple[Digraph, int, list]:
    # Priority queue for A* search
    frontier = []  # (priority, state, cost)
    heappush(frontier, (self.heuristics(node), node, 0))
    explored = set()
    dot = Digraph()

    # A* search loop
    while len(frontier) > 0:
      _, current_state, cost = heappop(frontier)

      if current_state not in explored:

        # Add node to graph
        current_state.draw(dot)

        # Check if current state is goal state
        if self.check_goal(current_state):
              print("reach goal")
              cost, path = self.find_cost_and_path(current_state, node)
              return dot, cost, path
        
        # Add current state to closed set
        explored.add(str(current_state))

        # print("Current state:")
        # print(current_state, "\n")
        # time.sleep(2)

        # Get successors
        successors = current_state.get_successors()

        # Generate possible moves
        for successor in successors:
            new_cost = cost + 1
            priority = new_cost + self.heuristics(successor)
            if str(successor) not in explored:
                heappush(frontier, (priority, successor, new_cost))

    # If no solution found
    return dot, 0, []


  def heuristics(self, node: Node): # Manhattan
    distance = 0
    state = node.state
    for i in range(3):
        for j in range(3):
            if state[i][j] != 0:
                target_x = (state[i][j] - 1) // 3
                target_y = (state[i][j] - 1) % 3
                distance += abs(i - target_x) + abs(j - target_y)
    return distance

