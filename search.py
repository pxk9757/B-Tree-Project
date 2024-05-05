import time
import random
import matplotlib.pyplot as plt

class BTreeNode:
    def __init__(self, leaf=True):
        self.leaf = leaf
        self.keys = []
        self.children = []

    def search(self, key):
        i = 0
        while i < len(self.keys) and key > self.keys[i]:
            i += 1
        if i < len(self.keys) and key == self.keys[i]:
            return True
        if self.leaf:
            return False
        return self.children[i].search(key)

    # Other methods...

class BTree:
    def __init__(self, t):
        self.root = BTreeNode(leaf=True)
        BTree.t = t

    # Other methods...

class BenchmarkBTree:
    def __init__(self, t):
        self.btree = BTree(t)

    def generate_random_data(self, size):
        return [random.randint(1, 1000000) for _ in range(size)]

    def benchmark_search(self, data):
        start_time = time.time()
        for key in data:
            self.btree.root.search(key)
        end_time = time.time()
        return end_time - start_time

    def analyze_search(self, data_sizes):
        best_case_times = []
        average_case_times = []
        worst_case_times = []

        for size in data_sizes:
            data = self.generate_random_data(size)

            # Best case: Key is at the root
            self.btree = BTree(3)
            search_time = self.benchmark_search([data[0]])
            best_case_times.append(search_time)

            # Worst case: Key is not present in the tree
            self.btree = BTree(3)
            search_time = self.benchmark_search([size + 1])  # Key guaranteed to be greater than any in data
            worst_case_times.append(search_time)

            # Average case: Randomly generated keys
            search_time = self.benchmark_search([random.choice(data)])
            average_case_times.append(search_time)

        return best_case_times, average_case_times, worst_case_times

def plot_search_analysis(data_sizes, best_case_times, average_case_times, worst_case_times):
    plt.plot(data_sizes, best_case_times, label='Best Case')
    plt.plot(data_sizes, average_case_times, label='Average Case')
    plt.plot(data_sizes, worst_case_times, label='Worst Case')
    plt.xlabel('Data Size')
    plt.ylabel('Time (seconds)')
    plt.title('Search Operation Analysis')
    plt.legend()
    plt.show()

# Example usage:
btree = BenchmarkBTree(3)
data_sizes = [1000, 5000, 10000, 20000, 50000]  # Varying data sizes

best_case_times, average_case_times, worst_case_times = btree.analyze_search(data_sizes)

plot_search_analysis(data_sizes, best_case_times, average_case_times, worst_case_times)
