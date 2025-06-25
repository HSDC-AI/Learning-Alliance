# 相向双指针

## No 167 两数之和 II - 输入有序数组

维护两个指针，一个从头开始，一个从尾开始。
因为数组是一个有序数组，所以可以得到如下的推导：
如果头尾两个指针对应的数字相加大于target，那么就认为尾部的数不管加数组中的哪个数，都是会大于target，就把它排掉，R-1位。
同理，头尾两个指针对应的数小于target的话，那就说明头部指针不管加哪个数都是小于target的，那就把头指针也排掉，L+1位。
最后两个指针对应的数相加得到target的时候，就可以返回结果了，并且因为题目中定义的是从1开始的index，那么LR就都加一

```java
public int[] twoSum(int[] numbers, int target) {
        int[] result = new int[2];
        int L = 0, R = numbers.length - 1;
        while (true){
            if(numbers[L] + numbers[R] > target){
                R--;
                continue;
            }
            if(numbers[L] + numbers[R] < target){
                L++;
                continue;
            }
            if (numbers[L] + numbers[R] == target){
                result[0] = L + 1;
                result[1] = R + 1;
                break;
            }
        }
        return result;
    }
```

## 两数之和2

这是力扣第一题，也是求两数之和，但是我们要返回那两个数的index，这样就不可以排序了。而相向指针的前提条件是需要先排序，所以创建了一个temp 数组，用来记录加起来是target的两个数字，然后再做一次循环，去找temp array中和nums相同的数的index，这个时候就需要创建一个变量来记录一下第一位已经更新了，不然当遇到重复元素的时候，还是会把第一位冲掉


```java
public int[] twoSum(int[] nums, int target) {
    int[] temp = Arrays.copyOf(nums, nums.length);
    Arrays.sort(temp);
    int [] result = new int[2];
    int [] tempResult = new int[2];
    int L = 0, K = nums.length-1;

    while (true){
        if(temp[L] + temp[K] == target) {
            tempResult[0] = temp[L];
            tempResult[1] = temp[K];
            break;
        }

        if(temp[L] + temp[K] > target){
            K--;
        }

        if(temp[L] + temp[K] < target){
            L++;
        }
    }
    boolean isUpdatedFirst = false;
    for(int i=0;i<nums.length;i++){
        if(tempResult[0] == nums[i] && !isUpdatedFirst ) {
            result[0] = i;
            isUpdatedFirst = true;
        }

        if(tempResult[1] == nums[i]) result[1] = i;
    }
    return result;
}
```


## 三数之和

初看题目后一脸懵，后面看了解析后，才知道原来可以接着使用相向指针去解这道题。但是一个难点就是这其中是三个指针，i j k。 题目要求顺序无所谓那就先排序，可以避免很多次后续的比较。第一个代码快是自己借鉴完后写的，没有三个优化，超时了。又翻回去看解析才发现原来还是有迹可循，通过对固定index的item进行比较会得到更多的信息。

这里也学到了一个思路，如果只去比较两个数的结果，那么就只能得到O(1)的结果，也就是一个结果，没有任何其他的信息。
但是如果比较一些有规律的数，比如排序后，nums[i]（当前数） + nums[i+1] + nums[i+2] 这三个最小数的和如果大于0，那么当前数和后面任意两个数相加都会大于0。 那么这里就通过一个判断条件，得到了更多的信息。

还有在k--; j++的时候也要跳过重复item，这样会节省很多时间


```java
int j = i + 1, k = nums.length - 1;
// i 这个指针不变，要遍历i后面的元素，是否和i相加等于0
while (j < k){
    int sum = nums[i] + nums[j] + nums[k];
    if(sum == 0){
        result.add(List.of(nums[i],nums[j],nums[k]));
        j++;
        // 跳过重复元素，上面只会跳过i，jk也要手动跳过一次
        while (j < k){
            if (nums[j] == nums[j-1]){
                j++;
            }
        }
        k--;
        while (j < k){
            if (nums[k] == nums[k+1]){
                k--;
            }
        }
    }else if(sum > 0){
        k--;
    }else if(sum < 0){
        j++;
    }
}
```

```java
// 先给数组排个序，让我们可以借鉴两数之和的思路
nums = Arrays.stream(nums).sorted().toArray();
List<List<Integer>> result = new ArrayList<>();
List<Integer> array;
// i < nums.length-2 是要给jk留位置
for (int i = 0; i < nums.length-2; i++) {
    // 优化1 如果当前数+当前数后两个数的和 > 0，则说明当前数和后面的任意两个数加起来都大于0，没必要再找了
    if(nums[i] + nums[i + 1] + nums[i + 2] > 0) break;
    // 优化2 如果当前数+最大的两个数<0,说明当前数和后面的任意数的和都是小于0的，当前数就没必要往下执行了，但是下一个数又比当前数大，就继续找
    if(nums[i] + nums[nums.length-1] + nums[nums.length-2] < 0) continue;
    // 因为不可以有重复的，当前和上一个item相同就跳过
    if(i > 0 && nums[i] == nums[i-1]) continue;

    int j = i + 1, k = nums.length - 1;
    // i 这个指针不变，要遍历i后面的元素，是否和i相加等于0
    while (j < k){
        int sum = nums[i] + nums[j] + nums[k];
        if(sum == 0){
            result.add(List.of(nums[i],nums[j],nums[k]));
            j++;
            // 优化3 跳过重复元素，上面只会跳过i，jk也要手动跳过一次
            while (j < k && nums[j] == nums[j-1]) j++;
            k--;
            while (j < k && nums[k] == nums[k+1]) k--;
        }else if(sum > 0){
            k--;
            while (j < k && nums[k] == nums[k+1]) k--;
        }else if(sum < 0){
            j++;
            while (j < k && nums[j] == nums[j-1]) j++;
        }
    }
}
return result;
```