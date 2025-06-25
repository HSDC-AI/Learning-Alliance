# Redis 主从复制 + 哨兵模式下的分布式锁实现

## 一、背景与原理

### 1.1 主从复制与哨兵模式简介
- **主从复制**：Redis 支持一主多从架构，主节点负责写操作，从节点负责数据同步和读操作。主从复制提升了系统的可用性和读性能。
- **哨兵模式**：Redis Sentinel（哨兵）用于监控主从节点的健康状态，自动完成主从切换（failover），并通知客户端新的主节点地址，实现高可用。

### 1.2 分布式锁的基本原理
- 分布式锁用于保证在分布式系统中同一时刻只有一个客户端能获得某个资源的访问权。
- Redis 实现分布式锁常用的命令是 `SET key value NX PX <timeout>`，即：
  - `NX`：仅当 key 不存在时才设置
  - `PX <timeout>`：设置过期时间，防止死锁
- 客户端释放锁时需确保只删除自己加的锁（通常用唯一 value 标识持有者）。

### 1.3 主从复制+哨兵下的分布式锁注意事项
- **写一致性问题**：主从复制是异步的，主节点写入后从节点可能还未同步，若主节点宕机，锁可能丢失。
- **RedLock 算法**：为了解决单点主节点失效带来的锁安全问题，Redis 官方提出了 RedLock 算法（多主多副本环境下的分布式锁），但在大多数业务场景下，单 Redis + 合理超时设置已能满足需求。
- **哨兵切换**：客户端需感知主节点变化，自动重连新主节点。

## 二、Java 代码实现（Jedis + 哨兵模式）

### 2.1 依赖引入
```xml
<dependency>
    <groupId>redis.clients</groupId>
    <artifactId>jedis</artifactId>
    <version>4.4.3</version>
</dependency>
```

### 2.2 Jedis 哨兵模式连接
```java
import redis.clients.jedis.Jedis;
import redis.clients.jedis.JedisSentinelPool;
import java.util.HashSet;
import java.util.Set;

// 配置哨兵地址和主节点名称
Set<String> sentinels = new HashSet<>();
sentinels.add("127.0.0.1:26379");
sentinels.add("127.0.0.1:26380");
sentinels.add("127.0.0.1:26381");
String masterName = "mymaster";

// 创建哨兵池
JedisSentinelPool pool = new JedisSentinelPool(masterName, sentinels);

try (Jedis jedis = pool.getResource()) {
    // 使用 jedis 实例进行操作
}
```

### 2.3 分布式锁实现
```java
import java.util.UUID;

public class RedisDistributedLock {
    private final JedisSentinelPool pool;
    private static final String LOCK_SUCCESS = "OK";
    private static final long DEFAULT_EXPIRE = 10000; // 10秒

    public RedisDistributedLock(JedisSentinelPool pool) {
        this.pool = pool;
    }

    // 加锁
    public String lock(String lockKey, long expireMillis) {
        String uniqueId = UUID.randomUUID().toString();
        try (Jedis jedis = pool.getResource()) {
            String result = jedis.set(lockKey, uniqueId, "NX", "PX", expireMillis);
            if (LOCK_SUCCESS.equals(result)) {
                return uniqueId; // 获得锁，返回唯一标识
            }
        }
        return null; // 未获得锁
    }

    // 解锁（Lua脚本保证原子性）
    public boolean unlock(String lockKey, String uniqueId) {
        String luaScript = "if redis.call('get', KEYS[1]) == ARGV[1] then return redis.call('del', KEYS[1]) else return 0 end";
        try (Jedis jedis = pool.getResource()) {
            Object result = jedis.eval(luaScript, 1, lockKey, uniqueId);
            return Long.valueOf(1).equals(result);
        }
    }
}
```

### 2.4 使用示例
```java
public class LockDemo {
    public static void main(String[] args) {
        // ...哨兵池配置同上...
        RedisDistributedLock lock = new RedisDistributedLock(pool);
        String lockKey = "my:lock";
        String lockId = lock.lock(lockKey, 5000); // 请求5秒锁
        if (lockId != null) {
            try {
                // 执行业务逻辑
                System.out.println("获得锁，执行业务...");
            } finally {
                boolean released = lock.unlock(lockKey, lockId);
                System.out.println("释放锁: " + released);
            }
        } else {
            System.out.println("未获得锁");
        }
    }
}
```

## 三、最佳实践与注意事项
- 锁的超时时间要合理设置，防止死锁。
- 业务执行时间应远小于锁的过期时间。
- 推荐使用 Lua 脚本保证解锁的原子性。
- 生产环境建议使用 Redisson 等高层库，支持自动续期、看门狗等高级特性。
- 哨兵模式下，客户端要能自动感知主节点变化。

## 四、参考资料
- [Redis 官方文档 - 分布式锁](https://redis.io/topics/distlock)
- [Redisson 官方文档](https://github.com/redisson/redisson/wiki)
- [Redis 哨兵模式](https://redis.io/docs/management/sentinel/) 