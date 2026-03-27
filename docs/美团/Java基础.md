# 美团 - Java基础

> 本文档整理自 美团 面经真题，按知识点归类

## 目录

- [五、Java 基础高频题](#五、Java-基础高频题)

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


