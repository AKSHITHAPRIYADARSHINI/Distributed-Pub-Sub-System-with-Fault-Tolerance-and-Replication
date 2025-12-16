# Distributed Pub/Sub System with Fault Tolerance and Replication

A robust peer-to-peer distributed publish/subscribe system featuring multi-node topic replication, automatic fault tolerance mechanisms, and dynamic topology management. Built with Python for efficient distributed computing and real-time message synchronization.

## Overview

This system implements a decentralized pub/sub architecture where peer nodes independently manage topics while coordinating with other peers through TCP communication. The architecture ensures high availability through topic replication, automatic failover to replica nodes when primary nodes fail, and consistent data synchronization across the network.

### Key Capabilities

- **Decentralized P2P Architecture**: Nodes operate independently with no single point of failure
- **Topic Replication**: Automatic replication across multiple nodes for fault tolerance
- **Fault Detection & Recovery**: Heartbeat-based monitoring with automatic failover mechanisms
- **Real-time Synchronization**: Message consistency maintained across all replicas
- **Concurrent Operations**: Multi-threaded connection handling for high throughput
- **Dynamic Topology**: Runtime node addition/removal without system restart
- **Comprehensive Benchmarking**: Performance metrics and fault tolerance validation

---

## Features

### Core Features
- ✅ **Topic Management** - Create, publish to, and list topics dynamically
- ✅ **Message Publishing** - Publish messages to topics with automatic replica synchronization
- ✅ **Subscription System** - Subscribe to topics and receive real-time notifications
- ✅ **Message Retrieval** - Fetch all messages from a topic with latency measurements

### Reliability Features
- ✅ **Fault Tolerance** - Automatic detection and recovery from node failures
- ✅ **Replica Failover** - Seamless rerouting to replica nodes when primary fails
- ✅ **Data Consistency** - Verified synchronization across all replica nodes
- ✅ **Heartbeat Monitoring** - Periodic health checks every 3 seconds
- ✅ **Failure Recovery** - Lost topics recovered from replicas during node recovery

### Performance Features
- ✅ **Multithreading** - Handle multiple concurrent connections
- ✅ **Throughput Benchmarking** - Measure messages published per second
- ✅ **Latency Analysis** - Monitor topic creation, fetch, and publish latencies
- ✅ **Performance Visualization** - Matplotlib graphs for trend analysis

---

## Architecture

### Components

```
┌─────────────────────────────────────────────────────────┐
│              Peer-to-Peer Network                       │
├─────────────────────────────────────────────────────────┤
│  PeerNode (peer.py)                                     │
│  ├─ Topics Management                                   │
│  ├─ Message Publishing                                  │
│  ├─ Subscription Handling                               │
│  ├─ ReplicationManager (replicate.py)                   │
│  ├─ NodeManager (node_manager.py)                       │
│  └─ Heartbeat Sender/Listener                           │
└─────────────────────────────────────────────────────────┘
         ↕                    ↕                    ↕
    TCP Socket           TCP Socket           TCP Socket
         ↕                    ↕                    ↕
    Node 1 (5001)       Node 2 (5002)       Node 3 (5003)
```

### File Structure

| File | Purpose |
|------|---------|
| **peer.py** | Main peer node implementation with TCP server, topic management, and replication logic |
| **client.py** | CLI client for sending requests to peer nodes |
| **benchmark.py** | Performance benchmarking with comprehensive fault tolerance testing |
| **replicate.py** | Topic replication manager for data consistency |
| **node_manager.py** | Network topology and failure detection management |
| **requirements.txt** | Python dependencies (matplotlib) |

---

## Installation & Setup

### Prerequisites
- Python 3.7 or higher
- pip (Python package manager)

### Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

Or install manually:

```bash
pip install matplotlib
```

### Step 2: Project Structure

Ensure all files are in the same directory:

```
project/
├── peer.py
├── client.py
├── benchmark.py
├── replicate.py
├── node_manager.py
├── requirements.txt
└── README.md
```

---

## Usage Guide

### Quick Start

#### Terminal 1: Start Peer Node 1
```bash
python peer.py
# Enter node ID: 1
# Enter port: 5001
```

#### Terminal 2: Start Peer Node 2
```bash
python peer.py
# Enter node ID: 2
# Enter port: 5002
```

#### Terminal 3: Start Peer Node 3 (Replica)
```bash
python peer.py
# Enter node ID: 3
# Enter port: 5003
```

#### Terminal 4: Run Client
```bash
python client.py
# Follow the interactive prompts
```

---

## Client Operations

Once the client runs, you can perform these operations:

### 1. Create a Topic
```
Action: create_topic
Input: Topic name (e.g., "events")
Response: {'status': 'topic_created', 'topic': 'events'}
```

### 2. Publish a Message
```
Action: publish
Input: Topic name and message content
Response: {'status': 'message_published'}
Note: Message automatically replicated to all replica nodes
```

### 3. Fetch Messages
```
Action: fetch_messages
Input: Topic name
Response: List of all messages in the topic
Measures: Retrieval latency
```

### 4. Subscribe to Topic
```
Action: subscribe
Input: Topic name and subscriber ID
Response: {'status': 'subscribed', 'topic': 'events'}
Note: Subscriber receives notifications on new messages
```

### 5. List All Topics
```
Action: fetch_topics
Input: None
Response: List of all available topics
```

### 6. Exit
```
Closes the client connection and exits
```

---

## Fault Tolerance Testing

Run the enhanced benchmark with automatic fault tolerance validation:

```bash
python benchmark.py
# Enter server port: 5001
```

### Test Coverage

The benchmark automatically performs:

1. **Primary Node Availability Test**
   - Verifies primary node connectivity
   - Records success/failure metrics

2. **Replica Failover Test**
   - Simulates primary node failure
   - Validates automatic failover to replicas
   - Verifies data retrieval from replica nodes

3. **Data Consistency Test**
   - Compares message counts across nodes
   - Validates replication synchronization
   - Detects data inconsistencies

4. **Node Recovery Test**
   - Monitors node recovery after failure
   - Validates post-recovery functionality

5. **Performance Benchmarks**
   - Topic creation latency
   - Message publishing throughput
   - Message fetch latency
   - Subscription latency

### Expected Output

```
======================================================================
FAULT TOLERANCE TEST 0 Simulating failure of Node 0...
======================================================================

[TEST 1] Checking primary node availability...
  ✓ Primary node (port 5001) is available

[TEST 2] Checking data consistency before failure...
  ✓ Data is consistent across all nodes

[TEST 3] Testing replica failover when primary is down...
  ✓ Successfully retrieved data from replica (port 5002)

[TEST 4] Verifying node recovery...
  ✓ Node recovered and is back online

[TEST 5] Validating data consistency after recovery...
  ✓ Data consistency verified

======================================================================
```

---

## Performance Metrics

The system generates three benchmark graphs:

### 1. Create Topic Latency
- X-axis: Iteration number
- Y-axis: Latency in seconds
- Shows topic creation performance over time

### 2. Publish Messages Throughput
- X-axis: Iteration number
- Y-axis: Messages per second
- Indicates system's message publishing capacity

### 3. Fetch Messages Latency
- X-axis: Iteration number
- Y-axis: Latency in seconds
- Shows retrieval performance consistency

---

## Configuration

### Peer Network Configuration (in peer.py)

```python
peer_list = [(i, 'localhost', 5000 + i) for i in range(1, 9)]
```

Adjust to your needs:
- First parameter: Peer ID
- Second parameter: IP address (change for distributed setup)
- Third parameter: Starting port

### Replication Factor

Default: Topics replicated to 3 replica nodes

To modify, edit `replicate.py`:
```python
replication_factor = 3  # Change as needed
```

### Heartbeat Interval

Default: 3 seconds

To modify in `peer.py`:
```python
time.sleep(3)  # Change to desired interval
```

---

## API Reference

### Client Request Format

```python
request = {
    "action": "create_topic",     # Required
    "topic_name": "my_topic",     # Required for topic operations
    "message": "Hello World",     # Required for publish
    "subscriber_id": "user_123"   # Required for subscribe
}
```

### Server Response Format

```python
# Success response
{"status": "topic_created", "topic": "my_topic"}

# Fetch response
["Message 1", "Message 2", "Message 3"]

# Error response
{"status": "topic_not_found"}
```

---

## System Requirements

| Component | Requirement |
|-----------|-------------|
| Python | 3.7+ |
| RAM | Minimum 512MB for 8 nodes |
| Network | TCP connectivity between nodes |
| OS | Windows, macOS, Linux |

---

## Troubleshooting

### Issue: "Address already in use" error
**Solution**: Wait 30 seconds or use a different port number

### Issue: Connection refused
**Solution**: Ensure all peer nodes are running before starting the client

### Issue: Data inconsistency detected
**Solution**: Verify all replica nodes are online and reachable

### Issue: Benchmark shows 0 throughput
**Solution**: Check that at least one peer node is running on the specified port

---

## Performance Characteristics

### Typical Latencies (Single Node)
- Topic Creation: ~0.001s
- Message Publishing: ~0.002s per message
- Message Fetch: ~0.001s

### Throughput
- Publishing: 100-500 messages/second (varies by system)
- Subscription Notifications: Real-time

### Fault Tolerance Metrics
- Failure Detection Time: ~3 seconds (heartbeat interval)
- Failover Time: ~1 second
- Data Consistency Verification: < 2 seconds

---

## Educational Value

This project demonstrates:
- **Distributed Systems**: P2P architecture without centralization
- **Fault Tolerance**: Replica failover and recovery patterns
- **Concurrency**: Multi-threaded network programming
- **Data Consistency**: Synchronization mechanisms
- **Performance Analysis**: Benchmarking distributed systems
- **Network Programming**: TCP socket communication
- **System Monitoring**: Heartbeat-based health checks

---

## Example Workflow

```bash
# Terminal 1: Start 3 peer nodes
python peer.py  # Node 1, port 5001
python peer.py  # Node 2, port 5002
python peer.py  # Node 3, port 5003

# Terminal 4: Run client
python client.py

# Client session:
> Create topic "news"
> Publish "Breaking News" to "news"
> Subscribe as "user1" to "news"
> Fetch messages from "news"
> [Simulate Node 1 failure]
> Messages still available from replicas

# Terminal 5: Run benchmark
python benchmark.py
> Generates performance graphs
> Validates fault tolerance
> Reports consistency metrics
```

---

## Contributing

For improvements or bug fixes:

1. Test changes locally on multiple nodes
2. Verify fault tolerance mechanisms still work
3. Run benchmark suite before committing
4. Document any configuration changes

---

## License

This project is provided as-is for educational purposes.

---

## Technical Details

### Message Flow

```
Client → PeerNode (create_topic)
         ↓
    PeerNode.create_topic()
         ↓
    ReplicationManager.replicate_topic()
         ↓
    Replicas on Node 2, 3, 4
         ↓
    Response: topic_created ✓
```

### Fault Tolerance Flow

```
Primary Node Down
         ↓
Heartbeat Timeout (3s)
         ↓
NodeManager.detect_failure()
         ↓
Client Request Received
         ↓
Failover to Replica
         ↓
Request Fulfilled ✓
```

---

##  Support

For questions about:
- **Distributed Systems**: Review the peer.py implementation
- **Fault Tolerance**: See benchmark.py fault tolerance tests
- **Replication**: Check replicate.py synchronization logic
- **Network Setup**: Modify peer_list in peer.py

---

**Last Updated**: December 2024  
**Version**: 1.0  
**Status**: Production Ready