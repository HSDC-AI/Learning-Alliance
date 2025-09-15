




a = 100
a = "asdasd"  

# print(a)

# message = "你好，{0}, 成绩提升了{1: .1f}, 继续努力".format("小名", 17.123)
# print(message)


# r = 2.5
# s = 3.14 * r ** 2

# circle_info = f"半径为{r}的圆的面积为{s: .2f}"
# print(circle_info)


# names = ['a', 'b', 'c']
# print(f"列表长度: {len(names)}") # 长度
# print(f"第一个元素: {names[0]}") # 第一个
# print(f"最后一个元素: {names[-1]}") # 最后一个
# print(f"倒数第二个元素: {names[-2]}") # 倒数第二个
# print(f"从第二个到第三个元素: {names[1:3]}") # 从第二个到第三个
# names.append('d') # 添加到末尾
# print(f"添加到末尾后的列表: {names}")
# names.insert(0, 'e') # 插入到第一个
# print(f"插入到第一个后的列表: {names}")
# names.pop() # 删除末尾
# print(f"删除末尾后的列表: {names}")
# names.pop(0) # 删除第一个
# print(f"删除第一个后的列表: {names}")
# names[0] = 'f' # 修改第一个
# print(f"修改第一个后的列表: {names}")
# names.remove('c') # 删除指定元素
# print(f"删除指定元素后的列表: {names}")
# names.sort() # 排序
# print(f"排序后的列表: {names}")
# names.reverse() # 反转
# print(f"反转后的列表: {names}")
# names.clear() # 清空列表
# print(f"清空后的列表: {names}")

# tuple
# 元组一旦初始化就不能修改
# names_tuple = ('a', 'b', 'c')
# print(f"元组长度: {len(names_tuple)}") # 长度
# print(f"第一个元素: {names_tuple[0]}") # 第一个
# print(f"最后一个元素: {names_tuple[-1]}") # 最后一个
# print(f"倒数第二个元素: {names_tuple[-2]}") # 倒数第二个
# print(f"从第二个到第三个元素: {names_tuple[1:3]}") # 从第二个到第三个


# one_tuple = (1,) # 一个元素的元组 注意避免歧义加一个逗号
# a_tuple = (1, 2, [3, 4]) # 元组中可以包含列表
# a_tuple[2][0] = 5 # 元组中包含的列表可以修改， 但是不能修改元组本身
# print(f"修改后的元组: {a_tuple}")


# age = 20
# if age >= 18:
#     print("adult")
# elif age >= 6:
#     print("teenager") # 注意这里没有else
# else:
#     print("kid")

# a = 10
# if a:
#     print("a is not 0") # 非0为True
# else:
#     print("a is 0") # 0为False
    
# x = "aa"
# if x:
#     print("x is not empty") # 非空为True
# else:
#     print("x is empty") # 空为False

# input
# name = input("请输入你的名字: ")
# print(f"你好, {name}")

# s = input("请输入的年龄: ")
# s_strip = input("请输入的年龄: ").strip()  # 去除空格
# print(f"你的年龄是: {s}")
# print(f"你的年龄是: {s_strip}")
# s = int(s)
# if s > 18:
#     print("你已经成年了")
# else:
#     print("你还没有成年")


# 模式匹配
# score = input("请输入分数: ").strip()
# score = int(score)
# match score:
#     case x if x < 10:
#         print('score is less than 10.')
#     case 15:
#         print('score is 15.')
#     case 11 | 22:
#         print('score is 11 or 22.')
#     case x if x > 60 and x < 100:
#         print('score is greater than 60 and less than 100.')
#     case _: # _表示匹配到其他任何情况
#         print('score is other.')

# 列表匹配 
# 用args = ['gcc', 'hello.c']存储，下面的代码演示了如何用match匹配来解析这个列表：
# args = ['gcc', 'hello.c', 'world.c']
# match args:
#     case ['gcc']: 
#         # 如果仅出现gcc 报错
#         print('gcc: missing source file(s).')
#     case ['gcc', file1, *files]: 
#         # 第一个元素必须是字符串 'gcc'
#         # 第二个元素会被赋值给变量 file1
#         # 剩余的所有元素会被收集到变量 files 中（作为列表）
#         # case ['gcc', file1, *files]: 至少两个元素
#         # case ['gcc', *files]: 仅 gcc就能匹配上了   *files是可选传入的
#         # 如果出现gcc 后面跟着一个文件名和多个文件名 打印gcc compile: hello.c, world.c
#         print('gcc compile: ' + file1 + ', ' + ', '.join(files))
#     case ['clean']: 
#         # 如果出现clean 打印clean
#         print('clean')
#     case _:
#         # 如果出现其他情况 打印invalid command.
#         print('invalid command.')

# 循环
# names = ['a', 'b', 'c']
# for name in names:
#     print(name)
    
# sum = 0
# for i in [1, 2, 3, 4, 5]:
#     sum += i
# print(sum)

# sum = 0
# for i in range(1, 10):
#     sum += i
# print(sum)

# sum = 0
# while sum < 10:
#     sum += 1
#     print(sum)
#     if sum == 5:
#         continue
#     print(sum)
#     if sum == 8:
#         break
#     print(sum)
    


# Dict

# dict = {
#     'Michael': 95,
#     'Bob': 75,
#     'Tracy': 85
# }
# print(dict)
# print(len(dict.keys())) # 打印键的数量
# print(len(dict)) # 打印键值对的数量

# dict['Adam'] = 67
# dict['Jack'] = 90
# print(dict['Adam'])

# if 'Bob' in dict:
#     print('Boc is in dict')
# else:
#     print('Boc is not in dict')
    
# print(dict.get('Bob')) # 获取Bob的值 如果Bob不存在 返回None
# print(dict.get('Bob', 100)) # 获取Bob的值 如果Bob不存在 返回100
# print(dict.get('Bobcccc', 100)) 

# dict.pop('Bob') # 删除Bob
# print(dict)

# dict.popitem() # 删除最后一个键值对
# print(dict)

# dict.clear() # 清空字典
# print(dict)


# # Set

# s = {1, 2, 3, 4, 5}
# print(s)

# s.add(6) # 添加元素
# print(s)

# s.remove(1) # 删除元素
# print(s)

# s.pop() # 删除最后一个元素

# func

# print(f"abs(10) = {abs(10)}")
# print(f"abs(-20) = {abs(-20)}")
# print(f"abs(10.5) = {abs(10.5)}")

# print(f"max(1, 2, 3, 4, 5) = {max(1, 2, 3, 4, 5)}")

# print(f"int('123') = {int('123')}")
# print(f"int(12.3) = {int(12.3)}")
# print(f"float('12.34') = {float('12.34')}")
# print(f"str(1.23) = {str(1.23)}")
# print(f"bool(1) = {bool(1)}")
# print(f"bool('') = {bool('')}")


# a = abs
# print(f"a = abs, a(-10) = {a(-10)}")

# n1 = 244

# def my_abs(x):
#     if x >= 0:
#         return x
#     else:
#         return -x

# print(f"my_abs(-10) = {my_abs(-10)}")



# from func_test import my_abs
# print(f"my_abs(-10) func_test = {my_abs(-10)}")


# from func_test import move
# import math
# print(f"move(100, 100, 60, math.pi/6) = {move(100, 100, 60, math.pi/6)}")

# from func_test import quadratic
# print('quadratic(2, 3, 1) =', quadratic(2, 3, 1))
# print('quadratic(1, 3, -4) =', quadratic(1, 3, -4))
# if quadratic(2, 3, 1) != (-0.5, -1.0):
#     print('测试失败')
# elif quadratic(1, 3, -4) != (1.0, -4.0):
#     print('测试失败')
# else:
#     print('测试成功')


# from func_test import power
# print(f"power(5) = {power(5)}")
# print(f"power(5, 2) = {power(5, 3)}")


# from func_test import enroll
# enroll('Sarah', 'F')
# enroll('Bob', 'M', 7)
# enroll('Adam', 'M', city='Tianjin')


# from func_test import add_end
# print(add_end([1, 2, 3]))
# print(add_end())
# print(add_end())
# print(add_end([1, 2, 3]))
# print(add_end())





# # 关键字参数
# def person(name, age, **kw):
#     print('name:', name, 'age:', age, 'other:', kw)

# print(person('Michael', 30))
# print(person('Bob', 35, city='Beijing'))
# print(person('Adam', 45, gender='M', job='Engineer'))



# 切片
# L = ['Michael', 'Bob', 'Tracy', 'Sarah', 'Jack', 'Tom', 'Jerry']
# print(f"取前3个：{L[0:3]}")
# print(f"取前3个，第一个0可以省略：{L[:3]}")
# print(f"从索引1开始，取到索引3（不包括3）：{L[1:3]}")
# print(f"最后两个：{L[-2:]}")
# print(f"倒数第一个：{L[-1]}")
# print(f"前10个每两个取一个：{L[:10:2]}")
# print(f"所有元素每两个取一个：{L[::2]}")
# print(f"所有元素倒序：{L[::-1]}")
# print(f"复制list：{L[:]}")



## 迭代
# # list
# L = ['Michael', 'Bob', 'Tracy', 'Sarah', 'Jack', 'Tom', 'Jerry']
# for name in L:
#     print(name)

# for i, name in enumerate(L):
#     print(i, name)

# #元组
# for x, y in [(1, 1), (2, 4), (3, 9)]:
#     print(x, y)

# # dict
# d = {'a': 1, 'b': 2, 'c': 3}
# for key in d:
#     print(key)

# for value in d.values():
#     print(value)

# for key, value in d.items():
#     print(key, value)

# # 字符串
# for ch in 'ABC':
#     print(ch)

# # 列表生成式
# L = [x*x for x in range(1, 11)] # 生成1到10的平方
# print(L)

# L = [x*x for x in range(1, 11) if x % 2 == 0] # 生成1到10的平方，只保留偶数
# print(L)

# L = [m + n for m in 'ABC' for n in 'XYZ']
# print(L)

# # dict
# map = {'a': 1, 'b': 2, 'c': 3}
# L1 = [ k + '=' + str(v) for k, v in map.items()]
# print(L1) # ['a=1', 'b=2', 'c=3']
    
# 生成器

# L = [x * x for x in range(10)]
# print(L)

# g = (x * x for x in range(10))
# # print(next(g))
# # print(next(g))
# # print(next(g))
# print("-------------------")
# for n in g:
#     print(n)
# print("-------------------")
# for n in g:
#     print(n)


# def fic(max):
#     # 第一个  第二个 是1, 1, 2, 3  其他的都是前两个数相加
#     n, a, b = 0, 0, 1
#     while(n < max):
#         # print(b)
#         yield b
#         # a, b = b, a + b
        
#         c = a
#         a = b
#         b = c + b
#         n = n + 1
#     return 'done'

# f = fic(5)
# print(next(f))
# print(next(f))
# print(next(f))
# print(next(f))
# print(next(f))

# for n in f:
#     print(n)
    
# # def triangles1():
# #     L = [1]
# #     while True:
# #         yield 
# #         L = [1] + [L[i] + L[i+1] for i in L[:-1]] + [1]

# def triangles():
#     L = [1]
#     while True:
#         yield L
#         lM = [L[i] + L[i+1] for i in range(len(L)-1)]
#         L = [1] + lM + [1]

# t = triangles()
# print(next(t))
# print(next(t))
# print(next(t))
# print(next(t))
# print(next(t))

# 高阶函数

# print(abs(-10))
# x = abs(-10)
# f = abs
# def add(x, y, f):
#     return f(x) + f(y)
# print(add(1, 2, abs))
# print(add(-5, 6, abs))

# def f(x):
#     return x * x

# r = map(f, [1, 2, 3, 4, 5])
# print(r)
# print(list(r))
# # for i in r:
# #     print(i)

# #reduce
# from functools import reduce
# def add(x, y):
#     return x + y

# r = reduce(add, [1, 2, 3, 4, 5])
# print(r)



# def is_odd(x):
#     return x % 2 == 1

# r = list(filter(is_odd, [1, 2, 3, 4, 5]))
# print(r)

# def not_empty(s):
#     return s and s.strip()
# r = list(filter(not_empty, ['A', '', 'B', None, 'C', '  ']))
# print(r)

# # sorted
# r = sorted([36, 5, -12, 9, -21])
# print(r)

# 练习  获取list中的素数

# def _odd_iter():
#     print("🔢 [_odd_iter] 开始生成奇数序列...")
#     n = 1
#     count = 0
#     while True:
#         n = n + 2
#         count += 1
#         print(f"🔢 [_odd_iter] 生成第{count}个奇数: {n}")
#         yield n
        
# def _not_divisible(n):
#     print(f"🔍 [_not_divisible] 创建过滤函数，用于过滤掉能被 {n} 整除的数")
#     def filter_func(x):
#         is_not_divisible = x % n > 0
#         if is_not_divisible:
#             print(f"✅ [filter] {x} ÷ {n} = {x//n}...{x%n} (余数>0，保留)")
#         else:
#             print(f"❌ [filter] {x} ÷ {n} = {x//n} (整除，过滤掉)")
#         return is_not_divisible
#     return filter_func

# def primes():
#     print("🚀 [primes] 素数生成器启动!")
#     print("🚀 [primes] 首先输出唯一的偶数素数: 2")
#     yield 2
    
#     print("🔢 [primes] 创建奇数序列...")
#     it = _odd_iter() # 初始序列
#     step = 1
    
#     while True:
#         print(f"\n📍 [primes] === 第 {step} 轮过滤 ===")
#         print(f"📍 [primes] 向filter请求下一个通过过滤的数字...")
#         print(f"🔄 [primes] filter开始工作，检查_odd_iter生成的数字...")
#         n = next(it) # 返回序列的第一个数
#         print(f"✅ [primes] filter找到通过条件的数字: {n} (这必定是素数!)")
#         yield n
        
#         print(f"🔍 [primes] 用素数 {n} 过滤序列，移除所有 {n} 的倍数...")
#         it = filter(_not_divisible(n), it) # 构造新序列
#         print(f"✨ [primes] 过滤完成，新序列已准备好，等待下一轮...")
#         step += 1

# print("🌟 开始寻找小于100的所有素数:")
# print("=" * 50)

# found_primes = []
# for n in primes():
#     if n < 100:
#         found_primes.append(n)
#         print(f"🎯 找到素数: {n}")
#     else:
#         print(f"🛑 遇到大于等于100的数 ({n})，停止搜索")
#         break

# print("=" * 50)
# print(f"🏆 总结: 小于100的素数共有 {len(found_primes)} 个")
# print(f"🏆 完整列表: {found_primes}")

# print("\n" + "="*60)
# print("🧪 Filter工作机制演示 - 理解为什么会打印那么多数字")
# print("="*60)


# def _odd_iter():
#     n = 1
#     count = 0
#     while True:
#         n = n + 2
#         count += 1
#         yield n
        
# def _not_divisible(n):
#     return lambda x: x % n > 0

# def primes():
#     yield 2
#     it = _odd_iter() # 初始序列
#     while True:
#         n = next(it) # 返回序列的第一个数
#         yield n
#         it = filter(_not_divisible(n), it) # 构造新序列

# for n in primes():
#     if n < 100:
#         print(f"🎯 找到素数: {n}")
#     else:
#         break


# sorted()

# s = sorted([36, 5, -12, 9, -21])
# print(s)

# s = sorted([36, 5, -12, 9, -21], key=abs)
# print(s)

# filtered = filter(lambda x: x > 0, [1, -2, 3, -4])

# print(list(filtered))

# def strSorted():
#     return lambda x: x.startswith('Z')
# s = sorted(['bob', 'about', 'Zoo', 'Credit'], key=strSorted(), reverse=True)
# print(s)


# 返回函数

# def calc_sum(*args):
#     ax = 0
#     for n in args:
#         ax = ax + n
#     return ax

# s = calc_sum(1, 2, 3, 4, 5)
# print(s)

# def lazy_sum(*args):
#     def sum():
#         ax = 0
#         for n in args:
#             ax = ax + n
#         return ax
#     return sum

# s = lazy_sum(1, 2, 3, 4, 5)
# print(s())


# def count():
#     fs = []
#     for i in range(1, 4):
#         def f():
#              return i*i
#         fs.append(f)
#     return fs

# f1, f2, f3 = count()

# print(f1())
# print(f2())
# print(f3())


# def count():
#     fs = []
#     for i in range(1, 4):
#         fs.append(lambda x=i: x*x)
#     return fs

# f1, f2, f3 = count()

# print(f1())
# print(f2())
# print(f3())

# # print(f1())
# # print(f2())   
# # print(f3())


# def createCounter():
#     x = 0
#     def counter():
#         nonlocal x
#         x = x + 1
#         return x
#     return counter

# counterA = createCounter()
# print(counterA())
# print(counterA())


# lambda
# l = list(map(lambda x: x * x, [1, 2, 3, 4, 5]))
# print(l)

# # lambda 相当于以下函数

# def f(x):
#     return x * x


# f = lambda x: x * x
# print(f(5))

# # 也可以作为函数返回
# def build(x, y):
#     return lambda: x * x + y * y

# f = build(2, 3)
# print(f())


# def id_odd(x):
#     return lambda x: x % 2 == 1

# r = list(filter(id_odd, range(1, 20)))
# print(r)

# r = list(filter(lambda x: x % 2 == 1, range(1, 20)))
# print(r)

# 装饰器
# def log(func):
#     def wrapper(*args, **kw):
#         print(f"call {func.__name__}()...")
#         return func(*args, **kw)
#     return wrapper

# @log
# def now():
#     return "2025-01-01"
# print(now())

# def log2(text):
#     def decorator(func):
#         def wrapper(*args, **kw):
#             print(f"{text} call {func.__name__}()...")
#             return func(*args, **kw)
#         return wrapper
#     return decorator

# @log2("execute")
# def now2():
#     return "2025-01-01"
# print(now2())

# from functools import partial
# def power(base, exponent):
#     return base ** exponent

# square = partial(power, exponent=2)
# cube = partial(power, exponent=3)

# print(square(5))
# print(cube(5))



# # from hello import test
# # test()
# print("对象类型 type(123)：", type(123))
# print("对象类型 type(\"str\")：", type("str"))
# print("对象类型 type(None)：", type(None))
# type(123)==type(456) # true
# type(123)==int # true
# type("str")==str  # true
# # 对象是否是函数
# import types
# def fn():
#     pass

# type(fn) == types.FunctionType # true
# type(abs) == types.FunctionType # true
# type(lambda x: x) == types.FunctionType # true
# type(x for x in range(10)) == types.GeneratorType # true
# type(x for x in range(10)) == types.GeneratorType # true
 
# # isinstance()
# class Animal:
#     pass
# class Dog(Animal):
#     pass
# class Husky(Dog):
#     pass

# a = Animal()
# d = Dog()
# h = Husky()
# print(isinstance(a, Animal)) # true
# print(isinstance(d, Animal)) # true
# print(isinstance(h, Animal)) # true
# print(isinstance(h, Dog)) # true
# print(isinstance(h, Husky)) # true
# print(isinstance(a, Dog)) # false

# # dir()

# print(dir("ABC"))
# print(dir(d))
# len('ABC')


# class Student:
#     # 可读写
#     @property
#     def score(self):
#         return self._score
#     @score.setter
#     def score(self, value):
#         if not isinstance(value, int):
#             raise ValueError('score must be an integer!')
#         if value < 0 or value > 100:
#             raise ValueError('score must between 0 ~ 100!')
#         self._score = value
    
#     # 只读
#     @property
#     def birth(self):
#         return self._birth


# class Student:
#     def __init__(self, name):
#         self.name = name

#     def __str__(self):
#         return f"Student object (name: {self.name})"

# print(Student("张三"))

# 枚举
# from enum import Enum, unique

# Month = Enum('Month', ('Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'))
# print(Month.Jan)
# print(Month.Jan.value)
# print(Month['Jan'])
# print(Month(1))

# @unique
# class Weekday(Enum):
#     MONDAY = 1
#     TUESDAY = 2
#     WEDNESDAY = 3
#     THURSDAY = 4
#     FRIDAY = 5
#     SATURDAY = 6
#     SUNDAY = 7
    
# for name, member in Weekday.__members__.items():
#     print(name, member)

# print(Weekday.MONDAY)
# print(Weekday.MONDAY.value)
# print(Weekday['MONDAY'])
# print(Weekday(1))

# import pickle
# d = dict(name='Bob', age=20, score=88)
# dump = pickle.dumps(d)
# print(dump)

# f = open('dump.txt', 'wb')
# pickle.dump(d, f)
# f.close()

# with open('dump.txt', 'rb') as f:
#     d = pickle.load(f)
#     print(d)

# # json

# import json
# d = dict(name='Bob Json', age=30, score=90)
# dump= json.dumps(d)
# print(dump)

# json_str = '{"age": 20, "score": 88, "name": "Bob Json String"}'
# d = json.loads(json_str)
# print(d)



# class Student(object):
#     def __init__(self, name, age, score):
#         self.name = name
#         self.age = age
#         self.score = score
        
# def student2dict(std):
#     return {
#         'name': std.name,
#         'age': std.age,
#         'score': std.score
#     }
        
# s = Student('Bob Object', 20, 88)
# dump = json.dumps(s, default=student2dict)
# print(dump)



import os

# print(f"Process {os.getpid()} start...")

# pid = os.fork()
# if pid == 0 :
#     print(f"I am child process {os.getpid()} and my parent is {os.getppid()}.")
# else:
#     print(f"I {os.getpid()} just created a child process {pid}.")
    

from multiprocessing import Pool
import os, time, random

def long_time_task(name):
    print(f"Run task {name} ({os.getpid()})")
    start = time.time()
    time.sleep(random.random() * 3)
    end = time.time()
    print(f"Task {name} runs {end - start} seconds.")

if __name__ == "__main__":
    print(f"Parent process {os.getpid()}.")
    p = Pool(4)
    for i in range(5):
        p.apply_async(long_time_task, args=(i,))
    print("Waiting for all subprocesses done...")
    p.close()
    p.join()
    print("All subprocesses done.")
