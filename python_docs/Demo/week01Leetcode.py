from typing import List

class Solution: 
    # [两数之和](https://leetcode.cn/problems/two-sum/) 
    # 输入：nums = [2,7,11,15], target = 9
    # 输出：[0,1]

    def twoSum(self, nums: List[int], target: int) -> List[int]:
        map = {}
        for (i, item) in enumerate(nums):
            key = target - item
            value = map.get(key)
            if value is not None:
                return [value, i]
            map[item] = i
        return []
    

    # [有效的括号](https://leetcode.cn/problems/valid-parentheses/)
    # 给定一个只包括 '('，')'，'{'，'}'，'['，']' 的字符串 s ，判断字符串是否有效。
    # 示例 1：
    # 输入：s = "()"
    # 输出：true
    def isValid(self, s: str) -> bool:
        stack = []
        map = {")": "(", "}": "{", "]": "["}
        for chat in s:
            if map.get(chat) is not None:
                if stack[0] == map.get(chat):
                    stack.remove(stack[0])
                    continue
                stack.insert(0, chat)    
            else:
                stack.insert(0, chat)    
        return len(stack) == 0




    # [翻转字符串](https://leetcode.cn/problems/reverse-string/)
    # 编写一个函数，其作用是将输入的字符串反转过来。输入字符串以字符数组 s 的形式给出。
    # 不要给另外的数组分配额外的空间，你必须原地修改输入数组、使用 O(1) 的额外空间解决这一问题。
    # 示例 1：
    # 输入：s = ["h","e","l","l","o"]
    # 输出：["o","l","l","e","h"]
    def reverseString(self, s: List[str]) -> None:
        """
        Do not return anything, modify s in-place instead.
        """
        leading, trailing = 0, len(s) - 1
        while leading < trailing:
            s[leading], s[trailing] = s[trailing], s[leading]            
            leading, trailing = leading + 1, trailing - 1
        print(s)
        




if __name__ == "__main__":
    solution = Solution()
    # print(solution.twoSum([2,7,11,15], 9))
    print(solution.isValid("[]()"))
    print(solution.reverseString(["h","e","l","l","o"]))