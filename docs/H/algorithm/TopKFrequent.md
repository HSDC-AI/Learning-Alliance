# TOP K 前K个高频元素

这道题主要是通过map和priorityQueue，来实现的。

重点1：需要设置PriorityQueue的排序顺序，使用map.get(a) - map.get(b) 来排序，这样的话就避免了通过a,b key的排序，也就保证了我们队列中元素顺序是按value来排序的，堆低就可以存放最大值，堆顶是最小值了。

重点2：保证队列中只有k个元素，在队列达到k size后，就需要比对当前key对应的频率和队列头对应的频率哪一个更大，大的放在队列头中。因为我们已经针对队列进行了排序，所以这里可以保证队列头就是频率最小的。

重点3：在给数组赋值的时候，要从后往前赋值，也是因为我们使用的是小顶堆的原因。

在实现的时候我走了点弯路，因为没有特别设置使用map value进行排序，而对key进行了排序，导致在和堆顶进行比较时，虽然比堆顶小，但是会比堆顶的子节点大，但是这个数又并没有塞入到队列中的bug。

为了解决这个bug，又针对子节点进行了比较，这种方式是错误的。因为这样破坏了父子有序性和完全二叉树结构。

```java
/**
 * No.347. 前K个高频元素
 */
public class TopKFrequent {
    public static void main(String[] args) {
        int[] nums = {2,3,4,1,4,0,4,-1,-2,-1};
        TopKFrequent topKFrequent = new TopKFrequent();
        System.out.println(Arrays.toString(topKFrequent.topKFrequent(nums, 2)));
    }

    public int[] topKFrequent(int[] nums, int k) {
        // 使用map记录每一个数字出现的频率，merge可以很好的处理重复数字，当数字第一次加到map后，默认值是1，往后如果有map里找到了这个key，那么就执行sum操作
        Map<Integer, Integer> map = new HashMap<>();
        for (int num : nums) {
            map.merge(num, 1, Integer::sum);
        }
        // 创建一个小顶堆队列，堆顶元素是最小值，按照map的值进行升序排序
        PriorityQueue<Integer> queue = new PriorityQueue<>((a, b) -> map.get(a) - map.get(b));
        for(Integer key : map.keySet()){
            // 当队列size小于要求的k长度时，直接添加元素
            if(queue.size() < k){
                queue.offer(key);
            }else{
                // 当size达到k长度时，就需要判断下当前key对应的频率是否大于堆顶key对应的频率，如果大于，那么就移除堆顶元素，并将当前key添加到队列中
                if(map.get(key) > map.get(queue.peek())){
                    queue.poll();
                    queue.offer(key);
                }
            }
        }
        int[] result = new int[k];
        // 这里需要从后往前复制，因为堆顶元素是最小值，所以就可以塞到队列的最后一位。
        for (int i = k-1; i >=0 ; i--) {
            result[i] = queue.poll();
        }
        return result;
    }
}
```

以下是相同问题的变种，只不过从数字换成了单词，并且同频的单词之间要按照字典顺序排列。

通过这个例子巩固了以下如何在创建PriorityQueue的时候就规定好排序方式

```java

package BinaryTree;

import java.util.*;

/**
 * No.692, 前K个高频单词
 */
public class TopKFrequentWords {
    public static void main(String[] args) {
        String[] words = new String[]{"glarko","zlfiwwb","nsfspyox","pwqvwmlgri","qggx","qrkgmliewc","zskaqzwo","zskaqzwo","ijy","htpvnmozay","jqrlad","ccjel","qrkgmliewc","qkjzgws","fqizrrnmif","jqrlad","nbuorw","qrkgmliewc","htpvnmozay","nftk","glarko","hdemkfr","axyak","hdemkfr","nsfspyox","nsfspyox","qrkgmliewc","nftk","nftk","ccjel","qrkgmliewc","ocgjsu","ijy","glarko","nbuorw","nsfspyox","qkjzgws","qkjzgws","fqizrrnmif","pwqvwmlgri","nftk","qrkgmliewc","jqrlad","nftk","zskaqzwo","glarko","nsfspyox","zlfiwwb","hwlvqgkdbo","htpvnmozay","nsfspyox","zskaqzwo","htpvnmozay","zskaqzwo","nbuorw","qkjzgws","zlfiwwb","pwqvwmlgri","zskaqzwo","qengse","glarko","qkjzgws","pwqvwmlgri","fqizrrnmif","nbuorw","nftk","ijy","hdemkfr","nftk","qkjzgws","jqrlad","nftk","ccjel","qggx","ijy","qengse","nftk","htpvnmozay","qengse","eonrg","qengse","fqizrrnmif","hwlvqgkdbo","qengse","qengse","qggx","qkjzgws","qggx","pwqvwmlgri","htpvnmozay","qrkgmliewc","qengse","fqizrrnmif","qkjzgws","qengse","nftk","htpvnmozay","qggx","zlfiwwb","bwp","ocgjsu","qrkgmliewc","ccjel","hdemkfr","nsfspyox","hdemkfr","qggx","zlfiwwb","nsfspyox","ijy","qkjzgws","fqizrrnmif","qkjzgws","qrkgmliewc","glarko","hdemkfr","pwqvwmlgri"};
        TopKFrequentWords topKFrequentWords = new TopKFrequentWords();
        System.out.println(topKFrequentWords.topKFrequent(words, 14));
    }

    public List<String> topKFrequent(String[] words, int k) {
        Map<String, Integer> map = new HashMap<>();
        for (String word : words) {
            map.merge(word, 1, Integer::sum);
        }
        // 重中之重，这里有两层逻辑，第一层是按频率排序，第二层是同频的情况，按字典表升序排
        // 这里的排序需要按条件来拆分，如果频率相同，那就需要按字典升序进行排序
        // a.compareToIgnoreCase(b) 如果a在b前，那就会返回负数，
        // eg: a:aa, b:aaa, a.compareToIgnoreCase(b) 会得到负数，说明aa在前，但是根据需求，aaa才应该放到堆顶，所以这里取反
        // 按频率排序就是 a的value 大于 b的value，这里很好理解
        PriorityQueue<String> queue = new PriorityQueue<>((a,b) -> {
            if(map.get(a) - map.get(b) == 0){
                return -a.compareToIgnoreCase(b);
            }else{
                return map.get(a) - map.get(b);
            }
        });
        
        // 这里和TopKFrequent处理的思路不同，之前那个是先比较，在放入队列，这个是先放入队列，因为堆顶肯定是最小的，而且超过了size，就可以直接删除
        for(String key : map.keySet()){
            queue.offer(key);
            if(queue.size() > k){
                queue.poll();
            }
        }
        String[] arrays = new String[k];
        for (int i = k - 1; i >=0; i--) {
            String poll = queue.poll();
            arrays[i] = poll;
        }
        List<String> result = Arrays.asList(arrays);
        return result;
    }
}

```