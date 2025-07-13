# 239. 滑动窗口最大值

以下是我自己的解法，但是窗口移动一次就需要遍历一次窗口中的数组，时间复杂度比较高，于是在这道题中就学习了单调队列，通过单调队列来把查找窗口中的最大值优化成O(1)。

```java

/**
 * 自己的解法，使用定长的窗口并且加上大顶堆来实现的，思路没问题就是时间复杂度高，超时了。
 * 因为每一次循环都需要把窗口中的数循环一遍，窗口走多少次，就要循环多少次
 * @param nums
 * @param k
 * @return
 */
public int[] maxSlidingWindow1(int[] nums, int k) {
    PriorityQueue<Integer> queue = new PriorityQueue<>((a1, a2) -> a2 - a1);;
    int left = 0, right = left + k - 1;
    List<Integer> ans = new ArrayList<>();
    for (int i = 0; i < nums.length; i++) {
        queue.offer(nums[i]);
        if(i == right){
            left++;
            i = left - 1;
            right = left + k - 1;
            ans.add(queue.poll());
            queue.clear();
        }
    }
    int[] ansArray = new int[ans.size()];
    for (int i = 0; i < ansArray.length; i++) {
        ansArray[i] = ans.get(i);
    }
    return ansArray;
}

```    

关于单调队列的解释，我也看了几个文章，但是还是觉得https://labuladong.online/algo/data-structure/monotonic-queue/ 这个写的是比较好的，很清晰的描述了什么是单调队列以及单调队列的用法， 比AI和网上的文章要理解起来要顺畅。

那什么是单调队列？
单调队列的数据结构其实就是一个双向队列，但是队列中的数都是单调递增（或递减）的，入列的时候将元素从队尾加入，如果队尾的数小于当前的元素，那么就把队尾的数删掉，并且这里是要进行循环去判断的，直到队尾的数比当前元素要大。这样的话从队头来看这就是一个从小到大的顺序。

```java
/**
 * 更为清晰的单调队列的实现
 * @param nums
 * @param k
 * @return
 */
public int[] maxSlidingWindow(int[] nums, int k) {
    MonotonicQueue queue = new MonotonicQueue();
    List<Integer> ans = new ArrayList<>();

    for (int i = 0; i < nums.length; i++) {
        queue.push(nums[i]);
        // 窗口形成后再判断大小
        if(i >= k-1){
            ans.add(queue.max());
            // 移除窗口左边的数
            queue.pop(nums[i-k+1]);
        }
    }
    return ans.stream().mapToInt(Integer::intValue).toArray();
}

class MonotonicQueue{
    private final Deque<Integer> queue = new LinkedList<>();

    public void push(int num){
        // 如果队尾的元素比当前num小，那么就删掉，这样的话就形成了一个递减的单调队列
        while(!queue.isEmpty() && queue.peekLast() < num){
            queue.pollLast();
        }
        queue.addLast(num);
    }

    // 队列是递减的，那头一个就是最大值
    public int max(){
        return queue.getFirst();
    }

    // 对头元素如果是num就删掉，保证了元素挪出窗口
    public void pop(int num){
        if(queue.getFirst().equals(num))  queue.pollFirst();
    }
}
```