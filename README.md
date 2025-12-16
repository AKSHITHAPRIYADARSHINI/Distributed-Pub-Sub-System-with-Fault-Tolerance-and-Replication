# Decentralized Pub/Sub System with Replication and Fault Tolerance

## Introduction

This report details the design and implementation of a distributed system featuring replicated topics for performance optimization, fault tolerance, and dynamic topology reconfiguration. It evaluates API functionality, node synchronization, failure recovery, and scalability, demonstrating robustness and adaptability through benchmarking and analysis. The system balances performance with reliability for efficient distributed operations.

## Table of Contents
- [Features](#features)
- [Components](#files)
- [Technology & Libraries](#technologies&libraries)
- [Installation](#installation)
- [Project Structure](#order)
- [Usage](#running-the-application)

## Features
- **Peer-to-Peer Architecture** : Peer nodes independently manage topics and interact with other peers, following a decentralized architecture.
- **Topic Management**: Peers can create, list, and publish to topics, allowing dynamic and flexible topic management.
- **Replication**: Topics are replicated to other peers to ensure fault tolerance and data availability.
- **Subscription Management**: Peers can subscribe to topics and receive real-time updates when messages are published.
- **Multithreading**: Uses multithreading to handle multiple incoming connections and requests simultaneously, ensuring non-blocking operations.
- **Node Management**: Manages the list of peers in the network, handling node addition and removal.
- **Failure Detection**: Detects node failures via heartbeat signals and reroutes requests to replica nodes if the main node is down.
- **Dynamic Topology**: Supports the addition and removal of peers during runtime, allowing the system to adapt to changing network conditions.
- **Heartbeat Handling**: Periodically sends and listens for heartbeat signals to detect node status and failures.
- **Topic Replication**: Replicates topics across multiple peers to improve data availability and fault tolerance.
- **Replication Factor**: Defines how many replicas each topic will have on different peers, ensuring optimized data access.
- **Synchronization**: Synchronizes messages across replica nodes when a message is published to a topic, ensuring consistency.
- **Fault Tolerance**: Ensures that topics are still accessible from replica nodes in case the main node fails.
- **Client Requests**: The client sends requests to the peer node for actions such as creating topics, publishing messages, and fetching messages.
- **TCP Communication**: Uses TCP sockets to send and receive data from the peer nodes, ensuring reliable communication.
- **Subscription Mechanism**: Clients can subscribe to topics and receive notifications of new messages.
- **Error Handling**: Handles errors like connection failures and invalid actions, providing appropriate feedback to the user.

## Components
- **peer.py**: Implements a peer node in a decentralized P2P system, handling topic creation, publishing, subscribing, and replication. It supports multithreading and fault tolerance through replica nodes.

- **client.py**: Provides a command-line interface for interacting with peer nodes. Supports creating topics, publishing messages, subscribing to topics, and fetching messages, with error handling for failed connections.

- **benchmark.py**: Benchmarks the system by measuring latency and throughput for topic creation, message publishing, and subscription. Results are visualized with Matplotlib for performance analysis.

- **replicate.py**: Manages topic replication across multiple peers to ensure fault tolerance and data availability. Synchronizes messages between replica nodes.

- **node_manager.py**: Manages peer node list, detects failures, and reroutes requests to replica nodes. Supports dynamic addition/removal of peers and uses heartbeat signals for node monitoring.

## Technologies & Libraries
- Sockets (TCP/IP): For communication between peers and clients.
- Multithreading: For concurrent handling of multiple client connections.
- Pickle: For serializing data for transmission.
- Data Structures: Lists, sets, and dictionaries for managing peer lists and topics.
- Heartbeat Mechanism: For fault detection in peers.
- Matplotlib: For visualizing benchmarking results.
- Time Module: For measuring performance metrics like latency and throughput.


## Installation
**Step 1: Install Python and Pip
Make sure you have Python 3.x and pip installed.

For Ubuntu/Debian:

bash
[Copy code]
sudo apt update
sudo apt install python3 python3-pip

For CentOS/Fedora:

bash
[Copy code]
sudo yum install python3 python3-pip

Verify installation:

bash
[Copy code]
python3 --version
pip3 --version

**Step 2: Install Required Libraries

Use pip to install Matplotlib , Pickle:

bash
[Copy code]
pip3 install matplotlib  or
pip install -r requirements.txt

(or)

pip3 install -r requirements.txt
from the document made in the PA2 zip file.

## Project Structure 
    ├── peer.py                # Peer server code (handles topics and connections)
    ├── client.py              # Client code (sends requests to peer nodes)
    ├── benchmark.py           # Benchmark script for testing latency and throughput
    ├── replicate.py           # Replication manager (handles topic replication)
    ├── node_manager.py        # Node manager (handles peer nodes and failure recovery)


## Usage
--**Step 1** : Starting the Peer Network 

1. Open a terminal window. 
2. Run peer.py to initialize all peer nodes after importing the step 2 and step 3 files: 
Open 8 terminals or run 8 instances of peer.py, each with different node_id and port: 
bash 
[Copy code] 
python peer.py 
Enter unique node_id and port for each instance (e.g., 5001, 5002, ...). 
Each node will begin listening on its unique port for incoming connections. 

--**Step 2**: Add node_manager.py and replicate.py file into the programming platform 
1. import the node_manager.py file from the zip file into the vs code platform 
2. import the replicate.py file from the zip file into the vs code platform.  

--**Step 3**: Using the Client 
To run client.py, use the following format: 
bash 
[Copy code] 
python client.py 

**Available Actions in the Client** 

1. ` Create a Topic ` 
Action: "create_topic" 
Description: This action creates a new topic on the server. 
Input: Topic name (string). 
Output: Confirmation message indicating that the topic was created. 
Example: 
[Copy code] 
Enter the topic name: my_new_topic 
Response: {'status': 'topic_created', 'topic': 'my_new_topic'} 

2. ` Publish a Message to a Topic ` 
Action: "publish" 
Description: This action publishes a message to an existing topic. 
Input: Topic name (string), Message (string). 
Output: Confirmation message indicating that the message was successfully published. 
Example: 
[Copy code] 
Enter the topic name: my_new_topic 
Enter the message to publish: Hello, this is a test message! 
Response: {'status': 'message_published'} 

3. ` Fetch Messages from a Topic ` 
Action: "fetch_messages" 
Description: This action fetches all messages from a specified topic. 
Input: Topic name (string). 
Output: List of messages in the topic. 
Example: 
[Copy code] 
Enter the topic name: my_new_topic 
Messages: ['Hello, this is a test message!'] 
 
4.` Subscribe to a Topic ` 
Action: "subscribe" 
Description: This action subscribes a user to a specified topic, allowing them to receive notifications of new messages. 
Input: Topic name (string), Subscriber ID (string). 
Output: Confirmation message indicating that the subscription was successful. 
Example: 
[Copy code] 
Enter the topic name to subscribe: my_new_topic 
Enter your subscriber ID: user123 
Response: {'status': 'subscribed', 'topic': 'my_new_topic'} 
 
5.` List All Topics ` 
Action: "fetch_topics" 
Description: This action lists all available topics on the server. 
Input: None. 
Output: A list of all available topics. 
Example: 
[Copy code] 
Available Topics: ['my_new_topic', 'another_topic'] 

6.` Exit ` 
Action: No specific action; this is simply the command to exit the program. 
Input: None. 
Output: Exits the client program. 
Example: 
[Copy code] 
Exiting Pub/Sub Client. Goodbye! 


--**Step 3** : Benchmark the System 
Open a separate terminal and execute benchmark.py to assess latency and throughput: 
bash 
[Copy code] 
python benchmark.py 
------------------------------------------------------------------------------------------------------------------------------------------
#   D i s t r i b u t e d - P u b - S u b - S y s t e m - w i t h - F a u l t - T o l e r a n c e - a n d - R e p l i c a t i o n  
 