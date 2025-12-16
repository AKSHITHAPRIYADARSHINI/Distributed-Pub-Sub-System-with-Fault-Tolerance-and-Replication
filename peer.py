import socket
import threading
import time
import pickle
from replicate import ReplicationManager
from node_manager import NodeManager


class PeerNode:
    def __init__(self, node_id, port, peer_list):
        self.node_id = node_id
        self.port = port
        self.peer_list = peer_list  # [(peer_id, ip, port)]
        self.topics = {}  # {topic_name: [messages]}
        self.subscribers = {}  # {topic_name: [subscriber_ids]}
        self.replication_manager = ReplicationManager()
        self.node_manager = NodeManager(peer_list)
        self.lock = threading.Lock()

    def start_server(self):
        """Start the peer server."""
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind(('localhost', self.port))
        server.listen(5)
        print(f"Node {self.node_id} is online on port {self.port}.")
        threading.Thread(target=self.handle_connections, args=(server,), daemon=True).start()

    def handle_connections(self, server):
        """Handle incoming connections."""
        while True:
            client, _ = server.accept()
            threading.Thread(target=self.handle_client, args=(client,), daemon=True).start()

    def handle_client(self, client):
        """Handle requests from other nodes/clients."""
        try:
            data = pickle.loads(client.recv(4096))  # Increased buffer size
            response = self.process_request(data)
            client.sendall(pickle.dumps(response))  # Use sendall to ensure full data is sent
        finally:
            client.close()

    def process_request(self, data):
        """Process API actions."""
        action = data.get("action")
        if action == "create_topic":
            return self.create_topic(data['topic_name'])
        elif action == "publish":
            return self.publish_message(data['topic_name'], data['message'])
        elif action == "fetch_messages":
            return self.fetch_messages(data['topic_name'])
        elif action == "subscribe":
            return self.subscribe_to_topic(data['topic_name'], data['subscriber_id'])
        elif action == "fetch_topics":
            return self.topics
        return {"status": "unknown_action"}

    def create_topic(self, topic_name):
        """Create a new topic and replicate it."""
        with self.lock:
            if topic_name not in self.topics:
                self.topics[topic_name] = []
                self.subscribers[topic_name] = []
                self.replication_manager.replicate_topic(topic_name, self.peer_list)
        return {"status": "topic_created", "topic": topic_name}

    def publish_message(self, topic_name, message):
        """Publish a message to a topic."""
        with self.lock:
            if topic_name in self.topics:
                self.topics[topic_name].append(message)
                self.replication_manager.synchronize_replicas(topic_name, message)
                for subscriber in self.subscribers.get(topic_name, []):
                    print(f"Notification sent to subscriber {subscriber} for topic '{topic_name}'.")
                return {"status": "message_published"}
            return {"status": "topic_not_found"}

    def fetch_messages(self, topic_name):
        """Fetch all messages from a topic."""
        with self.lock:
            return self.topics.get(topic_name, [])

    def subscribe_to_topic(self, topic_name, subscriber_id):
        """Subscribe a user to a topic."""
        with self.lock:
            if topic_name in self.subscribers:
                if subscriber_id not in self.subscribers[topic_name]:
                    self.subscribers[topic_name].append(subscriber_id)
                return {"status": "subscribed", "topic": topic_name}
            return {"status": "topic_not_found"}

    def start_heartbeat_sender(self):
        """Send heartbeats to other peers."""
        def send_heartbeat():
            while True:
                for peer_id, ip, port in self.peer_list:
                    try:
                        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
                            client.connect((ip, port))
                            client.send(pickle.dumps({"action": "heartbeat", "node_id": self.node_id}))
                    except ConnectionError:
                        pass
                time.sleep(3)

        threading.Thread(target=send_heartbeat, daemon=True).start()


if __name__ == "__main__":
    print("Welcome to the Peer-to-Peer Pub/Sub System")

    node_id = int(input("Enter your node ID (e.g., 1, 2, 3, ...): "))
    port = int(input("Enter the port number (e.g., 5001, 5002, ...): "))

    peer_list = [(i, 'localhost', 5000 + i) for i in range(1, 9)]

    node = PeerNode(node_id=node_id, port=port, peer_list=peer_list)
    node.start_server()
    node.start_heartbeat_sender()

    while True:
        time.sleep(1)

