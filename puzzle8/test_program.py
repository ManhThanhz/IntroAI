from game import Game

class AlgorithmResult:
    def __init__(self) -> None:
        self.n = 0
        self.all_cost = []

    def add_case(self, cost: int):
        self.n += 1
        self.all_cost.append(cost)

    def get_highest_cost(self):
        return max(self.all_cost)

    def compute_average_cost(self):
        total = 0
        for cost in self.all_cost:
            total += cost
        return total / self.n

class TestProgram:
    def test_algorithm(self, n, game, node_arr, algorithm) -> AlgorithmResult:
        print("\nTest for ", algorithm)
        result = AlgorithmResult()
        fail = 0
        for node in node_arr:
            # print("State:\n", node)
            game.set_board(node)
            game.set_algorithm(algorithm)
            _, cost, _ = game.solve_board()
            if cost != 0:
                result.add_case(cost)
            else:
                fail += 1
        print("Finish!")
        print("Success on ", n - fail, "/", n, " cases")
        return result
