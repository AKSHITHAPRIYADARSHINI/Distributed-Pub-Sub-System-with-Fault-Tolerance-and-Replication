import time
import random
import matplotlib.pyplot as plt

class Node:
    def __init__(self, node_id):
        self.node_id = node_id
        self.data = {}
        self.is_active = True

    def update(self, key, value):
        if self.is_active:
            self.data[key] = value

    def read(self, key):
        if self.is_active:
            return self.data.get(key, None)
        return None


class DistributedSystem:
    def __init__(self, num_nodes):
        self.nodes = [Node(i) for i in range(num_nodes)]
        self.replica_logs = []

    def replicate(self, key, value, consistency="eventual"):
        for node in self.nodes:
            if consistency == "strong":
                node.update(key, value)
            elif consistency == "eventual":
                if node.is_active:
                    node.update(key, value)
                    time.sleep(random.uniform(0.1, 0.5))  # Simulate delay
            self.replica_logs.append((time.time(), node.node_id, key, node.read(key)))

    def inject_fault(self, node_id):
        self.nodes[node_id].is_active = False

    def recover_node(self, node_id):
        self.nodes[node_id].is_active = True


def experiment_fault_tolerance():
    system = DistributedSystem(5)
    faults = []

    # Perform initial replication
    print("Initial replication...")
    system.replicate("key1", "value1", consistency="eventual")

    # Inject a fault
    print("Injecting faults...")
    faults.append(time.time())
    system.inject_fault(2)
    system.replicate("key2", "value2", consistency="eventual")

    # Recover from fault
    print("Recovering node...")
    faults.append(time.time())
    system.recover_node(2)
    system.replicate("key3", "value3", consistency="eventual")

    return system.replica_logs, faults


# Generate Graph
def plot_results(logs, faults):
    times, nodes, keys, values = zip(*logs)
    plt.figure(figsize=(10, 5))

    plt.scatter(times, nodes, c='blue', label="Replication Events")
    for fault_time in faults:
        plt.axvline(x=fault_time, color='red', linestyle='--', label="Fault Event")

    plt.xlabel("Time")
    plt.ylabel("Node ID")
    plt.title("Replication Events and Fault Tolerance")
    plt.legend()
    plt.show()


# Run experiment and plot results
logs, faults = experiment_fault_tolerance()
plot_results(logs, faults)
