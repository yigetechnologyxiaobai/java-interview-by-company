# 小红书 Java 面试题

## 面试风格

**特点**：注重实战能力，关注高并发场景，喜欢项目经验

**轮次**：通常 2-3 轮技术面 + 1 轮 HR

**重点**：Redis、MySQL、分布式、高并发、业务场景设计

---

## 一、Redis 高频题

### Q1: Redis 为什么快？

**参考答案**：

1. **内存操作**：数据在内存中，读写速度快
2. **单线程**：无锁竞争，无上下文切换开销
3. **IO 多路复用**：基于 epoll 实现高并发
4. **高效数据结构**：SDS、跳表、压缩列表

**为什么用单线程**：
- 性能瓶颈在内存和网络，不在 CPU
- 多线程竞争开销大
- 实现简单，易于维护

**Redis 6.0 多线程**：
- 仅用于网络 IO（读写数据）
- 数据处理仍是单线程
- 提升网络 IO 性能

**追问**：
- Redis 单线程如何处理并发连接？
- IO 多路复用原理？

### Q2: Redis 数据结构？

**参考答案**：

| 类型 | 底层实现 | 典型场景 |
|------|---------|---------|
| String | SDS（简单动态字符串） | 缓存、计数器、分布式锁 |
| Hash | 哈希表 + 压缩列表 | 对象存储、购物车 |
| List | 压缩列表 + 双向链表 | 队列、消息列表 |
| Set | 哈希表 + 整数集合 | 标签、共同关注 |
| ZSet | 跳表 + 哈希表 | 排行榜、热搜榜 |

**跳表特点**：
- 多层链表，查找 O(log n)
- 实现简单，易于维护
- 支持范围查询

**压缩列表**：
- 连续内存，节省空间
- 元素少、元素小的时候使用

**追问**：
- 为什么用跳表不用红黑树？
- SDS 和 C 字符串区别？

### Q3: 缓存穿透、击穿、雪崩？

**参考答案**：

| 问题 | 原因 | 解决方案 |
|------|------|---------|
| 穿透 | 查询不存在的数据 | 布隆过滤器、缓存空值 |
| 击穿 | 热点 key 过期 | 永不过期、互斥锁 |
| 雪崩 | 大量 key 同时过期 | 随机过期时间、多级缓存 |

**布隆过滤器**：
- 位图 + 多个哈希函数
- 判断元素可能存在或一定不存在
- 优点：空间效率高
- 缺点：有误判率，不支持删除

**互斥锁**：
```java
String value = redis.get(key);
if (value == null) {
    if (redis.setnx(lockKey, "1", 10)) {
        value = db.query(key);
        redis.set(key, value, 3600);
        redis.del(lockKey);
    } else {
        Thread.sleep(50);
        // 重试
    }
}
```

**追问**：
- 布隆过滤器原理？
- 如何设计多级缓存？

### Q4: Redis 集群方案？

**参考答案**：

| 方案 | 描述 | 优缺点 |
|------|------|--------|
| 主从复制 | 一主多从 | 读性能提升，写不能扩展 |
| 哨兵 | 监控+故障转移 | 高可用，写不能扩展 |
| Cluster | 分片集群 | 读写都能扩展 |

**Cluster 原理**：
- 16384 个槽位分配到各节点
- CRC16(key) % 16384 定位槽位
- 节点间 Gossip 通信
- 自动故障转移

**追问**：
- Cluster 如何做故障转移？
- 客户端如何知道 key 在哪个节点？

### Q5: Redis 分布式锁？

**参考答案**：

**基本实现**：
```redis
# 加锁
SET lock:key value NX PX 30000

# 解锁（Lua 脚本保证原子性）
if redis.call("GET", KEYS[1]) == ARGV[1] then
    return redis.call("DEL", KEYS[1])
else
    return 0
end
```

**Redisson 增强**：
- 可重入锁
- 看门狗自动续期
- 红锁（Redlock）

**看门狗机制**：
- 默认锁过期时间 30s
- 每 10s 自动续期到 30s
- 防止业务执行时间超过锁过期时间

**追问**：
- 锁过期了但业务没执行完怎么办？
- 主从切换导致锁丢失怎么办？

---

## 二、MySQL 高频题

### Q6: 索引为什么用 B+ 树？

**参考答案**：

**B+ 树特点**：
1. **树高度低**：3-4 层可存千万级数据，IO 次数少
2. **范围查询友好**：叶子节点链表
3. **磁盘利用率高**：非叶子节点只存键值

**与 B 树区别**：
| 特性 | B 树 | B+ 树 |
|------|------|-------|
| 数据存储 | 所有节点 | 只有叶子节点 |
| 范围查询 | 需要中序遍历 | 叶子节点链表 |
| 树高度 | 较高 | 较低 |

**聚簇索引**：
- 数据存储在叶子节点
- 主键索引就是聚簇索引

**非聚簇索引**：
- 叶子节点存储主键值
- 需要回表查询

**追问**：
- 为什么用自增主键？
- 覆盖索引的优势？

### Q7: 索引优化？

**参考答案**：

**索引设计原则**：
1. 选择区分度高的列
2. 遵循最左前缀原则
3. 避免索引列做运算
4. 控制索引数量（单表 5 个以内）

**索引失效场景**：
- LIKE 以 % 开头
- 对索引列做运算
- 类型隐式转换
- 使用函数
- OR 条件（部分列无索引）

**覆盖索引**：
- 查询的列都在索引中
- 不需要回表，性能更好

**索引下推**：
- MySQL 5.6 新特性
- 在索引遍历过程中过滤

**追问**：
- 如何分析慢查询？
- 联合索引设计原则？

### Q8: MVCC 原理？

**参考答案**：

**核心组件**：
1. **隐藏字段**：
   - DB_TRX_ID：事务 ID
   - DB_ROLL_PTR：回滚指针

2. **Undo Log**：版本链

3. **Read View**：可见性判断
   - m_ids：活跃事务 ID 列表
   - min_trx_id：最小活跃事务 ID
   - max_trx_id：下一个事务 ID

**隔离级别**：
- RC：每次 select 生成新的 Read View
- RR：事务第一次 select 生成 Read View

**追问**：
- MVCC 能解决幻读吗？
- 当前读和快照读区别？

### Q9: 深分页问题？

**参考答案**：

**问题**：`LIMIT 100000, 10` 需要扫描前 100010 行

**解决方案**：

1. **子查询优化**：
```sql
SELECT * FROM t WHERE id >= (
    SELECT id FROM t ORDER BY id LIMIT 100000, 1
) LIMIT 10;
```

2. **Join 优化**：
```sql
SELECT t.* FROM t 
INNER JOIN (SELECT id FROM t ORDER BY id LIMIT 100000, 10) tmp
ON t.id = tmp.id;
```

3. **记录上次最大 ID**：
```sql
SELECT * FROM t WHERE id > ? ORDER BY id LIMIT 10;
```

---

## 三、分布式高频题

### Q10: 分布式事务？

**参考答案**：

| 方案 | 原理 | 场景 |
|------|------|------|
| 2PC | 准备 + 提交 | 强一致 |
| TCC | Try-Confirm-Cancel | 高并发 |
| 本地消息表 | 消息 + 定时任务 | 最终一致 |
| 事务消息 | RocketMQ 半消息 | 最终一致 |
| Seata AT | 全局锁 + Undo Log | 简单场景 |

**TCC 流程**：
1. Try：预留资源
2. Confirm：确认提交
3. Cancel：回滚释放

**追问**：
- TCC 空回滚问题？
- 悬挂问题如何解决？

### Q11: 消息队列？

**参考答案**：

| MQ | 特点 | 场景 |
|----|------|------|
| Kafka | 高吞吐 | 日志、大数据 |
| RocketMQ | 事务消息 | 金融、电商 |
| RabbitMQ | 功能丰富 | 中小规模 |

**消息不丢失**：
- 生产者：事务/Confirm
- Broker：同步刷盘、主从同步
- 消费者：手动 ACK

**消息不重复**：
- 幂等设计
- 唯一 ID + 数据库唯一索引
- Redis SETNX

**追问**：
- 如何保证消息顺序？
- 延迟队列实现？

---

## 四、高并发场景题

### Q12: 秒杀系统设计？

**参考答案**：

**架构分层**：
```
用户 → CDN → 网关 → 应用服务 → 缓存 → MQ → 数据库
```

**核心设计**：
1. **前端限流**：按钮置灰、验证码
2. **网关限流**：令牌桶、漏桶
3. **缓存预热**：库存预热到 Redis
4. **原子扣减**：Lua 脚本
5. **异步下单**：MQ 处理

**Lua 脚本原子扣减**：
```lua
if redis.call('GET', KEYS[1]) <= 0 then
    return -1
end
redis.call('DECR', KEYS[1])
return 1
```

**防超卖**：
```sql
UPDATE stock SET count = count - 1 
WHERE id = ? AND count > 0;
```

**追问**：
- 如何防止同一用户重复下单？
- 高并发下如何保证库存准确？

### Q13: Feed 流设计？

**参考答案**：

**推拉模式**：
- **推模式**：写扩散，适合小 V
- **拉模式**：读扩散，适合大 V
- **推拉结合**：大 V 用拉，小 V 用推

**存储设计**：
- Redis：热点数据、计数器
- MySQL：持久化存储
- ES：搜索

**性能优化**：
- 分页加载
- 预加载
- CDN 加速

**追问**：
- 如何处理热点用户？
- 如何保证实时性？

### Q14: 点赞系统设计？

**参考答案**：

**核心功能**：
- 点赞/取消点赞
- 获取点赞数
- 查看点赞列表
- 查看是否已点赞

**数据结构**：
```redis
# 点赞计数
SET like:count:post:{postId} 100

# 点赞用户集合
SADD like:users:post:{postId} userId
```

**优化**：
- Redis 缓存热点数据
- MQ 异步写数据库
- 定时任务同步

**追问**：
- 如何防止重复点赞？
- 高并发下如何保证一致性？

---

## 五、Java 基础高频题

### Q15: HashMap 原理？

**参考答案**：

**JDK 1.8 结构**：数组 + 链表 + 红黑树

**put 流程**：
1. 计算 hash
2. 定位桶
3. 桶为空 → 直接插入
4. 桶不为空 → 遍历链表/红黑树
5. 相同 key → 覆盖 value
6. 链表长度 >= 8 → 红黑树

**追问**：
- 为什么线程不安全？
- ConcurrentHashMap 实现？

### Q16: 线程池参数？

**参考答案**：

```java
ThreadPoolExecutor(
    int corePoolSize,
    int maximumPoolSize,
    long keepAliveTime,
    TimeUnit unit,
    BlockingQueue<Runnable> workQueue,
    RejectedExecutionHandler handler
)
```

**追问**：
- 为什么不用 Executors？
- 如何合理设置参数？

---

## 六、JVM 高频题

### Q17: JVM 内存结构？

**参考答案**：

**运行时数据区**：
1. 程序计数器
2. 虚拟机栈
3. 本地方法栈
4. 堆
5. 方法区

**追问**：
- 堆和栈的区别？
- OOM 排查？

### Q18: 垃圾收集器？

**参考答案**：

| 收集器 | 类型 | 特点 |
|--------|------|------|
| Serial | 单线程 | 简单 |
| Parallel | 并行 | 吞吐优先 |
| CMS | 并发 | 低延迟 |
| G1 | 分代 | 可预测停顿 |
| ZGC | 并发 | 超大内存 |

**追问**：
- CMS 和 G1 区别？
- 如何选择垃圾收集器？

---

## 七、Spring 高频题

### Q19: Spring Bean 生命周期？

**参考答案**：

1. 实例化
2. 属性赋值
3. 初始化
4. 销毁

**追问**：
- 循环依赖如何解决？
- Bean 的作用域？

### Q20: Spring 事务传播机制？

**参考答案**：

| 传播行为 | 说明 |
|---------|------|
| REQUIRED | 有则加入，无则新建 |
| SUPPORTS | 有则加入，无则非事务 |
| REQUIRES_NEW | 新建事务，挂起当前 |
| NESTED | 嵌套事务 |

**追问**：
- 事务失效场景？
- 如何解决事务失效？

---

## 八、算法题

小红书算法难度中等：

1. **数组**：三数之和、最大子数组和
2. **链表**：反转链表、合并有序链表
3. **树**：层序遍历、最近公共祖先
4. **动态规划**：背包问题
5. **字符串**：最长无重复子串

---

## 九、面试技巧

1. **重视实战**：小红书偏爱场景题，准备秒杀、Feed 流等
2. **项目经验**：项目难点要能说清楚
3. **技术广度**：Redis、MySQL、分布式都要懂
4. **业务理解**：理解小红书业务，点赞、推荐等
5. **保持热情**：展示对技术的热情和学习能力

---

## 十、2026 Java 一面真题

> 来源：牛客网 2026-03
> 特点：八股为主，不问项目，网络题多

### Q1: HashMap 是线程安全的吗？

**参考答案**：不是。

**HashMap 线程不安全的原因**：
1. **并发扩容导致数据丢失**：多线程同时扩容，链表可能形成环（JDK 1.7）
2. **数据覆盖**：并发 put 时，后写入的覆盖先写入的

**线程安全替代方案**：
- `ConcurrentHashMap`：推荐
- `Collections.synchronizedMap(new HashMap<>())`：性能差
- `Hashtable`：古老，不推荐

---

### Q2: ConcurrentHashMap 如何保证线程安全？

**参考答案**：

**JDK 1.7**：分段锁（Segment）
- 将数据分成多个段，每段一个锁
- 并发访问不同段不冲突

**JDK 1.8**：CAS + synchronized
- 取消分段锁，改用节点级锁
- 使用 CAS 进行无锁插入
- 使用 synchronized 锁住链表头/树根

```java
// put 核心逻辑
final V putVal(K key, V value, boolean onlyIfAbsent) {
    // 1. 计算 hash
    int hash = spread(key.hashCode());
    
    // 2. 遍历 table
    for (Node<K,V>[] tab = table;;) {
        Node<K,V> f; int n, i, fh;
        if (tab == null || (n = tab.length) == 0)
            tab = initTable();
        else if ((f = tabAt(tab, i = (n - 1) & hash)) == null) {
            // 3. CAS 插入新节点（无锁）
            if (casTabAt(tab, i, null, new Node<K,V>(hash, key, value, null)))
                break;
        }
        else {
            synchronized (f) {  // 4. synchronized 锁住头节点
                // 插入或更新
            }
        }
    }
    return null;
}
```

---

### Q3: CAS 操作是什么？

**参考答案**：

CAS（Compare And Swap）：比较并交换，是一种无锁并发控制机制。

**原理**：
```java
// 伪代码
boolean compareAndSwap(int expected, int newValue) {
    if (this.value == expected) {
        this.value = newValue;
        return true;
    }
    return false;
}
```

**特点**：
- 原子操作，不需要加锁
- 由 CPU 硬件支持

**ABA 问题**：
- 线程 A 读取 value = 1
- 线程 B 改成 2，又改回 1
- 线程 A CAS 成功，但值已被修改过

**解决方案**：加版本号
```java
// AtomicStampedReference 带版本号
AtomicStampedReference<Integer> ref = new AtomicStampedReference<>(1, 0);
```

---

### Q4: 如何解决 Hash 冲突？

**参考答案**：

| 方法 | 原理 | 应用 |
|------|------|------|
| 链地址法 | 冲突元素组成链表 | HashMap |
| 开放地址法 | 找下一个空位 | ThreadLocalMap |
| 再哈希法 | 用另一个哈希函数 | 不常用 |
| 公共溢出区 | 冲突元素放溢出表 | 不常用 |

**HashMap 的链地址法**：
- JDK 1.7：链表头插法
- JDK 1.8：链表尾插法 + 红黑树（链表长度 ≥ 8）

---

### Q5: volatile 如何保证有序性？

**参考答案**：

**内存屏障**：
- 写操作前加 StoreStore 屏障
- 写操作后加 StoreLoad 屏障
- 读操作后加 LoadLoad + LoadStore 屏障

**禁止指令重排**：
```java
// 单例模式双重检验锁
class Singleton {
    private volatile static Singleton instance;
    
    public static Singleton getInstance() {
        if (instance == null) {
            synchronized (Singleton.class) {
                if (instance == null) {
                    instance = new Singleton();
                    // 没有 volatile，可能发生：
                    // 1. 分配内存
                    // 2. instance 指向内存（重排）
                    // 3. 初始化对象
                    // 其他线程拿到未初始化的对象！
                }
            }
        }
        return instance;
    }
}
```

---

### Q6: TCP 四次挥手能不能是三次？

**参考答案**：

**为什么需要四次**：
- 服务端收到 FIN 后，可能还有数据要发送
- 所以 ACK 和 FIN 分开发送

**三次挥手的情况**：
当服务端没有数据要发送时，可以将 ACK 和 FIN 合并，变成三次：
```
客户端 FIN → 服务端
服务端 ACK + FIN → 客户端（合并）
客户端 ACK → 服务端
```

---

### Q7: TCP 报文段最大限制是多少？

**参考答案**：

**MSS（Maximum Segment Size）**：
- TCP 数据部分的最大长度
- 通常 = MTU - IP 头 - TCP 头 = 1500 - 20 - 20 = 1460 字节

**影响因素**：
- MTU（Maximum Transmission Unit）：链路层限制，以太网 1500 字节
- Path MTU Discovery：路径上最小的 MTU

---

### Q8: TCP 滑动窗口机制？

**参考答案**：

**作用**：流量控制，防止发送方发太快，接收方来不及处理。

**原理**：
```
发送窗口：
| 已发送已确认 | 已发送未确认 | 可发送 | 不可发送 |
              |←  窗口大小  →|

接收窗口：
| 已接收 | 可接收 | 不可接收 |
        |← 窗口 →|
```

**滑动过程**：
1. 收到 ACK，窗口向右滑动
2. 接收方通过 ACK 告知窗口大小
3. 窗口为 0 时，发送方停止发送

---

### Q9: 线程池核心线程数为什么设置为 CPU 核心数？

**参考答案**：

**CPU 密集型任务**：
- 线程数 = CPU 核心数 + 1
- 避免 CPU 切换开销
- +1 是为了某个线程阻塞时备用

**IO 密集型任务**：
- 线程数 = CPU 核心数 × (1 + 等待时间/计算时间)
- IO 等待时 CPU 空闲，可以多开线程

**示例**：
```java
// 4 核 CPU，CPU 密集型
int cpuCores = Runtime.getRuntime().availableProcessors();
ThreadPoolExecutor executor = new ThreadPoolExecutor(
    cpuCores,           // 核心线程 = 4
    cpuCores * 2,       // 最大线程 = 8
    60L, TimeUnit.SECONDS,
    new LinkedBlockingQueue<>(1000)
);
```

---

### Q10: Redis 宕机后有什么措施？

**参考答案**：

**持久化**：
- RDB：快照，恢复快，可能丢数据
- AOF：追加日志，数据完整，恢复慢
- 混合持久化：RDB + AOF

**高可用**：
- 主从复制：读写分离
- 哨兵模式：自动故障转移
- Cluster 集群：分片 + 高可用

**降级方案**：
```java
// 缓存穿透保护
public Object getWithFallback(String key) {
    Object value = redis.get(key);
    if (value == null) {
        // Redis 宕机，查数据库
        value = db.query(key);
        // 记录日志，告警
        log.warn("Redis fallback to DB");
    }
    return value;
}
```

---

### Q11: 向量数据库是什么？相似度计算原理？

**参考答案**：

**向量数据库**：存储和检索向量数据的数据库，用于语义搜索、推荐系统。

**常用数据库**：Milvus、Pinecone、Chroma、Weaviate

**相似度计算**：
- **余弦相似度**：`cos(θ) = A·B / (|A| × |B|)`
- **欧氏距离**：`√(Σ(Ai - Bi)²)`
- **点积**：`A·B = Σ(Ai × Bi)`

**RAG 应用**：
```python
# 1. 文本转向量
embedding = model.encode("查询文本")

# 2. 向量检索
results = vector_db.search(embedding, top_k=5)

# 3. 返回相似文档
for doc in results:
    print(doc.text, doc.score)
```

---

### Q12: 手写单例模式（双重检验锁）

**参考答案**：

```java
public class Singleton {
    // volatile 防止指令重排
    private volatile static Singleton instance;
    
    private Singleton() {}
    
    public static Singleton getInstance() {
        if (instance == null) {              // 第一次检查
            synchronized (Singleton.class) {
                if (instance == null) {      // 第二次检查
                    instance = new Singleton();
                }
            }
        }
        return instance;
    }
}
```

**为什么需要 volatile**：
- `new Singleton()` 不是原子操作
- 可能发生指令重排：分配内存 → 赋值引用 → 初始化
- 其他线程可能拿到未初始化的对象

---

**面试总结**：
- 小红书一面八股为主，不问项目
- 网络题多（TCP、TLS、滑动窗口）
- 并发题深入（volatile、CAS、线程池）
- 手撕代码考单例模式

---

[返回目录](../README.md)