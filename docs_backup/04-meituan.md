# 美团 Java 面试题

## 面试风格

**特点**：注重实战能力，偏爱场景题，考察广度和深度并重

**轮次**：通常 3 轮技术面 + 1 轮 HR

**重点**：MySQL、Redis、分布式系统、高并发、业务场景设计

---

## 一、MySQL 高频题

### Q1: MySQL 索引优化实战？

**参考答案**：

**索引设计原则**：
1. 选择区分度高的列
2. 遵循最左前缀原则
3. 避免索引列做运算
4. 控制索引数量（单表 5 个以内）

**常见优化**：
```sql
-- 联合索引 (a, b, c)
WHERE a = 1 AND b = 2 AND c = 3  -- 走索引
WHERE a = 1 AND c = 3           -- 部分走索引（a）
WHERE b = 2 AND c = 3           -- 不走索引
WHERE a = 1 ORDER BY b          -- 走索引，排序也优化
```

**索引失效场景**：
- LIKE 以 % 开头
- 对索引列做运算
- 类型隐式转换
- 使用函数
- OR 条件（部分列无索引）

**追问**：
- 如何分析慢查询？（EXPLAIN）
- 覆盖索引的优势？
- 索引下推是什么？

### Q2: MySQL 主从复制延迟怎么解决？

**参考答案**：

**延迟原因**：
1. 从库单线程重放 Binlog
2. 大事务执行时间长
3. 网络延迟
4. 从库硬件性能差

**解决方案**：
1. **并行复制**：MySQL 5.7+ 支持基于 LOGICAL_CLOCK 的并行复制
2. **半同步复制**：主库等待至少一个从库确认
3. **业务优化**：
   - 读写分离时，关键读走主库
   - 引入缓存层
   - 分库分表减少单库压力

**追问**：
- 半同步和异步复制的区别？
- 如何监控主从延迟？（SHOW SLAVE STATUS）

### Q3: 如何解决 MySQL 深分页问题？

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

**追问**：
- 为什么子查询更快？
- 这种方案有什么限制？

---

## 二、Redis 高频题

### Q4: Redis 缓存一致性方案？

**参考答案**：

**方案对比**：

| 方案 | 描述 | 问题 |
|------|------|------|
| 先删缓存，再更新库 | 删除后，读请求可能读旧值写回 | 缓存脏数据 |
| 先更库，再删缓存 | 更新后删除缓存 | 可能删除失败 |
| 延时双删 | 更新库 → 删缓存 → 延时 → 再删缓存 | 增加复杂度 |

**推荐方案**：先更库 + 删缓存 + 消息队列重试

**追问**：
- 为什么要用消息队列？
- 缓存过期时间如何设置？

### Q5: Redis 分布式锁实现？

**参考答案**：

**基本实现**：
```java
// 加锁
SET lock:key value NX PX 30000

// 解锁（Lua 脚本保证原子性）
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

**追问**：
- 锁过期了但业务没执行完怎么办？
- 主从切换导致锁丢失怎么办？

### Q6: Redis 集群方案？

**参考答案**：

| 方案 | 描述 | 优缺点 |
|------|------|--------|
| 主从复制 | 一主多从 | 读性能提升，写不能扩展 |
| 哨兵 | 监控+故障转移 | 高可用，但写不能扩展 |
| Cluster | 分片集群 | 读写都能扩展，16384 槽位 |

**Cluster 原理**：
- 16384 个槽位分配到各节点
- CRC16(key) % 16384 定位槽位
- 节点间 Gossip 通信

**追问**：
- Cluster 如何做故障转移？
- 客户端如何知道 key 在哪个节点？

---

## 三、分布式高频题

### Q7: 分布式事务解决方案？

**参考答案**：

**方案对比**：

| 方案 | 原理 | 适用场景 |
|------|------|---------|
| 2PC | 准备 + 提交 | 强一致性要求 |
| TCC | Try-Confirm-Cancel | 高并发、最终一致 |
| 本地消息表 | 消息 + 定时任务 | 最终一致 |
| 事务消息 | RocketMQ 半消息 | 最终一致 |
| Seata AT | 全局锁 + Undo Log | 简单场景 |

**TCC 流程**：
1. Try：预留资源
2. Confirm：确认提交
3. Cancel：回滚释放

**追问**：
- TCC 的空回滚问题？
- 悬挂问题如何解决？

### Q8: 消息队列如何保证消息不丢失？

**参考答案**：

**生产者端**：
- 开启事务消息
- 使用 Confirm 模式
- 消息持久化

**Broker 端**：
- 同步刷盘
- 主从同步复制

**消费者端**：
- 手动 ACK
- 幂等处理

**RocketMQ 事务消息**：
1. 发送半消息
2. 执行本地事务
3. 提交/回滚消息
4. 回查机制

**追问**：
- 如何保证消息顺序？
- 如何处理消息重复？

---

## 四、高并发场景题

### Q9: 如何设计一个秒杀系统？

**参考答案**：

**架构分层设计**：

```
用户 → CDN → 网关 → 应用服务 → 缓存 → MQ → 数据库
```

**核心要点**：

1. **前端**：
   - 按钮置灰防重复点击
   - CDN 静态资源缓存
   - 验证码/答题限流

2. **网关层**：
   - 限流（令牌桶/漏桶）
   - 黑名单拦截
   - 请求过滤

3. **应用层**：
   - 库存预热到 Redis
   - 原子扣减（Lua 脚本）
   - MQ 异步下单

4. **数据层**：
   - 乐观锁防超卖
   - 分库分表
   - 读写分离

**防超卖方案**：
```sql
UPDATE stock SET count = count - 1 
WHERE id = ? AND count > 0;
```

**追问**：
- 如何防止同一用户重复下单？
- 高并发下如何保证库存准确？

### Q10: 如何设计一个订单系统？

**参考答案**：

**核心模块**：
1. **订单创建**：幂等设计、库存预占
2. **订单支付**：状态机、超时取消
3. **订单履约**：拆单、合单
4. **订单取消**：库存释放、优惠回退

**状态机设计**：
```
待支付 → 已支付 → 待发货 → 已发货 → 已完成
   ↓                  ↓
  取消               退款
```

**关键设计**：
- 订单号生成（Snowflake）
- 分布式事务（TCC/本地消息表）
- 分库分表（用户 ID 分片）
- 延迟队列处理超时

**追问**：
- 如何保证订单号唯一？
- 订单超时自动取消如何实现？

---

## 五、Java 基础高频题

### Q11: HashMap 底层实现？

**参考答案**：

**JDK 1.8 结构**：数组 + 链表 + 红黑树

**put 流程**：
1. 计算 hash = (h = key.hashCode()) ^ (h >>> 16)
2. 定位桶：hash & (n - 1)
3. 桶为空 → 直接插入
4. 桶不为空 → 遍历链表/红黑树
5. 相同 key → 覆盖 value
6. 链表长度 >= 8 且容量 >= 64 → 红黑树

**扩容**：
- 触发：size > capacity * loadFactor
- 扩容 2 倍
- 元素重新分配

**追问**：
- 为什么负载因子是 0.75？
- JDK 1.7 和 1.8 的区别？

### Q12: ConcurrentHashMap 如何保证线程安全？

**参考答案**：

**JDK 1.7**：Segment + ReentrantLock（分段锁）

**JDK 1.8**：CAS + synchronized

**put 流程**：
1. 计算 hash，定位桶
2. 桶为空 → CAS 插入
3. 桶不为空 → synchronized 锁头节点
4. 链表/红黑树插入
5. 链表长度 >= 8 → 红黑树

**为什么放弃分段锁**：
1. 每个 Segment 占用内存
2. 并发度固定
3. synchronized 优化后性能提升

**追问**：
- ConcurrentHashMap 能完全替代 Hashtable 吗？
- 如何实现复合操作原子性？

### Q13: 线程池核心参数？

**参考答案**：

```java
ThreadPoolExecutor(
    int corePoolSize,       // 核心线程数
    int maximumPoolSize,    // 最大线程数
    long keepAliveTime,     // 非核心线程空闲存活时间
    TimeUnit unit,
    BlockingQueue<Runnable> workQueue,  // 工作队列
    ThreadFactory threadFactory,         // 线程工厂
    RejectedExecutionHandler handler     // 拒绝策略
)
```

**执行流程**：
1. 线程数 < corePoolSize → 创建核心线程
2. 线程数 >= corePoolSize → 放入队列
3. 队列满 → 创建非核心线程
4. 线程数 = maximumPoolSize → 执行拒绝策略

**拒绝策略**：
- AbortPolicy：抛异常（默认）
- CallerRunsPolicy：调用者执行
- DiscardPolicy：丢弃
- DiscardOldestPolicy：丢弃最老的任务

**追问**：
- 为什么不建议用 Executors？
- 如何合理设置参数？

---

## 六、JVM 高频题

### Q14: JVM 内存模型？

**参考答案**：

**运行时数据区**：
1. **程序计数器**：当前线程执行的字节码行号
2. **虚拟机栈**：方法调用的栈帧
3. **本地方法栈**：Native 方法服务
4. **堆**：对象实例存储
5. **方法区**：类信息、常量、静态变量

**JVM 内存模型（JMM）**：
- 主内存：共享变量存储
- 工作内存：线程私有副本
- happens-before 原则

**追问**：
- 堆和栈的区别？
- 对象一定在堆上分配吗？

### Q15: 垃圾收集器选择？

**参考答案**：

| 收集器 | 类型 | 适用场景 |
|--------|------|---------|
| Serial | 单线程 | 客户端 |
| Parallel | 并行 | 吞吐优先 |
| CMS | 并发 | 低延迟 |
| G1 | 分代 | 大内存 |
| ZGC | 并发 | 超大内存 |

**G1 特点**：
- Region 分区
- 可预测停顿
- 无碎片

**追问**：
- CMS 和 G1 的区别？
- 如何选择垃圾收集器？

---

## 七、Spring 高频题

### Q16: Spring Bean 生命周期？

**参考答案**：

1. **实例化**：创建对象
2. **属性赋值**：依赖注入
3. **初始化**：
   - Aware 接口回调
   - BeanPostProcessor（Before）
   - InitializingBean
   - init-method
   - BeanPostProcessor（After）
4. **销毁**：
   - DisposableBean
   - destroy-method

**追问**：
- 循环依赖如何解决？
- Bean 的作用域？

### Q17: Spring 事务传播机制？

**参考答案**：

| 传播行为 | 说明 |
|---------|------|
| REQUIRED | 有则加入，无则新建（默认） |
| SUPPORTS | 有则加入，无则非事务 |
| MANDATORY | 必须有事务 |
| REQUIRES_NEW | 新建事务，挂起当前 |
| NOT_SUPPORTED | 非事务执行 |
| NEVER | 非事务执行，有则异常 |
| NESTED | 嵌套事务 |

**事务失效场景**：
1. 方法非 public
2. 同类调用（绕过代理）
3. 异常被捕获
4. 数据库不支持事务

**追问**：
- REQUIRED 和 NESTED 区别？
- 如何解决事务失效问题？

---

## 八、算法题

美团算法难度中等，偏重实战

### 常考题型

1. **数组**：
   - 三数之和
   - 最长无重复子串
   - 最大子数组和

2. **链表**：
   - 反转链表
   - 合并有序链表
   - 环检测

3. **树**：
   - 层序遍历
   - 最近公共祖先
   - 二叉树序列化

4. **动态规划**：
   - 最长递增子序列
   - 打家劫舍
   - 零钱兑换

5. **SQL**：
   - 复杂查询
   - 窗口函数
   - 索引优化

---

## 九、项目深挖

美团非常注重项目经验，常见追问：

1. **项目难点是什么？**
2. **为什么选择这个方案？**
3. **有没有考虑其他方案？**
4. **遇到什么问题？怎么解决的？**
5. **如果重新设计，会怎么改进？**
6. **系统的 QPS 是多少？**
7. **如何做性能优化？**

---

## 十、面试技巧

1. **重视实战**：美团偏爱场景题，准备项目细节
2. **数据说话**：系统的 QPS、RT 等指标要清楚
3. **方案对比**：回答设计题时多给几种方案对比
4. **关注业务**：美团业务驱动，理解业务很重要
5. **保持谦虚**：不懂就说不懂，不要强行解释

---

## 十一、2026 Java 面经真题

> 来源：牛客网 2026-03
> 特点：项目深挖 + 分布式锁 + 场景题

### 一面真题

#### Q1: 分布式锁如何实现？锁误删怎么解决？

**参考答案**：

**Redis 分布式锁**：
```java
// 加锁
String lockKey = "lock:" + resourceId;
String requestId = UUID.randomUUID().toString();
Boolean acquired = redis.set(lockKey, requestId, "NX", "EX", 30);

// 解锁（Lua 脚本保证原子性）
String script = "if redis.call('get', KEYS[1]) == ARGV[1] then " +
                "return redis.call('del', KEYS[1]) else return 0 end";
redis.eval(script, Collections.singletonList(lockKey), requestId);
```

**锁误删问题**：
- 线程 A 获取锁，执行时间超过过期时间
- 锁自动释放，线程 B 获取锁
- 线程 A 执行完毕，删除了 B 的锁

**解决方案**：
1. **看门狗机制**：自动续期
   ```java
   // Redisson 看门狗
   RLock lock = redisson.getLock("myLock");
   lock.lock();  // 默认 30s，每 10s 续期一次
   ```

2. **value 存唯一标识**：解锁时校验
   ```java
   if (requestId.equals(redis.get(lockKey))) {
       redis.del(lockKey);
   }
   ```

---

#### Q2: 缓存穿透、雪崩、击穿？

**参考答案**：

| 问题 | 原因 | 解决方案 |
|------|------|---------|
| 穿透 | 查询不存在的数据 | 布隆过滤器、空值缓存 |
| 雪崩 | 大量缓存同时失效 | 随机过期时间、多级缓存 |
| 击穿 | 热点 Key 过期 | 互斥锁、永不过期 |

**穿透解决**：
```java
public Object query(String key) {
    Object value = redis.get(key);
    if (value != null) {
        return "NULL".equals(value) ? null : value;
    }
    
    // 布隆过滤器判断
    if (!bloomFilter.mightContain(key)) {
        return null;  // 一定不存在
    }
    
    // 查数据库
    value = db.query(key);
    if (value == null) {
        redis.set(key, "NULL", 60);  // 空值缓存
    } else {
        redis.set(key, value, 300);
    }
    return value;
}
```

---

#### Q3: synchronized 和 Lock 的区别？

**参考答案**：

| 特性 | synchronized | Lock |
|------|-------------|------|
| 实现 | JVM 关键字 | Java 类 |
| 释放 | 自动 | 手动 unlock() |
| 公平性 | 非公平 | 可选 |
| 中断 | 不可 | lockInterruptibly() |
| 条件变量 | 单一 | 多 Condition |

**使用场景**：
- 简单同步：synchronized
- 需要公平锁、可中断、多条件：ReentrantLock

---

#### Q4: 同一用户并发下单如何加锁？

**参考答案**：

**方案 1：synchronized 锁字符串**：
```java
synchronized (userId.intern()) {  // intern() 返回常量池引用
    // 下单逻辑
}
```

**问题**：字符串常量池有限，可能导致内存问题。

**方案 2：分段锁**：
```java
public class SegmentLock {
    private final Object[] locks;
    
    public SegmentLock(int segments) {
        locks = new Object[segments];
        for (int i = 0; i < segments; i++) {
            locks[i] = new Object();
        }
    }
    
    public Object getLock(String key) {
        int index = Math.abs(key.hashCode()) % locks.length;
        return locks[index];
    }
}

// 使用
synchronized (segmentLock.getLock(userId)) {
    // 下单逻辑
}
```

---

#### Q5: 算法题 - 复原 IP 地址

**题目**：给定字符串，返回所有可能的 IP 地址组合。

**参考解答**：
```java
public List<String> restoreIpAddresses(String s) {
    List<String> result = new ArrayList<>();
    backtrack(s, 0, 0, new ArrayList<>(), result);
    return result;
}

private void backtrack(String s, int start, int segments, 
                       List<String> path, List<String> result) {
    if (segments == 4 && start == s.length()) {
        result.add(String.join(".", path));
        return;
    }
    
    for (int len = 1; len <= 3 && start + len <= s.length(); len++) {
        String part = s.substring(start, start + len);
        if (isValid(part)) {
            path.add(part);
            backtrack(s, start + len, segments + 1, path, result);
            path.remove(path.size() - 1);
        }
    }
}

private boolean isValid(String part) {
    if (part.length() > 1 && part.charAt(0) == '0') return false;
    int num = Integer.parseInt(part);
    return num >= 0 && num <= 255;
}
```

---

**面试总结**：
- 美团重视项目深挖，分布式场景题多
- 分布式锁、缓存三兄弟是必考
- 算法题偏中等，但要求手写完整

---

---

## 二、2026 最新面经

### 美团一面面经（2026-03-27）

**来源**：[牛客网 - 美团日常java 一面 面经](https://www.nowcoder.com/feed/main/detail/cab2ca60f7b44cf384770617d75e1c82)

#### Q1: 分布式锁误删问题如何解决？

**参考答案**：

**问题场景**：
1. 线程 A 获取锁，设置过期时间 30s
2. 线程 A 执行业务逻辑超过 30s，锁自动过期
3. 线程 B 获取锁并开始执行
4. 线程 A 执行完毕，删除了线程 B 持有的锁

**解决方案**：

**方案 1：value 存唯一标识**
```java
// 加锁时存入唯一标识
String requestId = UUID.randomUUID().toString();
SET lock:key requestId NX PX 30000

// 解锁时 Lua 脚本校验
if redis.call("GET", KEYS[1]) == ARGV[1] then
    return redis.call("DEL", KEYS[1])
else
    return 0
end
```

**方案 2：看门狗自动续期**
```java
// Redisson 实现
RLock lock = redisson.getLock("myLock");
lock.lock();  // 默认 30s，后台线程每 10s 续期一次

// 业务执行完毕
lock.unlock();
```

**追问**：线程如何感知锁快要超时？  
**答**：Redisson 看门狗机制会在后台启动一个定时任务，每隔一段时间（默认过期时间的 1/3）检查锁是否还被当前线程持有，如果是则续期。

---

#### Q2: 缓存穿透、缓存雪崩、缓存击穿是什么？如何防止？

**参考答案**：

| 问题 | 定义 | 解决方案 |
|------|------|---------|
| **缓存穿透** | 查询不存在的数据，请求穿透到数据库 | 布隆过滤器、空值缓存 |
| **缓存雪崩** | 大量缓存同时失效，请求压垮数据库 | 随机过期时间、多级缓存、熔断降级 |
| **缓存击穿** | 热点 Key 过期，大量请求同时打到数据库 | 互斥锁、永不过期、逻辑过期 |

**代码示例**：

**防止穿透（空值缓存）**：
```java
public Object query(String key) {
    Object value = redis.get(key);
    if (value != null) {
        return "NULL".equals(value) ? null : value;
    }
    
    value = db.query(key);
    if (value == null) {
        redis.set(key, "NULL", 60);  // 缓存空值
    } else {
        redis.set(key, value, 300);
    }
    return value;
}
```

**防止击穿（互斥锁）**：
```java
public Object queryWithLock(String key) {
    Object value = redis.get(key);
    if (value == null) {
        String lockKey = "lock:" + key;
        try {
            // 获取互斥锁
            if (redis.set(lockKey, "1", "NX", "EX", 10)) {
                value = db.query(key);
                redis.set(key, value, 300);
                return value;
            }
            // 等待重试
            Thread.sleep(50);
            return queryWithLock(key);
        } finally {
            redis.del(lockKey);
        }
    }
    return value;
}
```

---

#### Q3: synchronized 和 Lock 的区别是什么？

**参考答案**：

| 特性 | synchronized | Lock (ReentrantLock) |
|------|-------------|---------------------|
| **实现层面** | JVM 关键字，底层通过 monitor | Java API，基于 AQS |
| **释放锁** | 自动释放（代码块结束或异常） | 手动 unlock()，需在 finally 中 |
| **公平性** | 非公平锁 | 可选公平/非公平 |
| **中断响应** | 不可中断 | lockInterruptibly() 可响应中断 |
| **条件变量** | 单一条件（wait/notify） | 多 Condition，精细控制 |
| **性能** | JDK 1.6 后优化，差距不大 | 高竞争时略优 |

**使用场景**：
- 简单同步：synchronized 更简洁
- 需要公平锁、可中断、多条件变量：ReentrantLock

**代码对比**：
```java
// synchronized
synchronized (lock) {
    // 业务逻辑
}

// ReentrantLock
lock.lock();
try {
    // 业务逻辑
} finally {
    lock.unlock();
}
```

---

#### Q4: 在单台机器部署的情况下，如何对同一个用户加锁以确保接口的线程安全？

**场景**：同一用户用不同设备去下单，也就是不同线程同一 userId，如何保证线程安全？

**参考答案**：

**方案 1：synchronized 锁字符串常量池**
```java
public void placeOrder(String userId) {
    synchronized (userId.intern()) {  // intern() 返回常量池中的引用
        // 下单逻辑
    }
}
```

**原理**：`String.intern()` 返回字符串在常量池中的引用，相同字符串返回同一对象，因此可以作为锁对象。

**缺点**：字符串常量池有限，大量用户可能导致内存问题。

**方案 2：分段锁（推荐）**
```java
public class SegmentLock {
    private final Object[] locks;
    private final int segments;
    
    public SegmentLock(int segments) {
        this.segments = segments;
        this.locks = new Object[segments];
        for (int i = 0; i < segments; i++) {
            locks[i] = new Object();
        }
    }
    
    public Object getLock(String key) {
        int index = Math.abs(key.hashCode()) % segments;
        return locks[index];
    }
}

// 使用
synchronized (segmentLock.getLock(userId)) {
    // 下单逻辑
}
```

**方案 3：ConcurrentHashMap 存储锁对象**
```java
private final ConcurrentHashMap<String, Object> userLocks = new ConcurrentHashMap<>();

public void placeOrder(String userId) {
    Object lock = userLocks.computeIfAbsent(userId, k -> new Object());
    synchronized (lock) {
        // 下单逻辑
    }
    // 可选：移除不再使用的锁
    userLocks.remove(userId, lock);
}
```

---

#### Q5: 算法题 - 复原 IP 地址

**题目**：给定一个只包含数字的字符串，返回所有可能的有效 IP 地址组合。

**示例**：
- 输入："25525511135"
- 输出：["255.255.11.135", "255.255.111.35"]

**参考答案**：

```java
public List<String> restoreIpAddresses(String s) {
    List<String> result = new ArrayList<>();
    backtrack(s, 0, 0, new ArrayList<>(), result);
    return result;
}

private void backtrack(String s, int start, int segments, 
                       List<String> path, List<String> result) {
    // 终止条件：分成 4 段且用完所有字符
    if (segments == 4 && start == s.length()) {
        result.add(String.join(".", path));
        return;
    }
    
    // 剪枝：已分 4 段但字符没用完，或字符用完但不足 4 段
    if (segments == 4 || start == s.length()) {
        return;
    }
    
    // 尝试 1-3 位长度
    for (int len = 1; len <= 3 && start + len <= s.length(); len++) {
        String part = s.substring(start, start + len);
        if (isValid(part)) {
            path.add(part);
            backtrack(s, start + len, segments + 1, path, result);
            path.remove(path.size() - 1);
        }
    }
}

private boolean isValid(String part) {
    // 前导零检查：长度 > 1 时不能以 0 开头
    if (part.length() > 1 && part.charAt(0) == '0') {
        return false;
    }
    // 数值范围检查：0-255
    int num = Integer.parseInt(part);
    return num >= 0 && num <= 255;
}
```

**参数说明**：
- `start`：当前处理到的字符串起始位置
- `segments`：已分成的段数（IP 地址共 4 段）
- `path`：当前路径，存储已分的段
- `result`：结果集

**时间复杂度**：O(3^4)，最多递归 4 层，每层 3 种选择

---

[返回目录](../README.md)