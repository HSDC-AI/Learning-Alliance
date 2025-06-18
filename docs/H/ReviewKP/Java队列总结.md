# Java队列（Queue）和双端队列（Deque）总结

## 1. Queue接口

Queue是Java集合框架中的一个接口，它继承自Collection接口。Queue接口定义了一个队列的基本操作，包括添加、删除和检查元素。

### 1.1 Queue接口的主要方法

```java
public interface Queue<E> {
    // 添加元素
    boolean add(E e);      // 添加元素，如果队列已满则抛出异常
    boolean offer(E e);    // 添加元素，如果队列已满则返回false
    
    // 删除元素
    E remove();           // 移除并返回队首元素，如果队列为空则抛出异常
    E poll();             // 移除并返回队首元素，如果队列为空则返回null
    
    // 获取元素
    E element();          // 返回队首元素但不移除，如果队列为空则抛出异常
    E peek();             // 返回队首元素但不移除，如果队列为空则返回null
}
```

### 1.2 Queue接口的完整示例

```java
public class QueueExample {
    public static void main(String[] args) {
        // 创建队列
        Queue<String> queue = new LinkedList<>();
        
        // 1. 添加元素
        // 使用add方法
        try {
            queue.add("First");
            queue.add("Second");
            queue.add("Third");
        } catch (IllegalStateException e) {
            System.out.println("队列已满，无法添加元素");
        }
        
        // 使用offer方法
        boolean offered = queue.offer("Fourth");
        if (!offered) {
            System.out.println("队列已满，无法添加元素");
        }
        
        // 2. 获取元素
        // 使用element方法
        try {
            String first = queue.element();
            System.out.println("队首元素: " + first);  // 输出: First
        } catch (NoSuchElementException e) {
            System.out.println("队列为空");
        }
        
        // 使用peek方法
        String peeked = queue.peek();
        if (peeked != null) {
            System.out.println("队首元素: " + peeked);  // 输出: First
        } else {
            System.out.println("队列为空");
        }
        
        // 3. 删除元素
        // 使用remove方法
        try {
            String removed = queue.remove();
            System.out.println("移除的元素: " + removed);  // 输出: First
        } catch (NoSuchElementException e) {
            System.out.println("队列为空");
        }
        
        // 使用poll方法
        String polled = queue.poll();
        if (polled != null) {
            System.out.println("移除的元素: " + polled);  // 输出: Second
        } else {
            System.out.println("队列为空");
        }
        
        // 4. 遍历队列
        System.out.println("\n遍历队列:");
        while (!queue.isEmpty()) {
            System.out.println(queue.poll());
        }
    }
}
```

## 2. Deque接口

Deque（Double Ended Queue）是一个双端队列接口，它继承自Queue接口。Deque允许在队列的两端进行插入和删除操作。

### 2.1 Deque接口的主要方法

```java
public interface Deque<E> extends Queue<E> {
    // 在队首添加元素
    void addFirst(E e);           // 添加元素，如果队列已满则抛出异常
    boolean offerFirst(E e);      // 添加元素，如果队列已满则返回false
    
    // 在队尾添加元素
    void addLast(E e);            // 添加元素，如果队列已满则抛出异常
    boolean offerLast(E e);       // 添加元素，如果队列已满则返回false
    
    // 在队首删除元素
    E removeFirst();              // 移除并返回队首元素，如果队列为空则抛出异常
    E pollFirst();                // 移除并返回队首元素，如果队列为空则返回null
    
    // 在队尾删除元素
    E removeLast();               // 移除并返回队尾元素，如果队列为空则抛出异常
    E pollLast();                 // 移除并返回队尾元素，如果队列为空则返回null
    
    // 获取队首元素
    E getFirst();                 // 返回队首元素但不移除，如果队列为空则抛出异常
    E peekFirst();                // 返回队首元素但不移除，如果队列为空则返回null
    
    // 获取队尾元素
    E getLast();                  // 返回队尾元素但不移除，如果队列为空则抛出异常
    E peekLast();                 // 返回队尾元素但不移除，如果队列为空则返回null
    
    // 栈操作
    void push(E e);               // 将元素压入栈顶
    E pop();                      // 弹出栈顶元素
    E peek();                     // 查看栈顶元素
}
```

### 2.2 Deque接口的完整示例

```java
public class DequeExample {
    public static void main(String[] args) {
        // 创建双端队列
        Deque<String> deque = new ArrayDeque<>();
        
        // 1. 在队首添加元素
        try {
            deque.addFirst("First");
            deque.addFirst("Second");
        } catch (IllegalStateException e) {
            System.out.println("队列已满，无法添加元素");
        }
        
        boolean offeredFirst = deque.offerFirst("Third");
        if (!offeredFirst) {
            System.out.println("队列已满，无法添加元素");
        }
        
        // 2. 在队尾添加元素
        try {
            deque.addLast("Fourth");
            deque.addLast("Fifth");
        } catch (IllegalStateException e) {
            System.out.println("队列已满，无法添加元素");
        }
        
        boolean offeredLast = deque.offerLast("Sixth");
        if (!offeredLast) {
            System.out.println("队列已满，无法添加元素");
        }
        
        // 3. 获取元素
        // 获取队首元素
        try {
            String first = deque.getFirst();
            System.out.println("队首元素: " + first);  // 输出: Third
        } catch (NoSuchElementException e) {
            System.out.println("队列为空");
        }
        
        String peekedFirst = deque.peekFirst();
        if (peekedFirst != null) {
            System.out.println("队首元素: " + peekedFirst);  // 输出: Third
        }
        
        // 获取队尾元素
        try {
            String last = deque.getLast();
            System.out.println("队尾元素: " + last);  // 输出: Sixth
        } catch (NoSuchElementException e) {
            System.out.println("队列为空");
        }
        
        String peekedLast = deque.peekLast();
        if (peekedLast != null) {
            System.out.println("队尾元素: " + peekedLast);  // 输出: Sixth
        }
        
        // 4. 删除元素
        // 删除队首元素
        try {
            String removedFirst = deque.removeFirst();
            System.out.println("移除的队首元素: " + removedFirst);  // 输出: Third
        } catch (NoSuchElementException e) {
            System.out.println("队列为空");
        }
        
        String polledFirst = deque.pollFirst();
        if (polledFirst != null) {
            System.out.println("移除的队首元素: " + polledFirst);  // 输出: Second
        }
        
        // 删除队尾元素
        try {
            String removedLast = deque.removeLast();
            System.out.println("移除的队尾元素: " + removedLast);  // 输出: Sixth
        } catch (NoSuchElementException e) {
            System.out.println("队列为空");
        }
        
        String polledLast = deque.pollLast();
        if (polledLast != null) {
            System.out.println("移除的队尾元素: " + polledLast);  // 输出: Fifth
        }
        
        // 5. 作为栈使用
        System.out.println("\n作为栈使用:");
        Deque<String> stack = new ArrayDeque<>();
        
        // 压栈
        stack.push("Stack1");
        stack.push("Stack2");
        stack.push("Stack3");
        
        // 出栈
        while (!stack.isEmpty()) {
            System.out.println(stack.pop());  // 输出: Stack3, Stack2, Stack1
        }
        
        // 6. 作为队列使用
        System.out.println("\n作为队列使用:");
        Deque<String> queue = new ArrayDeque<>();
        
        // 入队
        queue.offerLast("Queue1");
        queue.offerLast("Queue2");
        queue.offerLast("Queue3");
        
        // 出队
        while (!queue.isEmpty()) {
            System.out.println(queue.pollFirst());  // 输出: Queue1, Queue2, Queue3
        }
        
        // 7. 双向遍历
        System.out.println("\n双向遍历:");
        Deque<Integer> numbers = new LinkedList<>();
        numbers.addLast(1);
        numbers.addLast(2);
        numbers.addLast(3);
        
        // 从前向后遍历
        System.out.println("从前向后遍历:");
        for (Integer num : numbers) {
            System.out.println(num);  // 输出: 1, 2, 3
        }
        
        // 从后向前遍历
        System.out.println("从后向前遍历:");
        Iterator<Integer> descendingIterator = numbers.descendingIterator();
        while (descendingIterator.hasNext()) {
            System.out.println(descendingIterator.next());  // 输出: 3, 2, 1
        }
    }
}
```

> descendingIterator() 也是一个比较重要的方法，省去了我们自己实现从后往前遍历，直接用它就可以完成

## 3. 主要实现类比较

### 3.1 Queue实现类

| 实现类 | 特点 | 适用场景 |
|--------|------|----------|
| LinkedList | 双向链表实现，支持快速插入删除 | 需要频繁插入删除操作 |
| PriorityQueue | 基于优先级堆的无界队列 | 需要按优先级处理元素 |
| ArrayBlockingQueue | 基于数组的有界阻塞队列 | 固定大小的生产者-消费者模式 |
| LinkedBlockingQueue | 基于链表的可选有界阻塞队列 | 可变大小的生产者-消费者模式 |
| ConcurrentLinkedQueue | 基于链表的无界线程安全队列 | 高并发环境 |

### 3.2 Deque实现类

| 实现类 | 特点 | 适用场景 |
|--------|------|----------|
| ArrayDeque | 基于数组实现，无容量限制 | 需要高效的双端操作，内存敏感 |
| LinkedList | 双向链表实现 | 需要频繁的插入删除操作，双向遍历 |


### 3.3 PriorityQueue

PriorityQueue 是在 JDK1.5 中被引入的, 其与 Queue 的区别在于元素出队顺序是与优先级相关的，即总是优先级最高的元素先出队。这里列举其相关的一些要点：
* PriorityQueue 利用了二叉堆的数据结构来实现的，底层使用可变长的数组来存储数据PriorityQueue 通过堆元素的上浮和下沉，实现了在 O(logn) 的时间复杂度内插入元素和删除堆顶元素。
* PriorityQueue 是非线程安全的，且不支持存储 NULL 和 non-comparable 的对象。
* PriorityQueue 默认是小顶堆，但可以接收一个 Comparator 作为构造参数，从而来自定义元素优先级的先后。
* PriorityQueue 默认小顶堆

PriorityQueue 在面试中可能更多的会出现在手撕算法的时候，典型例题包括堆排序、求第 K 大的数、带权图的遍历等，所以需要会熟练使用才行。

#### 3.3.1 二叉堆
二叉堆就长这样，本质是一棵**完全二叉树**
* 结构规则​：除最后一层外，其他层节点全满，最后一层节点从左到右紧密排列（不留空洞）。
* ​存储方式​：用数组存储，而非指针。节点位置通过下标计算得出，节省内存且操作高效。

```java
数组 [50, 30, 20, 15, 10, 8] 可表示如下最大堆：
       50  
     /    \  
    30     20  
   /  \   /  
  15  10 8  
```
二叉堆只要求父子节点有序，​不要求兄弟节点有序。例如，上例中 30 和 20 无需比较大小。

数组下标的“定位公式”
若数组下标从 ​0​ 开始（常见编程实现）

* ​父节点位置​：父 index = (当前 index - 1) / 2（向下取整）
* ​左子节点​：左子 index = 2 × 当前 index + 1
* ​右子节点​：右子 index = 2 × 当前 index + 2
> 节点 20（下标为 2）的父节点是 (2-1)/2 = 0（即 50），左子是 2×2+1=5（即 8），右子超出数组范围。

1. 插入元素（上浮）​​
    * ​步骤​：
        1. 新元素放入数组末尾；
        2. ​上浮（Bubble Up）​​：若比父节点大（最大堆）或小（最小堆），则与父节点交换，重复直到满足堆性质。
    * ​时间复杂度​：​O(log n)​​（最多交换树的高度次）。
​
2. 删除根节点（下沉）​​
    * 步骤​：
        1. 移除根节点（即数组首元素）；
        2. 将数组末尾元素移到根位置；
        3. ​下沉（Bubble Down）​​：与较大的子节点（最大堆）或较小的子节点（最小堆）交换，直到满足堆性质.
    * 时间复杂度​：​O(log n)​



二叉堆是以下算法的基石
1. 优先队列：医院急诊按病情轻重排队，系统任务按优先级调度
2. 堆排序：通过反复移除根节点，实现 O(n log n) 的排序算法
3. Top K 问题​： 快速从海量数据中找出前 K 大/小的值（如热搜排行榜）

二叉堆的“灵魂三问”​
1. ​是什么​？→ 用数组存储的完全二叉树，父子节点有序。
2. 怎么变​？→ 插入时末尾上浮，删除时末尾补位后下沉。
3. ​有啥用​？→ 秒找最大值/最小值，支持动态排序和优先级调度。


### 3.4 BlockingQueue

支持没有元素时阻塞，直到有元素；还支持如果队列已满，可以一直等到队列可以放入新元素时再放入。

几种常见的阻塞类型
* ArrayBlockingQueue：使用数组实现的有界阻塞队列。在创建时需要指定容量大小，并支持公平和非公平两种方式的锁访问机制。
* LinkedBlockingQueue：使用单向链表实现的可选有界阻塞队列。在创建时可以指定容量大小，如果不指定则默认为Integer.MAX_VALUE。和ArrayBlockingQueue不同的是， 它仅支持非公平的锁访问机制。
* PriorityBlockingQueue：支持优先级排序的无界阻塞队列。元素必须实现Comparable接口或者在构造函数中传入Comparator对象，并且不能插入 null 元素。
* SynchronousQueue：同步队列，是一种不存储元素的阻塞队列。每个插入操作都必须等待对应的删除操作，反之删除操作也必须等待插入操作。因此，SynchronousQueue通常用于线程之间的直接传递数据。
* DelayQueue：延迟队列，其中的元素只有到了其指定的延迟时间，才能够从队列中出队。


## 4. 最佳实践

1. 选择队列实现时考虑以下因素：
   - 是否需要线程安全
   - 是否需要阻塞操作
   - 队列大小是否固定
   - 性能要求
   - 内存使用情况

2. 使用建议：
   - 单线程环境优先使用ArrayDeque
   - 需要线程安全时使用ConcurrentLinkedQueue
   - 需要阻塞操作时使用BlockingQueue的实现类
   - 需要优先级排序时使用PriorityQueue
   - 需要双向操作时使用Deque接口的实现类

3. 性能优化：
   - 合理设置队列容量
   - 使用批量操作
   - 避免频繁的队列操作
   - 根据实际需求选择合适的实现类 