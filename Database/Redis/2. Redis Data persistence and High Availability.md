# Chapter 2: Redis Data Persistence and High Availability

## 2.1 Persistence Mechanisms - RDB Snapshots vs AOF

Redis provides two main persistence mechanisms to prevent data loss in case of server failures, each with distinct trade-offs between performance and durability.

### RDB (Redis Database) Snapshots

RDB creates point-in-time snapshots of the entire dataset, saving it as a binary file called `dump.rdb`. The snapshot captures the complete state of all keys and values at a specific moment.

**How RDB Works**

When an RDB save is triggered, Redis forks a child process that writes the snapshot while the parent process continues handling client requests normally. This ensures minimal impact on server performance.

**RDB Configuration**

RDB saves can be triggered automatically using the `save` directive:

```
save 900 1        # Save after 900 seconds if at least 1 key changed
save 300 100      # Save after 300 seconds if at least 100 keys changed
save 60 10000     # Save after 60 seconds if at least 10,000 keys changed
```

**Advantages of RDB**

- Highly efficient and compact format, resulting in small file sizes ideal for backups
- Very fast recovery time on restart compared to AOF, especially with large datasets
- No impact on Redis performance after fork completes
- Supports point-in-time recovery by keeping multiple snapshots
- Can be easily transferred to other systems for disaster recovery

**Disadvantages of RDB**

- Data loss risk: All changes since the last snapshot are lost if server crashes
- Forking large datasets can cause brief performance impact or high memory usage
- Increased I/O load during snapshot creation
- Entire dataset must fit in memory to be saved

### AOF (Append-Only File)

AOF logs every write operation received by the server. On restart, Redis replays these operations to reconstruct the dataset. Commands are logged in the same format as the Redis protocol.

**How AOF Works**

Every write command (SET, INCR, LPUSH, etc.) is immediately appended to the AOF file. The server then syncs this data to disk based on the configured fsync policy.

**AOF fsync Policies**

**fsync always**: Syncs after every write command

- Maximum durability: only loses the current command being executed if crash occurs
- Lowest performance: each write waits for disk sync
- Use for: Critical data where loss is unacceptable

**fsync everysec** (default): Syncs once per second

- Balanced approach: typically lose at most 1-2 seconds of data
- Good performance: fsync happens in background without blocking writes
- Use for: Most production applications

**fsync no**: Let operating system decide when to fsync (typically 30 seconds)

- Best performance: no disk sync overhead
- Worst durability: can lose up to 30 seconds of data
- Use for: Non-critical caches where data loss is acceptable

**Advantages of AOF**

- Greater durability with configurable fsync policies
- Provides fine-grained control over performance vs durability trade-offs
- Human-readable format allows inspection and manual recovery
- Automatic background rewrite prevents file from growing infinitely
- Can write even if disk space is limited (continues in memory if AOF write fails)

**Disadvantages of AOF**

- Slower startup time compared to RDB, especially with large datasets
- Generally larger file size than RDB snapshots
- Can be slower in write-heavy workloads with aggressive fsync policies
- AOF rewrite can temporarily use significant disk I/O and memory

### AOF Rewrite

As AOF files grow, Redis periodically rewrites the AOF file to create a more compact representation of the dataset. Instead of replaying all historical commands, it creates an AOF file with just the current state.

**Automatic Rewrite Triggers**

```
auto-aof-rewrite-percentage 100    # Rewrite if size > 100% of last size
auto-aof-rewrite-min-size 64mb     # Only rewrite if file > 64MB
```

When both conditions are met, Redis background saves rewrite the AOF file while continuing to serve clients. During rewrite, new commands are buffered and appended after the rewrite completes.

## 2.2 AOF Rewrite and fsync Policies

### Understanding fsync Behavior

**fsync() System Call**: fsync ensures data written to file buffers is physically written to disk. Without fsync, data remains in the operating system's file buffer and could be lost during a crash.

**Performance Impact**: fsync is an expensive operation. Calling it after every write significantly impacts throughput but guarantees durability.

### AOF Rewrite Process

**Steps in AOF Rewrite**

1. Redis forks a background child process
2. Child process scans entire database and writes current state to new temporary AOF file
3. Parent process continues handling requests, buffering new write commands
4. Once child finishes writing, it signals parent
5. Parent appends buffered commands to temporary file
6. Temporary file is renamed to replace old AOF file

**Configuration Parameters**

```
appendfilename "appendonly.aof"           # AOF filename
appendonly yes                            # Enable AOF
appendfsync everysec                      # fsync policy
auto-aof-rewrite-percentage 100           # Rewrite trigger condition
auto-aof-rewrite-min-size 67108864        # 64MB minimum size for rewrite
aof-rewrite-incremental-fsync yes         # Incremental fsync during rewrite
```

### Hybrid Persistence (RDB + AOF)

Modern Redis supports combining both RDB and AOF for optimal durability:

```
aof-use-rdb-preamble yes
```

With hybrid persistence enabled, Redis periodically creates RDB snapshots but also maintains an AOF file with commands since the last snapshot. On restart, Redis loads the snapshot first (fast), then replays AOF commands.

**Benefits**

- Fast recovery using RDB base
- Enhanced durability with AOF incremental changes
- Reduced data loss window
- Combines advantages of both approaches

## 2.3 Data Durability Trade-offs and Performance Impact

### Durability vs Performance Matrix

| Approach       | Data Loss Risk       | Performance | Recovery Time | Use Case           |
| -------------- | -------------------- | ----------- | ------------- | ------------------ |
| No Persistence | All data on crash    | Best        | N/A           | Non-critical cache |
| RDB only       | Since last snapshot  | Excellent   | Fast          | Standard caching   |
| AOF (no fsync) | Up to 30 seconds     | Excellent   | Slow          | Non-critical data  |
| AOF (everysec) | Up to 2 seconds      | Good        | Slow          | Most applications  |
| AOF (always)   | Current command only | Poor        | Slow          | Critical data      |
| RDB + AOF      | Since last RDB       | Good        | Fast          | High availability  |

### Performance Considerations

**RDB Snapshot Impact**

- Fork operation can cause latency spike with very large datasets
- Memory usage temporarily doubles during fork (copy-on-write)
- Reduced performance during background save due to forking overhead
- Brief client-side latency (milliseconds to seconds for multi-GB datasets)

**AOF Impact**

- Write throughput reduced due to fsync overhead
- AOF rewrite can temporarily block reads/writes for brief periods
- Disk I/O during rewrite affects other operations
- CPU overhead for command logging is minimal

**Optimization Strategies**

- Use RDB for large datasets where periodic snapshots are acceptable
- Use AOF with `everysec` for most applications
- Use RDB + AOF for critical production systems
- Schedule RDB snapshots during low-traffic periods
- Monitor fsync blocking using Redis latency monitoring tools
- Use faster storage (SSD) to reduce fsync latency

## 2.4 Redis Replication (Master-Slave Architecture)

### Master-Slave Replication Overview

Redis replication is asynchronous by default, allowing high performance. The master node accepts all write operations and replicates changes to slave (replica) nodes. Slaves can serve read operations, distributing load across multiple instances.

**Key Characteristics**

- **Asynchronous**: Changes propagated to slaves with minimal delay (low latency)
- **Non-blocking**: Master continues accepting requests during replication
- **Cascading Support**: Slaves can have their own slaves, forming replication chains
- **Read Scaling**: Slaves handle read-only queries, reducing master load

### Replication Process

**Initial Connection**

1. Slave connects to master using SLAVEOF command
2. Slave sends PSYNC command with its replication ID and offset
3. Master checks if partial resync is possible

**Full Resynchronization**

When a slave connects for the first time or cannot perform partial resync:

1. Master starts background saving (BGSAVE), creating an RDB snapshot
2. Master begins buffering all write commands received during save
3. RDB snapshot is transferred to slave over the network
4. Slave saves RDB to disk, then loads it into memory
5. Master streams all buffered commands to slave
6. Slave executes commands to reach master's current state

**Partial Resynchronization**

When a slave reconnects after brief disconnection:

1. Slave sends PSYNC with last known replication ID and offset
2. Master checks if requested offset is still in replication backlog
3. If yes, master sends only commands since that offset (much faster)
4. If no, full resync is performed

### Replication ID and Offset

**Replication ID**: A 40-character pseudo-random string identifying the master's dataset history. Each master generates unique IDs; replicas inherit the master's ID.

**Replication Offset**: A monotonically increasing counter tracking bytes of replication stream sent. Incremented for every byte regardless of connected replicas.

**Example Replication State**

```
Master: replication_id=abc123xyz, offset=50000
Slave:  replication_id=abc123xyz, offset=49900
```

The slave is 100 bytes behind the master and needs commands representing those 100 bytes.

### Configuration

```
# On slave
slaveof master_ip master_port          # Set master (deprecated: use replicaof)
replicaof master_ip master_port        # Set master (Redis 5.0+)
slave-read-only yes                    # Prevent writes to slave (deprecated)
replica-read-only yes                  # Prevent writes to replica (Redis 5.0+)

# Replication buffer configuration
client-output-buffer-limit replica 256mb 64mb 60  # Slave output buffer

# Backlog for partial resync
repl-backlog-size 1mb                  # Default 1MB
repl-backlog-ttl 3600                  # Keep backlog 1 hour
```

## 2.5 Replication Offset and Partial Resynchronization

### Understanding Replication Offset

The replication offset represents the stream position in master-slave communication. Both master and slave maintain offsets to identify their position in replication history.

**Master Offset**: Incremented for every byte of commands generated, regardless of slaves

**Slave Offset**: Tracks the last byte position slave has successfully processed

**Backlog Buffer**: A circular buffer (default 1MB) on master storing recent commands for partial resync recovery

### Partial Resynchronization Process

**Scenario: Slave Disconnection and Reconnection**

```
Time 0: Slave connected, both at offset 1000
Time 5: Network fails, slave disconnects
Time 10: Master now at offset 2000 (1000 bytes of new commands)
Time 12: Slave reconnects
Slave sends: PSYNC replicationID 1000
Master checks if offset 1000 is in backlog
If yes: Send 1000 bytes of commands (partial resync)
If no: Send full RDB snapshot (full resync)
```

### Backlog Management

**Backlog Behavior**

- Commands written to circular buffer as they're executed
- Buffer stores commands as a replication stream (not raw Redis commands)
- When buffer fills, oldest data is overwritten
- TTL expires backlog if no replicas are connected

**Configuration Tuning**

For high-write workloads, increase backlog size to avoid unnecessary full resyncs:

```
repl-backlog-size 512mb                # Larger backlog
repl-backlog-ttl 7200                  # Longer TTL (2 hours)
```

**Why Partial Resync Matters**

- Avoids expensive full RDB snapshot transfer
- Dramatically reduces recovery time (milliseconds vs seconds/minutes)
- Reduces network bandwidth usage
- Minimizes master's fork overhead

### Common Partial Resync Failures

**Network Disconnection Too Long**: Backlog fills faster than new commands arrive on slave

**Example**: 1MB backlog fills in 10 seconds with high write rate; if disconnected for 30 seconds, partial resync fails

**Solution**: Increase `repl-backlog-size` or reduce `repl-backlog-ttl` for faster cleanup

**Replication ID Mismatch**: Slave has replication ID from different master's history

**Solution**: Manual failover uses `FAILOVER` command to preserve replication history

## 2.6 Redis Sentinel for Automatic Failover

### What is Redis Sentinel?

Sentinel is a distributed system that monitors master and replica instances, automatically promoting a replica to master when the master fails. It handles failover orchestration, configuration updates, and client notifications.

**Sentinel Responsibilities**

- **Monitoring**: Continuously checks master and replica health
- **Failure Detection**: Determines when master is unreachable
- **Failover**: Automatically promotes best replica to master
- **Configuration Management**: Notifies clients of new master address
- **Replica Reconfiguration**: Updates replicas to replicate from new master

### Sentinel Quorum Concept

**Quorum**: Minimum number of Sentinels that must agree master is down before initiating failover

```
sentinel monitor mymaster 127.0.0.1 6379 2
```

This configures monitoring of "mymaster" at 127.0.0.1:6379 with quorum of 2.

**Quorum vs Majority**

- **Quorum** (2 Sentinels): Minimum needed to declare failure
- **Majority** (3 out of 5 Sentinels): Required to authorize failover

Example with 5 Sentinels and quorum 2:

1. Two Sentinels detect master unreachable → failure confirmed
2. One Sentinel becomes failover leader candidate
3. Needs 3 votes from other Sentinels → majority reached
4. Failover proceeds

### Sentinel Configuration

**Basic Sentinel Setup**

```
sentinel monitor mymaster 127.0.0.1 6379 2
sentinel down-after-milliseconds mymaster 5000
sentinel failover-timeout mymaster 180000
sentinel parallel-syncs mymaster 1
sentinel auth-pass mymaster password
```

**Configuration Explanation**

| Option                  | Value    | Meaning                                   |
| ----------------------- | -------- | ----------------------------------------- |
| monitor                 | 2        | Quorum: 2 Sentinels must agree on failure |
| down-after-milliseconds | 5000     | 5 seconds to mark master as down          |
| failover-timeout        | 180000   | 180 seconds timeout for failover          |
| parallel-syncs          | 1        | 1 replica syncs at a time post-failover   |
| auth-pass               | password | Password for connecting to instances      |

### Failover Process

**Step-by-Step Failover**

1. **Failure Detection**: Quorum of Sentinels detect master unreachable
2. **Leader Election**: Sentinels elect a leader for failover
3. **Replica Selection**: Leader selects best replica based on:
   - Replication offset (most synced)
   - Priority configuration
   - Replica ID
4. **Promotion**: Elected replica promoted to master via SLAVEOF NO ONE
5. **Reconfiguration**: Other replicas reconfigured to replicate from new master
6. **Client Notification**: Sentinels notify clients of new master address
7. **Old Master Handling**: If old master recovers, becomes slave to new master

### Replica Selection Logic

Sentinel chooses replica for promotion considering:

```
# Priority (lower is better)
slave-priority 100

# Then checks:
1. Replication offset (most complete data)
2. Replica priority value
3. Replica ID (as tiebreaker)
```

## 2.7 Sentinel Configuration and Monitoring

### Key Sentinel Directives

**Monitoring Configuration**

```
sentinel monitor <master-name> <ip> <port> <quorum>
```

Multiple master sets can be monitored:

```
sentinel monitor master1 192.168.1.10 6379 2
sentinel monitor master2 192.168.1.11 6379 2
```

**Timing Configuration**

```
sentinel down-after-milliseconds mymaster 30000
# Master declared down after 30 seconds without response

sentinel failover-timeout mymaster 180000
# Failover timeout of 3 minutes

sentinel auth-pass mymaster redis-pass
# Password for connecting to master
```

### Sentinel Monitoring Commands

**Check Sentinel Status**

```
sentinel masters
# Lists all monitored masters

sentinel master mymaster
# Information about specific master

sentinel slaves mymaster
# Lists replicas of master

sentinel sentinels mymaster
# Lists other Sentinel instances
```

**Runtime Configuration**

```
sentinel monitor newmaster 192.168.1.20 6379 3
sentinel set mymaster down-after-milliseconds 40000
sentinel remove mymaster
```

### Monitoring and Alerts

**Important Metrics to Monitor**

- Master/replica availability
- Failover frequency and duration
- Replication lag
- Sentinel process health
- Configuration consistency across Sentinels

**Common Issues**

**Split Brain**: Network partition causes multiple masters

**Prevention**: Majority-based quorum ensures split doesn't allow multiple failovers

**Sentinel Cascade**: Sentinels lose quorum due to failures

**Solution**: Run odd number of Sentinels (3, 5, 7) to maintain majority

## 2.8 Redis Cluster for Horizontal Scaling and Sharding

### What is Redis Cluster?

Cluster is a distributed version of Redis providing horizontal scaling by partitioning data across multiple nodes. Each node stores a subset of the data, scaling both memory capacity and throughput.

**Cluster vs Master-Slave**

| Feature         | Master-Slave             | Cluster                          |
| --------------- | ------------------------ | -------------------------------- |
| Scaling         | Vertical only            | Horizontal                       |
| Data Partition  | All data on each replica | Data distributed across nodes    |
| Write Scaling   | No (single master)       | Yes (multiple masters)           |
| Fault Tolerance | One failure tolerated    | Multiple node failures tolerated |
| Complexity      | Simple                   | Complex                          |
| Client Support  | Simple                   | Requires cluster-aware client    |

### Cluster Architecture

Redis Cluster consists of multiple master nodes, each managing a subset of data. Each master can have replicas for redundancy.

**Example Cluster**

```
3 Masters + 3 Replicas (3-node cluster):
├─ Master A (slots 0-5461)
│  └─ Replica A1
├─ Master B (slots 5462-10922)
│  └─ Replica B1
└─ Master C (slots 10923-16383)
   └─ Replica C1
```

### Hash Slots

Redis Cluster uses hash slots to partition data. There are 16,384 hash slots (0-16383).

**Hash Slot Calculation**

```
HASH_SLOT = CRC16(key) mod 16384
```

Each master node is assigned a range of slots. All keys in a given slot go to the node owning that slot.

**Example Slot Distribution** (3 master nodes)

```
Master A: slots 0 – 5461
Master B: slots 5462 – 10922
Master C: slots 10923 – 16383
```

**Dynamic Slot Assignment**

Slots can be moved between nodes without downtime:

1. Source node prepares data for migration
2. Destination node pulls keys incrementally
3. Client redirects operations during migration
4. Process continues until all keys moved

### Multi-Key Operations and Hash Tags

Cluster supports multi-key operations only if all keys belong to the same slot.

**Hash Tags**: Force multiple keys into same slot

```
user:{123}:profile
user:{123}:settings
user:{123}:preferences
```

Only the part in braces `{123}` is hashed, ensuring all three keys go to the same slot.

**Multi-Key Command Example**

```
MSET user:{123}:profile "data" user:{123}:settings "config"
# Valid - both keys in same slot due to hash tag

MSET user:123 "data" user:456 "data"
# Invalid - keys in different slots
```

## 2.9 Cluster Slots and Hash Tags

### Slot Management Commands

**View Cluster Information**

```
cluster info                    # General cluster info
cluster nodes                   # Nodes and slot assignment
cluster slots                   # Slots and node mappings
cluster keyslot key             # Get slot for specific key
```

**Manual Slot Assignment**

```
cluster addslots 0-5461         # Assign slots to this node
cluster delslots 0-5461         # Remove slots from this node
cluster setslot 0 node node-id  # Migrate slot to specific node
```

### Hash Tags for Slot Locality

**Use Case**: Group related data together

```
# All user data in same node
user:{1001}:name = "Alice"
user:{1001}:email = "alice@example.com"
user:{1001}:score = 100

# Enables atomic operations
MGET user:{1001}:name user:{1001}:email user:{1001}:score
```

**Hash Tag Rules**

- Everything between first `{` and first `}` is the hash tag
- If no braces, entire key is hashed
- `{tag}` followed by other characters: only tag is hashed

```
foo{bar}baz          # Hash tag: "bar"
{baz}                # Hash tag: "baz"
hello{world}         # Hash tag: "world"
{a}{b}               # Hash tag: "a" (first occurrence)
nobraces             # Hash tag: "nobraces"
```

## 2.10 Cluster Failover and Topology Changes

### Cluster Failover Process

**Automatic Failover**

When master node fails, one of its replicas is promoted:

1. Replica detects master failure (no responses)
2. Replica increments its configEpoch
3. Replica sends CLUSTERDOWN messages to other nodes
4. Other nodes reach consensus on new master
5. Replica becomes new master automatically

**Manual Failover**

For maintenance or planned failover:

```
cluster failover [force|takeover]
```

- **FORCE**: Skip consensus, promote immediately
- **TAKEOVER**: Replica ignores master status

### Topology Changes

**Adding Nodes to Cluster**

```
# 1. Create new node in cluster mode
redis-server --cluster-enabled yes --port 7001

# 2. Use redis-cli to add slot range to new node
redis-cli --cluster add-node 127.0.0.1:7001 127.0.0.1:7000

# 3. Reshard slots from existing nodes to new node
redis-cli --cluster reshard 127.0.0.1:7000
```

**Removing Nodes from Cluster**

```
# 1. Migrate all slots from node to other nodes
redis-cli --cluster reshard 127.0.0.1:7000 \
  --from node-id \
  --to other-node-id

# 2. Once node has no slots, remove it
redis-cli --cluster del-node 127.0.0.1:7000 node-id
```

### Resharding and Rebalancing

**Resharding**: Moving slots from one node to another for load balancing

```
redis-cli --cluster reshard 127.0.0.1:7000 \
  --cluster-slots 1000 \
  --cluster-from node1 \
  --cluster-to node2 \
  --cluster-yes
```

**Online Resharding**: Can be performed without downtime; clients automatically redirected to new node

**Rebalancing**: Distributing slots evenly across all nodes

```
redis-cli --cluster rebalance 127.0.0.1:7000
```

### Cluster Client Redirection

Clients connecting to cluster must handle:

**MOVED**: Permanent slot ownership change

```
MOVED 1234 192.168.1.10:6379
# Slot 1234 now owned by 192.168.1.10:6379 permanently
```

**ASK**: Temporary redirection during migration

```
ASK 1234 192.168.1.10:6379
# Key temporarily available at new node, old node still owns slot
```

Cluster-aware clients (redis-py, node-redis, etc.) automatically handle these redirects and update their routing tables.

### Monitoring Cluster Health

**Cluster Health Checks**

```
cluster info                    # Node count, state
cluster nodes                   # Each node's status
redis-cli --cluster check       # Validate cluster consistency
```

**Common Cluster Issues**

**Split Brain**: Network partition creates two independent clusters

**Prevention**: Use minimum node count (typically 6+) and majority-based decisions

**Slot Gaps**: Some slots not assigned to any node

**Detection**: `cluster slots` shows incomplete coverage

**Recovery**: Manually assign slots using `cluster addslots`
