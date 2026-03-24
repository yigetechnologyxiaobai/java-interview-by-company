# 腾讯 Java 面试题

## 面试风格

**特点**：注重基础扎实，算法能力，对细节追问

**轮次**：通常 2-3 轮技术面 + 1 轮 HR

**重点**：算法、网络、操作系统、Java 基础

**面试官画像**：喜欢问"底层怎么实现的"，算法必考

---

## 一、算法高频题

腾讯非常看重算法，难度 LeetCode 中等偏上

### 1. 链表专题

**反转链表**

```java
// 迭代法
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

// 递归法
public ListNode reverseList(ListNode head) {
    if (head == null || head.next == null) {
        return head;
    }
    ListNode newHead = reverseList(head.next);
    head.next.next = head;
    head.next = null;
    return newHead;
}
```

**时间复杂度**：O(n)
**空间复杂度**：迭代 O(1)，递归 O(n)

**合并 K 个有序链表**

```java
// 优先队列法
public ListNode mergeKLists(ListNode[] lists) {
    if (lists == null || lists.length == 0) return null;
    
    PriorityQueue<ListNode> pq = new PriorityQueue<>((a, b) -> a.val - b.val);
    for (ListNode node : lists) {
        if (node != null) pq.offer(node);
    }
    
    ListNode dummy = new ListNode(0);
    ListNode curr = dummy;
    
    while (!pq.isEmpty()) {
        ListNode node = pq.poll();
        curr.next = node;
        curr = curr.next;
        if (node.next != null) {
            pq.offer(node.next);
        }
    }
    
    return dummy.next;
}

// 分治法
public ListNode mergeKLists(ListNode[] lists) {
    return merge(lists, 0, lists.length - 1);
}

private ListNode merge(ListNode[] lists, int left, int right) {
    if (left == right) return lists[left];
    if (left > right) return null;
    
    int mid = (left + right) / 2;
    return mergeTwoLists(merge(lists, left, mid), merge(lists, mid + 1, right));
}

private ListNode mergeTwoLists(ListNode l1, ListNode l2) {
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

**LRU 缓存**

```java
class LRUCache {
    private int capacity;
    private Map<Integer, Node> cache;
    private Node head, tail;
    
    class Node {
        int key, value;
        Node prev, next;
        Node(int key, int value) {
            this.key = key;
            this.value = value;
        }
    }
    
    public LRUCache(int capacity) {
        this.capacity = capacity;
        cache = new HashMap<>();
        head = new Node(0, 0);
        tail = new Node(0, 0);
        head.next = tail;
        tail.prev = head;
    }
    
    public int get(int key) {
        if (!cache.containsKey(key)) return -1;
        Node node = cache.get(key);
        removeNode(node);
        addToHead(node);
        return node.value;
    }
    
    public void put(int key, int value) {
        if (cache.containsKey(key)) {
            Node node = cache.get(key);
            node.value = value;
            removeNode(node);
            addToHead(node);
        } else {
            Node node = new Node(key, value);
            cache.put(key, node);
            addToHead(node);
            if (cache.size() > capacity) {
                Node removed = tail.prev;
                removeNode(removed);
                cache.remove(removed.key);
            }
        }
    }
    
    private void removeNode(Node node) {
        node.prev.next = node.next;
        node.next.prev = node.prev;
    }
    
    private void addToHead(Node node) {
        node.next = head.next;
        node.prev = head;
        head.next.prev = node;
        head.next = node;
    }
}

// 使用 LinkedHashMap（面试加分）
class LRUCache extends LinkedHashMap<Integer, Integer> {
    private int capacity;
    
    public LRUCache(int capacity) {
        super(capacity, 0.75f, true);
        this.capacity = capacity;
    }
    
    public int get(int key) {
        return super.getOrDefault(key, -1);
    }
    
    public void put(int key, int value) {
        super.put(key, value);
    }
    
    @Override
    protected boolean removeEldestEntry(Map.Entry<Integer, Integer> eldest) {
        return size() > capacity;
    }
}
```

### 2. 树专题

**二叉树层序遍历**

```java
public List<List<Integer>> levelOrder(TreeNode root) {
    List<List<Integer>> result = new ArrayList<>();
    if (root == null) return result;
    
    Queue<TreeNode> queue = new LinkedList<>();
    queue.offer(root);
    
    while (!queue.isEmpty()) {
        int size = queue.size();
        List<Integer> level = new ArrayList<>();
        for (int i = 0; i < size; i++) {
            TreeNode node = queue.poll();
            level.add(node.val);
            if (node.left != null) queue.offer(node.left);
            if (node.right != null) queue.offer(node.right);
        }
        result.add(level);
    }
    return result;
}
```

**最近公共祖先**

```java
public TreeNode lowestCommonAncestor(TreeNode root, TreeNode p, TreeNode q) {
    if (root == null || root == p || root == q) return root;
    
    TreeNode left = lowestCommonAncestor(root.left, p, q);
    TreeNode right = lowestCommonAncestor(root.right, p, q);
    
    if (left != null && right != null) return root;
    return left != null ? left : right;
}
```

### 3. 动态规划专题

**最长递增子序列**

```java
// O(n²) 解法
public int lengthOfLIS(int[] nums) {
    int n = nums.length;
    int[] dp = new int[n];
    Arrays.fill(dp, 1);
    int max = 1;
    
    for (int i = 1; i < n; i++) {
        for (int j = 0; j < i; j++) {
            if (nums[i] > nums[j]) {
                dp[i] = Math.max(dp[i], dp[j] + 1);
            }
        }
        max = Math.max(max, dp[i]);
    }
    return max;
}

// O(n log n) 解法（面试加分）
public int lengthOfLIS(int[] nums) {
    int n = nums.length;
    int[] tails = new int[n];
    int size = 0;
    
    for (int num : nums) {
        int left = 0, right = size;
        while (left < right) {
            int mid = (left + right) / 2;
            if (tails[mid] < num) {
                left = mid + 1;
            } else {
                right = mid;
            }
        }
        tails[left] = num;
        if (left == size) size++;
    }
    return size;
}
```

### 4. 滑动窗口

**最长无重复子串**

```java
public int lengthOfLongestSubstring(String s) {
    Map<Character, Integer> map = new HashMap<>();
    int max = 0, left = 0;
    
    for (int right = 0; right < s.length(); right++) {
        char c = s.charAt(right);
        if (map.containsKey(c)) {
            left = Math.max(left, map.get(c) + 1);
        }
        map.put(c, right);
        max = Math.max(max, right - left + 1);
    }
    return max;
}
```

---

## 二、计算机网络高频题

### Q1: TCP 三次握手？

**核心概念**：

TCP 建立连接需要三次握手，确保双方都有发送和接收能力。

**握手流程**：

```
┌─────────────────────────────────────────────────────────────────┐
│                       TCP 三次握手                               │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  客户端                    服务端                               │
│     │                        │                                 │
│     │───SYN=1, seq=x────────►│  第一次握手                     │
│     │    (请求连接)          │  客户端 → SYN_SENT              │
│     │                        │                                 │
│     │◄──SYN=1, ACK=1, ───────│  第二次握手                     │
│     │    ack=x+1, seq=y      │  服务端 → SYN_RCVD              │
│     │    (确认并同意)        │                                 │
│     │                        │                                 │
│     │───ACK=1, ack=y+1───────►│  第三次握手                     │
│     │    (确认)              │  双方 → ESTABLISHED             │
│     │                        │                                 │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

**为什么是三次？**

1. **防止历史连接**：两次握手无法区分是新的连接请求还是旧的延迟请求
2. **同步序列号**：双方都需要确认对方的初始序列号
3. **防止资源浪费**：避免服务端为无效连接分配资源

**示例场景**：

```
两次握手的问题：

客户端发送 SYN=1（延迟，未到达）
    │
    ▼
客户端超时，重发 SYN=1
    │
    ▼
服务端收到第二个 SYN，建立连接
    │
    ▼
连接关闭后，第一个延迟的 SYN 到达
    │
    ▼
两次握手：服务端立即建立连接，等待数据
    │         → 浪费资源！
    ▼
三次握手：服务端回复 SYN+ACK，客户端发现是历史请求
              → 发送 RST 拒绝，不建立连接
```

**追问延伸**：
- SYN 攻击是什么？
  - 攻击者发送大量伪造 IP 的 SYN 包
  - 服务端 SYN_RCVD 状态堆积，耗尽资源
  - 防御：SYN Cookie、缩短超时时间、增加半连接队列大小

```bash
# Linux 防御 SYN 攻击
net.ipv4.tcp_syncookies = 1      # 开启 SYN Cookie
net.ipv4.tcp_max_syn_backlog = 8192  # 增加半连接队列
net.ipv4.tcp_synack_retries = 2  # 减少 SYN+ACK 重试次数
```

---

### Q2: TCP 四次挥手？

**核心概念**：

TCP 关闭连接需要四次挥手，因为 TCP 是全双工通信。

**挥手流程**：

```
┌─────────────────────────────────────────────────────────────────┐
│                       TCP 四次挥手                               │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  主动关闭方                 被动关闭方                          │
│     │                        │                                 │
│     │───FIN=1, seq=u────────►│  第一次挥手                     │
│     │    (请求关闭)          │  主动方 → FIN_WAIT_1             │
│     │                        │                                 │
│     │◄──ACK=1, ack=u+1───────│  第二次挥手                     │
│     │    (确认)              │  主动方 → FIN_WAIT_2             │
│     │                        │  被动方 → CLOSE_WAIT             │
│     │                        │                                 │
│     │◄──FIN=1, ACK=1, ───────│  第三次挥手                     │
│     │    seq=w, ack=u+1      │  被动方 → LAST_ACK              │
│     │    (请求关闭)          │                                 │
│     │                        │                                 │
│     │───ACK=1, ack=w+1───────►│  第四次挥手                     │
│     │    (确认)              │  主动方 → TIME_WAIT (2MSL)      │
│     │                        │  被动方 → CLOSED                │
│     │                        │                                 │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

**为什么是四次？**

- TCP 是全双工，每个方向需要单独关闭
- 被动方收到 FIN 后，可能还有数据要发送
- 所以 ACK 和 FIN 分开发送（三次握手的 SYN+ACK 可以合并）

**TIME_WAIT 状态**：

```
持续 2MSL（Maximum Segment Lifetime）

作用：
1. 确保最后一个 ACK 到达被动方
   - 如果被动方没收到 ACK，会重发 FIN
   - TIME_WAIT 可以重发 ACK

2. 让旧连接的包消失
   - 防止旧连接的延迟包影响新连接

问题：
- TIME_WAIT 过多，占用端口资源
- 高并发短连接场景下尤其严重
```

**追问延伸**：
- TIME_WAIT 过多怎么办？

```bash
# Linux 优化
net.ipv4.tcp_tw_reuse = 1     # 允许复用 TIME_WAIT 状态的连接
net.ipv4.tcp_tw_recycle = 1   # 快速回收 TIME_WAIT（已废弃）
net.ipv4.tcp_max_tw_buckets = 5000  # TIME_WAIT 最大数量

# 应用层优化
# 1. 使用长连接
# 2. 主动关闭方让被动方先关闭（服务端设置）
```

---

### Q3: TCP 和 UDP 区别？

**核心概念**：

TCP 和 UDP 是传输层两大协议，设计目标不同。

**对比表格**：

| 维度 | TCP | UDP |
|------|-----|-----|
| 连接 | 面向连接 | 无连接 |
| 可靠性 | 可靠传输（确认、重传） | 不可靠 |
| 有序性 | 有序（序列号） | 无序 |
| 流量控制 | 有（滑动窗口） | 无 |
| 拥塞控制 | 有（慢启动、拥塞避免） | 无 |
| 传输效率 | 低（首部 20 字节） | 高（首部 8 字节） |
| 适用场景 | 文件传输、HTTP | 实时音视频、DNS |

**TCP 可靠传输机制**：

```
┌─────────────────────────────────────────────────────────────────┐
│                    TCP 可靠传输机制                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  1. 序列号（Sequence Number）                                   │
│     └─ 每个字节都有序号，保证有序                               │
│                                                                 │
│  2. 确认应答（ACK）                                              │
│     └─ 收到数据后发送 ACK 确认                                  │
│                                                                 │
│  3. 超时重传（RTO）                                              │
│     └─ 未收到 ACK 则重传                                        │
│     └─ RTO 动态计算（RTT 加权平均）                             │
│                                                                 │
│  4. 滑动窗口（Flow Control）                                     │
│     └─ 接收方告知发送方可接收的数据量                           │
│     └─ 防止发送方发送过快                                       │
│                                                                 │
│  5. 拥塞控制（Congestion Control）                               │
│     └─ 慢启动：指数增长                                         │
│     └─ 拥塞避免：线性增长                                       │
│     └─ 拥塞发生：门限减半，重新慢启动                           │
│     └─ 快速恢复：拥塞后快速恢复                                 │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

**适用场景**：

| 场景 | 选择 | 原因 |
|------|------|------|
| HTTP/HTTPS | TCP | 需要可靠 |
| 文件传输 | TCP | 不能丢数据 |
| 实时音视频 | UDP | 可容忍丢包，追求实时 |
| DNS 查询 | UDP | 快速，数据量小 |
| 游戏 | UDP | 低延迟优先 |

---

### Q4: HTTP 和 HTTPS 区别？

**核心概念**：

HTTPS = HTTP + SSL/TLS，提供加密传输。

**对比表格**：

| 维度 | HTTP | HTTPS |
|------|------|-------|
| 传输 | 明文 | SSL 加密 |
| 端口 | 80 | 443 |
| 证书 | 不需要 | 需要 CA 证书 |
| 性能 | 更快 | 略慢（SSL 握手） |
| 安全 | 不安全 | 安全 |

**HTTPS 握手过程**：

```
┌─────────────────────────────────────────────────────────────────┐
│                      HTTPS 握手过程                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  客户端                    服务端                               │
│     │                        │                                 │
│     │───ClientHello─────────►│  1. 支持的加密套件、随机数       │
│     │                        │                                 │
│     │◄──ServerHello──────────│  2. 选择加密套件、随机数         │
│     │◄──Certificate──────────│     证书                        │
│     │◄──ServerHelloDone──────│                                 │
│     │                        │                                 │
│     │───ClientKeyExchange───►│  3. 生成预主密钥，用公钥加密     │
│     │───ChangeCipherSpec────►│     切换加密                    │
│     │───Finished────────────►│     验证                        │
│     │                        │                                 │
│     │◄──ChangeCipherSpec─────│  4. 切换加密                    │
│     │◄──Finished─────────────│     验证                        │
│     │                        │                                 │
│     ══════════════════════════  加密通信开始                    │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

**加密方式**：

```
┌─────────────────────────────────────────────────────────────────┐
│                      加密方式对比                                │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  对称加密（AES、DES）                                            │
│     └─ 同一把密钥加密解密                                       │
│     └─ 速度快，适合大量数据                                     │
│     └─ 问题：密钥如何安全传输？                                 │
│                                                                 │
│  非对称加密（RSA、ECC）                                          │
│     └─ 公钥加密，私钥解密                                       │
│     └─ 安全，适合密钥交换                                       │
│     └─ 问题：速度慢                                             │
│                                                                 │
│  HTTPS 混合加密                                                 │
│     └─ 用非对称加密传输对称密钥                                 │
│     └─ 用对称加密传输实际数据                                   │
│     └─ 兼顾安全与性能                                           │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

**追问延伸**：
- 为什么 HTTPS 混合使用两种加密？
  - 非对称加密安全但慢，对称加密快但密钥传输不安全
  - 混合使用：用非对称传对称密钥，用对称传数据

---

### Q5: 输入 URL 到页面展示的过程？

**核心概念**：

这是一个综合性问题，涵盖网络、浏览器渲染等多方面。

**完整流程**：

```
┌─────────────────────────────────────────────────────────────────┐
│                    URL 到页面展示流程                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  1. URL 解析                                                    │
│     └─ 判断是搜索还是 URL                                       │
│     └─ 检查 HSTS 列表                                          │
│                                                                 │
│  2. DNS 解析                                                    │
│     ┌─────────────────────────────────────────────────────┐   │
│     │  浏览器缓存 → 系统缓存 → hosts 文件                  │   │
│     │      ↓                                             │   │
│     │  本地 DNS 服务器                                    │   │
│     │      ↓                                             │   │
│     │  根 DNS → 顶级 DNS → 权威 DNS                       │   │
│     └─────────────────────────────────────────────────────┘   │
│                                                                 │
│  3. TCP 连接                                                    │
│     └─ 三次握手                                                 │
│     └─ HTTPS 的 TLS 握手                                        │
│                                                                 │
│  4. HTTP 请求                                                   │
│     └─ 构造请求报文                                             │
│     └─ 添加请求头（Cookie、User-Agent）                        │
│                                                                 │
│  5. 服务器处理                                                   │
│     └─ Nginx 反向代理                                          │
│     └─ 应用服务器处理                                           │
│     └─ 数据库查询                                               │
│     └─ 返回响应                                                 │
│                                                                 │
│  6. 浏览器渲染                                                   │
│     ┌─────────────────────────────────────────────────────┐   │
│     │  HTML → DOM 树                                      │   │
│     │  CSS → CSSOM 树                                     │   │
│     │  DOM + CSSOM → 渲染树                               │   │
│     │  布局（Layout）→ 绘制（Paint）→ 合成                │   │
│     └─────────────────────────────────────────────────────┘   │
│                                                                 │
│  7. 加载完成                                                     │
│     └─ 触发 onload 事件                                         │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

**追问延伸**：
- DNS 解析过程？

```
查询 www.example.com 的 IP：

1. 浏览器缓存：有则返回
2. 系统缓存：有则返回
3. hosts 文件：有则返回
4. 本地 DNS 服务器：
   - 有缓存则返回
   - 无则递归查询：
     a. 根 DNS：返回 .com 的 DNS 地址
     b. .com DNS：返回 example.com 的 DNS 地址
     c. example.com DNS：返回 www.example.com 的 IP
```

- 浏览器渲染过程？
  - 解析 HTML → DOM 树
  - 解析 CSS → CSSOM 树
  - 合并 → 渲染树
  - 布局（计算位置和大小）
  - 绘制（像素填充）
  - 合成（多层合成）

---

## 三、操作系统高频题

### Q6: 进程和线程的区别？

**核心概念**：

进程是资源分配的基本单位，线程是 CPU 调度的基本单位。

**对比表格**：

| 维度 | 进程 | 线程 |
|------|------|------|
| 定义 | 资源分配基本单位 | CPU 调度基本单位 |
| 地址空间 | 独立 | 共享进程地址空间 |
| 创建开销 | 大（需要分配资源） | 小（共享进程资源） |
| 通信 | 复杂（IPC） | 简单（共享内存） |
| 切换开销 | 大 | 小 |
| 安全性 | 一个进程崩溃不影响其他 | 一个线程崩溃可能影响整个进程 |

**进程通信方式（IPC）**：

```
┌─────────────────────────────────────────────────────────────────┐
│                       进程通信方式                               │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  1. 管道（Pipe）                                                 │
│     └─ 匿名管道：父子进程                                       │
│     └─ 命名管道：无亲缘关系进程                                 │
│     └─ 单向，数据流形式                                         │
│                                                                 │
│  2. 消息队列（Message Queue）                                    │
│     └─ 存储在内核                                               │
│     └─ 有格式                                                   │
│     └─ 可以随机读取                                             │
│                                                                 │
│  3. 共享内存（Shared Memory）                                    │
│     └─ 最快的 IPC                                               │
│     └─ 直接读写内存                                             │
│     └─ 需要同步机制                                             │
│                                                                 │
│  4. 信号量（Semaphore）                                          │
│     └─ 进程同步                                                 │
│     └─ 计数器                                                   │
│     └─ 常与共享内存配合                                         │
│                                                                 │
│  5. Socket                                                       │
│     └─ 跨机器通信                                               │
│     └─ 网络通信                                                 │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

**线程同步方式**：

```java
// 1. synchronized
public synchronized void method() {}

// 2. Lock
Lock lock = new ReentrantLock();
lock.lock();
try {
    // 临界区
} finally {
    lock.unlock();
}

// 3. volatile（可见性）
private volatile boolean flag = true;

// 4. CAS（乐观锁）
AtomicInteger count = new AtomicInteger(0);
count.incrementAndGet();

// 5. ThreadLocal（线程隔离）
ThreadLocal<String> threadLocal = new ThreadLocal<>();
```

---

### Q7: 死锁条件？

**核心概念**：

死锁是两个或多个进程互相等待对方释放资源，导致都无法继续执行。

**四个必要条件**：

```
┌─────────────────────────────────────────────────────────────────┐
│                       死锁四个必要条件                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  1. 互斥条件（Mutual Exclusion）                                 │
│     └─ 资源只能被一个进程使用                                   │
│                                                                 │
│  2. 请求保持条件（Hold and Wait）                                │
│     └─ 持有资源同时请求其他资源                                 │
│                                                                 │
│  3. 不剥夺条件（No Preemption）                                  │
│     └─ 资源不能被强制抢占                                       │
│                                                                 │
│  4. 循环等待条件（Circular Wait）                                │
│     └─ 进程间形成循环等待关系                                   │
│                                                                 │
│  四个条件同时满足才会死锁                                        │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

**死锁示例**：

```java
public class DeadlockDemo {
    private static final Object lockA = new Object();
    private static final Object lockB = new Object();
    
    public static void main(String[] args) {
        new Thread(() -> {
            synchronized (lockA) {
                System.out.println("Thread 1: 持有 lockA");
                try { Thread.sleep(100); } catch (InterruptedException e) {}
                synchronized (lockB) {  // 等待 lockB
                    System.out.println("Thread 1: 持有 lockA 和 lockB");
                }
            }
        }).start();
        
        new Thread(() -> {
            synchronized (lockB) {
                System.out.println("Thread 2: 持有 lockB");
                try { Thread.sleep(100); } catch (InterruptedException e) {}
                synchronized (lockA) {  // 等待 lockA
                    System.out.println("Thread 2: 持有 lockA 和 lockB");
                }
            }
        }).start();
    }
}
```

**解决方法**：

```
┌─────────────────────────────────────────────────────────────────┐
│                       死锁解决方法                               │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  1. 预防（破坏四个条件之一）                                     │
│     └─ 互斥：无法破坏（资源特性）                               │
│     └─ 请求保持：一次性申请所有资源                             │
│     └─ 不剥夺：申请不到时释放已持有资源                         │
│     └─ 循环等待：按顺序申请资源                                 │
│                                                                 │
│  2. 避免（银行家算法）                                           │
│     └─ 分配前检查是否会导致死锁                                 │
│     └─ 安全则分配，否则等待                                     │
│                                                                 │
│  3. 检测和恢复                                                   │
│     └─ 定期检测死锁                                             │
│     └─ 发现死锁后剥夺资源或终止进程                             │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

### Q8: 进程调度算法？

**核心概念**：

进程调度决定哪个进程获得 CPU 使用权。

**常见算法**：

| 算法 | 说明 | 优点 | 缺点 |
|------|------|------|------|
| FCFS | 先来先服务 | 简单 | 护航效应 |
| SJF | 短作业优先 | 平均等待时间短 | 长作业饥饿 |
| RR | 时间片轮转 | 公平 | 上下文切换开销 |
| Priority | 优先级调度 | 重要任务优先 | 低优先级饥饿 |
| MLFQ | 多级反馈队列 | 综合 | 复杂 |

**多级反馈队列**：

```
┌─────────────────────────────────────────────────────────────────┐
│                    多级反馈队列调度                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Queue 1 (最高优先级，时间片最短)                               │
│  ┌───┬───┬───┬───┐                                             │
│  │P1 │P2 │P3 │...│                                             │
│  └───┴───┴───┴───┘                                             │
│         ↓ 用完时间片，降到下一队列                              │
│                                                                 │
│  Queue 2 (中等优先级，时间片中)                                 │
│  ┌───┬───┬───┬───┐                                             │
│  │P4 │P5 │P6 │...│                                             │
│  └───┴───┴───┴───┘                                             │
│         ↓                                                       │
│                                                                 │
│  Queue 3 (最低优先级，时间片最长)                               │
│  ┌───┬───┬───┬───┐                                             │
│  │P7 │P8 │P9 │...│                                             │
│  └───┴───┴───┴───┘                                             │
│                                                                 │
│  特点：                                                         │
│  - 短作业优先完成（在高层队列）                                 │
│  - 长作业不会饥饿（最终会在底层队列执行）                       │
│  - I/O 密集型优先（用完时间片少，留在高层）                     │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

### Q9: 内存管理方式？

**核心概念**：

内存管理包括分页、分段、段页式，以及虚拟内存。

**分页 vs 分段**：

| 维度 | 分页 | 分段 |
|------|------|------|
| 单位 | 固定大小页 | 逻辑段（变长） |
| 目的 | 内存利用率 | 逻辑完整性 |
| 碎片 | 内部碎片 | 外部碎片 |
| 共享 | 不方便 | 方便 |

**虚拟内存**：

```
┌─────────────────────────────────────────────────────────────────┐
│                       虚拟内存                                   │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  虚拟地址空间 >> 物理内存                                       │
│                                                                 │
│  虚拟地址 → 页表 → 物理地址                                     │
│                                                                 │
│  页面置换算法：                                                  │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  OPT:   置换最长时间不使用的（理论最优，无法实现）       │   │
│  │  FIFO:  置换最早进入的（简单，可能有 Belady 异常）       │   │
│  │  LRU:   置换最近最少使用的（常用，效果好）               │   │
│  │  Clock: 近似 LRU，用引用位                              │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│  优点：                                                         │
│  - 逻辑上扩充内存                                               │
│  - 程序可以使用比物理内存更大的地址空间                         │
│  - 内存保护                                                     │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 四、Java 基础高频题

### Q10: HashMap 源码分析？

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

**put 流程**：

```java
public V put(K key, V value) {
    // 1. 计算 hash
    int hash = hash(key);
    
    // 2. 定位桶
    int index = (n - 1) & hash;
    
    // 3. 桶为空 → 直接插入
    if (tab[index] == null) {
        tab[index] = new Node(hash, key, value, null);
    }
    // 4. 桶不为空 → 处理冲突
    else {
        Node<K,V> e; K k;
        // 4.1 相同 key → 覆盖
        if (p.hash == hash && (k = p.key) == key || key.equals(k)) {
            e = p;
        }
        // 4.2 红黑树
        else if (p instanceof TreeNode) {
            e = ((TreeNode<K,V>)p).putTreeVal(this, tab, hash, key, value);
        }
        // 4.3 链表
        else {
            for (int binCount = 0; ; ++binCount) {
                if ((e = p.next) == null) {
                    p.next = new Node(hash, key, value, null);
                    // 链表长度 >= 8 转红黑树
                    if (binCount >= TREEIFY_THRESHOLD - 1)
                        treeifyBin(tab, hash);
                    break;
                }
                if (e.hash == hash && (k = e.key) == key || key.equals(k))
                    break;
                p = e;
            }
        }
        // 5. 覆盖 value
        if (e != null) {
            V oldValue = e.value;
            e.value = value;
            return oldValue;
        }
    }
    
    // 6. 扩容
    if (++size > threshold)
        resize();
    
    return null;
}
```

**扩容机制**：

```
扩容条件：size > capacity * loadFactor

扩容过程：
1. 容量翻倍（2 的幂）
2. 创建新数组
3. 元素重新分配：
   - 原位置：hash & oldCap == 0
   - 原位置 + oldCap：hash & oldCap != 0

示例：
原容量 = 16，元素在位置 5
新容量 = 32
如果 hash 第 5 位为 0，仍在位置 5
如果 hash 第 5 位为 1，移动到位置 5 + 16 = 21
```

**面试加分点**：
> JDK 1.7 和 1.8 区别：

| 维度 | JDK 1.7 | JDK 1.8 |
|------|---------|---------|
| 结构 | 数组 + 链表 | 数组 + 链表 + 红黑树 |
| 插入方式 | 头插法 | 尾插法 |
| 扩容 | 重新计算位置 | 原位置或原位置+oldCap |
| hash 计算 | 9 次扰动 | 1 次扰动 |

> 为什么线程不安全？
> 1. JDK 1.7 头插法可能导致死循环
> 2. 并发 put 可能丢失数据
> 3. 扩容时数据丢失

---

### Q11: ConcurrentHashMap 如何保证线程安全？

**核心概念**：

ConcurrentHashMap 是线程安全的 HashMap。

**JDK 1.8 实现**：

```java
final V putVal(K key, V value, boolean onlyIfAbsent) {
    int hash = spread(key.hashCode());
    
    for (Node<K,V>[] tab = table;;) {
        Node<K,V> f; int n, i, fh;
        
        // 1. 桶为空 → CAS 插入
        if (tab == null || (n = tab.length) == 0)
            tab = initTable();
        else if ((f = tabAt(tab, i = (n - 1) & hash)) == null) {
            if (casTabAt(tab, i, null, new Node<K,V>(hash, key, value, null)))
                break;
        }
        // 2. 正在扩容 → 协助扩容
        else if ((fh = f.hash) == MOVED)
            tab = helpTransfer(tab, f);
        // 3. 桶不为空 → synchronized 锁头节点
        else {
            synchronized (f) {
                // 遍历链表或红黑树
                // ...
            }
        }
    }
    return null;
}
```

**对比**：

| 维度 | Hashtable | ConcurrentHashMap |
|------|-----------|-------------------|
| 锁粒度 | 整个表 | 单个桶 |
| 性能 | 低 | 高 |
| null 键/值 | 允许 | 不允许 |

---

### Q12: ThreadLocal 原理？

**核心概念**：

ThreadLocal 提供线程局部变量，每个线程独立。

**原理图**：

```
Thread
└── ThreadLocalMap
    └── Entry (WeakReference<ThreadLocal>)
        ├── key: ThreadLocal (弱引用)
        └── value: 值 (强引用)
```

**内存泄漏原因**：

1. key 是弱引用，GC 后变为 null
2. value 是强引用，仍被 Entry 引用
3. 线程不结束，value 无法回收

**解决**：使用后调用 remove()

```java
ThreadLocal<String> local = new ThreadLocal<>();
try {
    local.set("value");
    // 使用
} finally {
    local.remove();  // 必须清理
}
```

---

## 五、MySQL 高频题

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

**MVCC 原理**：

```
核心组件：
1. 隐藏字段：DB_TRX_ID、DB_ROLL_PTR
2. Undo Log：版本链
3. Read View：可见性判断

RC：每次 SELECT 生成新的 Read View
RR：事务第一次 SELECT 生成 Read View，后续复用
```

---

### Q14: 索引设计原则？

**设计原则**：

1. 选择区分度高的列
2. 遵循最左前缀原则
3. 避免索引失效
4. 控制索引数量（5 个以内）
5. 优先考虑覆盖索引

**索引失效场景**：

```sql
-- 1. LIKE 以 % 开头
WHERE name LIKE '%三';   -- 失效

-- 2. 对索引列做运算
WHERE YEAR(create_time) = 2024;  -- 失效

-- 3. 类型隐式转换
WHERE phone = 13800138000;  -- phone 是 varchar，失效

-- 4. 使用函数
WHERE LOWER(name) = 'zhangsan';  -- 失效

-- 5. 不等于
WHERE name != '张三';  -- 可能失效
```

---

## 六、Redis 高频题

### Q15: Redis 为什么快？

**核心概念**：

Redis 性能极高，QPS 可达 10 万+。

**原因分析**：

```
┌─────────────────────────────────────────────────────────────────┐
│                    Redis 高性能原因                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  1. 内存操作                                                     │
│     └─ 无磁盘 IO                                                │
│     └─ 内存访问速度 ns 级                                       │
│                                                                 │
│  2. 单线程模型                                                   │
│     └─ 无锁竞争                                                 │
│     └─ 无上下文切换                                             │
│     └─ CPU 缓存友好                                             │
│                                                                 │
│  3. IO 多路复用                                                  │
│     └─ epoll (Linux)                                           │
│     └─ 单线程处理大量连接                                       │
│                                                                 │
│  4. 高效数据结构                                                  │
│     └─ SDS (Simple Dynamic String)                             │
│     └─ 哈希表（渐进式 rehash）                                  │
│     └─ 跳表（ZSet）                                             │
│     └─ 压缩列表（小数据量）                                     │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

**追问延伸**：
- Redis 6.0 为什么引入多线程？
  - 多线程处理网络 IO（读写数据）
  - 命令执行仍是单线程
  - 提升网络 IO 性能

---

### Q16: 缓存穿透、击穿、雪崩？

**问题对比**：

```
┌─────────────────────────────────────────────────────────────────┐
│                    缓存三大问题                                  │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  1. 缓存穿透（Penetration）                                      │
│     原因：查询不存在的数据                                       │
│     解决：                                                       │
│       - 布隆过滤器                                               │
│       - 缓存空值（设置短过期时间）                               │
│                                                                 │
│  2. 缓存击穿（Breakdown）                                        │
│     原因：热点 key 过期，大量请求穿透到数据库                    │
│     解决：                                                       │
│       - 热点数据永不过期                                         │
│       - 互斥锁（只让一个请求查库）                               │
│                                                                 │
│  3. 缓存雪崩（Avalanche）                                        │
│     原因：大量 key 同时过期，或 Redis 宕机                       │
│     解决：                                                       │
│       - 随机过期时间                                             │
│       - 多级缓存                                                 │
│       - Redis 集群高可用                                         │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

**布隆过滤器**：

```java
// 使用 Redisson 布隆过滤器
RBloomFilter<String> bloomFilter = redisson.getBloomFilter("user:bloom");
bloomFilter.tryInit(1000000, 0.01);  // 预计 100 万，误判率 1%

// 添加元素
bloomFilter.add("user:1001");

// 判断是否存在
if (bloomFilter.contains("user:1001")) {
    // 可能存在，查缓存/数据库
} else {
    // 一定不存在，直接返回
}
```

---

## 七、系统设计

腾讯常考设计题：

### 1. 短链接系统

```
设计要点：
1. ID 生成：Snowflake → 62 进制编码
2. 存储：Redis 缓存 + MySQL 持久化
3. 重定向：301 永久（SEO 友好）或 302 临时（统计）
4. 高可用：多机房部署，DNS 轮询
```

### 2. 消息推送系统

```
设计要点：
1. 长连接：WebSocket
2. 连接管理：用户 ID → Gateway 映射
3. 消息路由：Redis Pub/Sub
4. 离线消息：存储后推送
```

### 3. 分布式 ID 生成

| 方案 | 优点 | 缺点 |
|------|------|------|
| UUID | 简单 | 无序，太长 |
| 数据库自增 | 简单 | 单点，性能瓶颈 |
| Snowflake | 分布式，有序 | 依赖时钟 |
| Leaf | 综合，高性能 | 实现复杂 |

---

[返回目录](../README.md)