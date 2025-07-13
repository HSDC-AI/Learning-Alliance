# 560 和为 K 的子数组

最一开始想通过滑动窗口去解，在窗口中每次计算sum然后和k进行比较，但是这种方式是很耗时的，时间复杂度干到了O(n²)，直接给整超时了。
所以学习了一下deepseek的解法，使用哈希表和前缀和的方式去解

```java
**
 * 560. 和为 K 的子数组
 * 给你一个整数数组 nums 和一个整数 k ，请你统计并返回 该数组中和为 k 的子数组的个数 。
 *
 * 子数组是数组中元素的连续非空序列。
 *
 * 示例 1：
 * 输入：nums = [1,1,1], k = 2
 * 输出：2
 *
 * 示例 2：
 * 输入：nums = [1,2,3], k = 3
 * 输出：2
 *
 * 思路是通过不定长滑动窗口去判断窗口数组元素的和是否等于k，如果等于k就将ans++，如果大于k，那窗口就停止扩大，因为题目给出了数组是连续的
 */


public class SubArraySum {
    public static void main(String[] args) {
        System.out.println(subarraySum(new int[]{1,2,3}, 3));
    }

    /**
     * // 自己的解法
     * 使用动态滑动窗口，在循环中按照窗口大小copy了子数组，并且计算了子数组元素的和。如果右指针到了nums到头了，但是左指针没到头，
     * 那么就把左指针加一位，右指针再拨回来，重新循环。
     * 两个指针在开始的时候都指向同一个数
     *
     * 思路是没问题的，但是超时了。因为计算sum导致时间复杂度成了 O(n²)
     * @param nums
     * @param k
     * @return
     */
    public static int subarraySum1(int[] nums, int k) {
        int left = 0, ans = 0;
        for (int right = 0; right < nums.length; ) {
            int[] sub = new int[right - left + 1];
            System.arraycopy(nums, left, sub, 0, right - left + 1);
            int subSum = Arrays.stream(sub).sum();
            if(subSum == k){
                ans++;
            }
            right++;
            if(right == nums.length && left != nums.length-1){
                left++;
                right = left;
            }
        }
        return ans;
    }


    /**
     * 学习使用前缀和+哈希表来实现
     * 问题：计算前缀和为什么就能直到符合条件的子数组出现的个数？
     *
     * 思考：前缀和就是子数组的的内部元素和，这个sum和k是相等的，就说明出现过一次符合条件的数组，所以我们可以直接使用前缀和来统计出现数组的个数
     *
     * 前缀和公式：当前累计和 - j位置累计和 = k
     * @param nums
     * @param k
     * @return
     */
    public static int subarraySum(int[] nums, int k) {
        // 记录前缀和出现的次数，key是前缀和，value是出现的次数
        Map<Integer, Integer> preSumMap = new HashMap<>();
        // 也叫哨兵，一般在创建前缀和数组的时候都会在第一位上加一个0，意味着原数组从index=0前面没有和
        preSumMap.put(0, 1);
        int preSum = 0, ans = 0;
        for(int num : nums){
            // 计算前缀和，也就是当前位置和前面所有数的和
            preSum += num;
            // key是历史累计和，value是历史和出现的次数
            // 如1，2，3 k=3 这个case
            // 第一次循环 preSum = 1，差=-2，就返回0
            // 第二次循环 preSum = 3，差=0，map中有一个哨兵0，ans返回1
            // 第三次循环 preSum = 6，差=3，map中有一个3，ans返回2
            // 因为key是前缀和，所以如果当前累计和减去k，在map中出现过，说明有符合条件的数组，ans++
            ans += preSumMap.getOrDefault(preSum - k, 0);
            preSumMap.put(preSum, preSumMap.getOrDefault(preSum, 0) + 1);
        }
        return ans;
    }


}   
```


再来看一个前缀和的例子，使用公式能很快的计算出区间中的和
```java
import java.util.Arrays;

public class PrefixSumDemo {
    private int[] preSum;

    // 构造前缀和数组
    public PrefixSumDemo(int[] nums) {
        // 多开一位，preSum[0]=0 作为哨兵值
        preSum = new int[nums.length + 1];
        for (int i = 1; i <= nums.length; i++) {
            // 递推公式：当前前缀和 = 上一项前缀和 + 原数组当前值
            preSum[i] = preSum[i - 1] + nums[i - 1];
        }
    }

    // 查询区间和 [left, right]
    public int queryRange(int left, int right) {
        // 公式：preSum[right+1] - preSum[left]
        return preSum[right + 1] - preSum[left];
    }

    public static void main(String[] args) {
        int[] nums = {3, 1, 4, 2, 5};
        PrefixSumDemo demo = new PrefixSumDemo(nums);
        
        // 输出前缀和数组: [0, 3, 4, 8, 10, 15]
        System.out.println("前缀和数组: " + Arrays.toString(demo.preSum)); 
        
        // 测试查询
        System.out.println("区间 [1,3] 的和: " + demo.queryRange(1, 3)); // 1+4+2 = 7
        System.out.println("区间 [0,4] 的和: " + demo.queryRange(0, 4)); // 3+1+4+2+5 = 15
    }
}
```

## 303

力扣中还有一道easy的专门练习前缀和的题，创建一个arraylist接收前缀和，取的时候直接通过公式去取。

303. 区域和检索 - 数组不可变

```java
private List<Integer> sum = new ArrayList<Integer>();

// 构造中初始化时创建前缀和数组
public NumArray(int[] nums){
    sum.add(0);
    for(int num : nums){
        sum.add(num+sum.get(sum.size()-1));
    }
}
// 按index直接取
public int sumRange(int left, int right) {
    return sum.get(right+1) - sum.get(left);
}
```