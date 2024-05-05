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

    def remove_from_leaf(self, idx):
        self.keys.pop(idx)

    def remove_from_non_leaf(self, idx):
        key = self.keys[idx]
        if len(self.children[idx].keys) >= BTree.t:
            pred = self.children[idx].get_max()
            self.keys[idx] = pred
            self.children[idx].delete(pred)
        elif len(self.children[idx + 1].keys) >= BTree.t:
            succ = self.children[idx + 1].get_min()
            self.keys[idx] = succ
            self.children[idx + 1].delete(succ)
        else:
            self.merge_children(idx)
            self.children[idx].delete(key)

    def get_min(self):
        if self.leaf:
            return self.keys[0]
        return self.children[0].get_min()

    def get_max(self):
        if self.leaf:
            return self.keys[-1]
        return self.children[-1].get_max()

    def merge_children(self, idx):
        child = self.children[idx]
        sibling = self.children[idx + 1]
        child.keys.append(self.keys[idx])
        child.keys.extend(sibling.keys)
        if not child.leaf:
            child.children.extend(sibling.children)
        self.keys.pop(idx)
        self.children.pop(idx + 1)

    def borrow_from_prev(self, idx):
        child = self.children[idx]
        sibling = self.children[idx - 1]
        child.keys.insert(0, self.keys[idx - 1])
        if not child.leaf:
            child.children.insert(0, sibling.children.pop())
        self.keys[idx - 1] = sibling.keys.pop()

    def borrow_from_next(self, idx):
        child = self.children[idx]
        sibling = self.children[idx + 1]
        child.keys.append(self.keys[idx])
        if not child.leaf:
            child.children.append(sibling.children.pop(0))
        self.keys[idx] = sibling.keys.pop(0)

    def fill_child(self, idx):
        if idx != 0 and len(self.children[idx - 1].keys) >= BTree.t:
            self.borrow_from_prev(idx)
        elif idx != len(self.keys) and len(self.children[idx + 1].keys) >= BTree.t:
            self.borrow_from_next(idx)
        else:
            if idx != len(self.keys):
                self.merge_children(idx)
            else:
                self.merge_children(idx - 1)

    def delete(self, key):
        idx = self.find_key(key)
        if idx < len(self.keys) and self.keys[idx] == key:
            if self.leaf:
                self.remove_from_leaf(idx)
            else:
                self.remove_from_non_leaf(idx)
        else:
            if self.leaf:
                print("Key not found")
                return
            flag = idx == len(self.keys)
            if len(self.children[idx].keys) < BTree.t:
                self.fill_child(idx)
            if flag and idx > len(self.keys):
                self.children[idx - 1].delete(key)
            else:
                self.children[idx].delete(key)

    def search(self, key):
        idx = self.find_key(key)
        if idx < len(self.keys) and self.keys[idx] == key:
            return True
        if self.leaf:
            return False
        return self.children[idx].search(key)


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

    def search(self, key):
        return self.root.search(key)

    def delete(self, key):
        if not self.search(key):
            print("Key not found")
            return
        self.root.delete(key)
        if len(self.root.keys) == 0:
            if len(self.root.children) > 0:
                self.root = self.root.children[0]
            else:
                self.root = BTreeNode(leaf=True)


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

    def benchmark_search(self, data):
        start_time = time.time()
        for key in data:
            self.btree.search(key)
        end_time = time.time()
        return end_time - start_time

    def benchmark_deletion(self, data):
        start_time = time.time()
        for key in data:
            self.btree.delete(key)
        end_time = time.time()
        return end_time - start_time

    def run_benchmarks(self, data_sizes):
        insertion_times = []
        search_times = []
        deletion_times = []

        for size in data_sizes:
            data = self.generate_random_data(size)

            insertion_time = self.benchmark_insertion(data)
            insertion_times.append(insertion_time)

            search_time = self.benchmark_search(data)
            search_times.append(search_time)

            deletion_time = self.benchmark_deletion(data)
            deletion_times.append(deletion_time)

        return insertion_times, search_times, deletion_times

def plot_results(data_sizes, insertion_times, search_times, deletion_times):
    plt.plot(data_sizes, insertion_times, label='Insertion')
    plt.plot(data_sizes, search_times, label='Search')
    plt.plot(data_sizes, deletion_times, label='Deletion')
    plt.xlabel('Data Size')
    plt.ylabel('Time (seconds)')
    plt.title('B-tree Benchmark Results')
    plt.legend()
    plt.show()

# Example usage:
btree = BenchmarkBTree(3)
data_sizes = [1000, 5000, 10000, 20000, 50000]  # Varying data sizes

insertion_times, search_times, deletion_times = btree.run_benchmarks(data_sizes)

plot_results(data_sizes, insertion_times, search_times, deletion_times)
