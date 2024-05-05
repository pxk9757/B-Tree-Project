import time
import random
import matplotlib.pyplot as plt

class BTreeNode:
    def __init__(self, leaf=True):
        self.leaf = leaf
        self.keys = []
        self.children = []

    def split_child(self, idx, child):
        t = BTree.t
        new_child = BTreeNode(leaf=child.leaf)
        self.children.insert(idx + 1, new_child)
        self.keys.insert(idx, child.keys[t - 1])
        new_child.keys = child.keys[t:]
        child.keys = child.keys[:t - 1]
        if not child.leaf:
            new_child.children = child.children[t:]
            child.children = child.children[:t]

    def insert_non_full(self, key):
        i = len(self.keys) - 1
        if self.leaf:
            self.keys.append(None)
            while i >= 0 and key < self.keys[i]:
                self.keys[i + 1] = self.keys[i]
                i -= 1
            self.keys[i + 1] = key
        else:
            while i >= 0 and key < self.keys[i]:
                i -= 1
            i += 1
            if len(self.children[i].keys) == (2 * BTree.t) - 1:
                self.split_child(i, self.children[i])
                if key > self.keys[i]:
                    i += 1
            self.children[i].insert_non_full(key)

    def find_key(self, key):
        i = 0
        while i < len(self.keys) and key > self.keys[i]:
            i += 1
        return i

    # Other methods...

class BTree:
    def __init__(self, t):
        self.root = BTreeNode(leaf=True)
        BTree.t = t

    def insert(self, key):
        root = self.root
        if len(root.keys) == (2 * BTree.t) - 1:
            new_root = BTreeNode(leaf=False)
            new_root.children.append(self.root)
            new_root.split_child(0, self.root)
            self.root = new_root
        self.root.insert_non_full(key)

    # Other methods...

class BenchmarkBTree:
    def __init__(self, t):
        self.btree = BTree(t)

    def generate_random_data(self, size):
        return [random.randint(1, 1000000) for _ in range(size)]

    def benchmark_insertion(self, data):
        start_time = time.time()
        for key in data:
            self.btree.insert(key)
        end_time = time.time()
        return end_time - start_time

    def analyze_insertion(self, data_sizes):
        best_case_times = []
        average_case_times = []
        worst_case_times = []

        for size in data_sizes:
            data = self.generate_random_data(size)

            # Best case: Already balanced tree
            self.btree = BTree(3)
            insertion_time = self.benchmark_insertion(data)
            best_case_times.append(insertion_time)

            # Worst case: Tree needs rebalancing after each insertion
            self.btree = BTree(3)
            self.btree.insert(data[0])
            insertion_time = self.benchmark_insertion(data[1:])
            worst_case_times.append(insertion_time)

            # Average case: Uniformly distributed keys
            insertion_time = self.benchmark_insertion(data)
            average_case_times.append(insertion_time)

        return best_case_times, average_case_times, worst_case_times

def plot_insertion_analysis(data_sizes, best_case_times, average_case_times, worst_case_times):
    plt.plot(data_sizes, best_case_times, label='Best Case')
    plt.plot(data_sizes, average_case_times, label='Average Case')
    plt.plot(data_sizes, worst_case_times, label='Worst Case')
    plt.xlabel('Data Size')
    plt.ylabel('Time (seconds)')
    plt.title('Insertion Operation Analysis')
    plt.legend()
    plt.show()

# Example usage:
btree = BenchmarkBTree(3)
data_sizes = [1000, 5000, 10000, 20000, 50000]  # Varying data sizes

best_case_times, average_case_times, worst_case_times = btree.analyze_insertion(data_sizes)

plot_insertion_analysis(data_sizes, best_case_times, average_case_times, worst_case_times)
