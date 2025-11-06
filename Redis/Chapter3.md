# Chapter 3: Advanced Redis Concepts

## 3.1 Redis Transactions (MULTI, EXEC, WATCH, DISCARD)

Redis transactions allow executing multiple commands atomically. All commands in a transaction are executed sequentially without interruption from other clients, ensuring atomicity at the Redis level.

### MULTI and EXEC

**MULTI** marks the start of a transaction block. After MULTI, all subsequent commands are queued instead of executed immediately.

**EXEC** executes all queued commands atomically. Redis ensures that no other commands from other clients will execute between the queued commands.

### Basic Transaction Pattern

```
MULTI
SET key1 value1
INCR counter
LPUSH mylist item
EXEC
```

**Execution Flow**

1. MULTI starts transaction mode for this connection
2. SET, INCR, LPUSH commands are queued (not executed)
3. EXEC executes all three commands atomically
4. Returns array of results: [OK, 1, 1] (or actual values)

### QUEUED Response

After MULTI, each command returns "QUEUED" instead of executing:

```
MULTI           → OK
SET key value   → QUEUED
GET key         → QUEUED
EXEC            → returns results array
```

### DISCARD Command

Aborts the transaction and discards all queued commands without executing them.

```
MULTI
SET key1 value1
DISCARD         → Transaction aborted
```

After DISCARD, the connection exits transaction mode and key1 is unchanged.

### Transaction Guarantees and Limitations

**What MULTI/EXEC Provides**

- **Atomic Execution**: All commands execute without other clients interfering
- **Queuing**: Commands execute in order as queued
- **All-or-Nothing**: Either all commands execute or transaction is aborted

**Important Limitations**

Unlike relational database transactions, Redis transactions:

- **No Rollback**: If a command fails execution, others still execute
- **No Partial Rollback**: Cannot undo commands within transaction
- **Syntax Errors Caught Early**: Command syntax errors are detected during MULTI phase

### Transaction Error Handling

**Syntax Errors (Before EXEC)**

```
MULTI
SET key1 value1
INCR              # Missing key - syntax error
EXEC              # Returns error, transaction aborted
```

**Runtime Errors (After EXEC)**

```
MULTI
LPUSH mykey item  # mykey doesn't exist (creates list)
INCR mykey        # Error - trying to increment a list
EXEC
```

The LPUSH succeeds and INCR fails, but both were attempted. Redis doesn't rollback LPUSH.

## 3.2 Optimistic Locking with WATCH

WATCH implements optimistic locking for conditional transaction execution. It monitors keys for changes and aborts the transaction if any watched key is modified.

### WATCH Mechanism

WATCH establishes a dependency: "Only execute this transaction if these keys remain unchanged."

### Basic WATCH Pattern

```
WATCH mykey
val = GET mykey
val = val + 1
MULTI
SET mykey val
EXEC
```

If another client modifies mykey between WATCH and EXEC, the transaction aborts (EXEC returns nil).

### Multi-Key WATCH

```
WATCH key1 key2 key3
MULTI
SET key1 value1
SET key2 value2
EXEC
```

Transaction aborts if ANY watched key is modified by another client.

### UNWATCH Command

Removes all watched keys from the current connection, allowing transaction to proceed even if watched keys changed.

```
WATCH mykey
val = GET mykey
if (val is already updated) {
    UNWATCH
    return
}
MULTI
SET mykey newval
EXEC
```

### Common Use Case: Atomic Increment with Check

```
WATCH counter
current = GET counter
if (current >= limit) {
    UNWATCH
    return "Limit exceeded"
}
MULTI
INCR counter
EXEC
```

Ensures counter doesn't exceed limit even with concurrent increments.

### WATCH Behavior

**Reset Points**

WATCH is automatically cleared after:

- EXEC (whether successful or failed)
- DISCARD (aborts transaction)
- New WATCH command (replaces previous watches)

**Transaction Conflict**

When watched key modified:

- EXEC returns nil (not false, not 0 - specifically nil)
- Application detects nil and retries from WATCH

### Real-World Example: Bank Transfer

```
def transfer_funds(from_account, to_account, amount):
    while true:
        WATCH from_account, to_account

        from_balance = GET from_account
        if (from_balance < amount):
            UNWATCH
            return "Insufficient funds"

        MULTI
        DECRBY from_account amount
        INCRBY to_account amount

        result = EXEC
        if (result is not nil):
            return "Transfer successful"
        # Retry if conflict detected
```

## 3.3 Pub/Sub Messaging Pattern

Redis Pub/Sub implements the publisher-subscriber messaging pattern for real-time communication between clients.

### Core Concepts

**Publisher**: Sends messages to channels using PUBLISH command

**Subscriber**: Listens for messages on channels using SUBSCRIBE command

**Channel**: Logical message conduit connecting publishers and subscribers

**Fire-and-Forget**: Messages are not persisted; only active subscribers receive them

### Basic Pub/Sub Operations

**Publishing Messages**

```
PUBLISH chat:room1 "Hello everyone!"
```

Returns number of subscribers that received the message.

**Subscribing to Channels**

```
SUBSCRIBE chat:room1 chat:room2
```

Puts client in subscriber mode. Only Pub/Sub commands can be executed:

- SUBSCRIBE, UNSUBSCRIBE
- PSUBSCRIBE, PUNSUBSCRIBE
- QUIT

Regular commands (GET, SET, etc.) are rejected.

**Unsubscribing**

```
UNSUBSCRIBE chat:room1
```

Removes subscription. Client remains in subscriber mode unless all subscriptions ended.

### Message Format

Subscriber receives:

```
1) "message"
2) "chat:room1"
3) "Hello everyone!"
```

Array with three elements: message type, channel name, message content

### Pattern-Based Subscriptions (PSUBSCRIBE)

Subscribe to channels matching glob patterns:

```
PSUBSCRIBE chat:*
PSUBSCRIBE notifications:user:*
PSUBSCRIBE order.*
```

Matches:

- `chat:*` → chat:room1, chat:general, chat:private
- `notifications:user:*` → notifications:user:123, notifications:user:456
- `order.*` → order.created, order.shipped, order.cancelled

**Pattern Subscription Message**

```
1) "pmessage"
2) "order.*"
3) "order.created"
4) {"order_id": 123}
```

Includes matched pattern and actual channel.

### Pub/Sub Limitations

**No Message Persistence**: Messages not stored; disconnected subscribers lose messages

**No Acknowledgment**: Publisher doesn't know if subscribers received message

**No Message Queue**: If no subscribers when published, message is lost

**Subscriber-Only Mode**: Subscribers cannot execute regular commands

### Use Cases

**Real-Time Notifications**: Send alerts to all connected clients

**Chat Applications**: Broadcast messages to chat rooms

**Live Updates**: Stream price updates, sports scores to multiple clients

**Event Broadcasting**: Notify multiple services of important events

**Live Dashboards**: Update metrics and dashboards in real-time

## 3.4 Pub/Sub vs Streams Comparison

Redis Streams (introduced in Redis 5.0) offer an alternative to Pub/Sub with persistence and consumer groups.

| Feature         | Pub/Sub              | Streams                               |
| --------------- | -------------------- | ------------------------------------- |
| Persistence     | No                   | Yes (persisted)                       |
| Message History | None                 | Full history retained                 |
| Consumer Groups | Not supported        | Supported                             |
| Guarantees      | Best-effort          | At-least-once delivery                |
| Latency         | Sub-millisecond      | Similar, with persistence overhead    |
| Use Case        | Real-time, transient | Event sourcing, audit logs            |
| Replay          | Impossible           | Full replay capability                |
| Scalability     | Many subscribers     | Many consumers processing same stream |

**When to Use Pub/Sub**

- Real-time notifications (no need to store)
- Live chat and messaging
- Sensor data broadcasting
- Cache invalidation broadcasts

**When to Use Streams**

- Event sourcing and audit trails
- Durable message queues
- Multi-consumer processing
- Message replay requirements

## 3.5 Pipelining for Bulk Operations

Pipelining sends multiple commands in a single request, reducing network round trips and dramatically improving throughput.

### How Pipelining Works

Without Pipelining (5 separate requests):

```
Request 1: SET key1 value1 → Response OK
Request 2: SET key2 value2 → Response OK
Request 3: SET key3 value3 → Response OK
Request 4: GET key1        → Response value1
Request 5: GET key2        → Response value2
```

With Pipelining (1 request):

```
Request:  SET key1 value1; SET key2 value2; SET key3 value3; GET key1; GET key2
Response: OK, OK, OK, value1, value2
```

### Performance Benefits

**Throughput Improvement**: 5-10x improvement on loopback, even greater on network

**Reason**: Eliminates context switching overhead

- Without pipelining: Each command requires read() and write() syscalls
- With pipelining: Multiple commands read in single read() call, responses sent in single write() call

### Pipelining Example (Python)

```python
import redis

r = redis.Redis()

# Without pipelining
for i in range(1000):
    r.set(f"key:{i}", f"value:{i}")

# With pipelining
pipe = r.pipeline()
for i in range(1000):
    pipe.set(f"key:{i}", f"value:{i}")
pipe.execute()
```

The pipelined version is typically 5-10 times faster.

### Optimal Batch Size

```python
pipe = r.pipeline(transaction=False)
for i in range(100000):
    pipe.set(f"key:{i}", f"value:{i}")

    if i % 1000 == 0:  # Execute every 1000 commands
        pipe.execute()
        pipe = r.pipeline(transaction=False)

if len(pipe) > 0:
    pipe.execute()
```

Balance between:

- Small batches: More network requests, but lower memory
- Large batches: Fewer requests, but more buffered commands

### Transaction vs Non-Transaction Pipelines

**Non-Transaction Pipeline** (faster, no atomicity guarantee):

```python
pipe = r.pipeline(transaction=False)
```

Useful for bulk loading where atomicity not required.

**Transaction Pipeline** (atomic, slightly slower):

```python
pipe = r.pipeline(transaction=True)  # Default
```

Wraps pipeline in MULTI/EXEC for atomic execution.

## 3.6 Memory Management and Eviction Policies (LRU, LFU, TTL)

When Redis memory reaches maxmemory limit, eviction policies determine which keys to remove to make room for new data.

### Memory Configuration

```
maxmemory 256mb              # Maximum memory limit
maxmemory-policy allkeys-lru # Eviction policy
```

### Eviction Policy Types

**LRU (Least Recently Used) Policies**

**allkeys-lru**: Evicts least recently used keys from entire dataset

- Best for general caching
- Evicts least popular items
- High hit rate for popular items

**volatile-lru**: Evicts least recently used keys with TTL set

- Only evicts keys with expiration
- Never evicts keys without TTL
- Useful when some keys should never be evicted

**LFU (Least Frequently Used) Policies** (Redis 4.0+)

**allkeys-lfu**: Evicts least frequently used keys from entire dataset

- Tracks frequency of access, not recency
- Better for workloads with distinct popular items
- Adapts to changing access patterns

**volatile-lfu**: Evicts least frequently used keys with TTL set

- Combines LFU with expiration requirement
- Efficient when most keys have expiration

**TTL-Based Policies**

**volatile-ttl**: Evicts keys with shortest TTL remaining

- Useful when natural expiration is preferred
- Keeps keys with longer lifetime

**Other Policies**

**volatile-random**: Random eviction among keys with TTL

**allkeys-random**: Random eviction from all keys

**noeviction**: No eviction; returns error when memory full

- Use for critical data where data loss is unacceptable

### Eviction Policy Selection Matrix

| Use Case                 | Recommended Policy | Reason                               |
| ------------------------ | ------------------ | ------------------------------------ |
| General cache            | allkeys-lru        | Simple, effective for most scenarios |
| Social feed, leaderboard | allkeys-lfu        | Frequently accessed items stay       |
| Session storage          | volatile-lru       | Mixed TTL/permanent data             |
| Time-series data         | volatile-ttl       | Natural expiration aligns with use   |
| Critical app data        | noeviction         | Prevent data loss                    |
| Testing/development      | noeviction         | Easier to debug                      |

### LFU Configuration

```
lfu-log-factor 10       # Frequency counter accuracy
lfu-decay-time 1        # Minutes before counter decreases
```

**lfu-log-factor**: Higher values = more accurate frequency tracking but more overhead

**lfu-decay-time**: How often access count decreases for stale items

### Memory Analysis

```
INFO memory             # Memory statistics
MEMORY USAGE key        # Memory used by specific key
MEMORY STATS           # Detailed memory info
```

## 3.7 MEMORY Commands and Analysis

### Memory Information Commands

**MEMORY USAGE**

```
MEMORY USAGE mykey
```

Returns bytes consumed by key including metadata and overhead.

Useful for identifying large keys consuming excess memory.

**MEMORY STATS**

```
MEMORY STATS
```

Returns detailed memory breakdown:

- Peak memory usage
- Memory fragmentation ratio
- Allocator overhead
- Dataset breakdown by type

### Memory Optimization Strategies

**Identify Large Keys**

```
for key in all_keys:
    size = MEMORY USAGE key
    if size > threshold:
        delete or compress key
```

**Compression**: Store compressed data in strings

**Expiration**: Set appropriate TTL to free memory

**Encoding**: Use simpler data types when possible

## 3.8 Redis Lua Scripting and EVAL

Lua scripting allows executing multi-command scripts atomically on the Redis server with full control flow and conditional logic.

### EVAL Command

```
EVAL script numkeys [key [key ...]] [arg [arg ...]]
```

- **script**: Lua program code
- **numkeys**: Number of key arguments that follow
- **key**: Redis keys accessible via KEYS[] table
- **arg**: Additional arguments accessible via ARGV[] table

### Accessing Keys and Arguments

```
EVAL "return {KEYS[1], KEYS[2], ARGV[1], ARGV[2]}" 2 key1 key2 arg1 arg2
```

Returns: ["key1", "key2", "arg1", "arg2"]

### Redis Command Execution in Lua

```
EVAL "return redis.call('SET', KEYS[1], ARGV[1])" 1 mykey myvalue
EVAL "return redis.call('GET', KEYS[1])" 1 mykey
EVAL "return redis.call('INCR', KEYS[1])" 1 counter
```

**redis.call()**: Executes Redis command, propagates errors

**redis.pcall()**: Executes safely, returns error as value instead of throwing

### Atomic Counter with Limit

```lua
EVAL "
if redis.call('GET', KEYS[1]) < tonumber(ARGV[1]) then
    return redis.call('INCR', KEYS[1])
else
    return nil
end
" 1 counter 100
```

Increments counter only if below limit, atomically.

### Script Caching with EVALSHA

Scripts are cached after EVAL execution. Use SHA1 hash for subsequent calls:

```
SCRIPT LOAD "return 'hello'"
# Returns: "5f0d532a7d9b8c5be1fb4e7c8f9c5d5a"

EVALSHA 5f0d532a7d9b8c5be1fb4e7c8f9c5d5a 0
```

Much faster than re-transmitting entire script.

## 3.9 Atomic Operations with Lua Scripts

Lua ensures atomic multi-operation execution impossible with traditional MULTI/EXEC when conditional logic is required.

### Atomic Transfer with Conditions

```lua
EVAL "
local from_balance = redis.call('HGET', KEYS[1], 'balance')
local to_exists = redis.call('EXISTS', KEYS[2])

if from_balance < tonumber(ARGV[1]) then
    return 'Insufficient funds'
elseif to_exists == 0 then
    return 'Recipient not found'
else
    redis.call('HINCRBY', KEYS[1], 'balance', -tonumber(ARGV[1]))
    redis.call('HINCRBY', KEYS[2], 'balance', tonumber(ARGV[1]))
    return 'OK'
end
" 2 account1 account2 100
```

Atomic execution with complex logic impossible with WATCH/MULTI.

### Rate Limiting Script

```lua
EVAL "
local key = KEYS[1]
local limit = tonumber(ARGV[1])
local window = tonumber(ARGV[2])

local current = redis.call('INCR', key)
if current == 1 then
    redis.call('EXPIRE', key, window)
end

if current <= limit then
    return {1, limit - current}
else
    return {0, 0}
end
" 1 rate:user:123 10 60
```

Returns [1, remaining_quota] if allowed, if rate limited.

## 3.10 Redis Security (AUTH, ACL, SSL/TLS, Network Isolation)

### Simple Password Authentication (AUTH)

```
requirepass mypassword
```

Old-style authentication using requirepass directive.

Client authenticates with:

```
AUTH mypassword
```

### Access Control Lists (ACL) - Redis 6+

**Why ACLs?**

- Granular per-command and per-key permissions
- Multiple users with different privilege levels
- Better security than single password

### ACL Configuration

```
ACL SETUSER username on >password ~pattern +command1 +command2 -dangerous-command
```

- **on/off**: Enable/disable user
- **>password**: Set password (> means hash it)
- **~pattern**: Key patterns accessible (~ = can access)
- **+command**: Allow command (+ = grant)
- **-command**: Deny command (- = revoke)

### Built-in ACL Users

**default user**: Used if no username provided in AUTH

```
ACL SETUSER default on >newpassword ~* +@all
```

**@all**: Special category meaning all commands

### Command Categories

```
@read              # Read-only commands
@write             # Write commands
@admin             # Administrative commands
@fast              # O(1) commands
@pubsub            # Pub/Sub commands
@transaction       # Transaction commands
@keyspace          # Key-related commands
@generic           # Generic commands
```

### ACL Best Practices

```
ACL SETUSER readonly on >readpass ~* +@read
ACL SETUSER admin on >adminpass ~* +@all
ACL SETUSER app on >apppass ~user:* +get +hget +set +hset
```

Principle of least privilege: Users get only necessary permissions.

### TLS/SSL Encryption

**TLS Configuration**

```
port 0                          # Disable unencrypted port
tls-port 6379                   # Enable TLS on port 6379
tls-cert-file /path/to/cert.crt
tls-key-file /path/to/key.key
tls-ca-cert-file /path/to/ca.crt
tls-auth-clients yes            # Require client certificates
```

**Client Connection**

```python
import redis

r = redis.Redis(
    host='localhost',
    port=6379,
    ssl=True,
    ssl_certfile='/path/to/client.crt',
    ssl_keyfile='/path/to/client.key',
    ssl_ca_certs='/path/to/ca.crt'
)
```

### Network Isolation

**Bind to Specific Interface**

```
bind 127.0.0.1              # Localhost only
bind 192.168.1.100          # Specific IP
bind 127.0.0.1 ::1          # IPv4 and IPv6
```

**Firewall Rules**

- Restrict Redis port access to authorized networks
- Use VPC/security groups in cloud
- Never expose Redis to public internet

### Security Checklist

1. Change default password immediately
2. Use ACLs with least-privilege principle
3. Enable TLS for encrypted connections
4. Bind to internal IPs only
5. Use firewall rules to restrict access
6. Regularly audit access logs
7. Monitor AUTH failures
8. Update Redis regularly

## 3.11 Key Expiration and TTL Management

### Setting Expiration

**EXPIRE** (seconds):

```
EXPIRE mykey 300
```

Expires in 300 seconds (5 minutes).

**PEXPIRE** (milliseconds):

```
PEXPIRE mykey 300000
```

Expires in 300,000 milliseconds (5 minutes).

**SET with Expiration**:

```
SET mykey value EX 300      # Seconds
SET mykey value PX 300000   # Milliseconds
```

### Checking TTL

**TTL** (seconds remaining):

```
TTL mykey
```

Returns:

- Positive number: Seconds until expiration
- -1: Key exists but has no expiration
- -2: Key doesn't exist

**PTTL** (milliseconds remaining):

```
PTTL mykey
```

### Removing Expiration

**PERSIST** (make key permanent):

```
PERSIST mykey
```

Removes expiration, key becomes permanent.

### Expiration Behavior

**Passive Expiration**: When expired key is accessed, Redis deletes it

**Active Expiration**: Background task periodically removes expired keys

**Accuracy**: Expiration checked with sub-millisecond precision (since Redis 2.6)

### TTL Strategy Patterns

**Session Storage** (1 hour expiration):

```
SET session:abc123 userData EX 3600
```

**Cache** (5 minute expiration):

```
SET cache:user:123 cachedData EX 300
```

**Rate Limiting** (per-minute window):

```
SET rate:ip:192.168.1.1 count EX 60
```

**One-Time Token** (10 minute validity):

```
SET token:xyz789 verificationData EX 600
```

## 3.12 Scanning Keys Efficiently (SCAN vs KEYS)

### KEYS Command (Don't Use in Production)

```
KEYS pattern
```

**Behavior**

- Blocks Redis entirely while scanning
- Returns all matching keys at once
- O(N) where N is total keys in database

**Problems**

- Blocks all other clients during scan
- Can cause multi-second latency on large datasets
- Unacceptable in production with large keyspace

### SCAN Command (Production-Safe)

```
SCAN cursor [MATCH pattern] [COUNT count]
```

**Returns**: [new_cursor, matched_keys_batch]

**Behavior**

- Iterates keyspace incrementally
- Doesn't block for extended periods
- Returns partial results
- O(1) per call, O(N) for full iteration

### SCAN Iterator Pattern

```python
cursor = 0
keys = []

while True:
    cursor, batch = redis.scan(cursor, match='user:*', count=100)
    keys.extend(batch)

    if cursor == 0:
        break  # Iteration complete

print(f"Found {len(keys)} keys")
```

### SCAN Guarantees and Limitations

**Guarantees**

- No key returned twice in single SCAN iteration
- If key exists before iteration starts, eventually returned
- If key created/deleted during iteration, might or might not be returned

**Limitations**

- Doesn't provide point-in-time snapshot
- Pattern matching happens on every element checked (performance cost)
- COUNT is hint, not exact (might return more/fewer)

### SCAN Variants

**SSCAN** (Set members):

```
SSCAN myset cursor [MATCH pattern] [COUNT count]
```

**HSCAN** (Hash fields):

```
HSCAN myhash cursor [MATCH pattern] [COUNT count]
```

**ZSCAN** (Sorted set members):

```
ZSCAN myzset cursor [MATCH pattern] [COUNT count]
```

### Pattern Matching Syntax

```
*      → Matches any number of characters
?      → Matches exactly one character
[abc]  → Matches a, b, or c
[a-z]  → Matches any character a to z
```

### Performance Optimization

**Use COUNT wisely**

```
SCAN 0 MATCH user:* COUNT 1000
```

Higher COUNT = fewer calls but more blocking per call

**Match pattern first**

```
SCAN 0 MATCH session:* COUNT 100
```

Filtering with MATCH reduces returned keys.

**Consider alternatives**

For large keyspace with complex queries:

- Build and maintain secondary indices using Sets
- Use Redis Search (Redis Stack)
- Use database-specific modules
