from copy import deepcopy
import random

class Node:

  def __init__(self, state, action = None, parent = None):
    self.state = state # 2D list (3x3)
    self.id = str(self) # identifier of node
    self.action = action
    self.parent = parent

  def __str__(self):
    if not self.state[0] == []:
        lst_str = []
        for s in self.state:
            one_str = ''.join('_' if (elem == 0) else str(elem) for elem in s)
            lst_str.append(one_str)
        return '\n'.join(one_str for one_str in lst_str)
    return None
  
  def __lt__(self, other):
      choice = random.choice([self, other])
      return choice

  def get_successors(self):
    successors = []
    i, j = self.get_blank_pos(self.state)
    if j != 2:
      self.get_specific_successor(successors, "Left")
    if j != 0:
      self.get_specific_successor(successors, "Right")
    if i != 2:
      self.get_specific_successor(successors, "Up")
    if i != 0:
      self.get_specific_successor(successors, "Down")

    return successors

  def get_specific_successor(self, successors, action):
      new_state = self.get_successor(action, deepcopy(self.state))
      n = Node(new_state, action, self)
      successors.append(n)

  def get_successor(self, action, state):
    pi, pj = self.get_blank_pos(state)
    pi, pj = self.get_dest_pos(action, pi, pj)
    if 0 <= pi and pi < 3 and 0 <= pj and pj < 3:
      if action == 'Left':
        state[pi][pj - 1] = state[pi][pj]
      if action == 'Right':
        state[pi][pj + 1] = state[pi][pj]
      if action == 'Up':
        state[pi-1][pj] = state[pi][pj]
      if action == 'Down':
        state[pi+1][pj] = state[pi][pj]
      state[pi][pj] = 0
      return state
    return None

  def get_dest_pos(self, action, pi, pj):
    if action == 'Left':
      pj += 1
    if action == 'Right':
      pj -= 1
    if action == 'Up':
      pi += 1
    if action == 'Down':
      pi -= 1
    return pi, pj

  def get_blank_pos(self, state):
    for i, row in enumerate(state):
        for j, elem in enumerate(row):
            if elem == 0:
                return i, j
    return None

  def get_id(self):
    return self.id

  def get_node_str(self):
    return str(self)

  def get_action(self):
    return self.action

  def draw(self, dot):
    dot.node(self.get_id(), self.get_node_str())
    if self.parent is not None:
      dot.edge(self.parent.get_id(), self.get_id(), self.get_action())