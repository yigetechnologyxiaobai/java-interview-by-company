# 京东 - Java基础

> 本文档整理自 京东 面经真题，按知识点归类

## 目录

- [一、Java 基础高频题](#一、Java-基础高频题)

---

## 一、Java 基础高频题


### Q1: String、StringBuilder、StringBuffer 区别？

**参考答案**：

| 类 | 可变性 | 线程安全 | 性能 |
|----|--------|---------|------|
| String | 不可变 | 安全 | 最差 |
| StringBuffer | 可变 | 安全（synchronized） | 中 |
| StringBuilder | 可变 | 不安全 | 最好 |

**使用场景**：
- String：字符串常量，少量拼接
- StringBuilder：单线程大量拼接
- StringBuffer：多线程大量拼接

**追问**：
- String 为什么不可变？（final char[] value）
- 字符串拼接底层实现？

### Q2: ArrayList 和 LinkedList 区别？

**参考答案**：

| 特性 | ArrayList | LinkedList |
|------|-----------|------------|
| 底层结构 | 数组 | 双向链表 |
| 随机访问 | O(1) | O(n) |
| 插入删除 | O(n) | O(1) |
| 内存占用 | 连续空间 | 节点指针 |

**使用场景**：
- ArrayList：查询多、增删少
- LinkedList：增删多、查询少

**追问**：
- ArrayList 扩容机制？
- LinkedList 为什么很少用？

### Q3: HashMap 底层原理？

**参考答案**：

**JDK 1.8 结构**：数组 + 链表 + 红黑树

**put 流程**：
1. 计算 hash：`(h = key.hashCode()) ^ (h >>> 16)`
2. 定位桶：`hash & (n - 1)`
3. 桶为空 → 直接插入
4. 桶不为空 → 遍历链表/红黑树
5. 相同 key → 覆盖 value
6. 链表长度 >= 8 且容量 >= 64 → 红黑树

**扩容**：
- 触发：size > capacity * loadFactor
- 容量翻倍
- 元素重新分配

**追问**：
- 为什么负载因子是 0.75？
- JDK 1.7 和 1.8 区别？
- 为什么线程不安全？

### Q4: ConcurrentHashMap 如何保证线程安全？

**参考答案**：

**JDK 1.7**：Segment + ReentrantLock（分段锁）

**JDK 1.8**：CAS + synchronized

**put 流程**：
1. 计算 hash，定位桶
2. 桶为空 → CAS 插入
3. 桶不为空 → synchronized 锁头节点
4. 插入链表或红黑树

**为什么 JDK 1.8 放弃分段锁**：
1. 每个 Segment 占用内存
2. 并发度固定
3. synchronized 优化后性能提升

**追问**：
- ConcurrentHashMap 和 Hashtable 区别？
- size() 如何实现？

### Q5: Java 异常体系？

**参考答案**：

```
Throwable
├── Error（错误）
│   ├── VirtualMachineError
│   ├── OutOfMemoryError
│   └── StackOverflowError
└── Exception（异常）
    ├── IOException（检查异常）
    ├── SQLException（检查异常）
    └── RuntimeException（运行时异常）
        ├── NullPointerException
        ├── ArrayIndexOutOfBoundsException
        └── ClassCastException
```

**Error vs Exception**：
- Error：程序无法处理的错误
- Exception：程序可以处理的异常

**检查异常 vs 运行时异常**：
- 检查异常：编译时检查，必须处理
- 运行时异常：编译时不检查

**追问**：
- try-catch-finally 执行顺序？
- finally 中的 return？

---


