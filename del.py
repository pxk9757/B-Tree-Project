import time
import random
import matplotlib.pyplot as plt

class BTreeNode:
    def __init__(self, leaf=True):
        self.leaf = leaf
        self.keys = []
        self.children = []

    def delete(self, key):
        if key in self.keys:
            self.keys.remove(key)
            return True, self

        return False, self

    # Other methods...

class BTree:
    def __init__(self, t):
        self.root = BTreeNode(leaf=True)
        BTree.t = t

    def delete(self, key):
        if not self.root:
            return False

        deleted, self.root = self.root.delete(key)

        if not self.root.keys:
            self.root = None

        return deleted

    # Other methods...

class BenchmarkBTree:
    def __init__(self, t):
        self.btree = BTree(t)

    def generate_random_data(self, size):
        return [random.randint(1, 1000000) for _ in range(size)]

    def benchmark_deletion(self, data):
        start_time = time.time()
        for key in data:
            self.btree.delete(key)
        end_time = time.time()
        return end_time - start_time

    def analyze_deletion(self, data_sizes):
        best_case_times = []
        average_case_times = []
        worst_case_times = []

        for size in data_sizes:
            data = self.generate_random_data(size)

            # Best case: Key to be deleted is at the root
            self.btree = BTree(3)
            self.btree.root = BTreeNode(leaf=True)  # Reset root to an empty leaf node
            self.btree.root.keys = [data[0]]  # Insert key directly at the root
            deletion_time = self.benchmark_deletion([data[0]])
            best_case_times.append(deletion_time)

            # Worst case: Key to be deleted requires merging of nodes
            self.btree = BTree(3)
            for key in data:
                self.btree.delete(key)
            deletion_time = self.benchmark_deletion([random.choice(data)])
            worst_case_times.append(deletion_time)

            # Average case: Randomly generated keys
            self.btree = BTree(3)
            for key in data:
                self.btree.delete(key)
            deletion_time = self.benchmark_deletion([random.choice(data)])
            average_case_times.append(deletion_time)

        return best_case_times, average_case_times, worst_case_times

def plot_deletion_analysis(data_sizes, best_case_times, average_case_times, worst_case_times):
    plt.plot(data_sizes, best_case_times, label='Best Case')
    plt.plot(data_sizes, average_case_times, label='Average Case')
    plt.plot(data_sizes, worst_case_times, label='Worst Case')
    plt.xlabel('Data Size')
    plt.ylabel('Time (seconds)')
    plt.title('Deletion Operation Analysis')
    plt.legend()
    plt.show()

# Example usage:
btree = BenchmarkBTree(3)
data_sizes = [1000, 5000, 10000, 20000, 50000]  # Varying data sizes

best_case_times, average_case_times, worst_case_times = btree.analyze_deletion(data_sizes)

plot_deletion_analysis(data_sizes, best_case_times, average_case_times, worst_case_times)
