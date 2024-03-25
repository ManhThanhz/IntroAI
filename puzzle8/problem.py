import random
from graph import Node

class Problem():
    def __init__(self) -> None:
        pass

    def random_generate_multi_init(self, num: int) -> list[Node]:
        node_arr = []
        for i in range(num):
            node_arr.append(self.random_generate_init())
        
        return node_arr

    def random_generate_init(self) -> Node:
        
        random_shuffle = [0, 1, 2, 3, 4, 5, 6, 7, 8]
        random.shuffle(random_shuffle)

        arr = [[],[],[]]
        for i1 in range(3):
            for i2 in range(3):
                arr[i1].append(random_shuffle[i1*3 + i2])
        
        node = Node(arr)
        
        return node