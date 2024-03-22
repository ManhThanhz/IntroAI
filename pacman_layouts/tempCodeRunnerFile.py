def get_initial_state(self):
        pacman_position = None
        food_points = []
        corners = [(0, 0), (0, self.cols - 1), (self.rows - 1, 0), (self.rows - 1, self.cols - 1)]
        corners_visited = []

        for i in range(self.rows):
            for j in range(self.cols):
                if self.layout[i][j] == 'P':
                    pacman_position = (i, j)
                elif self.layout[i][j] == '.':
                    food_points.append((i, j))
                elif (i, j) in corners:
                    corners_visited.append((i, j))

        return State(pacman_position, food_points, corners_visited)