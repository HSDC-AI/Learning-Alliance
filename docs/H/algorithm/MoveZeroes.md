# 283

列一下自己的写法，虽然这道题过了，但是时间和空间复杂度有点高，而且没有完全满足要求去进行原地操作，毕竟新创建了一个list。而且这道题是归到了双指针里，但是没想明白双指针怎么做。下面我贴了灵神的双指针实现。

```java
/**
 * 283 移动零
 *
 * 给定一个数组 nums，编写一个函数将所有 0 移动到数组的末尾，同时保持非零元素的相对顺序。
 *
 * 请注意 ，必须在不复制数组的情况下原地对数组进行操作。
 *
 * 示例 1:
 *
 * 输入: nums = [0,1,0,3,12]
 * 输出: [1,3,12,0,0]
 * 示例 2:
 *
 * 输入: nums = [0]
 * 输出: [0]
 */
public static List<Integer> moveZeroes1(int[] nums) {
    // 额外使用一个list去记录非0的index
    List<Integer> list = new ArrayList<>();
    for (int i = 0; i < nums.length; i++) {
        if(nums[i] != 0 ) list.add(i);
    }
    // 将非0的index重新覆盖到数组上 
    for (int i = 0; i < list.size(); i++) {
        nums[i] = nums[list.get(i)];
    }
    // 计算是否还有空位没有补0
    int zeroNums = nums.length - list.size();
    if( zeroNums > 0){
        // 从list的长度开始，往后填0
        for (int i = list.size(); i < nums.length; i++) {
            nums[i] = 0;
        }
    }
    return Arrays.stream(nums).boxed().collect(Collectors.toList());
}
```

再列以下灵神的写法，i0记录的是最左边的0的位置，数组开头无非就是2种，1是0开头，2是非0开头，i0默认值是0，也就是在第二种case下，即便是非0开头，进入了if条件，也只会自己覆盖下自己而已。

然后非零数字每次和i0进行交换，就完成了这道题。

```java
public void moveZeroes(int[] nums) {
    int i0 = 0;
    for (int i = 0; i < nums.length; i++) {
        if (nums[i] != 0) {
            // 交换 nums[i] 和 nums[i0]
            int tmp = nums[i];
            nums[i] = nums[i0];
            nums[i0] = tmp;
            i0++;
        }
    }
}
```