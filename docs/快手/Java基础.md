# 快手 - Java基础

> 本文档整理自 快手 面经真题，按知识点归类

## 目录

- [一、Java 基础高频题](#一、Java-基础高频题)
- [五、网络编程高频题](#五、网络编程高频题)

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


