# No 167 两数之和 II - 输入有序数组

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