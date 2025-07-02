# 128 最长连续序列

个人思路：
先去重，然后再排序，接着遍历数组，当前后比较两个数差不为1时，将这段数组当作String传入Map作为key，这段数组长度作为vlaue，直到循环完数组，得到一个存有几段连续数组的map，和对应的长度。再循环map找到value是最大的。


```java

/**
 * No 128
 * 给定一个未排序的整数数组 nums ，找出数字连续的最长序列（不要求序列元素在原数组中连续）的长度。
 *
 * 请你设计并实现时间复杂度为 O(n) 的算法解决此问题。
 *
 * 示例 1：
 *
 * 输入：nums = [100,4,200,1,3,2]
 * 输出：4
 * 解释：最长数字连续序列是 [1, 2, 3, 4]。它的长度为 4。
 * 示例 2：
 *
 * 输入：nums = [0,3,7,2,5,8,4,6,0,1]
 * 输出：9
 * 示例 3：
 *
 * 输入：nums = [1,0,1,2]
 * 输出：3
 */
public class LongestSerialArray {
    public static void main(String[] args) {
        // 4,0,-4,-2,2,5,2,0,-8,-8,-8,-8,-1,7,4,5,5,-4,6,6,-3 排序后通过hashSet去重有问题，-2会跑到0前
        int[] nums = {4,0,-4,-2,2,5,2,0,-8,-8,-8,-8,-1,7,4,5,5,-4,6,6,-3};
        System.out.println(longestConsecutive(nums));
    }

    public static int longestConsecutive(int[] nums) {
        // 确保边界问题，如果length=1后面的for循环给map加数据是不走的
        if(nums.length == 1) return 1;
        // 通过set给数组去重
        Set<Integer> set = new HashSet<>();
        for(int num : nums){
            set.add(num);
        }

        if(set.size() == 1) return 1;
        // 去重完再排序，set只保证去重，不保证排序
        List<Integer> collect = new ArrayList<>(set);
        Collections.sort(collect);
        Map<String, Integer> map = new HashMap<>();
        int from = 0, bigest = 0;
        // index从1开始遍历，通过往后比的方式防止数组越界
        for (int i = 1; i < collect.size(); i++) {
            // 后一个跟前一个做比较，如果差不等于1 说明不连续，将这段数组作为key，长度作为value。
            // from记录一下每段数组是从哪里开始切
            if(collect.get(i) - 1 != collect.get(i-1)){
                // subList是左闭右开的，因为我们是从1开始遍历的，当i与i-1的差不等于1，i是不需要加入到key中的
                List<Integer> list = collect.subList(from, i);
                map.computeIfAbsent(String.valueOf(list), k -> list.size());
                from = i;
            }
            // 处理1，2，3，4这种一直都是连续到底的数组
            if(i == collect.size() - 1){
                // 左闭右开，得把右边的也加上
                List<Integer> list = collect.subList(from, i + 1);
                map.computeIfAbsent(String.valueOf(list), k -> list.size());
            }
        }
        // 遍历map来找出value是最大的，就是连续最长的数字序列
        Set<Map.Entry<String, Integer>> entries = map.entrySet();
        for(Map.Entry entry : entries){
            if(bigest < (int) entry.getValue()) bigest = (int) entry.getValue();
        }
        return bigest;
    }
}
```


```java

Set<Map.Entry<String, Integer>> entries = map.entrySet();
for(Map.Entry entry : entries){
    if(bigest < (int) entry.getValue()) bigest = (int) entry.getValue();
}

// 这三行代码可以优化为以下两种方式
// 直接取最大值，但是只能针对值来操作
Collections.max(map.values());
// 比较最大value，获得Entry，可以通过Entry获得key和value
map.entrySet().stream().max(Map.Entry.comparingByValue());

```



虽然我上面的写法也过了，但是打开题解后才发现，题目要求使用O(n)，使用排序的话是O(logn)，不符合题目要求，这就有点不知道怎么弄了，最后还是学习了灵神的实现，贴上来看一下。
使用Set集合去重是一致的，但是去重后灵神的算法就没有排序了，if(st.contains(x-1)) 就是去找最小的一个数（神操作+1），例如2，1，3，4，第一次进来x=2，if条件中是可以判断出来是有小于2的连续的数的，就跳过2，第二次进来就是1，if条件判断发现没有比1小的了，那么，1就是连续序列的起点。
接下来就是while循环去往下找比x大1的数，然后++，例如2，1，3，4，x=1时y=2，while循环结束后y=5，接着就是找出序列中最大的数，y-x这里来计算以下共计多少个数，5-1=4，那么最大长度就是4（神操作+2）。 

这思路，只能说是叹为观止，难以望其项背

```java
public static int longestConsecutive(int[] nums) {
    int ans = 0;
    Set<Integer> st = new HashSet<>();
    for (int num : nums) {
        st.add(num); // 把 nums 转成哈希集合
    }
    for (int x : st) { // 遍历哈希集合
        if (st.contains(x - 1)) {
            continue;
        }
        // x 是序列的起点
        int y = x + 1;
        while (st.contains(y)) { // 不断查找下一个数是否在哈希集合中
            y++;
        }
        // 循环结束后，y-1 是最后一个在哈希集合中的数
        ans = Math.max(ans, y - x); // 从 x 到 y-1 一共 y-x 个数
    }
    return ans;
}
```