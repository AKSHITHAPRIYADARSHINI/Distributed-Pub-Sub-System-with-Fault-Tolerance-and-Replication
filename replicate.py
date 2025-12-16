import random
import time

class ReplicationManager:
    def __init__(self, replication_factor=2, consistency_model="strong"):
        self.replication_factor = replication_factor
        self.consistency_model = consistency_model  # "strong" or "eventual"
        self.topic_replicas = {}  # {topic_name: [peer_list]}

    def replicate_topic(self, topic, peer_list):
        """Replicate a topic to the nearest peers."""
        sorted_peers = sorted(peer_list, key=lambda _: random.randint(1, 100))  # Simulate proximity
        self.topic_replicas[topic] = sorted_peers[:self.replication_factor]
        print(f"Replicated topic '{topic}' to {self.topic_replicas[topic]}")

    def synchronize_replicas(self, topic, message):
        """Synchronize replicas of a topic."""
        replicas = self.topic_replicas.get(topic, [])
        if self.consistency_model == "strong":
            for peer in replicas:
                print(f"Strong sync: Sending message '{message}' to replica {peer}")
        elif self.consistency_model == "eventual":
            for peer in replicas:
                print(f"Eventual sync: Queuing message '{message}' for replica {peer}")
                time.sleep(random.uniform(0.1, 0.5))  # Simulate delay
