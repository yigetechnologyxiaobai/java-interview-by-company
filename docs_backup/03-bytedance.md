# 字节跳动 Java 面试题

## 面试风格

**特点**：算法驱动，系统设计占比大，代码能力要求高

**轮次**：通常 3-4 轮技术面（每轮都有算法）

**重点**：算法、系统设计、基础

**面试官画像**：喜欢让候选人在白板/在线编辑器写代码，代码风格、边界处理都很重要

---

## 一、算法高频题

字节面试必考算法，难度 LeetCode 中等偏难

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

**复杂度分析**：
- 时间：O(n)，遍历一次
- 空间：迭代 O(1)，递归 O(n)（栈空间）

**合并 K 个有序链表**

```java
// 方法一：优先队列
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

// 方法二：分治法
public ListNode mergeKLists(ListNode[] lists) {
    return merge(lists, 0, lists.length - 1);
}

private ListNode merge(ListNode[] lists, int left, int right) {
    if (left == right) return lists[left];
    if (left > right) return null;
    
    int mid = (left + right) / 2;
    return mergeTwoLists(merge(lists, left, mid), merge(lists, mid + 1, right));
}
```

**复杂度对比**：
| 方法 | 时间 | 空间 |
|------|------|------|
| 优先队列 | O(nk log k) | O(k) |
| 分治 | O(nk log k) | O(log k) |

**链表环检测 + 环入口**

```java
public ListNode detectCycle(ListNode head) {
    ListNode slow = head, fast = head;
    
    // 1. 判断是否有环
    while (fast != null && fast.next != null) {
        slow = slow.next;
        fast = fast.next.next;
        if (slow == fast) {
            // 2. 找环入口
            ListNode ptr = head;
            while (ptr != slow) {
                ptr = ptr.next;
                slow = slow.next;
            }
            return ptr;
        }
    }
    return null;
}
```

**原理图**：

```
head → a → b → c → d → e
                 ↑       │
                 └─ f ←─┘

快慢指针相遇在 e 点
从 head 和相遇点同时出发，会在环入口相遇

证明：
设 a 为 head 到环入口的距离
设 b 为环入口到相遇点的距离
设 c 为相遇点到环入口的距离

快指针走的距离：a + b + n(b + c)
慢指针走的距离：a + b

快指针是慢指针的两倍：
a + b + n(b + c) = 2(a + b)
=> a = c + (n-1)(b + c)

即：从 head 走 a 步 = 从相遇点走 c + (n-1)圈
所以会相遇在环入口
```

### 2. 数组专题

**三数之和**

```java
public List<List<Integer>> threeSum(int[] nums) {
    List<List<Integer>> result = new ArrayList<>();
    Arrays.sort(nums);
    
    for (int i = 0; i < nums.length - 2; i++) {
        // 去重
        if (i > 0 && nums[i] == nums[i - 1]) continue;
        
        // 剪枝：最小值 > 0
        if (nums[i] > 0) break;
        
        int left = i + 1, right = nums.length - 1;
        while (left < right) {
            int sum = nums[i] + nums[left] + nums[right];
            if (sum == 0) {
                result.add(Arrays.asList(nums[i], nums[left], nums[right]));
                // 去重
                while (left < right && nums[left] == nums[left + 1]) left++;
                while (left < right && nums[right] == nums[right - 1]) right--;
                left++;
                right--;
            } else if (sum < 0) {
                left++;
            } else {
                right--;
            }
        }
    }
    return result;
}
```

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

**最大子数组和**

```java
public int maxSubArray(int[] nums) {
    int max = nums[0];
    int sum = 0;
    
    for (int num : nums) {
        if (sum > 0) {
            sum += num;
        } else {
            sum = num;
        }
        max = Math.max(max, sum);
    }
    return max;
}
```

### 3. 树专题

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

**验证二叉搜索树**

```java
public boolean isValidBST(TreeNode root) {
    return validate(root, Long.MIN_VALUE, Long.MAX_VALUE);
}

private boolean validate(TreeNode node, long min, long max) {
    if (node == null) return true;
    if (node.val <= min || node.val >= max) return false;
    return validate(node.left, min, node.val) && validate(node.right, node.val, max);
}
```

### 4. 动态规划专题

**最长递增子序列**

```java
// O(n log n) 解法
public int lengthOfLIS(int[] nums) {
    int[] tails = new int[nums.length];
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

**编辑距离**

```java
public int minDistance(String word1, String word2) {
    int m = word1.length(), n = word2.length();
    int[][] dp = new int[m + 1][n + 1];
    
    // 初始化
    for (int i = 0; i <= m; i++) dp[i][0] = i;
    for (int j = 0; j <= n; j++) dp[0][j] = j;
    
    for (int i = 1; i <= m; i++) {
        for (int j = 1; j <= n; j++) {
            if (word1.charAt(i - 1) == word2.charAt(j - 1)) {
                dp[i][j] = dp[i - 1][j - 1];
            } else {
                dp[i][j] = Math.min(dp[i - 1][j - 1], 
                           Math.min(dp[i - 1][j], dp[i][j - 1])) + 1;
            }
        }
    }
    return dp[m][n];
}
```

**打家劫舍**

```java
public int rob(int[] nums) {
    if (nums.length == 1) return nums[0];
    
    int prev2 = 0, prev1 = 0;
    for (int num : nums) {
        int curr = Math.max(prev1, prev2 + num);
        prev2 = prev1;
        prev1 = curr;
    }
    return prev1;
}
```

### 5. 回溯专题

**全排列**

```java
public List<List<Integer>> permute(int[] nums) {
    List<List<Integer>> result = new ArrayList<>();
    boolean[] used = new boolean[nums.length];
    backtrack(nums, used, new ArrayList<>(), result);
    return result;
}

private void backtrack(int[] nums, boolean[] used, List<Integer> path, List<List<Integer>> result) {
    if (path.size() == nums.length) {
        result.add(new ArrayList<>(path));
        return;
    }
    
    for (int i = 0; i < nums.length; i++) {
        if (used[i]) continue;
        used[i] = true;
        path.add(nums[i]);
        backtrack(nums, used, path, result);
        path.remove(path.size() - 1);
        used[i] = false;
    }
}
```

### 6. 图专题

**岛屿数量**

```java
public int numIslands(char[][] grid) {
    int count = 0;
    for (int i = 0; i < grid.length; i++) {
        for (int j = 0; j < grid[0].length; j++) {
            if (grid[i][j] == '1') {
                dfs(grid, i, j);
                count++;
            }
        }
    }
    return count;
}

private void dfs(char[][] grid, int i, int j) {
    if (i < 0 || i >= grid.length || j < 0 || j >= grid[0].length || grid[i][j] == '0') {
        return;
    }
    grid[i][j] = '0';
    dfs(grid, i + 1, j);
    dfs(grid, i - 1, j);
    dfs(grid, i, j + 1);
    dfs(grid, i, j - 1);
}
```

**课程表（拓扑排序）**

```java
public boolean canFinish(int numCourses, int[][] prerequisites) {
    // 构建邻接表和入度数组
    List<List<Integer>> adj = new ArrayList<>();
    int[] inDegree = new int[numCourses];
    for (int i = 0; i < numCourses; i++) {
        adj.add(new ArrayList<>());
    }
    for (int[] pre : prerequisites) {
        adj.get(pre[1]).add(pre[0]);
        inDegree[pre[0]]++;
    }
    
    // BFS
    Queue<Integer> queue = new LinkedList<>();
    for (int i = 0; i < numCourses; i++) {
        if (inDegree[i] == 0) queue.offer(i);
    }
    
    int count = 0;
    while (!queue.isEmpty()) {
        int course = queue.poll();
        count++;
        for (int next : adj.get(course)) {
            if (--inDegree[next] == 0) {
                queue.offer(next);
            }
        }
    }
    return count == numCourses;
}
```

### 手写代码要求

1. **时间复杂度分析**：必须能说出
2. **空间复杂度分析**：必须能说出
3. **边界条件**：
   - 输入为 null
   - 输入为空数组/空字符串
   - 输入长度为 1
4. **代码风格**：
   - 变量命名有意义
   - 代码缩进规范
   - 必要的注释

---

## 二、系统设计高频题

字节系统设计题很常见，需要系统思维

### Q1: 设计一个短链接系统

**需求分析**：
- 功能：长链接转短链接，短链接重定向到长链接
- QPS：假设 1 亿日活，平均每人 5 次，QPS ≈ 6000，峰值 3 万
- 存储：假设每天 5000 万新链接，每个链接 500 字节，每天 25GB

**架构设计**：

```
┌─────────────────────────────────────────────────────────────────┐
│                     短链接系统架构                               │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  用户                                                           │
│    │                                                            │
│    ▼                                                            │
│  DNS 负载均衡                                                   │
│    │                                                            │
│    ▼                                                            │
│  ┌───────────────────────────────────────────────────────────┐ │
│  │  API Gateway                                               │ │
│  │  - 限流                                                    │ │
│  │  - 鉴权                                                    │ │
│  └───────────────────────────────────────────────────────────┘ │
│    │                                                            │
│    ├──────────────┬──────────────┐                            │
│    ▼              ▼              ▼                            │
│  写服务          读服务          统计服务                       │
│  (短链接生成)    (重定向)        (访问统计)                     │
│    │              │              │                            │
│    ▼              ▼              ▼                            │
│  Redis          Redis          Kafka                          │
│  (缓存)         (缓存)         (消息队列)                      │
│    │              │              │                            │
│    ▼              ▼              ▼                            │
│  MySQL          MySQL          ClickHouse                     │
│  (持久化)       (持久化)       (数据分析)                      │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

**ID 生成方案**：

```
方案一：自增 ID
┌─────────────────────────────────────────────────────────────────┐
│  优点：简单，有序                                               │
│  缺点：暴露业务量，分布式环境下需要额外处理                      │
│  解决：可以加随机前缀                                           │
└─────────────────────────────────────────────────────────────────┘

方案二：Snowflake
┌─────────────────────────────────────────────────────────────────┐
│  优点：分布式，有序                                             │
│  缺点：依赖时钟，有时钟回拨问题                                  │
│  结构：64 位                                                    │
│  ├── 1 位：符号位                                               │
│  ├── 41 位：时间戳（69 年）                                     │
│  ├── 10 位：机器 ID                                             │
│  └── 12 位：序列号                                              │
└─────────────────────────────────────────────────────────────────┘

方案三：发号器服务
┌─────────────────────────────────────────────────────────────────┐
│  优点：简单，高性能                                             │
│  缺点：单点问题                                                 │
│  解决：多机房部署，每台机器分配不同 ID 段                        │
└─────────────────────────────────────────────────────────────────┘
```

**短链接生成**：

```java
public String generateShortUrl(long id) {
    // 62 进制编码：0-9, a-z, A-Z
    String chars = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ";
    StringBuilder sb = new StringBuilder();
    
    while (id > 0) {
        sb.append(chars.charAt((int)(id % 62)));
        id /= 62;
    }
    
    return sb.reverse().toString();
}

// 示例：id = 125 → "21"
// id = 1000000000 → "15FTGg"
```

**重定向策略**：

| 状态码 | 含义 | 适用场景 |
|--------|------|---------|
| 301 | 永久重定向 | SEO 友好，浏览器会缓存 |
| 302 | 临时重定向 | 需要统计，不缓存 |

---

### Q2: 设计一个消息推送系统

**需求分析**：
- 功能：即时消息推送、离线消息、群聊
- QPS：假设 1 亿用户，每秒 10 万条消息
- 延迟：毫秒级

**架构设计**：

```
┌─────────────────────────────────────────────────────────────────┐
│                     消息推送系统架构                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  用户设备                                                       │
│  ┌─────┐ ┌─────┐ ┌─────┐                                      │
│  │ App │ │ Web │ │ PC │                                       │
│  └──┬──┘ └──┬──┘ └──┬──┘                                      │
│     │       │       │                                          │
│     ▼       ▼       ▼                                          │
│  ┌───────────────────────────────────────────────────────────┐ │
│  │  Gateway 集群                                              │ │
│  │  - WebSocket 长连接管理                                    │ │
│  │  - 用户上线/下线                                            │ │
│  │  - 心跳检测                                                 │ │
│  └───────────────────────────────────────────────────────────┘ │
│    │                                                            │
│    ▼                                                            │
│  ┌───────────────────────────────────────────────────────────┐ │
│  │  Redis (用户连接映射)                                       │ │
│  │  user_id → gateway_ip                                      │ │
│  └───────────────────────────────────────────────────────────┘ │
│    │                                                            │
│    ▼                                                            │
│  ┌───────────────────────────────────────────────────────────┐ │
│  │  消息路由服务                                               │ │
│  │  - 根据 user_id 找到对应的 Gateway                         │ │
│  │  - 通过 Redis Pub/Sub 发送到目标 Gateway                   │ │
│  └───────────────────────────────────────────────────────────┘ │
│    │                                                            │
│    ▼                                                            │
│  ┌───────────────────────────────────────────────────────────┐ │
│  │  Kafka (消息队列)                                           │ │
│  │  - 削峰填谷                                                 │ │
│  │  - 离线消息存储                                             │ │
│  └───────────────────────────────────────────────────────────┘ │
│    │                                                            │
│    ▼                                                            │
│  ┌───────────────────────────────────────────────────────────┐ │
│  │  MySQL (消息持久化)                                         │ │
│  └───────────────────────────────────────────────────────────┘ │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

**核心流程**：

```
发送消息流程：
1. 发送方 → Gateway → 消息路由服务
2. 消息路由服务查 Redis：接收方的 Gateway
3. 接收方在线 → Redis Pub/Sub → Gateway → 接收方
4. 接收方离线 → 存 Kafka/MySQL → 上线后推送
```

---

### Q3: 设计一个分布式 ID 生成器

**方案对比**：

```
┌─────────────────────────────────────────────────────────────────┐
│                    分布式 ID 方案对比                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  方案一：UUID                                                   │
│  ┌───────────────────────────────────────────────────────────┐ │
│  │  优点：简单，本地生成                                      │ │
│  │  缺点：无序，太长（36 字符），不适合做主键                  │ │
│  └───────────────────────────────────────────────────────────┘ │
│                                                                 │
│  方案二：数据库自增                                             │
│  ┌───────────────────────────────────────────────────────────┐ │
│  │  优点：简单，有序                                          │ │
│  │  缺点：单点，性能瓶颈                                      │ │
│  │  改进：多台机器，设置不同步长                              │ │
│  └───────────────────────────────────────────────────────────┘ │
│                                                                 │
│  方案三：Snowflake                                              │
│  ┌───────────────────────────────────────────────────────────┐ │
│  │  优点：分布式，有序，高性能                                │ │
│  │  缺点：依赖时钟                                            │ │
│  │  结构：                                                    │ │
│  │  0 - 41位时间戳 - 10位机器ID - 12位序列号                  │ │
│  └───────────────────────────────────────────────────────────┘ │
│                                                                 │
│  方案四：Leaf（美团）                                            │
│  ┌───────────────────────────────────────────────────────────┐ │
│  │  Leaf-segment：号段模式，从数据库批量获取 ID                │ │
│  │  Leaf-snowflake：优化版 Snowflake，解决时钟回拨            │ │
│  └───────────────────────────────────────────────────────────┘ │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

**Snowflake 实现**：

```java
public class SnowflakeIdGenerator {
    private final long twepoch = 1288834974657L;
    private final long workerIdBits = 5L;
    private final long datacenterIdBits = 5L;
    private final long sequenceBits = 12L;
    
    private final long maxWorkerId = ~(-1L << workerIdBits);
    private final long maxDatacenterId = ~(-1L << datacenterIdBits);
    
    private final long workerIdShift = sequenceBits;
    private final long datacenterIdShift = sequenceBits + workerIdBits;
    private final long timestampLeftShift = sequenceBits + workerIdBits + datacenterIdBits;
    private final long sequenceMask = ~(-1L << sequenceBits);
    
    private long workerId;
    private long datacenterId;
    private long sequence = 0L;
    private long lastTimestamp = -1L;
    
    public synchronized long nextId() {
        long timestamp = System.currentTimeMillis();
        
        if (timestamp < lastTimestamp) {
            throw new RuntimeException("时钟回拨");
        }
        
        if (lastTimestamp == timestamp) {
            sequence = (sequence + 1) & sequenceMask;
            if (sequence == 0) {
                timestamp = tilNextMillis(lastTimestamp);
            }
        } else {
            sequence = 0L;
        }
        
        lastTimestamp = timestamp;
        
        return ((timestamp - twepoch) << timestampLeftShift)
            | (datacenterId << datacenterIdShift)
            | (workerId << workerIdShift)
            | sequence;
    }
    
    private long tilNextMillis(long lastTimestamp) {
        long timestamp = System.currentTimeMillis();
        while (timestamp <= lastTimestamp) {
            timestamp = System.currentTimeMillis();
        }
        return timestamp;
    }
}
```

---

### Q4: 设计一个微博 Feed 流

**核心概念**：

Feed 流是用户看到的内容列表，如微博首页、朋友圈。

**推拉模式对比**：

```
┌─────────────────────────────────────────────────────────────────┐
│                      Feed 流模式对比                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  推模式（写扩散）                                                │
│  ┌───────────────────────────────────────────────────────────┐ │
│  │  发布微博时，写入所有粉丝的收件箱                          │ │
│  │  优点：读快（直接查收件箱）                                │ │
│  │  缺点：写慢，大 V 粉丝多时写入压力大                       │ │
│  │  适用：粉丝少的普通用户                                    │ │
│  └───────────────────────────────────────────────────────────┘ │
│                                                                 │
│  拉模式（读扩散）                                                │
│  ┌───────────────────────────────────────────────────────────┐ │
│  │  读取时，从所有关注的人的发件箱拉取                        │ │
│  │  优点：写快（只写自己发件箱）                              │ │
│  │  缺点：读慢，关注的人多时查询慢                            │ │
│  │  适用：粉丝多的大 V                                        │ │
│  └───────────────────────────────────────────────────────────┘ │
│                                                                 │
│  推拉结合                                                        │
│  ┌───────────────────────────────────────────────────────────┐ │
│  │  普通用户：推模式                                          │ │
│  │  大 V：拉模式                                              │ │
│  │  平衡读写性能                                              │ │
│  └───────────────────────────────────────────────────────────┘ │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

**架构设计**：

```
用户发布微博：
1. 写入自己发件箱
2. 判断是否大 V
   - 是：只写自己发件箱
   - 否：写入所有粉丝收件箱（推模式）

用户读取 Feed：
1. 获取关注列表
2. 分类：普通用户 + 大 V
3. 普通用户：直接查收件箱
4. 大 V：查发件箱
5. 合并、排序、返回
```

---

### Q5: 设计一个秒杀系统

**核心设计**：

```
┌─────────────────────────────────────────────────────────────────┐
│                       秒杀系统架构                               │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  1. 前端层                                                       │
│     └─ 按钮置灰（防止重复点击）                                 │
│     └─ 验证码（防止机器人）                                     │
│     └─ CDN 加速静态资源                                         │
│                                                                 │
│  2. 网关层                                                       │
│     └─ 限流（令牌桶/漏桶）                                      │
│     └─ 黑名单过滤                                               │
│     └─ 用户鉴权                                                 │
│                                                                 │
│  3. 应用层                                                       │
│     └─ 本地缓存（库存预热）                                     │
│     └─ Redis 预扣库存                                           │
│     └─ 消息队列异步下单                                         │
│                                                                 │
│  4. Redis 层                                                     │
│     └─ 库存存储                                                 │
│     └─ 原子扣减（Lua 脚本）                                     │
│     └─ 防重复下单                                               │
│                                                                 │
│  5. MQ 层                                                        │
│     └─ 削峰填谷                                                 │
│     └─ 异步处理订单                                             │
│                                                                 │
│  6. 数据库层                                                     │
│     └─ 订单落库                                                 │
│     └─ 扣减库存（乐观锁）                                       │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

**防超卖实现**：

```java
// Redis Lua 脚本
String luaScript = """
    local stock = redis.call('get', KEYS[1])
    if not stock then
        return -1  -- 商品不存在
    end
    if tonumber(stock) <= 0 then
        return 0   -- 库存不足
    end
    redis.call('decr', KEYS[1])
    return 1       -- 扣减成功
    """;

Long result = redisTemplate.execute(
    new DefaultRedisScript<>(luaScript, Long.class),
    Collections.singletonList("stock:" + productId)
);

if (result == 1) {
    // 扣减成功，发送 MQ
    mqProducer.send(new OrderMessage(userId, productId));
}
```

**防重复下单**：

```java
// 使用 Redis SETNX
String key = "order:lock:" + userId + ":" + productId;
Boolean success = redisTemplate.opsForValue()
    .setIfAbsent(key, "1", 10, TimeUnit.MINUTES);

if (!success) {
    throw new RuntimeException("请勿重复下单");
}
```

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

## 四、MySQL 高频题

### Q9: 索引为什么用 B+ 树？

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

### Q10: MVCC 原理？

**核心组件**：

```
1. 隐藏字段
   - DB_TRX_ID：事务 ID
   - DB_ROLL_PTR：回滚指针

2. Undo Log（版本链）
   当前数据 → Undo Log 1 → Undo Log 2 → ...

3. Read View（可见性判断）
   - m_ids：活跃事务 ID 列表
   - min_trx_id：最小活跃事务 ID
   - max_trx_id：下一个事务 ID
```

**隔离级别实现**：

| 隔离级别 | Read View 生成 |
|---------|----------------|
| RC | 每次 SELECT 生成新的 |
| RR | 事务第一次 SELECT 生成，后续复用 |

---

## 五、Redis 高频题

### Q11: Redis 数据结构？

| 类型 | 底层实现 | 场景 |
|------|---------|------|
| String | SDS | 缓存、计数器、分布式锁 |
| Hash | 哈希表 | 对象存储 |
| List | 压缩列表 + 双向链表 | 队列、栈 |
| Set | 哈希表 + 整数集合 | 标签、共同关注 |
| ZSet | 跳表 + 哈希表 | 排行榜 |

**跳表结构**：

```
┌─────────────────────────────────────────────────────────────────┐
│                         跳表结构                                 │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Level 3: ────────────────────────►[50]────────────►NULL       │
│                                      │                          │
│  Level 2: ────►[20]───────────────►[50]────────────►NULL       │
│                  │                   │                          │
│  Level 1: ────►[20]────►[30]──────►[50]────►[60]──►NULL       │
│                  │         │         │        │                 │
│  Level 0: ►[10]►[20]►[25]►[30]►[40]►[50]►[60]►[70]►NULL       │
│                                                                 │
│  查找 50：Level 0 → 20 → Level 1 → 50（3 步）                  │
│  查找 25：Level 0 → 20 → 25（2 步）                             │
│                                                                 │
│  时间复杂度：O(log n)                                           │
│  空间复杂度：O(n)                                               │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

### Q12: Redis 持久化？

**RDB vs AOF**：

| 维度 | RDB | AOF |
|------|-----|-----|
| 原理 | 快照 | 追加命令 |
| 文件大小 | 小 | 大 |
| 恢复速度 | 快 | 慢 |
| 数据安全 | 可能丢数据 | 更安全 |
| 性能影响 | 小 | 大 |

**混合持久化（Redis 4.0）**：

```
RDB（全量）+ AOF（增量）

文件结构：
[RDB 数据] + [AOF 增量命令]

优点：恢复快 + 数据安全
```

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

## 八、2026 Java 面经真题

> 来源：牛客网 2026-05
> 特点：两面连着面，项目 + 八股 + 算法

### 一面真题

#### Q1: 让你实现一个 HashMap，你会如何设计？

**参考答案**：

1. **核心数据结构**：
   - 数组 + 链表 + 红黑树（JDK 1.8+）
   - 初始容量 16，负载因子 0.75

2. **哈希函数**：
   ```java
   int hash = key.hashCode() ^ (key.hashCode() >>> 16);  // 扰动函数
   int index = (n - 1) & hash;  // 位运算取模
   ```

3. **冲突解决**：
   - 链地址法
   - 链表长度 ≥ 8 且数组长度 ≥ 64 时转红黑树

4. **扩容机制**：
   - 当 size > threshold 时扩容 2 倍
   - 重新计算元素位置（高位/低位分流）

---

#### Q2: synchronized 性能为什么提高了？

**参考答案**：锁升级机制。

```
无锁 → 偏向锁 → 轻量级锁 → 重量级锁
```

| 锁状态 | 适用场景 | 性能 |
|--------|---------|------|
| 偏向锁 | 单线程访问 | 最高 |
| 轻量级锁 | 交替执行 | 高 |
| 重量级锁 | 竞争激烈 | 低 |

**升级过程**：
1. 偏向锁：对象头记录线程 ID
2. 轻量级锁：CAS 自旋尝试获取
3. 重量级锁：阻塞等待，OS 互斥量

---

#### Q3: HTTP 报文结构？头部有哪些字段？

**请求报文**：
```
POST /api/user HTTP/1.1          // 请求行
Host: www.example.com            // 请求头
Content-Type: application/json
Content-Length: 25

{"name":"Tom","age":20}          // 请求体
```

**常见请求头**：
- Host：目标主机
- Content-Type：请求体类型
- Authorization：认证信息
- User-Agent：客户端信息
- Accept：接受的内容类型

**常见响应头**：
- Content-Type：响应体类型
- Set-Cookie：设置 Cookie
- Cache-Control：缓存控制
- Location：重定向地址

---

#### Q4: TCP 三次握手，TIME_WAIT 和 CLOSE_WAIT 的作用？

**TIME_WAIT**：
- 主动关闭方进入
- 等待 2MSL（Maximum Segment Lifetime）
- 作用：确保最后的 ACK 到达对方

**CLOSE_WAIT**：
- 被动关闭方进入
- 等待应用层调用 close()
- 大量 CLOSE_WAIT 说明代码没正确关闭连接

**为什么是三次握手？**
- 两次可能导致：失效的 SYN 到达服务端，服务端误建立连接
- 三次确保双方都能确认对方的接收和发送能力

---

#### Q5: 算法题 - 表达式求值（+ - * /）

**参考解答**：
```java
public int calculate(String s) {
    Stack<Integer> stack = new Stack<>();
    int num = 0;
    char sign = '+';
    
    for (int i = 0; i < s.length(); i++) {
        char c = s.charAt(i);
        if (Character.isDigit(c)) {
            num = num * 10 + (c - '0');
        }
        if (!Character.isDigit(c) && c != ' ' || i == s.length() - 1) {
            switch (sign) {
                case '+': stack.push(num); break;
                case '-': stack.push(-num); break;
                case '*': stack.push(stack.pop() * num); break;
                case '/': stack.push(stack.pop() / num); break;
            }
            sign = c;
            num = 0;
        }
    }
    
    int result = 0;
    while (!stack.isEmpty()) result += stack.pop();
    return result;
}
```

**思路**：
- 乘除法立即计算
- 加减法入栈最后累加

---

### 二面真题

#### Q1: HTTPS 整个过程？

**参考答案**：

```
客户端                                服务端
   |                                    |
   | -------- Client Hello ----------> |  (支持的加密套件)
   |                                    |
   | <------- Server Hello ----------- |  (选择的加密套件)
   | <------- Certificate ------------- |  (服务端证书)
   |                                    |
   | -------- Client Key Exchange ---> |  (预主密钥，用公钥加密)
   | -------- Change Cipher Spec ----> |  (切换到加密通信)
   | -------- Finished ---------------> |
   |                                    |
   | <------- Change Cipher Spec ----- |  (切换到加密通信)
   | <------- Finished ---------------- |
   |                                    |
   | ======== 加密通信 ================ |
```

**对称 vs 非对称加密**：
- 非对称加密：用于交换对称密钥（RSA、ECDHE）
- 对称加密：用于实际数据传输（AES）

---

#### Q2: 死锁的条件和解决方法？

**四个必要条件**：
1. 互斥：资源只能被一个进程使用
2. 请求保持：持有资源又请求新资源
3. 不剥夺：不能强行剥夺资源
4. 循环等待：存在循环等待链

**解决方法**：
- **预防**：破坏四个条件之一
- **避免**：银行家算法
- **检测**：资源分配图
- **解除**：终止进程、剥夺资源

---

#### Q3: 算法题 - 最长公共连续子串

**参考解答**：
```java
public int longestCommonSubstring(String s1, String s2) {
    int m = s1.length(), n = s2.length();
    int[][] dp = new int[m + 1][n + 1];
    int maxLen = 0;
    
    for (int i = 1; i <= m; i++) {
        for (int j = 1; j <= n; j++) {
            if (s1.charAt(i - 1) == s2.charAt(j - 1)) {
                dp[i][j] = dp[i - 1][j - 1] + 1;
                maxLen = Math.max(maxLen, dp[i][j]);
            }
        }
    }
    
    return maxLen;
}
```

**时间复杂度**：O(m × n)
**空间复杂度**：O(m × n)

---

**面试总结**：
- 字节两面连着面，共约 2 小时
- 一面偏八股和基础，二面偏网络和算法
- 面试官引导式提问，体验较好

---

## 四、2026 最新面经

### 字节跳动一面面经（2026-03-27）

**来源**：[牛客网](https://www.nowcoder.com/enterprise/665/interview)

#### Q1: HTTPS 握手经过几个 RTT（Round Trip Time）？

**参考答案**：

HTTPS 握手过程包括 TCP 三次握手 + TLS 握手，总共需要 **2-3 个 RTT**。

**详细流程**：

```
RTT 1: TCP 三次握手
  客户端 ── SYN ──> 服务端
  客户端 <── SYN+ACK ── 服务端
  客户端 ── ACK ──> 服务端

RTT 2: TLS 握手（以 TLS 1.2 为例）
  客户端 ── ClientHello ──> 服务端
  客户端 <── ServerHello + Certificate + ServerHelloDone ── 服务端

RTT 3: TLS 握手完成
  客户端 ── ClientKeyExchange + ChangeCipherSpec + Finished ──> 服务端
  客户端 <── ChangeCipherSpec + Finished ── 服务端
```

**TLS 1.3 优化**：

TLS 1.3 将握手过程优化为 **1-RTT**：

```
RTT 1: TCP + TLS 合并
  客户端 ── SYN ──> 服务端
  客户端 <── SYN+ACK ── 服务端
  客户端 ── ACK + ClientHello + KeyShare ──> 服务端
  客户端 <── ServerHello + Certificate + Finished ── 服务端
```

**代码示例**：查看 TLS 版本

```bash
# 使用 openssl 查看 TLS 版本
openssl s_client -connect www.example.com:443 -tls1_3

# 查看握手详情
openssl s_client -connect www.example.com:443 -showcerts
```

**追问**：TLS 1.3 相比 TLS 1.2 有哪些改进？

1. 握手从 2-RTT 减少到 1-RTT
2. 移除了不安全的加密算法（如 RSA、CBC）
3. 支持 0-RTT 恢复（有重放攻击风险）

---

#### Q2: Redis 跳表（SkipList）了解吗？为什么 MySQL 不用跳表而用 B+ 树？

**参考答案**：

**跳表结构**：

跳表是在链表基础上改进的「多层」有序链表，能够快速定位数据。

```
Level 3: ────────────────────────►[50]────────────►NULL
                                      │
Level 2: ────►[20]───────────────►[50]────────────►NULL
                  │                   │
Level 1: ────►[20]────►[30]──────►[50]────►[60]──►NULL
                  │         │         │        │
Level 0: ►[10]►[20]►[25]►[30]►[40]►[50]►[60]►[70]►NULL
```

**查找过程**：
- 查找 50：Level 0 → 20 → Level 1 → 50（3 步）
- 时间复杂度：O(log n)
- 空间复杂度：O(n)

**为什么 MySQL 不用跳表**：

| 维度 | B+ 树 | 跳表 |
|------|-------|------|
| 磁盘 IO | 3-4 层可存千万数据 | 层数过高，IO 次数多 |
| 范围查询 | 叶子节点链表，高效 | 需要回到底层遍历 |
| 空间利用率 | 非叶子节点只存键值 | 每层都需要存储指针 |

**核心原因**：B+ 树的高度在 3 层时就能存储千万级别数据，而跳表维护同样数据量会导致层数过高，磁盘 IO 次数增多。

**代码示例**：Redis Zset 跳表实现

```c
// Redis 跳表节点结构
typedef struct zskiplistNode {
    sds ele;                          // 成员对象
    double score;                     // 分值
    struct zskiplistNode *backward;   // 后退指针
    struct zskiplistLevel {
        struct zskiplistNode *forward; // 前进指针
        unsigned long span;            // 跨度
    } level[];                        // 层
} zskiplistNode;
```

**追问**：为什么 Redis 使用跳表而不是红黑树？

1. 实现简单，易于理解和维护
2. 范围查询更高效（只需要遍历底层链表）
3. 内存占用更可控（可以通过调整概率控制层数）
4. 并发友好（锁粒度更细）

---

#### Q3: synchronized 支持重入吗？如何实现的？

**参考答案**：

synchronized 是**可重入锁**，同一个线程可以多次获取同一把锁。

**实现原理**：

每个对象的对象头中存储着锁状态和线程 ID：

```
对象头结构：
┌─────────────────────────────────────────┐
│  Mark Word (64 bits)                    │
├─────────────────────────────────────────┤
│  锁状态 | 线程ID | 锁计数器 | 其他       │
└─────────────────────────────────────────┘

偏向锁状态：
┌─────────────────────────────────────────┐
│  thread:23 | epoch:2 | age:4 | 1 | 01   │
└─────────────────────────────────────────┘

轻量级锁状态：
┌─────────────────────────────────────────┐
│  ptr_to_lock_record:62 | 00             │
└─────────────────────────────────────────┘

重量级锁状态：
┌─────────────────────────────────────────┐
│  ptr_to_heavyweight_monitor:62 | 10     │
└─────────────────────────────────────────┘
```

**重入过程**：

```java
public class ReentrantDemo {
    public synchronized void methodA() {
        methodB();  // 再次获取同一把锁，计数器 +1
    }
    
    public synchronized void methodB() {
        // 执行完毕后，计数器 -1
    }
}
```

**底层实现**：

1. **锁状态 = 0**：锁未被占用，CAS 获取锁，记录线程 ID
2. **锁状态 ≠ 0 且线程 ID = 当前线程**：可重入，计数器 +1
3. **锁状态 ≠ 0 且线程 ID ≠ 当前线程**：阻塞等待

**释放锁**：
- 每次退出 synchronized 方法/代码块，计数器 -1
- 计数器 = 0 时，真正释放锁

**代码示例**：验证可重入

```java
public class ReentrantTest {
    private final Object lock = new Object();
    
    public void outer() {
        synchronized (lock) {
            System.out.println("outer");
            inner();  // 可重入
        }
    }
    
    public void inner() {
        synchronized (lock) {
            System.out.println("inner");
        }
    }
    
    public static void main(String[] args) {
        new ReentrantTest().outer();
    }
}
// 输出：outer inner（不会死锁）
```

**追问**：synchronized 和 ReentrantLock 有什么区别？

| 维度 | synchronized | ReentrantLock |
|------|-------------|---------------|
| 实现层级 | JVM 层面 | API 层面 |
| 锁获取 | 自动 | 手动 lock()/unlock() |
| 公平性 | 非公平 | 可选公平/非公平 |
| 条件变量 | 单一 | 多个 Condition |
| 响应中断 | 不支持 | 支持 lockInterruptibly() |

---

#### Q4: MySQL 间隙锁（Gap Lock）的原理？什么时候会加间隙锁？

**参考答案**：

**间隙锁定义**：

Gap Lock 称为间隙锁，只存在于**可重复读（RR）隔离级别**，目的是解决幻读问题。

**原理**：

间隙锁锁住两个记录之间的间隙，防止其他事务在这个间隙中插入新记录。

```
假设表中有 id = 1, 5, 10 三条记录

间隙锁范围：
(-∞, 1), (1, 5), (5, 10), (10, +∞)

如果事务 A 在 id = 5 上加间隙锁 (1, 5)
则其他事务无法插入 id = 2, 3, 4 的记录
```

**什么时候加间隙锁**：

当使用唯一索引进行等值查询，且**查询的记录不存在**时，会加间隙锁。

```sql
-- 假设表中有 id = 1, 5, 10
-- 事务 A
SELECT * FROM user WHERE id = 3 FOR UPDATE;

-- 此时会加间隙锁 (1, 5)
-- 事务 B 插入 id = 2, 3, 4 都会被阻塞
INSERT INTO user (id, name) VALUES (3, 'test');  -- 阻塞
```

**间隙锁的特点**：

1. 间隙锁之间**兼容**（两个事务可以同时持有同一间隙的间隙锁）
2. 间隙锁目的是**防止插入**，不是防止读取
3. 只存在于可重复读隔离级别

**代码示例**：

```sql
-- 查看当前锁情况
SELECT * FROM performance_schema.data_locks\G;

-- 示例输出
*************************** 1. row ***************************
               ENGINE: INNODB
       ENGINE_LOCK_ID: 140234567890:1070:140234567890
ENGINE_TRANSACTION_ID: 4212345678901234
            THREAD_ID: 45
             EVENT_ID: 12
        OBJECT_SCHEMA: test
          OBJECT_NAME: user
       PARTITION_NAME: NULL
    SUBPARTITION_NAME: NULL
             INDEX_NAME: PRIMARY
OBJECT_INSTANCE_BEGIN: 140234567890
            LOCK_TYPE: RECORD
            LOCK_MODE: X,GAP              -- 间隙锁
          LOCK_STATUS: GRANTED
               LOCK_DATA: 5               -- 锁住 (1, 5) 间隙
```

**追问**：如何避免间隙锁？

1. 使用读提交（RC）隔离级别
2. 使用唯一索引查询存在的记录
3. 使用主键查询

---

#### Q5: 算法题 - 重排链表

**题目**：给定链表 1 → 2 → 3 → ... → n-1 → n，使用 O(1) 空间复杂度使其变为 1 → n → 2 → n-1 → ...

**参考答案**：

**思路**：
1. 找到链表中点
2. 反转后半部分
3. 合并两个链表

**代码实现**：

```java
public void reorderList(ListNode head) {
    if (head == null || head.next == null) return;
    
    // 1. 找中点（快慢指针）
    ListNode slow = head, fast = head;
    while (fast.next != null && fast.next.next != null) {
        slow = slow.next;
        fast = fast.next.next;
    }
    
    // 2. 反转后半部分
    ListNode second = reverse(slow.next);
    slow.next = null;  // 断开
    
    // 3. 合并两个链表
    ListNode first = head;
    while (second != null) {
        ListNode temp1 = first.next;
        ListNode temp2 = second.next;
        
        first.next = second;
        second.next = temp1;
        
        first = temp1;
        second = temp2;
    }
}

// 反转链表
private ListNode reverse(ListNode head) {
    ListNode prev = null, curr = head;
    while (curr != null) {
        ListNode next = curr.next;
        curr.next = prev;
        prev = curr;
        curr = next;
    }
    return prev;
}
```

**示例**：

```
输入：1 → 2 → 3 → 4 → 5
       ↓
中点：3
       ↓
反转：1 → 2 → 3, 5 → 4
       ↓
合并：1 → 5 → 2 → 4 → 3

输入：1 → 2 → 3 → 4 → 5 → 6
       ↓
中点：3
       ↓
反转：1 → 2 → 3, 6 → 5 → 4
       ↓
合并：1 → 6 → 2 → 5 → 3 → 4
```

**复杂度分析**：
- 时间复杂度：O(n)，遍历 3 次
- 空间复杂度：O(1)，只使用常数空间

**追问**：如果要求不能改变原链表结构怎么办？

可以先复制链表再操作，或者使用递归（但空间复杂度变为 O(n)）。

---

[返回目录](../README.md)