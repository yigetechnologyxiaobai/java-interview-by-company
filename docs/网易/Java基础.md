# 网易 - Java基础

> 本文档整理自 网易 面经真题，按知识点归类

## 目录

- [一、Java 基础高频题](#一、Java-基础高频题)

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


