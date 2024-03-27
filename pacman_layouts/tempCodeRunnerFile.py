or i in range(self.rows):
            for j in range(self.cols):
                if (i, j) == pacman_position:
                    print('P', end='')
                elif (i, j) in food_positions:
                    print('.', end='')
                elif self.layout[i][j] == 'P' or self.layout[i][j] == '.':
                    print(' ', end='')
                else:
                    print(self.layout[i][j], end='')  # Print original maze layout
            print(