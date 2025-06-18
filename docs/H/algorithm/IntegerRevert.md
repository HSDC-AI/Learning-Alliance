# 整数反转

这是力扣的第七题，[整数反转](https://leetcode.cn/problems/reverse-integer/description/)

看题干要求数的范围正好是Ineger的区间范围，第一次以为是包含两头的最大值和最小值，但是在提交的过程中出现了正好result是最大的情况，于是就改成了 >= Integer.MAX_VALUE。

最初的想法本来是把数字转成字符串数组，然后倒叙输出数字，并最后计算±，但是前几天看到一个通过%去取最后一位数字的算法，这样的话就就可以取到每一位数字，就不需要数组了，然后紧接着又想起来了栈，但是调查过后发现Stack因为性能问题是不推荐使用的，而且通过Deque（Queue的一个子类）也可以实现FILO，这样就可以循环输出队列，实现字符串反转了。

关于正负的问题，可以直接通过 * -1 来解决。也可以通过Math.abs()来取绝对值。

还有个关键的实现是通过Math.pow()来获取某个数的某个方值，这样正好能让我们的数组在位数上进一。

```java
import java.util.ArrayDeque;
import java.util.Deque;

/**
 * No.7
 */
public class IntegerRevert {
    public static void main(String[] args) {
        System.out.println(new IntegerRevert().reverse(1563847412));
    }

    public int reverse(int x) {
        if(x >= Integer.MAX_VALUE || x < Integer.MIN_VALUE){
            return 0;
        }
        Deque<Integer> queue = new ArrayDeque<>();
        boolean isNegative = x < 0;
        // 取绝对值
        int temp = isNegative ? x * -1 : x;
        // 计算数字位数，如果通过queue的size来处理循环的话循环会少，因为后面是通过使用pop()方法来弹出队列的，size直接就跟着减少了。如果不用这个临时变量，则可以使用peek()查看栈顶元素
        int numberOfDigits = 0;
        // 循环中会把temp这个临时的数字除以10，等到小于0后，也就意味着我们所有位数上的数字都加到了队列里了
        while( temp > 0){
            // 取最后以为数
            int lastNumber =  temp % 10;
            // 队列是空的情况，最后一位数是0的话就不添加到队列上，队列如果不是空的，也就意味着反转的数上低位数已经有数字了，那么高位数上也可以存在0
            if(lastNumber != 0){
                queue.push(lastNumber);
            }else if(queue.size() != 0){
                // 压到队列头部
                queue.push(lastNumber);
            }
            temp = temp / 10;
            numberOfDigits++;
        }
        int result = 0;
        for (int i = 0; i < numberOfDigits; i++){
            // 循环次数肯定是要比队列size大的，等到size为0的时候就没必要循环队列了
            if(queue.size() == 0){
                break;
            }
            // 从栈顶弹出
            Integer pop = queue.pop();
            // 取10的i次方，这样数字可以进位
            double pow = pop * Math.pow(10, i);
            result += pow;
            // 控制边界
            if(result >= Integer.MAX_VALUE ){
                return 0;
            }
        }
        // 控制正负
        result = isNegative ? result * -1 : result;
        return result;
    }
}

```