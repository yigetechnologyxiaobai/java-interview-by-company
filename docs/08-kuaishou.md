# 快手 Java 面试题

## 面试风格

**特点**：一面偏基础八股，二面深挖项目和算法（Hard 较多）

**轮次**：通常 2-3 轮技术面 + 1 轮 HR

**重点**：JUC 多线程、并发特性、网络编程、算法

**面试官画像**：一面常规八股，二面深挖项目，手撕 Hard 级别算法

---

## 一、Java 基础高频题

### Q1: HashMap 底层实现原理？

**核心概念**：

HashMap 是 Java 最常用的 Map 实现，基于哈希表。

**JDK 1.8 结构**：

```
┌─────────────────────────────────────────────────────────────────┐
│                    HashMap 结构 (JDK 1.8)                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Node[] table                                                   │
│  ┌─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┐            │
│  │Node │Node │Node │Node │Node │Node │Node │ ... │            │
│  └──┬──┴─────┴──┬──┴─────┴─────┴─────┴──┬──┴─────┘            │
│     │           │                       │                      │
│     ▼           ▼                       ▼                      │
│   链表         红黑树                  链表                     │
│   (长度<8)    (长度≥8)               (长度<8)                   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

**为什么用红黑树？**
- 链表长度过长时，查询效率 O(n)
- 红黑树查询效率 O(log n)
- 当链表长度 >= 8 且数组长度 >= 64 时转换

**put 流程**：

```java
public V put(K key, V value) {
    // 1. 计算 hash
    int hash = (key == null) ? 0 : (h = key.hashCode()) ^ (h >>> 16);
    
    // 2. 定位桶
    int index = (n - 1) & hash;
    
    // 3. 桶为空 → 直接插入
    // 4. 桶不为空 → 处理冲突
    // 5. 扩容
}
```

**线程安全的 Map**：
- ConcurrentHashMap（推荐）
- Hashtable（不推荐，性能差）
- Collections.synchronizedMap()

---

### Q2: ConcurrentHashMap 实现原理？

**核心概念**：

ConcurrentHashMap 是线程安全的 HashMap。

**JDK 1.7：分段锁**：
- 默认 16 个 Segment
- 每个 Segment 是一个小的 HashMap + ReentrantLock
- 并发度 = Segment 数量

**JDK 1.8：CAS + synchronized**：

```java
final V putVal(K key, V value, boolean onlyIfAbsent) {
    int hash = spread(key.hashCode());
    
    for (Node<K,V>[] tab = table;;) {
        // 1. 桶为空 → CAS 插入
        if ((f = tabAt(tab, i)) == null) {
            if (casTabAt(tab, i, null, new Node<>()))
                break;
        }
        // 2. 正在扩容 → 协助扩容
        else if ((fh = f.hash) == MOVED) {
            tab = helpTransfer(tab, f);
        }
        // 3. 桶不为空 → synchronized 锁头节点
        else {
            synchronized (f) {
                // 插入链表或红黑树
            }
        }
    }
}
```

**为什么 JDK 1.8 放弃分段锁？**
1. 每个 Segment 占用内存
2. 并发度固定
3. synchronized 优化后性能提升

---

## 二、多线程与并发高频题

### Q3: 并发三大特性是什么？

**核心概念**：

并发编程有三大特性：原子性、可见性、有序性。

```
┌─────────────────────────────────────────────────────────────────┐
│                      并发三大特性                                │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  1. 原子性（Atomicity）                                          │
│     └─ 操作不可分割，要么全部成功，要么全部失败                 │
│     └─ 问题：count++ 不是原子操作                               │
│     └─ 解决：synchronized、Lock、Atomic 类                      │
│                                                                 │
│  2. 可见性（Visibility）                                         │
│     └─ 一个线程修改后，其他线程能立即看到                       │
│     └─ 问题：缓存导致可见性问题                                 │
│     └─ 解决：volatile、synchronized、Lock、final               │
│                                                                 │
│  3. 有序性（Ordering）                                           │
│     └─ 程序执行顺序与代码顺序一致                               │
│     └─ 问题：指令重排序                                         │
│     └─ 解决：volatile、synchronized、Lock                      │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

**JMM（Java 内存模型）**：

```
┌─────────────────────────────────────────────────────────────────┐
│                       JMM 内存模型                               │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  线程 1                     线程 2                              │
│  ┌─────────────┐           ┌─────────────┐                    │
│  │ 工作内存     │           │ 工作内存     │                    │
│  │ (本地副本)   │           │ (本地副本)   │                    │
│  └──────┬──────┘           └──────┬──────┘                    │
│         │                         │                            │
│         │  read/write             │  read/write                │
│         │                         │                            │
│         ▼                         ▼                            │
│  ┌─────────────────────────────────────────────────────────┐  │
│  │                     主内存                               │  │
│  │              (共享变量存储位置)                           │  │
│  └─────────────────────────────────────────────────────────┘  │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

**happens-before 原则**：
- 程序顺序规则
- 监视器锁规则
- volatile 变量规则
- 线程启动规则
- 线程终止规则
- 传递性

---

### Q4: synchronized 锁优化过程？

**核心概念**：

JDK 6 对 synchronized 做了大量优化，引入锁升级机制。

**锁升级过程**：

```
无锁 → 偏向锁 → 轻量级锁 → 重量级锁

┌─────────────────────────────────────────────────────────────────┐
│                       锁升级详解                                 │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  偏向锁                                                          │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  场景：只有一个线程访问同步块                           │   │
│  │  原理：在 Mark Word 中记录线程 ID                       │   │
│  │  操作：同一线程重入，无需同步                           │   │
│  │  升级：出现其他线程竞争                                 │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│  轻量级锁                                                        │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  场景：两个线程交替执行，无真正竞争                      │   │
│  │  原理：CAS 将 Mark Word 复制到 Lock Record              │   │
│  │  操作：自旋等待                                         │   │
│  │  升级：自旋超过阈值或出现真正竞争                       │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│  重量级锁                                                        │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  场景：多个线程真正竞争                                 │   │
│  │  原理：基于 Monitor 实现                                │   │
│  │  操作：线程阻塞，等待唤醒                               │   │
│  │  特点：切换开销大                                       │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

**Mark Word 存储**：

```
┌─────────────────────────────────────────────────────────────────┐
│                     64 位对象头结构                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  偏向锁：                                                        │
│  ┌────────────────────────────────────┬───────┬────┬──────────┐│
│  │     thread ID (54)                 │ age(4)│ 1  │ lock(01) ││
│  └────────────────────────────────────┴───────┴────┴──────────┘│
│                                                                 │
│  轻量级锁：                                                      │
│  ┌────────────────────────────────────────────────┬───────────┐│
│  │          Lock Record 指针 (62)                  │ lock(00)  ││
│  └────────────────────────────────────────────────┴───────────┘│
│                                                                 │
│  重量级锁：                                                      │
│  ┌────────────────────────────────────────────────┬───────────┐│
│  │          Monitor 指针 (62)                      │ lock(10)  ││
│  └────────────────────────────────────────────────┴───────────┘│
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

### Q5: CAS 操作原理？

**核心概念**：

CAS（Compare And Swap）是比较并交换，是一种乐观锁机制。

**原理**：

```java
// CAS 伪代码
public boolean compareAndSwap(int expected, int newValue) {
    if (this.value == expected) {
        this.value = newValue;
        return true;
    }
    return false;
}
```

**Java 实现**：

```java
// AtomicInteger
public final int incrementAndGet() {
    return unsafe.getAndAddInt(this, valueOffset, 1) + 1;
}

// Unsafe 类
public final int getAndAddInt(Object o, long offset, int delta) {
    int v;
    do {
        v = getIntVolatile(o, offset);
    } while (!compareAndSwapInt(o, offset, v, v + delta));
    return v;
}
```

**ABA 问题**：

```
问题：
线程 1：读取 A → 准备改为 C
线程 2：读取 A → 改为 B → 改为 A
线程 1：CAS(A, C) 成功

解决：
- 加版本号
- AtomicStampedReference
```

**CAS vs synchronized**：

| 维度 | CAS | synchronized |
|------|-----|--------------|
| 类型 | 乐观锁 | 悲观锁 |
| 性能 | 无竞争时更好 | 竞争激烈时更好 |
| 问题 | ABA、自旋开销 | 阻塞开销 |

---

### Q6: 线程池的实现方式？

**核心概念**：

线程池通过复用线程，减少创建销毁开销。

**JDK 提供的线程池**：

```java
// 1. FixedThreadPool（固定大小）
ExecutorService fixed = Executors.newFixedThreadPool(10);
// 问题：队列无界，可能 OOM

// 2. CachedThreadPool（可缓存）
ExecutorService cached = Executors.newCachedThreadPool();
// 问题：线程无界，可能 OOM

// 3. SingleThreadExecutor（单线程）
ExecutorService single = Executors.newSingleThreadExecutor();
// 问题：队列无界，可能 OOM

// 4. ScheduledThreadPool（定时任务）
ScheduledExecutorService scheduled = Executors.newScheduledThreadPool(5);

// 5. WorkStealingPool（工作窃取）
ExecutorService workStealing = Executors.newWorkStealingPool();
```

**推荐方式**：

```java
ThreadPoolExecutor executor = new ThreadPoolExecutor(
    10,                             // 核心线程数
    20,                             // 最大线程数
    60L, TimeUnit.SECONDS,          // 空闲存活时间
    new ArrayBlockingQueue<>(1000), // 有界队列
    new ThreadFactoryBuilder().setNameFormat("worker-%d").build(),
    new ThreadPoolExecutor.CallerRunsPolicy()
);
```

**Future 实现**：

```java
Future<String> future = executor.submit(() -> {
    Thread.sleep(1000);
    return "result";
});

// 阻塞获取结果
String result = future.get();

// 超时获取
String result = future.get(5, TimeUnit.SECONDS);

// 取消任务
future.cancel(true);
```

**ForkJoin 框架**：

```java
// 分而治之，工作窃取
ForkJoinPool pool = new ForkJoinPool();

class SumTask extends RecursiveTask<Long> {
    private long[] array;
    private int start, end;
    
    @Override
    protected Long compute() {
        if (end - start <= THRESHOLD) {
            // 直接计算
        } else {
            // 拆分任务
            SumTask left = new SumTask(array, start, mid);
            SumTask right = new SumTask(array, mid, end);
            left.fork();
            right.fork();
            return left.join() + right.join();
        }
    }
}
```

---

## 三、JVM 高频题

### Q7: JVM 内存结构？

**核心概念**：

JVM 运行时数据区分为线程私有和线程共享两大部分。

**运行时数据区**：

```
┌─────────────────────────────────────────────────────────────────┐
│                        JVM 运行时数据区                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  线程私有：                                                      │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  程序计数器：当前线程执行的字节码行号                    │   │
│  │  虚拟机栈：方法调用的栈帧                               │   │
│  │  本地方法栈：Native 方法服务                            │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│  线程共享：                                                      │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  堆：对象实例存储，GC 主要区域                           │   │
│  │  ┌───────────────────┬───────────────────────┐         │   │
│  │  │  新生代 (1/3)      │     老年代 (2/3)      │         │   │
│  │  │  Eden + S0 + S1   │                      │         │   │
│  │  └───────────────────┴───────────────────────┘         │   │
│  │                                                         │   │
│  │  方法区：类信息、常量、静态变量                          │   │
│  │  JDK 8：元空间 (Metaspace，本地内存)                    │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

### Q8: 垃圾收集算法？

**核心概念**：

垃圾收集需要判断哪些对象是垃圾，然后回收。

**判断对象存活**：

```
引用计数法（不使用）：
- 计数器记录引用数
- 问题：循环引用无法回收

可达性分析（JVM 使用）：
- 从 GC Roots 开始遍历对象图
- 不可达的对象即为垃圾

GC Roots：
1. 虚拟机栈中引用的对象
2. 方法区中类静态属性引用的对象
3. 方法区中常量引用的对象
4. 本地方法栈中 JNI 引用的对象
```

**垃圾收集算法**：

| 算法 | 原理 | 优点 | 缺点 |
|------|------|------|------|
| 标记-清除 | 标记后清除 | 简单 | 有碎片 |
| 标记-整理 | 标记后整理 | 无碎片 | 移动成本 |
| 复制算法 | 复制存活对象 | 高效 | 空间浪费 |
| 分代收集 | 按分代选算法 | 综合 | 复杂 |

---

## 四、Spring 高频桶

### Q9: Spring、Spring MVC、Spring Boot 区别？

**核心概念**：

Spring 生态由多个项目组成，各司其职。

**对比**：

| 项目 | 定位 | 核心功能 |
|------|------|---------|
| Spring | 基础框架 | IoC、AOP |
| Spring MVC | Web 框架 | MVC 模式 |
| Spring Boot | 快速开发 | 自动配置 |

**Spring 核心模块**：

```
┌─────────────────────────────────────────────────────────────────┐
│                     Spring 核心模块                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  IoC 容器（控制反转）                                            │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  BeanFactory：基础容器                                  │   │
│  │  ApplicationContext：增强容器                           │   │
│  │  依赖注入：@Autowired、@Resource、构造器注入            │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│  AOP 框架（面向切面编程）                                        │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  动态代理：JDK、CGLIB                                   │   │
│  │  应用：事务、日志、权限                                  │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

**Spring Boot 自动装配原理**：

```
@SpringBootApplication
├── @SpringBootConfiguration
├── @ComponentScan
└── @EnableAutoConfiguration
    ├── @AutoConfigurationPackage
    └── @Import(AutoConfigurationImportSelector.class)
        └── 加载 META-INF/spring.factories
            └── 根据条件注解 @Conditional 决定是否装配
```

---

## 五、网络编程高频题

### Q10: WebSocket 实现原理？

**核心概念**：

WebSocket 是一种全双工通信协议。

**与 HTTP 区别**：

| 维度 | HTTP | WebSocket |
|------|------|-----------|
| 通信模式 | 半双工 | 全双工 |
| 连接 | 短连接 | 长连接 |
| 实时性 | 轮询 | 实时推送 |

**握手过程**：

```
客户端 → 服务端：
GET /chat HTTP/1.1
Upgrade: websocket
Connection: Upgrade
Sec-WebSocket-Key: dGhlIHNhbXBsZSBub25jZQ==

服务端 → 客户端：
HTTP/1.1 101 Switching Protocols
Upgrade: websocket
Connection: Upgrade
Sec-WebSocket-Accept: s3pPLMBiTxaQ9kYGzzhZRbK+xOo=
```

**Netty 实现**：

```java
EventLoopGroup bossGroup = new NioEventLoopGroup();
EventLoopGroup workerGroup = new NioEventLoopGroup();

ServerBootstrap bootstrap = new ServerBootstrap();
bootstrap.group(bossGroup, workerGroup)
    .channel(NioServerSocketChannel.class)
    .childHandler(new ChannelInitializer<SocketChannel>() {
        @Override
        protected void initChannel(SocketChannel ch) {
            ch.pipeline()
                .addLast(new HttpServerCodec())
                .addLast(new HttpObjectAggregator(65536))
                .addLast(new WebSocketServerProtocolHandler("/ws"))
                .addLast(new MyWebSocketHandler());
        }
    });

ChannelFuture future = bootstrap.bind(8080).sync();
```

---

## 六、分布式系统

### Q11: 什么是分布式事务？

**核心概念**：

分布式事务保证跨服务操作的原子性。

**解决方案**：

```
┌─────────────────────────────────────────────────────────────────┐
│                      分布式事务方案                               │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  1. 2PC（两阶段提交）                                            │
│     └─ 准备阶段 + 提交阶段                                      │
│     └─ 问题：阻塞、单点、数据不一致                             │
│                                                                 │
│  2. TCC（Try-Confirm-Cancel）                                    │
│     └─ Try：预留资源                                            │
│     └─ Confirm：确认提交                                        │
│     └─ Cancel：回滚释放                                         │
│     └─ 问题：业务侵入大                                         │
│                                                                 │
│  3. 本地消息表                                                   │
│     └─ 本地事务写入消息表                                       │
│     └─ 定时任务扫描发送                                         │
│     └─ 最终一致性                                               │
│                                                                 │
│  4. 事务消息（RocketMQ）                                         │
│     └─ 半消息                                                   │
│     └─ 本地事务                                                 │
│     └─ 提交/回滚                                                │
│                                                                 │
│  5. Seata                                                        │
│     └─ AT 模式：自动生成 Undo Log                               │
│     └─ TCC 模式：手动实现                                       │
│     └─ SAGA 模式：长事务                                        │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 七、算法题

快手算法难度较高，二面常有 Hard 级别：

### 1. 反转链表

```java
// 迭代
public ListNode reverseList(ListNode head) {
    ListNode prev = null, curr = head;
    while (curr != null) {
        ListNode next = curr.next;
        curr.next = prev;
        prev = curr;
        curr = next;
    }
    return prev;
}

// 递归
public ListNode reverseList(ListNode head) {
    if (head == null || head.next == null) return head;
    ListNode newHead = reverseList(head.next);
    head.next.next = head;
    head.next = null;
    return newHead;
}
```

### 2. 合并两个有序链表

```java
public ListNode mergeTwoLists(ListNode l1, ListNode l2) {
    if (l1 == null) return l2;
    if (l2 == null) return l1;
    if (l1.val < l2.val) {
        l1.next = mergeTwoLists(l1.next, l2);
        return l1;
    } else {
        l2.next = mergeTwoLists(l1, l2.next);
        return l2;
    }
}
```

### 3. 快速排序

```java
public void quickSort(int[] arr, int left, int right) {
    if (left >= right) return;
    int pivot = partition(arr, left, right);
    quickSort(arr, left, pivot - 1);
    quickSort(arr, pivot + 1, right);
}

private int partition(int[] arr, int left, int right) {
    int pivot = arr[right];
    int i = left;
    for (int j = left; j < right; j++) {
        if (arr[j] < pivot) {
            swap(arr, i++, j);
        }
    }
    swap(arr, i, right);
    return i;
}
```

---

## 八、面试技巧

1. **一面基础要扎实**：快手一面主打八股文，常规问题要熟练
2. **二面项目要深挖**：项目难点、技术选型要能说清楚
3. **算法要多练**：快手喜欢出 Hard，手撕能力要强
4. **JUC 要精通**：多线程场景题是快手特色

---

[返回目录](../README.md)