import socket
import pickle

class Client:
    def __init__(self, server_ip="localhost", server_port=5001):
        self.server_ip = server_ip
        self.server_port = server_port

    def send_request(self, request):
        """Send a request to the peer server."""
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
                client.connect((self.server_ip, self.server_port))
                client.send(pickle.dumps(request))

                # Receive and handle large data in chunks
                data = b""
                while True:
                    chunk = client.recv(4096)  # Increase buffer size to 4096 bytes
                    if not chunk:
                        break
                    data += chunk

                print(f"Received {len(data)} bytes of data")  # Debug: Log data size
                return pickle.loads(data)
        except ConnectionError as e:
            print(f"Connection error: {e}")
            return {"status": "connection_failed"}

if __name__ == "__main__":
    print("Welcome to the Pub/Sub Client!")

    server_ip = "localhost"
    server_port = int(input("Enter the server port (default: 5001): ").strip() or 5001)

    client = Client(server_ip, server_port)

    while True:
        print("\nChoose an action:")
        print("1. Create a Topic")
        print("2. Publish a Message to a Topic")
        print("3. Fetch Messages from a Topic")
        print("4. Subscribe to a Topic")
        print("5. List All Topics")
        print("6. Exit")
        choice = input("Enter your choice (1/2/3/4/5/6): ").strip()

        if choice == "1":
            topic_name = input("Enter the topic name: ").strip()
            response = client.send_request({"action": "create_topic", "topic_name": topic_name})
            print(f"Response: {response}")

        elif choice == "2":
            topic_name = input("Enter the topic name: ").strip()
            message = input("Enter the message to publish: ").strip()
            response = client.send_request({"action": "publish", "topic_name": topic_name, "message": message})
            print(f"Response: {response}")

        elif choice == "3":
            topic_name = input("Enter the topic name: ").strip()
            response = client.send_request({"action": "fetch_messages", "topic_name": topic_name})
            print(f"Messages: {response}")

        elif choice == "4":
            topic_name = input("Enter the topic name to subscribe: ").strip()
            subscriber_id = input("Enter your subscriber ID: ").strip()
            response = client.send_request({"action": "subscribe", "topic_name": topic_name, "subscriber_id": subscriber_id})
            print(f"Response: {response}")

        elif choice == "5":
            response = client.send_request({"action": "fetch_topics"})
            print(f"Available Topics: {list(response.keys())}")

        elif choice == "6":
            print("Exiting Pub/Sub Client. Goodbye!")
            break

        else:
            print("Invalid choice. Please select a valid action.")
