
# Python 基础

##运算符
- and  与
- or   或
- not  非

## 变量
动态：
``` python
a = 1
t_007 = 'T007'
answer = True
```

静态：
``` python
int a = 123
a = "ABC" # 错误： 不能把字符串给整形变量
```

## 常量
```python
PI = 3.141592653  # 在Python中没有常量保护机制  一般习惯 大写是常量

10/3   # 3.3333333333333335
9/3    # 3.0  
10//3  # 3   两个// 是整除
10%3   # 1   余数 
```


## 占位符

- %d	整数
- %f	浮点数
- %s	字符串
- %x	十六进制整数

### format
``` python
"你好，{0}, 成绩提升了{1: .1f}, 继续努力", format("小名"， 17.123)
```

### f-string
``` python 
r = 2.5
s = 3.14 * r ** 2
str = f"半径为{r}的圆的面积为{s: .2f}"
```

## list
list 是有序集合。可以随时删除和添加元素

``` python 
names = ['a', 'b', 'c']
len(names) # 长度
names[0] # 第一个
names[-1] # 最后一个
names[-2] # 倒数第二个
names[1:3] # 从第二个到第三个
names.append('d') # 添加到末尾
names.insert(0, 'e') # 插入到第一个
names.pop() # 删除末尾
names.pop(0) # 删除第一个
names[0] = 'f' # 修改第一个
names.remove('c') # 删除指定元素
names.sort() # 排序
names.reverse() # 反转
names.clear() # 清空列表

```

## tuple
元组： 另一种有序列表 
tuple和list很像 但是tuple一旦初始化就不等你修改
``` python 
names_tuple = ('a', 'b', 'c')
print(f"元组长度: {len(names_tuple)}") # 长度
print(f"第一个元素: {names_tuple[0]}") # 第一个
print(f"最后一个元素: {names_tuple[-1]}") # 最后一个
print(f"倒数第二个元素: {names_tuple[-2]}") # 倒数第二个
print(f"从第二个到第三个元素: {names_tuple[1:3]}") # 从第二个到第三个


one_tuple = (1,) # 一个元素的元组 注意避免歧义加一个逗号
a_tuple = (1, 2, [3, 4]) # 元组中可以包含列表
a_tuple[2][0] = 5 # 元组中包含的列表可以修改， 但是不能修改元组本身
```

## 条件判断

``` python 
age = 20
if age >= 18:
    print("adult")
elif age >= 6:
    print("teenager") # 注意这里没有else
else:
    print("kid")

a = 10
if a:
    print("a is not 0") # 非0为True
else:
    print("a is 0") # 0为False
    
x = "aa"
if x:
    print("x is not empty") # 非空为True
else:
    print("x is empty") # 空为False


```

## input
``` python 
s_strip = input("请输入的年龄: ").strip()  # 去除空格
print(f"你的年龄是: {s_strip}")

s = input("请输入的年龄: ")
print(f"你的年龄是: {s}")
s = int(s)
if s > 18:
    print("你已经成年了")
else:
    print("你还没有成年")
```

## 模式匹配

``` python 
# 模式匹配
score = input("请输入分数: ").strip()
score = int(score)
match score:
    case x if x < 10:
        print('score is less than 10.')
    case 15:
        print('score is 15.')
    case 11 | 22:
        print('score is 11 or 22.')
    case x if x > 60 and x < 100:
        print('score is greater than 60 and less than 100.')
    case _: # _表示匹配到其他任何情况
        print('score is other.')

# 列表匹配 
# 用args = ['gcc', 'hello.c']存储，下面的代码演示了如何用match匹配来解析这个列表：
args = ['gcc', 'hello.c', 'world.c']
match args:
    case ['gcc']: 
        # 如果仅出现gcc 报错
        print('gcc: missing source file(s).')
    case ['gcc', file1, *files]: 
        # 第一个元素必须是字符串 'gcc'
        # 第二个元素会被赋值给变量 file1
        # 剩余的所有元素会被收集到变量 files 中（作为列表）
        # case ['gcc', file1, *files]: 至少两个元素
        # case ['gcc', *files]: 仅 gcc就能匹配上了   *files是可选传入的
        # 如果出现gcc 后面跟着一个文件名和多个文件名 打印gcc compile: hello.c, world.c
        print('gcc compile: ' + file1 + ', ' + ', '.join(files))
    case ['clean']: 
        # 如果出现clean 打印clean
        print('clean')
    case _:
        # 如果出现其他情况 打印invalid command.
        print('invalid command.')
```

## 循环

``` python 
names = ['a', 'b', 'c']
for name in names:
    print(name)
    
sum = 0
for i in [1, 2, 3, 4, 5]:
    sum += i
print(sum)

sum = 0
for i in range(1, 10):
    sum += i
print(sum)

sum = 0
while sum < 10:
    sum += 1
    print(sum)
    if sum == 5:
        continue
    print(sum)
    if sum == 8:
        break
    print(sum)
```

## dict
``` python 

dict = {
    'Michael': 95,
    'Bob': 75,
    'Tracy': 85
}
print(dict)
print(len(dict.keys())) # 打印键的数量
print(len(dict)) # 打印键值对的数量

dict['Adam'] = 67
dict['Jack'] = 90
print(dict['Adam'])

if 'Bob' in dict:
    print('Boc is in dict')
else:
    print('Boc is not in dict')
    
print(dict.get('Bob')) # 获取Bob的值 如果Bob不存在 返回None
print(dict.get('Bob', 100)) # 获取Bob的值 如果Bob不存在 返回100
print(dict.get('Bobcccc', 100)) 

dict.pop('Bob') # 删除Bob
print(dict)

dict.popitem() # 删除最后一个键值对
print(dict)

dict.clear() # 清空字典
print(dict)
```

## Set
``` python 
s = {1, 2, 3, 4, 5}
print(s)

s.add(6) # 添加元素
print(s)

s.remove(1) # 删除元素
print(s)

s.pop() # 删除最后一个元素
```

## func

``` python 
def my_abs(x):
    if not isinstance(x, (int, float)):
        raise TypeError('bad operand type')
    if x >= 0:
        return x
    else:
        return -x
    
import math
def move(x, y, step, angle=0):
    nx = x + step * math.cos(angle)
    ny = y - step * math.sin(angle)
    return nx, ny
    
    
    
def quadratic(a, b, c):
    x1 = (-b + math.sqrt(b**2 - 4*a*c)) / (2*a)
    x2 = (-b - math.sqrt(b**2 - 4*a*c)) / (2*a)
    return x1, x2
```

## 位置参数  就是函数定义加了参数

默认参数规则
必选参数在前，默认参数在后，否则Python的解释器会报错
``` python 
# 位置参数
def power(x):
    return x * x

def power(x, n = 2):  # n = 2 就是默认参数  可选传递
    s = 1
    while n > 0:
        n = n - 1
        s = s * x
    return s


def enroll(name, gender, age=6, city='Beijing'):
    print('name:', name)
    print('gender:', gender)
    print('age:', age)
    print('city:', city)

enroll('Sarah', 'F')
enroll('Bob', 'M', 7) # 按顺序传递可以不写参数名字
enroll('Adam', 'M', city='Tianjin') # 不按顺序传递必须写参数名字



def add_end(L=[]):
    L.append('END')
    return L
from func_test import add_end
print(add_end([1, 2, 3]))  #  [1, 2, 3, 'END']
print(add_end()) # ['END']
print(add_end()) # ['END', 'END']
```
在add_end()中需要注意  两次的 add_end() 最终的结果是['END', 'END']
因为在python中  默认参数L的值也是一个变量，他只想对象[]
所以每次使用的时候都会被改变  会被记录

解决方案如下：  `默认参数必须只想不变对象!`

``` python 
def add_end(L=None):
    if L is None:
        L = []
    L.append('END')
    return L
```

## 可变参数

``` python 
nums = [1, 2, 3]

# 只能传递一个列表或者元组
def calc(numbers):
    sum = 0
    for n in numbers:
        sum = sum + n * n
    return sum
print(calc([1, 2, 3]))
print(calc(1, 2, 3))


print(calc(nums))

# 这个意思是你可以传递任何数量的参数， 传递的内容会被拆分开来
def calc(*numbers):
    sum = 0
    for n in numbers:
        sum = sum + n * n
    return sum

print(calc(*nums)) # 会把list中的所有数据平铺传递
# 等价于
print(calc(1, 2, 3))

print(1)
print(1, 2)
print()
```

## 关键字参数
``` python 
def person(name, age, **kw):
    print('name:', name, 'age:', age, 'other:', kw)

print(person('Michael', 30))
print(person('Bob', 35, city='Beijing'))
print(person('Adam', 45, gender='M', job='Engineer'))
```
func person 除了必选参数之外，还接受关键字参数kw  kw会自动组装为一个dict

``` python 

def func(city, job):
    print(city, job)

extra = {'city': 'Beijing', 'job': 'Engineer'}
func(**extra)  # 相当于 func(city='Beijing', job='Engineer')

```

### *解包 和 **解包的区别

`*iterable`
- 拆开成位置参数
- 容器要求: list/tuple/set
- 函数接收方式: positional args

`**dict`
- 拆开成关键字参数
- 容器要求: dict
- 函数接收方式: keyword args



# 高级特性

## 切片

取List和tuple的 部分元素
- 语法：L[start:end]
- 包含 start 对应的元素
- 不包含 end 对应的元素
- 如果省略 start → 从头开始
- 如果省略 end → 到列表末尾

``` python 
L = ['Michael', 'Bob', 'Tracy', 'Sarah', 'Jack', 'Tom', 'Jerry']
print(f"取前3个：{L[0:3]}")
print(f"取前3个，第一个0可以省略：{L[:3]}")
print(f"从索引1开始，取到索引3（不包括3）：{L[1:3]}")
print(f"最后两个：{L[-2:]}")
print(f"倒数第一个：{L[-1]}")
print(f"前10个每两个取一个：{L[:10:2]}")
print(f"所有元素每两个取一个：{L[::2]}")
print(f"所有元素倒序：{L[::-1]}")
print(f"复制list：{L[:]}")
```

## 迭代

``` python 
# list
L = ['Michael', 'Bob', 'Tracy', 'Sarah', 'Jack', 'Tom', 'Jerry']
for name in L:
    print(name)

for i, name in enumerate(L):
    print(i, name)

#元组
for x, y in [(1, 1), (2, 4), (3, 9)]:
    print(x, y)

# dict
d = {'a': 1, 'b': 2, 'c': 3}
for key in d:
    print(key)

for value in d.values():
    print(value)

for key, value in d.items():
    print(key, value)

# 字符串
for ch in 'ABC':
    print(ch)
```

# 列表生成式

原始for循环的 一个高阶写法   一行代码搞定

原始for循环：
``` python 
L = []
for x in range(1, 11):
    L.append(x * x)

# [1, 4, 9, 16, 25, 36, 49, 64, 81, 100]
```
生成式的：
``` python 
L = [x * x for x in range(1, 11)] # 生成1到10的平方
print(L)

# if判断条件在 前 的话必须有else
L = [x if x % 2 == 0 else -x for x in range(1, 11)] 
print(L)
# if判断条件在 后 的话不能有else
L = [x * x for x in range(1, 11) if x % 2 == 0] # 生成1到10的平方，只保留偶数
print(L)

# 嵌套循环  双层for循环  再多就不推荐了  
L = [m + n for m in 'ABC' for n in 'XYZ']
print(L)

# dict
map = {'a': 1, 'b': 2, 'c': 3}
L1 = [ k + '=' + str(v) for k, v in map.items()]
print(L1) # ['a=1', 'b=2', 'c=3']
   
```

## 生成器

简单的list和生成器
``` python 
L = [x * x for x in range(10)]
print(L)

g = (x * x for x in range(10))
# print(next(g))
# print(next(g))
# print(next(g))
print("-------------------")
for n in g:
    print(n)
print("-------------------")
for n in g:
    print(n)
```

斐波那契数的实现
``` python 
def fic(max):
    # 第一个  第二个 是1, 1, 2, 3  其他的都是前两个数相加
    n, a, b = 0, 0, 1
    while(n < max):
        # print(b)
        yield b
        # 方法1
        # a, b = b, a + b

        # 方法2
        c = a
        a = b
        b = c + b
        
        n = n + 1
    return 'done'

f = fic(5)


for n in f:
    print(n)
```

杨辉三角实现

``` python 
def triangles():
    L = [1]
    while True:
        yield L
        lM = [L[i] + L[i+1] for i in range(len(L)-1)]
        L = [1] + lM + [1]

t = triangles()
print(next(t))
print(next(t))
print(next(t))
print(next(t))
print(next(t))
```

# 高阶函数
``` python 
f = abs
def add(x, y, f):
    return f(x) + f(y)
print(add(1, 2, abs))
print(add(-5, 6, abs))
```
map：
对 可迭代对象 的每个元素应用一个函数，并返回结果 可迭代对象（Python 3 是迭代器，需要用 list() 才能看到列表）。

reduce：
将 一个序列的所有元素 通过指定函数 逐步合并，得到一个最终值


filter()

仔细理解这里面的运行过程
函数均为迭代器
it = filter(_not_divisible(n), it) # 构造新序列
每次构造新的筛选条件生成新的迭代器

然后再_odd_iter 去懒加载下一个数值时 要符合之前加的所有筛选条件

``` python
def _odd_iter():
    n = 1
    count = 0
    while True:
        n = n + 2
        count += 1
        yield n
        
def _not_divisible(n):
    return lambda x: x % n > 0

def primes():
    yield 2
    it = _odd_iter() # 初始序列
    while True:
        n = next(it) # 返回序列的第一个数
        yield n
        it = filter(_not_divisible(n), it) # 构造新序列

for n in primes():
    if n < 100:
        print(f"🎯 找到素数: {n}")
    else:
        break
```


sorted()

``` python 
s = sorted([36, 5, -12, 9, -21])
print(s)

s = sorted([36, 5, -12, 9, -21], key=abs)
print(s)

filtered = filter(lambda x: x > 0, [1, -2, 3, -4])

print(list(filtered))

def strSorted():
    return lambda x: x.startswith('Z')

s = sorted(['bob', 'about', 'Zoo', 'Credit'], key=strSorted(), reverse=True)
print(s)

```


# 返回函数

``` python 
# 普通循环
def calc_sum(*args):
    ax = 0
    for n in args:
        ax = ax + n
    return ax

s = calc_sum(1, 2, 3, 4, 5)
print(s)

# 返回函数
def lazy_sum(*args):
    def sum():
        ax = 0
        for n in args:
            ax = ax + n
        return ax
    return sum

s = lazy_sum(1, 2, 3, 4, 5)
print(s())


def count():
    fs = []
    for i in range(1, 4):
        def f():
             return i*i
        fs.append(f)
    return fs

f1, f2, f3 = count() # 将列表中的三个函数全部接收

print(f1()) # 9
print(f2()) # 9
print(f3()) # 9
# 全部返回9  因为在这个过程中i的值是引用的  所以到最后都是3



def count():
    fs = []
    for i in range(1, 4):
        fs.append(lambda x=i: x*x)
    return fs

f1, f2, f3 = count() 

print(f1()) # 1
print(f2()) # 4
print(f3()) # 9
# 理想状态   lambda把参数i 单独持有了  所有计算结果正确

# print(f1())
# print(f2())   
# print(f3())


#  计数器小练习
def createCounter():
    x = 0
    def counter():
        nonlocal x
        x = x + 1
        return x
    return counter

counterA = createCounter()
print(counterA())
print(counterA())
```

# 匿名函数  lambda
lambda 
冒号前面相当于是参数  后面是实现

lambda使用时机：

- 函数逻辑很简单（一行能写完）
- 只在这一个地方使用？
- 作为参数传递给其他函数？
- 临时性的小功能？

``` python 


# lambda
l = list(map(lambda x: x * x, [1, 2, 3, 4, 5]))
print(l)

# lambda 相当于以下函数

def f(x):
    return x * x


f = lambda x: x * x
print(f(5))

# 也可以作为函数返回
def build(x, y):
    return lambda: x * x + y * y

f = build(2, 3)
print(f())
```


# 装饰器
在不改变原来函数的前提下，给函数增加新的功能
``` python 
def log(func):
    def wrapper(*args, **kw):
        print(f"call {func.__name__}()...")
        return func(*args, **kw)
    return wrapper

@log
def now():
    return "2025-01-01"
print(now())

def log2(text):
    def decorator(func):
        def wrapper(*args, **kw):
            print(f"{text} call {func.__name__}()...")
            return func(*args, **kw)
        return wrapper
    return decorator

@log2("execute")
def now2():
    return "2025-01-01"
print(now2())
```


# 偏函数


如果只给函数参数一个常见的默认值，使用函数默认值
如果想要在运行时派生多个 准用版本 的函数 用偏函数
``` python 
from functools import partial

def power(base, exponent):
    return base ** exponent

square = partial(power, exponent=2)
cube = partial(power, exponent=3)

print(square(5))  # 25
print(cube(5))    # 125
```



# 模块

一般以下划线开头的都是私有函数  不希望外部调用
``` python 
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

' 模块注释文档 '

__author__ = '作者的名字'

import sys

def test():
    args = sys.argv
    if len(args) == 1:
        print('hello world')
    elif len(args) == 2:
        print(f'hello, {args[1]}!')
    else:
        print('too many arguments!')
        
def _private_test():
    print('this is a private test')

if __name__ == '__main__':
    test()


#使用
from hello import test
test()
```


# 获取对象信息

`type`
对象是什么类型的
``` python 
print("对象类型 type(123)：", type(123))
print("对象类型 type(\"str\")：", type("str"))
print("对象类型 type(None)：", type(None))
type(123)==type(456) # true
type(123)==int # true
type("str")==str  # true
# 对象是否是函数
import types
def fn():
    pass

type(fn) == types.FunctionType # true
type(abs) == types.FunctionType # true
type(lambda x: x) == types.FunctionType # true
type(x for x in range(10)) == types.GeneratorType # true
type(x for x in range(10)) == types.GeneratorType # true
 

```

`isinstance`
class的类型判断
``` python 
class Animal:
    pass
class Dog(Animal):
    pass
class Husky(Dog):
    pass

a = Animal()
d = Dog()
h = Husky()
print(isinstance(a, Animal)) # true
print(isinstance(d, Animal)) # true
print(isinstance(h, Animal)) # true
print(isinstance(h, Dog)) # true
print(isinstance(h, Husky)) # true
print(isinstance(a, Dog)) # false

```

`dir()`
获得一个对象的所有属性和方法  返回list
``` python 
print(dir("ABC"))
print(dir(d))
len('ABC')
```


## @property

``` python 


class Student:
    # 可读写
    @property
    def score(self):
        return self._score
    @score.setter
    def score(self, value):
        if not isinstance(value, int):
            raise ValueError('score must be an integer!')
        if value < 0 or value > 100:
            raise ValueError('score must between 0 ~ 100!')
        self._score = value
    
    # 只读
    @property
    def birth(self):
        return self._birth

```

## 多重继承
顾名思义

# 定制类

## `__str__`

`__str__`: 定义对象的字符串表示，返回给终端用户看的，通常是可读性强的字符串。当使用 `print()` 函数或 `str()` 函数时会调用这个方法。

`__repr__`: 定义对象的"官方"字符串表示，返回给程序员看的，通常应该是明确的、无歧义的。当在交互式命令行中直接输入对象名或使用 `repr()` 函数时会调用这个方法。理想情况下，`repr()` 返回的字符串应该是一个有效的 Python 表达式，可以重新创建该对象。

`__iter__`: 如果一个类想被用于for ... in循环  把自身当做迭代  不断的调用`__next__`

`__next__`: 配个`__iter__`使用  迭代器的next方法

`__getitem__`: 把实例当做 list使用可以使用  func[1]



``` python 
class Student:
    def __init__(self, name):
        self.name = name
    def __str__(self):
        return f"Student object (name: {self.name})"
    __repr__ = __str__

    def __iter__(self):
        return self # 实例本身就是迭代对象，故返回自己

    def __next__(self):
        self.a, self.b = self.b, self.a + self.b # 计算下一个值
        if self.a > 100000: # 退出循环的条件
            raise StopIteration()
        return self.a # 返回下一个值

    def __getitem__(self, n):
        a, b = 1, 1
        for x in range(n):
            a, b = b, a + b
        return a

print(Student("张三"))
```

`__getattr__`:多用于动态行为 当访问对象中 不存在的属性 时调用。当你访问一个不存在的属性时，Python 会调用对象的 __getattr__(self, name) 方法。 

`__call__`: 当 实例被当成函数调用 时触发。
``` python 
class Chain:
    def __init__(self, path=""):
        self._path = path

    def __getattr__(self, name):
        return Chain(f"{self._path}/{name}")

    def __call__(self, *args, **kwargs):
        return f"Requesting {self._path}, args={args}, kwargs={kwargs}"


c = Chain()
print(c.users.list())     # Requesting /users/list, args=(), kwargs={}
print(c.api.v1.user(id=1))  # Requesting /api/v1/user, args=(), kwargs={'id': 1}
```


# 枚举

``` python 
from enum import Enum, unique

Month = Enum('Month', ('Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'))
print(Month.Jan)
print(Month.Jan.value)
print(Month['Jan'])
print(Month(1))

@unique
class Weekday(Enum):
    MONDAY = 1
    TUESDAY = 2
    WEDNESDAY = 3
    THURSDAY = 4
    FRIDAY = 5
    SATURDAY = 6
    SUNDAY = 7
    
for name, member in Weekday.__members__.items():
    print(name, member)

print(Weekday.MONDAY)
print(Weekday.MONDAY.value)
print(Weekday['MONDAY'])
print(Weekday(1))
```
# IO编程

## 文件读写
正常使用文件需要` f = open('/path/to/file', 'r')`之后一定要 ` f.close()` 或者使用`with`方式读取 无需close、

普通文件 - f: `open('/Users/michael/test.jpg', 'rb')`  

二进制文件 - rb: `open('/Users/michael/test.jpg', 'rb')`

字符编码 - gbk: `open('/Users/michael/gbk.txt', 'r', encoding='gbk')`

读取size个字节的内容: `read(size)`

读取一行的内容: `readline()`

写文件: `f.write('Hello, world!')` 

``` python 
with open('/path/to/file', 'r') as f:
    print(f.read())

read(size)方法

``` python
## StringIO
很多时候读取的不一定是文件也可能是内存中的读写
from io import StringIO
f = StringIO('Hello!\nHi!\nGoodbye!')
    while True:
        s = f.readline()
        if s == '':
            break
        print(s.strip())

# Hello!
# Hi!
# Goodbye!

```
## BytesIO
二进制数据

``` python 
from io import BytesIO
f = BytesIO()
f.write('中文'.encode('utf-8'))
# 6
print(f.getvalue())
# b'\xe4\xb8\xad\xe6\x96\x87'

```
## 序列化
也有三方库使用，这里只做简单参考
``` python 
import pickle
d = dict(name='Bob', age=20, score=88)
dump = pickle.dumps(d)
print(dump)

f = open('dump.txt', 'wb')
pickle.dump(d, f)
f.close()

with open('dump.txt', 'rb') as f:
    d = pickle.load(f)
    print(d)

# json

import json
d = dict(name='Bob Json', age=30, score=90)
dump= json.dumps(d)
print(dump)

json_str = '{"age": 20, "score": 88, "name": "Bob Json String"}'
d = json.loads(json_str)
print(d)



class Student(object):
    def __init__(self, name, age, score):
        self.name = name
        self.age = age
        self.score = score
        
def student2dict(std):
    return {
        'name': std.name,
        'age': std.age,
        'score': std.score
    }
        
s = Student('Bob Object', 20, 88)
dump = json.dumps(s, default=student2dict)
print(dump)
```

# 进程和线程
# 进程
进程线程提速的原理就是  系统会快速切换每个正在执行的线程，如果是多核CPU可一实现真正的并发
如果是单核，提速的位置是在非CPU执行任务方面（比如网络请求的等待时间，I/O 密集）其实就是将资源的使用率提高了
`getppid()`: 可以拿到父进程的ID。

``` python 
import os

print(f"Process {os.getpid()} start...")

pid = os.fork()
if pid == 0 :
    print(f"I am child process {os.getpid()} and my parent is {os.getppid()}.")
else:
    print(f"I {os.getpid()} just created a child process {pid}.")
    

```

## Pool
需要启动大量的子进程，可以使用进程池的方式进行批量创建子进程
对`Pool`对象调用`join()` 方法会等待所有子进程执行完毕，调用`join()`之前必须先调用`close()`, 掉用`close()`之后就不能继续添加新的`Process`了

``` python 
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
    print("close")
    p.join()
    print("join")
    print("All subprocesses done.")

# Parent process 76657.
# Waiting for all subprocesses done...
# Run task 0 (76660)
# Run task 1 (76659)
# Run task 2 (76661)
# Run task 3 (76662)
# Task 3 runs 0.9405360221862793 seconds.
# Run task 4 (76662)
# Task 2 runs 1.2899131774902344 seconds.
# Task 1 runs 2.1461241245269775 seconds.
# Task 4 runs 1.2402539253234863 seconds.
# Task 0 runs 2.2287752628326416 seconds.
# All subprocesses done.

```
注意 0、1、2、3 是立即执行的  因为我们设置的 `Poll(4)` 4个任务其中一个完成之后才会继续

## 子进程

``` python 
```

## 多线程
多任务可以由多进程完成，也可以一个进程多线程完成
一个进程至少会有一个线程

线程是操作系统直接支持的执行单元， python也是 并且他是真正的 Posix Thread  而不是模拟出来的

Python 变一般用`threading` 的高级模块  他是对 `_thread`进行了封装，大多数情况下都能使用这个`threading`高级模块

``` python 

import threading, time

def loop():
    print(f'thread {threading.current_thread().name} is running...')
    n = 0
    while n < 5:
        n = n + 1
        print(f'thread {threading.current_thread().name} >>> {n}')
        time.sleep(1)
    print(f'thread {threading.current_thread().name} ended.')
    
    
print(f'thread {threading.current_thread().name} is running...')
t = threading.Thread(target=loop, name='LoopThread')
t.start()
t.join()
print(f'thread {threading.current_thread().name} ended.')

# thread MainThread is running...
# thread LoopThread is running...
# thread LoopThread >>> 1
# thread LoopThread >>> 2
# thread LoopThread >>> 3
# thread LoopThread >>> 4
# thread LoopThread >>> 5
# thread LoopThread ended.
# thread MainThread ended.
```
系统默认会启动一个 `MainThread` 的主线程，使用`current_thread()`可以回去当前线程的名字

我们在上面的代码 中使用了  `LoopThread`命名的子线程进行执行任务


## Lock
Lock 多线程和多进程最大的不同在于，多进程中，同一个变量，各自有一份copy存在每个进程中，互不影响

多线程中 所有变量都是线程共享的，所以任何一个变量，都是可以被任何一个线程修改，因此，线程之间共享数据最大的危险在于多个线程同时修改一个变量的时候，把内容改乱了

因此产生了Lock的存在

``` python 
balance = 0
lock = threading.Lock()

def change_it(n):
    # 先存后取，结果应该为0:
    global balance
    balance = balance + n
    balance = balance - n


def run_thread(n):
    for i in range(100000):
        # 先要获取锁:
        lock.acquire()
        try:
            # 放心地改吧:
            change_it(n)
        finally:
            # 改完了一定要释放锁:
            lock.release()

```
# 网络协议
`IPv4`: 32位整数，字符串格式如 `192.168.0.1`（按8位分组显示）

`IPv6`: 64位证书，`IPv4`的升级版，格式如 `2001:0db8:85a3:0042:1000:8a2e:0370:7334`

TCP协议的特点
- 建立在IP协议之上
- 提供可靠连接：通过握手建立连接
- 数据完整性: 对数据包编号，确保顺序接收
- 错误恢复：自动重发丢失的数据包

协议层接口
```
HTTP、SMTP 等应用层协议
    ↓
TCP协议
    ↓
IP协议
```

TCP 报文组成
- 传输数据
- 源IP地址 + 目标IP地址
- 源端口号 + 目标端口号

端口的作用
- **程序区分**: 区分同一台计算机上的不同网络程序
- **唯一标识**: 每个网络程序申请唯一端口号
- **通信基础**: 网络通信需要 IP地址 + 端口号 的组合
- **多连接支持**: 一个进程可同时与多台计算机建立连接

## 网络协议总结

### 🔗 **基础关系**
**所有协议都基于TCP**：HTTP、HTTPS、SSE、WebSocket都建立在可靠的TCP连接之上

### 📋 **协议特性对比**

| 协议 | 协议标识符 | 协议性质 | 通信方式 | 连接特点 | 主要用途 |
|------|------------|----------|----------|----------|----------|
| **HTTP** | `http://` | 应用层协议 | 请求-响应 | 短连接 | 网页浏览、API调用 |
| **HTTPS** | `https://` | HTTP+TLS加密 | 请求-响应 | 短连接 | 安全的网页浏览 |
| **SSE** | `http://` / `https://` | 基于HTTP的技术 | 单向推送 | 长连接 | 实时通知、状态更新 |
| **WebSocket** | `ws://` / `wss://` | 独立应用层协议 | 双向通信 | 长连接 | 聊天、游戏、实时协作 |

### 🏗️ **协议栈结构**
```
┌─────────────────────────────────────┐
│  HTTP  │ HTTPS │  SSE  │ WebSocket  │ ← 应用层
│http:// │https://│ http://│ws://wss:// │ ← 协议标识
├────────┼───────┼───────┼────────────┤
│   -    │  TLS  │   -   │    TLS     │ ← 安全层  
├────────┼───────┼───────┼────────────┤
│        TCP (传输层)                  │
├─────────────────────────────────────┤
│        IP (网络层)                   │
└─────────────────────────────────────┘
```

### 🎯 **核心要点**
1. **TCP是基础**：所有这些协议都依赖TCP的可靠传输
2. **协议标识**：每个协议都有自己的URL方案标识符
3. **HTTP系列**：HTTP/HTTPS/SSE都使用http(s)://标识
4. **WebSocket独特**：有专属的ws://和wss://标识符
5. **安全版本**：HTTPS用https://，WebSocket Secure用wss://

### 💡 **简记口诀**
- **HTTP** (`http://`)：传统网页，一问一答
- **HTTPS** (`https://`)：HTTP加锁，安全第一  
- **SSE** (`http(s)://`)：服务器推送，单向长连
- **WebSocket** (`ws://wss://`)：实时双向，游戏聊天


方法返回数据和客户端的额地址与端口 这样服务器收到数据后 直接调用就可以啊数据用UDOP发送给客户端  注意这里审掉了






``` python 
```

