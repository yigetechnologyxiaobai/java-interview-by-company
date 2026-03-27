# 小红书 - Java基础

> 本文档整理自 小红书 面经真题，按知识点归类

## 目录

- [五、Java 基础高频题](#五、Java-基础高频题)

---

## Java 基础高频题


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


