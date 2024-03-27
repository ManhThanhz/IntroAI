from graphviz import Digraph
from heapq import heappop, heappush
from node import Node


class SearchStrategy:
  
  def search(self, node: Node) -> tuple:
    return (0,0)
  
  def check_goal(self, state: Node):
    state_str = state.get_node_str()
    goal1 = Node([[1, 2, 3],[4, 5, 6],[7, 8, 0]])
    goal2 = Node([[0, 1, 2],[3, 4, 5],[6, 7, 8]])
    if (state_str == goal1.get_node_str()) or (state_str == goal2.get_node_str()):
      return True
    return False


  def find_cost_and_path(self, current_state: Node, initial_state: Node, dot: Digraph()):
    if current_state.parent == initial_state:
      current_state.draw(dot)
      return dot, 1, [current_state.action]
    else:
      dot, cost, path = self.find_cost_and_path(current_state.parent, initial_state, dot)
      cost += 1
      path.append(current_state.action)
      current_state.draw(dot)
      return dot, cost, path



class BFS(SearchStrategy):
  def search(self, node: Node) -> tuple:
    frontier = list()
    explored = set()
    frontier.append(node)

    while len(frontier) > 0:

      # Pop frontier
      front_node = frontier.pop(0)

      # Add to already explored node
      explored.add(str(front_node))

      # Get successor and start loop
      successors = front_node.get_successors()

      for successor in successors:

        # Skip already explored node
        if str(successor) not in explored:

          # Check goal and return if true
          if self.check_goal(successor):
            dot = Digraph()
            dot, cost, path = self.find_cost_and_path(successor, node, dot)
            return dot, cost, path
        
          # Add successor to frontier
          frontier.append(successor)

    return None, 0, []


  
class AStar(SearchStrategy):
  def search(self, node: Node) -> tuple[Digraph, int, list]:
    # Priority queue for A* search
    frontier = []  # (priority, state, cost)
    heappush(frontier, (self.heuristics(node), node, 0))
    explored = set()

    # A* search loop
    while len(frontier) > 0:
      _, current_state, cost = heappop(frontier)

      if str(current_state) not in explored:

        # Check if current state is goal state
        if self.check_goal(current_state):
              dot = Digraph()
              dot, cost, path = self.find_cost_and_path(current_state, node, dot)
              return dot, cost, path
        
        # Add current state to closed set
        explored.add(str(current_state))

        # Get successors
        successors = current_state.get_successors()

        # Generate possible moves
        for successor in successors:
            new_cost = cost + 1
            priority = new_cost + self.heuristics(successor)
            if str(successor) not in explored:
                heappush(frontier, (priority, successor, new_cost))

    # If no solution found
    return None, 0, []


  def heuristics(self, node: Node): # Manhattan distance
    distance = 0
    state = node.state
    for i in range(3):
        for j in range(3):
            if state[i][j] != 0:
                target_x = (state[i][j] - 1) // 3
                target_y = (state[i][j] - 1) % 3
                distance += abs(i - target_x) + abs(j - target_y)
    return distance

