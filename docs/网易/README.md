# 网易 面试题

## 面试风格

**特点**：注重分布式理解，关注多线程和项目经验

**轮次**：通常 2-3 轮技术面 + 1 轮 HR

**重点**：分布式系统、多线程、Spring 全家桶、MySQL、设计模式

**面试官画像**：喜欢问分布式项目经验，关注对分布式的理解深度

---

## 知识点索引

- [Java基础](Java基础.md)
- [并发编程](并发编程.md)
- [JVM](JVM.md)
- [数据库](数据库.md)
- [分布式](分布式.md)
- [真题收录](真题收录.md)


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
