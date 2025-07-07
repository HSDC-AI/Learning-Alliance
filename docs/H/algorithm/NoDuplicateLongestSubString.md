# 3 无重复字符的最长子串

这是一道通过滑动窗口来解决的题，老实说解法不是我做的，是找AI生成的，我的做法其实也是使用滑动窗口的想法，但是边界条件和index移动有很大的问题，也就一直没修好，我滑动的时候直接就把左指针跳到了重复字符的index上了，这种想法应该是属于动态的滑动窗口，但是我没写明白，也没从重复字符的下一位一个一个的遍历，这就是一个问题。而且我在判断字符是否重复的时候使用for循环了窗口的字符串，就导致了时间复杂度又升高了。也是一个问题。

而AI给的解决方案中，使用Map记录字符最近一次出现的位置，也就可以通过map来控制左指针的移动。举例：abca的时候，循环到了第二个a，左指针就移动到了b上，下一次循环的时候就从bca开始。

```java
/**
 * 3. 无重复字符的最长子串
 * 给定一个字符串 s ，请你找出其中不含有重复字符的 最长 子串 的长度。
 * 示例 1:
 * 输入: s = "abcabcbb"
 * 输出: 3
 * 解释: 因为无重复字符的最长子串是 "abc"，所以其长度为 3。
 *
 * 示例 2:
 * 输入: s = "bbbbb"
 * 输出: 1
 * 解释: 因为无重复字符的最长子串是 "b"，所以其长度为 1。
 *
 * 示例 3:
 * 输入: s = "pwwkew"
 * 输出: 3
 * 解释: 因为无重复字符的最长子串是 "wke"，所以其长度为 3。
 * 请注意，你的答案必须是 子串 的长度，"pwke" 是一个子序列，不是子串。
 * p和k中间包含了2个w
 */
public class NoDuplicateLongestSubString {
    public static void main(String[] args) {
        String s = "abcabcbb";
        System.out.println(lengthOfLongestSubstring(s));
    }
    public static int lengthOfLongestSubstring(String s) {
        if (s == null || s.isEmpty()) return 0;
        // 存储字符最近出现位置
        Map<Character, Integer> charIndexMap = new HashMap<>();
        // 设置两个指针，左右。左指针从头开始，然后遍历右指针
        int left = 0, maxLen = 0;
        // 遍历右指针
        for (int right = 0; right < s.length(); right++) {
            // 获取当前指针位置上的元素值
            char c = s.charAt(right);
            // 如果map中已经包含了当前元素，说明出现过这个元素了，并且当前元素的位置一定是要大于等于左指针，因为左右指针形成的窗口是动态的
            if (charIndexMap.containsKey(c) && charIndexMap.get(c) >= left) {
                // 左指针跳到重复字符的下一位
                left = charIndexMap.get(c) + 1;
            }
            // 更新字符位置
            charIndexMap.put(c, right);
            // 更新最大长度
            maxLen = Math.max(maxLen, right - left + 1);
        }
        return maxLen;
    }
}
```

我的解法

```java

public int lengthOfLongestSubstring(String s) {
        if(s == null || s.isEmpty()) return 0;
        int i = 0, j = 1, ans = 0;
        char[] array = s.toCharArray();
        while (true){
            if(i == array.length-1) {
                ans= Math.max(1, ans);
                break;
            }
            char[] window = new char[j-i+1];
            System.arraycopy(array, i, window, 0, j-i+1);
            boolean hasDuplicate = hasDuplicate(window, array[j]);
            if(!hasDuplicate){
                ans = Math.max(ans, window.length);
            }else{
                i = j;
                j = i + 1;
                if(ans == 0) ans = 1;
            }
            if(window.length == array.length) break;
            if(j != array.length-1 && !hasDuplicate) j++; else break;
        }
        return ans;
    }

    private static boolean hasDuplicate(char[] s, char target){
        if(s.length <= 1) return false;
        int count = 0;
        for(int i = 0; i < s.length; i++){
            if(s[i] == target) count++;
        }
        return count > 1;
    }
```
