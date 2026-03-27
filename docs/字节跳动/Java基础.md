# 字节跳动 - Java基础

> 本文档整理自 字节跳动 面经真题，按知识点归类

## 目录

- [三、Java 基础高频题](#三、Java-基础高频题)
- [六、网络高频题](#六、网络高频题)
- [七、操作系统高频题](#七、操作系统高频题)

---

## 三、Java 基础高频题


### Q6: HashMap 扩容机制？

**核心概念**：

HashMap 在元素数量超过阈值时自动扩容。

**扩容流程**：

```
触发条件：size > capacity * loadFactor

扩容过程：
1. 容量翻倍（保持 2 的幂）
2. 创建新数组
3. 数据迁移：
   - JDK 1.7：重新计算每个元素的位置
   - JDK 1.8：根据 hash & oldCap 判断

JDK 1.8 优化：
元素位置 = 原位置 或 原位置 + oldCap

示例：
原容量 = 16，元素在位置 5
hash = ...0101 (二进制)
新容量 = 32
hash & 16 = 0 → 仍在位置 5
hash & 16 = 1 → 移动到位置 5 + 16 = 21
```

**为什么容量是 2 的幂？**

```java
// 计算桶位置
index = (n - 1) & hash

// n 是 2 的幂，n-1 的二进制全是 1
// 如 n = 16，n-1 = 15 = 1111（二进制）
// hash & 1111 = hash 的低 4 位
// 等价于 hash % 16，但位运算更快
```

**追问延伸**：
- JDK 1.7 死循环问题？

```java
// JDK 1.7 头插法，并发扩容可能导致死循环
// A → B → null
// 线程 1 处理到 A
// 线程 2 完成扩容，变成 B → A → null
// 线程 1 继续，A.next = B，B.next = A
// 形成环：A → B → A → B → ...
```

---

### Q7: ConcurrentHashMap 如何保证线程安全？

**JDK 1.8 实现**：

```java
final V putVal(K key, V value, boolean onlyIfAbsent) {
    int hash = spread(key.hashCode());
    
    for (Node<K,V>[] tab = table;;) {
        Node<K,V> f; int n, i, fh;
        
        // 情况 1：桶为空，CAS 插入
        if (tab == null || (n = tab.length) == 0)
            tab = initTable();
        else if ((f = tabAt(tab, i = (n - 1) & hash)) == null) {
            if (casTabAt(tab, i, null, new Node<K,V>(hash, key, value, null)))
                break;
        }
        // 情况 2：正在扩容，协助扩容
        else if ((fh = f.hash) == MOVED)
            tab = helpTransfer(tab, f);
        // 情况 3：桶不为空，synchronized 锁头节点
        else {
            synchronized (f) {
                // 处理链表或红黑树
                // ...
            }
        }
    }
    return null;
}
```

**对比 JDK 1.7**：

| 维度 | JDK 1.7 | JDK 1.8 |
|------|---------|---------|
| 锁实现 | Segment + ReentrantLock | CAS + synchronized |
| 锁粒度 | Segment（16 个） | 桶头节点 |
| 并发度 | 最多 16 | 理论无限 |

---

### Q8: 线程池核心参数？

**参数说明**：

```java
ThreadPoolExecutor(
    int corePoolSize,      // 核心线程数
    int maximumPoolSize,   // 最大线程数
    long keepAliveTime,    // 空闲线程存活时间
    TimeUnit unit,         // 时间单位
    BlockingQueue<Runnable> workQueue,  // 工作队列
    ThreadFactory threadFactory,        // 线程工厂
    RejectedExecutionHandler handler    // 拒绝策略
)
```

**执行流程**：

```
提交任务
    │
    ▼
线程数 < core？─── 是 ──→ 创建核心线程
    │
    否
    │
    ▼
队列未满？─── 是 ──→ 加入队列
    │
    否
    │
    ▼
线程数 < max？─── 是 ──→ 创建非核心线程
    │
    否
    │
    ▼
执行拒绝策略
```

**为什么不用 Executors？**

| 线程池 | 问题 |
|--------|------|
| FixedThreadPool | 队列无界，可能 OOM |
| SingleThreadExecutor | 队列无界，可能 OOM |
| CachedThreadPool | 线程无界，可能 OOM |

---


## 六、网络高频题


### Q13: TCP 三次握手/四次挥手

见腾讯面经

### Q14: HTTP 状态码？

| 状态码 | 含义 | 常见场景 |
|--------|------|---------|
| 200 | 成功 | 正常响应 |
| 301 | 永久重定向 | 域名更换 |
| 302 | 临时重定向 | 短链接 |
| 304 | 未修改 | 缓存有效 |
| 400 | 请求错误 | 参数错误 |
| 401 | 未授权 | 未登录 |
| 403 | 禁止访问 | 无权限 |
| 404 | 未找到 | 资源不存在 |
| 500 | 服务器错误 | 代码异常 |
| 502 | 网关错误 | 上游服务不可用 |
| 503 | 服务不可用 | 过载/维护 |

---


## 七、操作系统高频题


### Q15: 进程通信方式？

1. **管道**：父子进程通信
2. **消息队列**：内核中的消息链表
3. **共享内存**：最快的 IPC
4. **信号量**：进程同步
5. **Socket**：跨机器通信

### Q16: 死锁？

**四个必要条件**：
1. 互斥
2. 请求保持
3. 不剥夺
4. 循环等待

**解决方法**：
- 预防：破坏四个条件之一
- 避免：银行家算法
- 检测：资源分配图
- 解除：剥夺资源、终止进程

---


