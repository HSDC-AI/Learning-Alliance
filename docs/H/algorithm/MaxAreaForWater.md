# 11 

使用双指针去解这道题，刚开始看的时候思路上有点没想明白，看了下评论中的思路，豁然开朗，发现是动态的求一下两个边的面积然后找出最大的。以下是我的实现

```java
/**
 *
 11. 盛最多水的容器
 提示
 给定一个长度为 n 的整数数组 height 。有 n 条垂线，第 i 条线的两个端点是 (i, 0) 和 (i, height[i]) 。

 找出其中的两条线，使得它们与 x 轴共同构成的容器可以容纳最多的水。

 返回容器可以储存的最大水量。
 输入：[1,8,6,2,5,4,8,3,7]
 输出：49

 说明：你不能倾斜容器。

 思路：使用双指针，从0开始循环，l和r，l 和 r 取最小值min，使用 min * （r-l) 也就是两条线之间的距离 计算一下面积，为什么加1呢，是因为要从1开始，0开始的话就算不了两条线之间的面积了。
 如果l < r ,那么l++，如果 r < l ,那么r--。然后再计算面积，直到l=r，退出循环
 */
public class MaxAreaForWater {
    public static void main(String[] args) {
//        int[] height = {1,8,6,2,5,4,8,3,7};
        int[] height = {0};
        System.out.println(maxArea(height));
    }

    public static int maxArea(int[] height) {
        int l=0, r=height.length-1, max = 0;
        // 当两个指针碰面时说明已经循环完毕，结束循环
        while (l != r) {
            // 找一下两个指针中线条最短的，因为只有最短的线条才控制着桶的高度
            int min = Math.min(height[l], height[r]);
            // 计算一下两条边的距离，也就是桶的宽度
            int dist = r - l;
            // 计算桶的面积，然后找到当前最大的值
            max = Math.max(max, min * dist);
            // 如果左边的桶边低于右边的，那么就把左边的线往右挪动1位。
            if (height[l] < height[r]) {
                l++;
                continue;
            }
            // 如果右边的桶边低于或等于左边的，那么就往左移动一位。等于是为了防止两个边都相等后造成死循环
            if (height[r] <= height[l]) {
                r--;
            }
        }
        return max;
    }
}
```