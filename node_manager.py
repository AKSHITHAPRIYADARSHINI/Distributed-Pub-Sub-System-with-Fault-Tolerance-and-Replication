import threading
import time

class NodeManager:
    def __init__(self, peer_list):
        self.nodes = {peer[0]: "online" for peer in peer_list}
        self.heartbeats = {}
        self.lock = threading.Lock()

    def start_heartbeat_monitor(self):
        """Monitor heartbeats to detect failures."""
        threading.Thread(target=self.monitor_heartbeats, daemon=True).start()

    def receive_heartbeat(self, node_id):
        """Update heartbeat timestamp for a node."""
        with self.lock:
            self.heartbeats[node_id] = time.time()

    def monitor_heartbeats(self):
        """Periodically check for missed heartbeats."""
        while True:
            with self.lock:
                for node, last_seen in list(self.heartbeats.items()):
                    if time.time() - last_seen > 5:
                        self.nodes[node] = "offline"
                        print(f"Node {node} marked offline.")
            time.sleep(1)

    def recover_node(self, node_id):
        """Recover a node and fetch its topics."""
        with self.lock:
            self.nodes[node_id] = "online"
            print(f"Node {node_id} rejoined and is online.")
