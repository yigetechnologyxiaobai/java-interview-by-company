# 网易 Java 面试题

## 面试风格

**特点**：注重分布式理解，关注多线程和项目经验

**轮次**：通常 2-3 轮技术面 + 1 轮 HR

**重点**：分布式系统、多线程、Spring 全家桶、MySQL、设计模式

**面试官画像**：喜欢问分布式项目经验，关注对分布式的理解深度

---

## 一、Java 基础高频题

### Q1: 运行一个只有 main 方法的类，JVM 中会发生什么？

**核心概念**：

理解 JVM 启动和类加载过程。

**详细流程**：

```
┌─────────────────────────────────────────────────────────────────┐
│                    JVM 启动和执行流程                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  1. JVM 启动                                                    │
│     └─ java 命令启动 JVM                                        │
│     └─ 创建 JVM 实例                                            │
│     └─ 初始化运行时数据区                                       │
│                                                                 │
│  2. 类加载                                                       │
│     └─ Bootstrap ClassLoader 加载核心类                         │
│     └─ Extension ClassLoader 加载扩展类                         │
│     └─ Application ClassLoader 加载应用类                       │
│     └─ 加载 → 验证 → 准备 → 解析 → 初始化                       │
│                                                                 │
│  3. 执行 main 方法                                               │
│     └─ 创建主线程                                               │
│     └─ 创建虚拟机栈                                             │
│     └─ 创建 main 方法的栈帧                                     │
│     └─ 执行字节码                                               │
│                                                                 │
│  4. 程序结束                                                     │
│     └─ main 方法返回                                            │
│     └─ 销毁 JVM 实例                                            │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

**内存变化**：

```java
public class HelloWorld {
    public static void main(String[] args) {
        System.out.println("Hello World");
    }
}

// JVM 内存变化：
// 1. 堆：HelloWorld 类对象、"Hello World" 字符串对象
// 2. 方法区：HelloWorld 类信息、main 方法信息
// 3. 虚拟机栈：main 方法的栈帧
// 4. 程序计数器：记录当前执行的字节码行号
```

---

### Q2: "helloworld" 字符串存储在哪里？

**核心概念**：

字符串在 JVM 中的存储位置取决于创建方式。

**存储位置**：

```
┌─────────────────────────────────────────────────────────────────┐
│                    字符串存储位置                                │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  方式一：字面量                                                  │
│  String s = "helloworld";                                       │
│  └─ 存储位置：字符串常量池（运行时常量池）                       │
│  └─ 编译期确定                                                  │
│                                                                 │
│  方式二：new                                                    │
│  String s = new String("helloworld");                          │
│  └─ 堆中创建对象                                                │
│  └─ 常量池中也有"helloworld"（如果之前没有）                    │
│                                                                 │
│  方式三：intern()                                               │
│  String s = "hello" + "world";                                 │
│  s.intern();                                                    │
│  └─ JDK 1.6：复制到常量池                                       │
│  └─ JDK 1.7+：引用指向堆中的对象                                │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

**字符串常量池位置变化**：

| JDK 版本 | 位置 |
|---------|------|
| JDK 6 | 永久代 |
| JDK 7 | 堆 |
| JDK 8+ | 堆 |

**示例**：

```java
String s1 = "helloworld";
String s2 = "helloworld";
String s3 = new String("helloworld");

System.out.println(s1 == s2);  // true，同一对象
System.out.println(s1 == s3);  // false，不同对象
System.out.println(s1 == s3.intern());  // true，intern() 返回常量池引用
```

---

### Q3: 面向对象三大特性？

**核心概念**：

面向对象三大特性：封装、继承、多态。

**1. 封装**：

```java
// 封装：隐藏实现细节，暴露公共接口
public class User {
    private String name;  // 私有属性
    private int age;
    
    // 公共 getter/setter
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

**好处**：
- 隐藏实现细节
- 数据校验
- 提高可维护性

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

**好处**：
- 代码复用
- 扩展功能

**3. 多态**：

```java
// 多态：同一方法，不同实现
public abstract class Shape {
    public abstract double area();
}

public class Circle extends Shape {
    private double radius;
    
    @Override
    public double area() {
        return Math.PI * radius * radius;
    }
}

public class Rectangle extends Shape {
    private double width, height;
    
    @Override
    public double area() {
        return width * height;
    }
}

// 使用
Shape shape = new Circle(5);
System.out.println(shape.area());  // 调用 Circle 的 area()
```

**多态条件**：
1. 继承
2. 重写
3. 父类引用指向子类对象

---

### Q4: 接口与抽象类的区别？

**核心概念**：

接口和抽象类都是抽象机制，但有本质区别。

**对比表格**：

| 维度 | 抽象类 | 接口 |
|------|--------|------|
| 关键字 | abstract class | interface |
| 继承 | 单继承 | 多实现 |
| 方法 | 可以有具体方法 | JDK 8 前只能抽象方法 |
| 变量 | 可以有普通变量 | 只能是 public static final |
| 构造器 | 有 | 无 |
| 设计目的 | 代码复用 | 定义规范 |

**代码示例**：

```java
// 抽象类
public abstract class Animal {
    protected String name;
    
    public Animal(String name) {
        this.name = name;
    }
    
    public abstract void makeSound();
    
    public void sleep() {
        System.out.println(name + " is sleeping");
    }
}

// 接口
public interface Flyable {
    void fly();
    
    // JDK 8 默认方法
    default void glide() {
        System.out.println("gliding");
    }
    
    // JDK 8 静态方法
    static void check() {
        System.out.println("checking");
    }
}
```

**使用场景**：
- 抽象类：相关类之间的代码共享（is-a 关系）
- 接口：定义行为规范（can-do 关系）

---

## 二、多线程与并发高频题

### Q5: Java 实现多线程有哪几种方式？

**核心概念**：

Java 提供多种创建线程的方式。

**四种方式**：

```java
// 1. 继承 Thread 类
public class MyThread extends Thread {
    @Override
    public void run() {
        System.out.println("Thread running");
    }
}
new MyThread().start();

// 2. 实现 Runnable 接口
public class MyRunnable implements Runnable {
    @Override
    public void run() {
        System.out.println("Runnable running");
    }
}
new Thread(new MyRunnable()).start();

// 3. 实现 Callable 接口（有返回值）
public class MyCallable implements Callable<String> {
    @Override
    public String call() throws Exception {
        return "Callable result";
    }
}
FutureTask<String> futureTask = new FutureTask<>(new MyCallable());
new Thread(futureTask).start();
String result = futureTask.get();

// 4. 线程池
ExecutorService executor = Executors.newFixedThreadPool(10);
executor.submit(() -> System.out.println("ThreadPool running"));
executor.shutdown();
```

**对比**：

| 方式 | 返回值 | 推荐 |
|------|--------|------|
| 继承 Thread | 无 | 不推荐（单继承限制） |
| 实现 Runnable | 无 | 推荐 |
| 实现 Callable | 有 | 需要返回值时使用 |
| 线程池 | 可选 | 推荐（生产环境） |

---

### Q6: Callable 和 Future 的了解？

**核心概念**：

Callable 可以返回结果，Future 用于获取结果。

**Callable vs Runnable**：

| 维度 | Runnable | Callable |
|------|----------|----------|
| 方法 | void run() | V call() throws Exception |
| 返回值 | 无 | 有 |
| 异常 | 不能抛出 | 可以抛出 |

**Future 方法**：

```java
Future<String> future = executor.submit(callable);

// 获取结果（阻塞）
String result = future.get();

// 超时获取
String result = future.get(5, TimeUnit.SECONDS);

// 取消任务
future.cancel(true);

// 判断是否完成
boolean done = future.isDone();

// 判断是否取消
boolean cancelled = future.isCancelled();
```

**CompletableFuture**（JDK 8）：

```java
// 异步执行
CompletableFuture<String> future = CompletableFuture.supplyAsync(() -> {
    return "result";
});

// 链式调用
CompletableFuture<String> result = future
    .thenApply(s -> s + " processed")
    .thenCompose(s -> CompletableFuture.supplyAsync(() -> s + " more"));

// 组合多个 Future
CompletableFuture<String> future1 = CompletableFuture.supplyAsync(() -> "A");
CompletableFuture<String> future2 = CompletableFuture.supplyAsync(() -> "B");
CompletableFuture<String> combined = future1.thenCombine(future2, (a, b) -> a + b);
```

---

### Q7: 如何确保线程执行顺序？

**核心概念**：

控制线程执行顺序有多种方式。

**方式一：join()**

```java
Thread t1 = new Thread(() -> System.out.println("T1"));
Thread t2 = new Thread(() -> {
    try {
        t1.join();  // 等待 t1 完成
    } catch (InterruptedException e) {}
    System.out.println("T2");
});
Thread t3 = new Thread(() -> {
    try {
        t2.join();  // 等待 t2 完成
    } catch (InterruptedException e) {}
    System.out.println("T3");
});

t3.start();
t2.start();
t1.start();
// 输出：T1 → T2 → T3
```

**方式二：CountDownLatch**

```java
CountDownLatch latch1 = new CountDownLatch(1);
CountDownLatch latch2 = new CountDownLatch(1);

Thread t1 = new Thread(() -> {
    System.out.println("T1");
    latch1.countDown();
});

Thread t2 = new Thread(() -> {
    try {
        latch1.await();
    } catch (InterruptedException e) {}
    System.out.println("T2");
    latch2.countDown();
});

Thread t3 = new Thread(() -> {
    try {
        latch2.await();
    } catch (InterruptedException e) {}
    System.out.println("T3");
});
```

**方式三：线程池 + Future**

```java
ExecutorService executor = Executors.newSingleThreadExecutor();
Future<?> f1 = executor.submit(() -> System.out.println("T1"));
f1.get();  // 等待完成
Future<?> f2 = executor.submit(() -> System.out.println("T2"));
f2.get();
Future<?> f3 = executor.submit(() -> System.out.println("T3"));
```

---

### Q8: wait 和 sleep 的区别？

**核心概念**：

wait 和 sleep 都可以让线程等待，但有本质区别。

**对比**：

| 维度 | wait() | sleep() |
|------|--------|---------|
| 所属类 | Object | Thread |
| 锁 | 释放锁 | 不释放锁 |
| 唤醒 | notify/notifyAll | 超时自动唤醒 |
| 使用位置 | 同步代码块 | 任意位置 |

**代码示例**：

```java
// wait() 必须在同步代码块中
synchronized (lock) {
    lock.wait();  // 释放锁，等待
}

// sleep() 可以在任意位置
Thread.sleep(1000);  // 不释放锁
```

**面试加分点**：
> 为什么 wait() 要在同步代码块中？
> - wait() 需要先获取对象锁
> - wait() 会释放锁，需要在同步块中才能获取锁

---

### Q9: 如何实现一个阻塞队列？

**核心概念**：

阻塞队列是一种支持阻塞操作的队列。

**实现**：

```java
public class MyBlockingQueue<T> {
    private final Queue<T> queue;
    private final int capacity;
    
    public MyBlockingQueue(int capacity) {
        this.queue = new LinkedList<>();
        this.capacity = capacity;
    }
    
    // 生产者：队满时阻塞
    public synchronized void put(T item) throws InterruptedException {
        while (queue.size() == capacity) {
            wait();  // 队满等待
        }
        queue.offer(item);
        notifyAll();  // 唤醒消费者
    }
    
    // 消费者：队空时阻塞
    public synchronized T take() throws InterruptedException {
        while (queue.isEmpty()) {
            wait();  // 队空等待
        }
        T item = queue.poll();
        notifyAll();  // 唤醒生产者
        return item;
    }
}
```

**使用场景**：
- 生产者-消费者模型
- 线程池任务队列
- 消息中间件

---

## 三、JVM 高频题

### Q10: 垃圾回收机制？

**核心概念**：

JVM 自动回收不再使用的对象，释放内存。

**判断对象存活**：

```
可达性分析：
- 从 GC Roots 开始遍历对象图
- 不可达的对象即为垃圾

GC Roots：
1. 虚拟机栈中引用的对象
2. 方法区中类静态属性引用的对象
3. 方法区中常量引用的对象
4. 本地方法栈中 JNI 引用的对象
```

**垃圾收集算法**：

| 算法 | 原理 | 适用场景 |
|------|------|---------|
| 标记-清除 | 标记后清除 | 老年代 |
| 标记-整理 | 标记后整理 | 老年代 |
| 复制算法 | 复制存活对象 | 新生代 |
| 分代收集 | 按分代选算法 | 综合 |

---

## 四、MySQL 高频题

### Q11: 索引设计原则？

**设计原则**：

```sql
-- 用户表
CREATE TABLE user (
    id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50) NOT NULL,
    gender TINYINT,
    phone VARCHAR(20),
    email VARCHAR(100)
);

-- 索引设计
-- 1. 主键索引：id
-- 2. 唯一索引：username（用户名唯一）
ALTER TABLE user ADD UNIQUE INDEX idx_username (username);

-- 3. 普通索引：phone（根据手机号查询）
ALTER TABLE user ADD INDEX idx_phone (phone);

-- 4. 联合索引：（gender, phone）如果经常按性别+手机查询
ALTER TABLE user ADD INDEX idx_gender_phone (gender, phone);
```

**为什么不建议在性别上建索引？**
- 区分度低（只有男/女）
- 选择性差，索引效果不明显

**如果用户名需要唯一，怎么建索引？**
```sql
ALTER TABLE user ADD UNIQUE INDEX idx_username (username);
```

---

## 五、Spring 高频题

### Q12: Spring、Spring Boot、Spring MVC 的区别？

**核心概念**：

Spring 生态由多个项目组成，各司其职。

**对比**：

| 项目 | 定位 | 核心功能 |
|------|------|---------|
| Spring | 基础框架 | IoC、AOP |
| Spring MVC | Web 框架 | MVC 模式、DispatcherServlet |
| Spring Boot | 快速开发 | 自动配置、起步依赖 |

**Spring 核心模块**：

```
┌─────────────────────────────────────────────────────────────────┐
│                     Spring 核心模块                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  IoC 容器                                                        │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  BeanFactory：基础容器                                  │   │
│  │  ApplicationContext：增强容器                           │   │
│  │  Bean 生命周期：实例化 → 属性赋值 → 初始化 → 销毁        │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│  AOP 框架                                                        │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  JDK 动态代理：接口                                     │   │
│  │  CGLIB：类                                              │   │
│  │  应用：事务、日志、权限                                  │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 六、分布式系统

### Q13: 如何理解分布式？

**核心概念**：

分布式系统是多台计算机协同工作，对外表现为一个系统。

**特点**：

```
┌─────────────────────────────────────────────────────────────────┐
│                      分布式系统特点                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  1. 分布性：组件分布在网络不同计算机上                          │
│                                                                 │
│  2. 并发性：多个节点同时处理请求                                │
│                                                                 │
│  3. 缺乏全局时钟：各节点时钟可能不同步                          │
│                                                                 │
│  4. 故障独立性：部分故障不影响整体                              │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

**为什么要做分布式？**
1. 高并发：单机性能瓶颈
2. 高可用：避免单点故障
3. 可扩展：水平扩展

**常见问题**：
1. 网络通信
2. 数据一致性
3. 分布式事务
4. 服务治理

---

## 七、设计模式

### Q14: Spring 中的设计模式？

**常见设计模式**：

| 模式 | Spring 应用 |
|------|-------------|
| 工厂模式 | BeanFactory、ApplicationContext |
| 单例模式 | Bean 默认单例 |
| 代理模式 | AOP |
| 模板方法 | JdbcTemplate、RedisTemplate |
| 策略模式 | Resource 加载策略 |
| 观察者模式 | ApplicationEvent |
| 适配器模式 | HandlerAdapter |
| 装饰器模式 | BeanWrapper |

**示例**：

```java
// 工厂模式
BeanFactory factory = new ClassPathXmlApplicationContext("beans.xml");
User user = (User) factory.getBean("user");

// 单例模式（Spring Bean 默认单例）
@Service
@Scope("singleton")
public class UserService {}

// 代理模式（AOP）
@Aspect
@Component
public class LoggingAspect {
    @Around("execution(* com.example.service.*.*(..))")
    public Object log(ProceedingJoinPoint pjp) throws Throwable {
        // 前置通知
        Object result = pjp.proceed();
        // 后置通知
        return result;
    }
}

// 模板方法
jdbcTemplate.query("SELECT * FROM user", (rs, rowNum) -> {
    return new User(rs.getLong("id"), rs.getString("name"));
});
```

---

## 八、面试技巧

1. **分布式要懂**：网易喜欢问分布式相关，要理解分布式概念
2. **多线程要精**：线程池、锁、协作机制都要熟悉
3. **项目要能讲**：项目背景、技术选型要能说清楚
4. **框架要了解**：Spring、MyBatis、Kafka、Netty
5. **设计模式**：23 种设计模式，重点掌握 Spring 中的应用

---

[返回目录](../README.md)