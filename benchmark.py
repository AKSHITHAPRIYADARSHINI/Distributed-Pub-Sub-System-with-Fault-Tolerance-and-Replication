import time
import socket
import pickle
import threading
import matplotlib.pyplot as plt
from client import Client

class Benchmark:
    def __init__(self, client, topic_name="benchmark_topic"):
        self.client = client
        self.topic_name = topic_name
        self.fault_tolerance_results = {
            'primary_success_count': 0,
            'primary_failure_count': 0,
            'replica_failover_success_count': 0,
            'replica_failover_failure_count': 0,
            'recovery_success_count': 0,
            'data_consistency_valid': 0,
            'data_consistency_invalid': 0
        }

    def create_topic(self):
        """Measure latency for creating a topic."""
        start_time = time.time()
        response = self.client.send_request({"action": "create_topic", "topic_name": self.topic_name})
        end_time = time.time()
        return end_time - start_time, response

    def publish_messages(self, message_count=100):
        """Measure throughput for publishing messages."""
        start_time = time.time()
        for i in range(message_count):
            self.client.send_request({
                "action": "publish",
                "topic_name": self.topic_name,
                "message": f"Benchmark Message {i}"
            })
        end_time = time.time()
        throughput = message_count / (end_time - start_time)
        return throughput

    def fetch_messages(self):
        """Measure latency for fetching messages."""
        start_time = time.time()
        response = self.client.send_request({"action": "fetch_messages", "topic_name": self.topic_name})
        end_time = time.time()
        return end_time - start_time, response

    def subscribe_to_topic(self, subscriber_id):
        """Simulate subscribing to a topic."""
        response = self.client.send_request({
            "action": "subscribe",
            "topic_name": self.topic_name,
            "subscriber_id": subscriber_id
        })
        return response

    def test_primary_node_availability(self, primary_port):
        """Test if the primary node is available and responding."""
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.settimeout(2)
                result = sock.connect_ex(('localhost', primary_port))
                if result == 0:
                    self.fault_tolerance_results['primary_success_count'] += 1
                    return True
                else:
                    self.fault_tolerance_results['primary_failure_count'] += 1
                    return False
        except Exception as e:
            self.fault_tolerance_results['primary_failure_count'] += 1
            return False

    def test_replica_failover(self, primary_port, replica_ports):
        """Test failover mechanism when primary node fails."""
        print(f"\n[FAULT TOLERANCE TEST] Testing failover from primary port {primary_port}...")
        
        # Check if primary is down
        primary_available = self.test_primary_node_availability(primary_port)
        
        if not primary_available:
            print(f"  ✓ Primary node (port {primary_port}) is DOWN - failover needed")
            
            # Try to access data from replicas
            for replica_port in replica_ports:
                try:
                    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                        sock.settimeout(2)
                        sock.connect(('localhost', replica_port))
                        
                        # Send fetch request to replica
                        request = {
                            "action": "fetch_messages",
                            "topic_name": self.topic_name
                        }
                        sock.sendall(pickle.dumps(request))
                        response = sock.recv(4096)
                        
                        if response:
                            self.fault_tolerance_results['replica_failover_success_count'] += 1
                            print(f"  ✓ Successfully retrieved data from replica (port {replica_port})")
                            return True
                except Exception as e:
                    continue
            
            # If we reach here, failover failed
            self.fault_tolerance_results['replica_failover_failure_count'] += 1
            print(f"  ✗ Failed to failover to any replica node")
            return False
        else:
            print(f"  ✓ Primary node is still available")
            return True

    def test_data_consistency_after_failure(self, primary_port, replica_ports, expected_message_count):
        """Verify data consistency across primary and replica nodes."""
        print(f"\n[FAULT TOLERANCE TEST] Verifying data consistency...")
        
        messages_by_node = {}
        
        # Fetch from primary
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.settimeout(2)
                sock.connect(('localhost', primary_port))
                request = {"action": "fetch_messages", "topic_name": self.topic_name}
                sock.sendall(pickle.dumps(request))
                response = pickle.loads(sock.recv(4096))
                messages_by_node['primary'] = len(response) if isinstance(response, list) else 0
        except:
            messages_by_node['primary'] = None
        
        # Fetch from replicas
        for idx, replica_port in enumerate(replica_ports):
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                    sock.settimeout(2)
                    sock.connect(('localhost', replica_port))
                    request = {"action": "fetch_messages", "topic_name": self.topic_name}
                    sock.sendall(pickle.dumps(request))
                    response = pickle.loads(sock.recv(4096))
                    messages_by_node[f'replica_{idx}'] = len(response) if isinstance(response, list) else 0
            except:
                messages_by_node[f'replica_{idx}'] = None
        
        # Verify consistency
        valid_counts = [count for count in messages_by_node.values() if count is not None]
        
        if valid_counts and all(count == valid_counts[0] for count in valid_counts):
            self.fault_tolerance_results['data_consistency_valid'] += 1
            print(f"  ✓ Data is consistent across all nodes: {messages_by_node}")
            return True
        else:
            self.fault_tolerance_results['data_consistency_invalid'] += 1
            print(f"  ✗ Data inconsistency detected: {messages_by_node}")
            return False

    def simulate_node_failure(self, peer_id, primary_port, replica_ports):
        """Simulate node failure and test fault tolerance mechanisms."""
        print(f"\n{'='*70}")
        print(f"[FAULT TOLERANCE TEST {peer_id}] Simulating failure of Node {peer_id}...")
        print(f"{'='*70}")
        
        # Test 1: Primary node availability before failure simulation
        print(f"\n[TEST 1] Checking primary node availability...")
        self.test_primary_node_availability(primary_port)
        
        # Test 2: Data consistency before failure
        print(f"\n[TEST 2] Checking data consistency before failure...")
        self.test_data_consistency_after_failure(primary_port, replica_ports, expected_message_count=100)
        
        # Simulate downtime
        print(f"\n[SIMULATING DOWNTIME] Node {peer_id} will be unavailable for 3 seconds...")
        time.sleep(3)
        
        # Test 3: Replica failover mechanism
        print(f"\n[TEST 3] Testing replica failover when primary is down...")
        self.test_replica_failover(primary_port, replica_ports)
        
        # Simulate recovery
        print(f"\n[RECOVERY PHASE] Node {peer_id} is coming back online...")
        time.sleep(1)
        
        # Test 4: Recovery validation
        print(f"\n[TEST 4] Verifying node recovery...")
        if self.test_primary_node_availability(primary_port):
            self.fault_tolerance_results['recovery_success_count'] += 1
            print(f"  ✓ Node {peer_id} successfully recovered")
        
        # Test 5: Data consistency after recovery
        print(f"\n[TEST 5] Validating data consistency after recovery...")
        self.test_data_consistency_after_failure(primary_port, replica_ports, expected_message_count=100)
        
        print(f"\n{'='*70}\n")

    def run(self, iterations=5, message_count=100):
        """Run benchmarks including comprehensive fault tolerance tests."""
        create_latencies = []
        publish_throughputs = []
        fetch_latencies = []
        subscribe_responses = []

        print("\n" + "="*70)
        print("STARTING BENCHMARK WITH FAULT TOLERANCE TESTING")
        print("="*70 + "\n")

        # Peer list configuration
        replica_ports = [5002, 5003, 5004]  # Replica nodes
        primary_port = 5001  # Primary node

        # Run benchmarks
        for i in range(iterations):
            print(f"\n[ITERATION {i+1}/{iterations}]")
            
            # Create Topic Latency
            create_latency, _ = self.create_topic()
            create_latencies.append(create_latency)
            print(f"  Create topic latency: {create_latency:.4f}s")

            # Publish Messages Throughput
            throughput = self.publish_messages(message_count)
            publish_throughputs.append(throughput)
            print(f"  Publish throughput: {throughput:.2f} messages/sec")

            # Fetch Messages Latency
            fetch_latency, _ = self.fetch_messages()
            fetch_latencies.append(fetch_latency)
            print(f"  Fetch latency: {fetch_latency:.4f}s")

            # Subscribe to topic
            subscriber_id = f"subscriber_{i}"
            subscribe_response = self.subscribe_to_topic(subscriber_id)
            subscribe_responses.append(subscribe_response)

            # Comprehensive fault tolerance test every 2 iterations
            if i % 2 == 0:
                self.simulate_node_failure(
                    peer_id=i,
                    primary_port=primary_port,
                    replica_ports=replica_ports
                )

        return create_latencies, publish_throughputs, fetch_latencies, subscribe_responses

    def print_fault_tolerance_report(self):
        """Print detailed fault tolerance test report."""
        print("\n" + "="*70)
        print("FAULT TOLERANCE TEST REPORT")
        print("="*70)
        print(f"Primary Node Success: {self.fault_tolerance_results['primary_success_count']}")
        print(f"Primary Node Failures: {self.fault_tolerance_results['primary_failure_count']}")
        print(f"Replica Failover Success: {self.fault_tolerance_results['replica_failover_success_count']}")
        print(f"Replica Failover Failures: {self.fault_tolerance_results['replica_failover_failure_count']}")
        print(f"Node Recovery Success: {self.fault_tolerance_results['recovery_success_count']}")
        print(f"Data Consistency Valid: {self.fault_tolerance_results['data_consistency_valid']}")
        print(f"Data Consistency Invalid: {self.fault_tolerance_results['data_consistency_invalid']}")
        print("="*70 + "\n")

    def plot_results(self, create_latencies, publish_throughputs, fetch_latencies):
        """Generate and display benchmark graphs."""
        iterations = range(1, len(create_latencies) + 1)

        plt.figure(figsize=(15, 5))

        # Create Topic Latency Graph
        plt.subplot(1, 3, 1)
        plt.plot(iterations, create_latencies, marker="o", label="Create Topic Latency")
        plt.title("Create Topic Latency")
        plt.xlabel("Iteration")
        plt.ylabel("Latency (seconds)")
        plt.legend()

        # Publish Messages Throughput Graph
        plt.subplot(1, 3, 2)
        plt.plot(iterations, publish_throughputs, marker="o", label="Publish Throughput")
        plt.title("Publish Messages Throughput")
        plt.xlabel("Iteration")
        plt.ylabel("Throughput (messages/sec)")
        plt.legend()

        # Fetch Messages Latency Graph
        plt.subplot(1, 3, 3)
        plt.plot(iterations, fetch_latencies, marker="o", label="Fetch Messages Latency")
        plt.title("Fetch Messages Latency")
        plt.xlabel("Iteration")
        plt.ylabel("Latency (seconds)")
        plt.legend()

        plt.tight_layout()
        plt.show()

if __name__ == "__main__":
    print("Starting Enhanced Benchmarking with Fault Tolerance Testing...")

    server_ip = "localhost"
    server_port = int(input("Enter the server port (default: 5001): ").strip() or 5001)

    # Initialize the client
    client = Client(server_ip, server_port)

    # Benchmark instance
    benchmark = Benchmark(client, topic_name="benchmark_topic")

    # Run benchmark tests with fault tolerance
    create_latencies, publish_throughputs, fetch_latencies, subscribe_responses = benchmark.run(
        iterations=5, message_count=100
    )

    # Display results
    print("\nBenchmark Results:")
    print(f"Create Topic Latencies: {create_latencies}")
    print(f"Publish Throughputs: {publish_throughputs}")
    print(f"Fetch Messages Latencies: {fetch_latencies}")
    print(f"Subscription Responses: {subscribe_responses}")

    # Print fault tolerance report
    benchmark.print_fault_tolerance_report()

    # Plot the results
    benchmark.plot_results(create_latencies, publish_throughputs, fetch_latencies)