# 百度 - Java基础

> 本文档整理自 百度 面经真题，按知识点归类

## 目录

- [一、Java 基础高频题](#一、Java-基础高频题)
- [五、操作系统高频题](#五、操作系统高频题)

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


