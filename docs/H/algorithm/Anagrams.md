# 49 字母异位词

给你一个字符串数组，请你将 字母异位词 组合在一起。可以按任意顺序返回结果列表。

输入: strs = ["eat", "tea", "tan", "ate", "nat", "bat"]

输出: [["bat"],["nat","tan"],["ate","eat","tea"]]

思路：遍历数组后，将字符串进行排序并放到Map<String, List<String>>中，将排序后的String作为key，原值作为value添加到list中。

这是借鉴了题解的解法，我自己原先的解法是：也是通过map来记录，key也是排序后的String，但是我想的要通过两层的循环来将数组遍历两遍来和key进行比较，是线上还是比较繁琐。

```java
public List<List<String>> groupAnagrams(String[] strs){
    Map<String, List<String>> map = new HashMap<>();
    for(String str : strs){
        char[] sorted = str.toCharArray();
        Arrays.sort(sorted);
        map.computeIfAbsent(new String(sorted), k -> new ArrayList<>()).add(str);
    }
    return new ArrayList<>(map.values());
}

```

> 介绍一下map中的这两个方法
> computeIfAbsent: 两个入参，第一个是key，第二个是Function，如果key不存在的话，就执行第二个参数的Function，上面的例子我们也可以看到，如果key不存在，就创建一个空的List。如果key存在则不执行Function。
> computeIfPresent: 同样也是两个参数，但是如果key存在的话才会执行，如果key不存在就不执行第二个Function参数了。