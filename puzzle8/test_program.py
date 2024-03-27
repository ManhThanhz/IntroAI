from game import Game

class AlgorithmResult:
    def __init__(self, n: int = 0, all_cost: list[int] = []) -> None:
        self.n = n
        self.all_cost = all_cost

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
        fail = 0
        result = AlgorithmResult()
        for node in node_arr:
            # print("State:\n", node)
            game.set_board(node)
            game.set_algorithm(algorithm)
            _, cost, _ = game.solve_board()
            if cost != 0:
                result.add_case(cost)
            else:
                fail += 1
        print("Finish!\n")
        print("Success on ", n - fail, "/", n, " cases")
        return result
    
    def compare_algorithm(self, n: int = 10, algorithms: list[str] = ["bfs"]) -> dict[str, AlgorithmResult]:
        results = dict()
        game = Game()
        node_arr = game.random_multi_initial_state(n)
        for algorithm in algorithms:
            results[algorithm] = self.test_algorithm(n, game, node_arr, algorithm)
        return results
