# 百度 Java 面试题

## 面试风格

**特点**：注重基础扎实，引导式提问，关注底层原理

**轮次**：通常 2-3 轮技术面 + 1 轮 HR

**重点**：Java 基础、多线程、JVM、MySQL、算法

**面试官画像**：喜欢引导式提问，会根据回答深入追问

---

## 一、Java 基础高频题

### Q1: HashMap 底层原理？

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
│  │ 0   │ 1   │ 2   │ 3   │ 4   │ 5   │ 6   │     │            │
│  └──┬──┴─────┴──┬──┴─────┴─────┴─────┴──┬──┴─────┘            │
│     │           │                       │                      │
│     ▼           ▼                       ▼                      │
│   链表         红黑树                  链表                     │
│   (长度<8)    (长度≥8)               (长度<8)                   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

**扰动函数**：

```java
static final int hash(Object key) {
    int h;
    // 高 16 位异或低 16 位，减少哈希冲突
    return (key == null) ? 0 : (h = key.hashCode()) ^ (h >>> 16);
}
```

**为什么用扰动函数？**
- 减少 hash 冲突
- 让 hash 的高位也参与运算
- 在数组长度较小时效果明显

**put 流程**：

```java
public V put(K key, V value) {
    // 1. 计算 hash
    int hash = hash(key);
    
    // 2. 定位桶：(n - 1) & hash，等价于 hash % n
    int index = (n - 1) & hash;
    
    // 3. 桶为空 → 直接插入
    if (tab[index] == null) {
        tab[index] = new Node(hash, key, value, null);
    }
    // 4. 桶不为空 → 处理冲突
    else {
        // 4.1 相同 key → 覆盖
        // 4.2 红黑树 → 插入树
        // 4.3 链表 → 尾插法插入，长度 >= 8 转红黑树
    }
    
    // 5. 扩容：size > threshold
    if (++size > threshold) {
        resize();
    }
}
```

**扩容机制**：

```
触发条件：size > capacity * loadFactor

JDK 1.8 优化：
元素位置 = 原位置 或 原位置 + oldCap

原理：
hash & oldCap == 0 → 原位置
hash & oldCap == 1 → 原位置 + oldCap

示例：
原容量 = 16，元素在位置 5
新容量 = 32
如果 hash 第 5 位为 0，仍在位置 5
如果 hash 第 5 位为 1，移动到位置 5 + 16 = 21
```

**面试加分点**：
> 为什么负载因子是 0.75？
> - 太小：空间浪费
> - 太大：哈希冲突多
> - 0.75 是时间和空间的折中

**追问延伸**：
- JDK 1.7 和 1.8 的区别？

| 维度 | JDK 1.7 | JDK 1.8 |
|------|---------|---------|
| 结构 | 数组 + 链表 | 数组 + 链表 + 红黑树 |
| 插入方式 | 头插法 | 尾插法 |
| 扩容 | 重新计算位置 | 原位置或原位置+oldCap |
| hash 计算 | 9 次扰动 | 1 次扰动 |

- 为什么线程不安全？
  - JDK 1.7 头插法可能导致死循环
  - 并发 put 可能丢失数据
  - 扩容时数据丢失

---

### Q2: ConcurrentHashMap 如何保证线程安全？

**核心概念**：

ConcurrentHashMap 是线程安全的 HashMap，JDK 1.7 和 1.8 实现差异很大。

**JDK 1.7：分段锁**：

```
┌─────────────────────────────────────────────────────────────────┐
│                    JDK 1.7 分段锁结构                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Segment[] segments（默认 16 个）                               │
│  ┌─────────┬─────────┬─────────┬─────────┐                     │
│  │Segment 0│Segment 1│Segment 2│  ...    │                     │
│  │(Reentrant│(Reentrant│(Reentrant│       │                     │
│  │  Lock)  │  Lock)  │  Lock)  │       │                     │
│  └────┬────┴────┬────┴────┬────┴─────────┘                     │
│       │         │         │                                     │
│       ▼         ▼         ▼                                     │
│  HashEntry[] HashEntry[] HashEntry[]                            │
│                                                                 │
│  特点：                                                         │
│  - 每个 Segment 独立加锁                                        │
│  - 并发度 = Segment 数量                                        │
│  - 锁粒度较粗                                                   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

**JDK 1.8：CAS + synchronized**：

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
                // 遍历链表或红黑树，插入节点
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
| 内存占用 | 每个 Segment 都要分配内存 | 更少 |

**面试加分点**：
> 为什么 JDK 1.8 放弃分段锁？
> 1. 每个 Segment 都要占用内存，空间开销大
> 2. 并发度受 Segment 数量限制（默认 16）
> 3. CAS + synchronized 锁粒度更细
> 4. JDK 对 synchronized 做了大量优化

---

### Q3: String 为什么不可变？

**核心概念**：

String 是 Java 中最常用的类之一，被设计为不可变。

**源码分析**：

```java
public final class String implements java.io.Serializable, Comparable<String>, CharSequence {
    // final 修饰，不可修改
    private final char[] value;  // JDK 8
    // private final byte[] value;  // JDK 9+
    
    private int hash;  // 缓存 hash 值
}
```

**不可变的原因**：

1. **final 类**：不能被继承
2. **final char[]**：引用不可变
3. **无修改方法**：没有提供修改内容的方法

**不可变的好处**：

```
┌─────────────────────────────────────────────────────────────────┐
│                    String 不可变的好处                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  1. 线程安全                                                     │
│     └─ 不可变对象天然线程安全                                   │
│     └─ 不需要同步                                               │
│                                                                 │
│  2. Hash 缓存                                                   │
│     └─ hash 值只计算一次，缓存起来                             │
│     └─ HashMap 的 key 性能好                                   │
│                                                                 │
│  3. 字符串常量池                                                 │
│     └─ 可以复用，节省内存                                       │
│     └─ String s1 = "hello"; String s2 = "hello"; // 同一对象   │
│                                                                 │
│  4. 安全性                                                       │
│     └─ 防止被恶意修改                                           │
│     └─ 如文件路径、网络 URL                                     │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

**面试加分点**：
> 可以写一个类继承 String 吗？
> - 不可以！String 是 final 类
> - final 类不能被继承

---

### Q4: 面向对象三大特性？

**核心概念**：

面向对象三大特性：封装、继承、多态。

**1. 封装**：

```java
// 封装：隐藏实现细节，暴露公共接口
public class Person {
    private String name;  // 私有属性
    private int age;
    
    // 公共方法
    public String getName() {
        return name;
    }
    
    public void setAge(int age) {
        if (age > 0 && age < 150) {  // 数据校验
            this.age = age;
        }
    }
}
```

**2. 继承**：

```java
// 继承：子类继承父类的属性和方法
public class Animal {
    protected String name;
    
    public void eat() {
        System.out.println(name + " is eating");
    }
}

public class Dog extends Animal {
    public void bark() {
        System.out.println(name + " is barking");
    }
}
```

**3. 多态**：

```java
// 多态：同一方法，不同实现
public abstract class Animal {
    public abstract void makeSound();
}

public class Dog extends Animal {
    @Override
    public void makeSound() {
        System.out.println("汪汪汪");
    }
}

public class Cat extends Animal {
    @Override
    public void makeSound() {
        System.out.println("喵喵喵");
    }
}

// 使用
Animal animal = new Dog();
animal.makeSound();  // 汪汪汪
```

**多态的三个条件**：
1. 继承
2. 重写
3. 父类引用指向子类对象

**抽象类 vs 接口**：

| 维度 | 抽象类 | 接口 |
|------|--------|------|
| 方法 | 可以有具体方法 | JDK 8 前只能抽象方法 |
| 变量 | 可以有普通变量 | 只能是 public static final |
| 继承 | 单继承 | 多实现 |
| 构造器 | 有 | 无 |
| 设计目的 | 代码复用 | 定义规范 |

---

## 二、多线程与并发高频题

### Q5: synchronized 底层原理？

**核心概念**：

synchronized 是 Java 内置的互斥锁，基于 Monitor 实现。

**三种使用方式**：

```java
public class SynchronizedDemo {
    // 1. 同步代码块（锁指定对象）
    public void block() {
        synchronized (this) {
            // 临界区
        }
    }
    
    // 2. 同步实例方法（锁 this）
    public synchronized void instanceMethod() {}
    
    // 3. 同步静态方法（锁 Class 对象）
    public static synchronized void staticMethod() {}
}
```

**底层原理**：

**同步代码块**：`monitorenter` / `monitorexit` 字节码指令

**同步方法**：`ACC_SYNCHRONIZED` 标志

**锁升级过程**：

```
无锁 → 偏向锁 → 轻量级锁 → 重量级锁

┌─────────────────────────────────────────────────────────────────┐
│                       锁升级过程                                 │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  偏向锁：同一线程重入，CAS 修改 Mark Word                       │
│  └─ 场景：只有一个线程访问同步块                                │
│  └─ 优点：几乎无额外开销                                        │
│                                                                 │
│  轻量级锁：多线程交替执行，CAS 自旋                             │
│  └─ 场景：两个线程交替执行，无真正竞争                          │
│  └─ 优点：不阻塞线程                                            │
│                                                                 │
│  重量级锁：竞争激烈，阻塞等待                                   │
│  └─ 场景：多个线程真正竞争                                      │
│  └─ 缺点：线程阻塞，切换开销大                                  │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

**面试加分点**：
> synchronized 和 ReentrantLock 区别：

| 维度 | synchronized | ReentrantLock |
|------|--------------|---------------|
| 实现层次 | JVM 关键字 | Java API |
| 锁释放 | 自动 | 手动 unlock() |
| 锁类型 | 非公平 | 可选公平/非公平 |
| 中断 | 不支持 | 支持 lockInterruptibly() |
| 条件变量 | 单一 | 多个 Condition |

---

### Q6: volatile 关键字？

**核心概念**：

volatile 保证可见性和禁止指令重排，但不保证原子性。

**两大特性**：

```
┌─────────────────────────────────────────────────────────────────┐
│                     volatile 两大特性                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  1. 可见性                                                       │
│     └─ 修改后立即同步到主内存                                   │
│     └─ 其他线程读取时从主内存刷新                               │
│     └─ 实现：lock 前缀指令                                      │
│                                                                 │
│  2. 禁止指令重排                                                 │
│     └─ 内存屏障（Memory Barrier）                               │
│     └─ LoadLoad、StoreStore、LoadStore、StoreLoad              │
│     └─ 保证有序性                                               │
│                                                                 │
│  不保证原子性                                                    │
│     └─ volatile int count = 0;                                  │
│     └─ count++;  // 不是原子操作                                │
│     └─ 读取、修改、写入三步                                     │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

**应用场景**：

```java
// 1. 状态标志位
private volatile boolean running = true;

public void stop() {
    running = false;
}

// 2. 双重检查锁单例
public class Singleton {
    private static volatile Singleton instance;
    
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

**为什么双重检查锁要用 volatile？**
- `instance = new Singleton()` 不是原子操作
- 分三步：分配内存 → 初始化对象 → 指向引用
- 可能重排为：分配内存 → 指向引用 → 初始化对象
- 其他线程可能拿到未初始化完成的对象

---

### Q7: 线程池核心参数？

**核心概念**：

线程池通过复用线程，减少创建销毁开销。

**核心参数**：

```java
ThreadPoolExecutor(
    int corePoolSize,              // 核心线程数
    int maximumPoolSize,           // 最大线程数
    long keepAliveTime,            // 空闲线程存活时间
    TimeUnit unit,                 // 时间单位
    BlockingQueue<Runnable> workQueue,  // 工作队列
    ThreadFactory threadFactory,   // 线程工厂
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

**四种拒绝策略**：

| 策略 | 行为 | 适用场景 |
|------|------|---------|
| AbortPolicy | 抛 RejectedExecutionException | 默认，需要感知错误 |
| CallerRunsPolicy | 调用者线程执行 | 不丢弃任务 |
| DiscardPolicy | 直接丢弃 | 允许丢失 |
| DiscardOldestPolicy | 丢弃队列最老任务 | 允许丢失旧任务 |

**为什么不用 Executors？**

| 线程池 | 问题 |
|--------|------|
| FixedThreadPool | 队列无界，可能 OOM |
| SingleThreadExecutor | 队列无界，可能 OOM |
| CachedThreadPool | 线程无界，可能 OOM |

---

### Q8: Java 线程有哪些状态？

**核心概念**：

Java 线程有 6 种状态。

**状态转换图**：

```
┌─────────────────────────────────────────────────────────────────┐
│                      Java 线程状态                               │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  NEW（新建）                                                     │
│     └─ 线程创建但未启动                                         │
│     │                                                           │
│     └─ start() ──────────────────────────────────┐             │
│                                                   │             │
│  RUNNABLE（可运行）                               ▼             │
│     └─ 正在运行或等待 CPU                         ┌────────┐   │
│     │                                              │RUNNABLE│   │
│     ├─ 获取锁失败 ──► BLOCKED（阻塞）              └────────┘   │
│     │                 └─ 等待获取锁                    ▲       │
│     │                 └─ 获取锁 ──────────────────────┘       │
│     │                                                        │
│     ├─ wait()/join()/park() ──► WAITING（等待）               │
│     │                            └─ 等待其他线程              │
│     │                            └─ notify()/notifyAll() ───┐ │
│     │                                                        │ │
│     ├─ sleep(time)/wait(time) ──► TIMED_WAITING（超时等待）  │ │
│     │                                └─ 等待指定时间          │ │
│     │                                └─ 时间到/notify() ─────┼─┘
│     │                                                        │
│     └─ run() 结束 ──► TERMINATED（终止）                     │
│                          └─ 线程结束                          │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

**状态说明**：

| 状态 | 说明 |
|------|------|
| NEW | 新建，未调用 start() |
| RUNNABLE | 可运行，等待 CPU 或正在运行 |
| BLOCKED | 阻塞，等待获取锁 |
| WAITING | 等待，需要其他线程唤醒 |
| TIMED_WAITING | 超时等待，到时间自动唤醒 |
| TERMINATED | 终止，run() 方法执行完毕 |

---

## 三、JVM 高频题

### Q9: JVM 内存结构？

**核心概念**：

JVM 运行时数据区分为线程私有和线程共享两大部分。

**运行时数据区**：

```
┌─────────────────────────────────────────────────────────────────┐
│                        JVM 运行时数据区                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────────── 线程私有 ───────────────────┐            │
│  │                                               │            │
│  │  ┌────────────┐ ┌────────────┐ ┌───────────┐ │            │
│  │  │程序计数器   │ │ 虚拟机栈   │ │本地方法栈 │ │            │
│  │  │PC Register │ │ VM Stack  │ │Native Stack│ │            │
│  │  └────────────┘ └────────────┘ └───────────┘ │            │
│  │                                               │            │
│  └───────────────────────────────────────────────┘            │
│                                                                 │
│  ┌─────────────────── 线程共享 ───────────────────┐            │
│  │                                               │            │
│  │  ┌─────────────────────────────────────────┐  │            │
│  │  │              堆 (Heap)                  │  │            │
│  │  │  新生代（Eden + S0 + S1） + 老年代       │  │            │
│  │  └─────────────────────────────────────────┘  │            │
│  │                                               │            │
│  │  ┌─────────────────────────────────────────┐  │            │
│  │  │         方法区 (元空间 Metaspace)        │  │            │
│  │  │  类信息、常量、静态变量、JIT 代码        │  │            │
│  │  └─────────────────────────────────────────┘  │            │
│  │                                               │            │
│  └───────────────────────────────────────────────┘            │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

**各区域说明**：

| 区域 | 作用 | 异常 |
|------|------|------|
| 程序计数器 | 当前线程执行的字节码行号 | 无 |
| 虚拟机栈 | 方法调用的栈帧 | StackOverflowError, OOM |
| 本地方法栈 | Native 方法服务 | StackOverflowError, OOM |
| 堆 | 对象实例存储 | OOM |
| 方法区 | 类信息、常量、静态变量 | OOM |

---

### Q10: 垃圾回收算法？

**核心概念**：

垃圾回收需要判断哪些对象是垃圾，然后回收。

**判断对象存活**：

**引用计数法**（不使用）：
- 计数器记录引用数
- 问题：循环引用无法回收

**可达性分析**（JVM 使用）：
- 从 GC Roots 开始遍历对象图
- 不可达的对象即为垃圾

**GC Roots**：
1. 虚拟机栈中引用的对象
2. 方法区中类静态属性引用的对象
3. 方法区中常量引用的对象
4. 本地方法栈中 JNI 引用的对象

**垃圾收集算法**：

| 算法 | 原理 | 优点 | 缺点 |
|------|------|------|------|
| 标记-清除 | 标记后清除 | 简单 | 有碎片 |
| 标记-整理 | 标记后整理 | 无碎片 | 移动成本 |
| 复制算法 | 复制存活对象 | 高效 | 空间浪费 |
| 分代收集 | 按分代选算法 | 综合 | 复杂 |

**分代收集**：
- 新生代：复制算法（存活率低）
- 老年代：标记-整理（存活率高）

---

## 四、MySQL 高频题

### Q11: 索引为什么用 B+ 树？

**核心概念**：

MySQL 使用 B+ 树作为索引结构。

**B+ 树特点**：

```
                    B+ 树结构
                    
                    ┌───────┐
                    │  20   │
                    └───┬───┘
                ┌────────┴────────┐
                ▼                 ▼
            ┌───────┐         ┌───────┐
            │10  20 │         │30  40 │
            └───────┘         └───────┘
                │                 │
        ┌───────┼───────┐    ┌───────┼───────┐
        ▼       ▼       ▼    ▼       ▼       ▼
    [data1] [data2] [data3] [data4] [data5] [data6]
        │       │       │       │       │       │
        └───────┴───────┴───────┴───────┴───────┘
                     叶子节点链表
```

**为什么用 B+ 树**：

| 特点 | 好处 |
|------|------|
| 树高度低 | 减少 IO 次数（3-4 层可存千万数据） |
| 叶子节点链表 | 范围查询高效 |
| 非叶子节点只存键值 | 单页存更多索引项 |

---

### Q12: 索引设计原则？

**设计原则**：

1. **选择区分度高的列**
   ```sql
   -- 区分度 = 不重复值数 / 总行数
   SELECT COUNT(DISTINCT name) / COUNT(*) FROM user;
   -- 越接近 1 越好
   ```

2. **遵循最左前缀原则**
   ```sql
   -- 联合索引 (a, b, c)
   WHERE a = 1                    -- 走索引
   WHERE a = 1 AND b = 2          -- 走索引
   WHERE b = 2                    -- 不走索引
   ```

3. **避免索引失效**
   ```sql
   -- LIKE 以 % 开头
   WHERE name LIKE '%abc';        -- 不走索引
   
   -- 对索引列做运算
   WHERE YEAR(create_time) = 2024; -- 不走索引
   
   -- 类型隐式转换
   WHERE phone = 13800000000;     -- phone 是 varchar，不走索引
   ```

4. **控制索引数量**：单表 5 个以内

---

### Q13: 事务隔离级别？

**核心概念**：

事务隔离级别解决并发事务的问题。

**隔离级别对比**：

| 隔离级别 | 脏读 | 不可重复读 | 幻读 |
|---------|------|-----------|------|
| READ UNCOMMITTED | ✅ | ✅ | ✅ |
| READ COMMITTED | ❌ | ✅ | ✅ |
| REPEATABLE READ | ❌ | ❌ | ✅ |
| SERIALIZABLE | ❌ | ❌ | ❌ |

**MySQL 默认 RR**，通过 MVCC + 间隙锁解决幻读。

---

## 五、操作系统高频题

### Q14: 用户态和核心态？

**核心概念**：

操作系统分为用户态和核心态，限制程序的权限。

**区别**：

| 维度 | 用户态 | 核心态 |
|------|--------|--------|
| 权限 | 受限 | 完全 |
| 可访问内存 | 用户空间 | 全部 |
| 可执行指令 | 非特权指令 | 所有指令 |

**切换条件**：
1. 系统调用
2. 异常
3. 外设中断

**为什么要切换？**
- 安全性：防止用户程序直接操作硬件
- 稳定性：隔离用户程序和内核
- 权限管理：不同级别程序有不同权限

---

## 六、系统设计

### Q15: 如何实现一个策略模式？

**核心概念**：

策略模式定义一系列算法，把它们封装起来，并使它们可以相互替换。

**代码示例**：

```java
// 策略接口
public interface PaymentStrategy {
    void pay(int amount);
}

// 具体策略
public class AlipayStrategy implements PaymentStrategy {
    @Override
    public void pay(int amount) {
        System.out.println("支付宝支付: " + amount);
    }
}

public class WechatPayStrategy implements PaymentStrategy {
    @Override
    public void pay(int amount) {
        System.out.println("微信支付: " + amount);
    }
}

// 上下文
public class PaymentContext {
    private PaymentStrategy strategy;
    
    public void setStrategy(PaymentStrategy strategy) {
        this.strategy = strategy;
    }
    
    public void pay(int amount) {
        strategy.pay(amount);
    }
}

// 使用
PaymentContext context = new PaymentContext();
context.setStrategy(new AlipayStrategy());
context.pay(100);
```

**应用场景**：
- 支付方式选择
- 排序算法选择
- 压缩算法选择

---

## 七、算法题

百度常考算法，难度中等：

### 1. 反转链表

```java
public ListNode reverseList(ListNode head) {
    ListNode prev = null;
    ListNode curr = head;
    while (curr != null) {
        ListNode next = curr.next;
        curr.next = prev;
        prev = curr;
        curr = next;
    }
    return prev;
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

1. **引导式回答**：百度喜欢引导式提问，回答时可以主动延伸
2. **基础要扎实**：八股文要熟练，底层原理要懂
3. **不懂就说不懂**：百度面试官比较实在，不会可以问
4. **准备好反问**：展示学习热情

---

[返回目录](../README.md)