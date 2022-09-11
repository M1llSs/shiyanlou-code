'''
python 闭包（closure）入门
'''


# 一切皆对象

# 1) 函数可以根据给定的参数返回一个值：

def hello(name):
    return 'Hello ' + name


print(hello('jack'))
print('函数参数个数：', hello.__code__.co_argcount)

# 2) 函数也是对象，可以把函数赋值给一个变量, 都指向同一个函数

h = hello

print(hello)  # <function hello at 0x000001653A89A200>
print(h)  # <function hello at 0x000001653A89A200>

print(h('bob'))


# 3) 函数里的函数

def hi():
    def bob():
        return 'Bob'

    print('Hi ' + bob())


hi()  # Out: Hi Bob


# bob 函数作用域在 hi 之内，全局调用会发生错误
# bob() NameError: name 'bob' is not defined

# 4) 函数作为返回值，也可以内部定义，也可以作为其它函数的参数。
# 这种在函数里传递、嵌套、返回其他函数的情况，称之为 高阶函数
def cook():
    def tomato():
        print('I am Tomato')

    return tomato


print(cook)  # <function cook at 0x0000013034C6AEF0>
print(cook())  # <function cook.<locals>.tomato at 0x0000019BE86EAF80>
c = cook()
c()  # Out: I am Tomato


# 5) 闭包与自由变量

# 一般来说函数中变量为局部变量，一旦函数执行完毕，其中变量就不可用了。
def fruit():
    food = 'apple'
    print(food)


fruit()  # Out: apple

# print(food) NameError: name 'food' is not defined

# 在高阶函数里
'''
高阶函数中，内层函数携带外层函数中的参数、变量及其环境，一同存在的状态（即使已经离开的创造它的外层函数）
被称为闭包。被携带的外层变量被称为自由变量，有时候也被形容为外层变量被闭包捕获了。
'''
f_kind = ''


def fruits():
    food = 'banana'

    def wrapper():
        print('i like ' + food)

    return wrapper


f = fruits()
f()  # Out: i like banana
print(fruits)  # <function fruits at 0x00000262102DB0A0>
print(fruits())  # <function fruits.<locals>.wrapper at 0x00000262102DB1C0>
print(f)
''' <function fruits.<locals>.wrapper at 0x00000262102DB130> 重新赋值后二个函数对象引用地址不同，互相不影响。 即使fruits
外层函数被删除，也不被影响'''

del fruits
f()  # Out: i like banana
# print(fruits) NameError: name 'fruits' is not defined
# print(fruits()) NameError: name 'fruits' is not defined
print(f)  # <function fruits.<locals>.wrapper at 0x00000262102DB130>


# 参数捕获
# 外层函数里的参数也可以成为自由变量，被封装到内层函数所在的环境中，这种局部变量起作用的特点的环境，有时候被称为作用域或者域
def cook(name):
    def wrapper():
        print('i am cooking ' + name)

    return wrapper


apple = cook('apple')
pear = cook('pear')
apple()  # Out:i am cooking apple
pear()  # Out:i am cooking pear


# 函数生成
# 外层函数可以携带参数，返回的内层函数也可以携带参数

def outer(x):
    def inner(y):
        print((x + y))

    return inner


outer(1)(2)  # Out: 3

'''
看到2个括号就代表函数就行了二次调用。第一个括号对应 outer 外层的参数，第二个括号里对应的 inner 内层的参数

因此，利用闭包携带参数并返回函数的这个特性，可以很方便的在一个底层函数的框架上组装出不同的功能。
外层函数传递的参数甚至可以是个函数。
'''
add_one = outer(1)
add_ten = outer(10)

add_one(5)  # Out: 6
add_ten(5)  # Out: 15

# 状态持有
'''
闭包中的自由变量有两个神奇的特性：

1）自由变量在闭包存在的期间，其中的值也会一直存在。因此闭包可以持有状态
2) 闭包与闭包之间的状态是隔离的
'''


# 记录每次取得的分数
def make_score():
    alist = []

    def inner(x):
        alist.append(x)
        # alist.append(x)
        # alist.append(3)
        print(alist)

    return inner


score = make_score()
# del make_score
score(10)  # Out: [10]
score(20)  # Out: [10, 20]
score(30)  # Out: [10, 20, 30]
'''
可以看出 score 闭包打印的列表记录了每次调用的结果
'''

first = make_score()
second = make_score()

first(21)  # Out: [21]
first(24)  # Out: [21, 24]

second(41)  # Out: [41]
second(42)  # Out: [41, 42]

print('first: ', first)
print('second: ', second)  # firsr 和 second 地址是不一样的、
'''
first 和 second 两个状态是隔离的，互不影响
'''

# 不变量状态
'''
如果要操作的自由变量是个不变量，比如数值型、字符串等，那么记得加nonlocal关键字
'''


def make_total():
    total = 10

    def inner(x):
        nonlocal total  # 此关键词就是告诉解释器；接下来的 total 变量不是本函数里的局部变量。你最好去闭包或者别的地方找找。
        total += x  # 如果上面不声明 nonlocal total 程序会报错。
        print(total)

    return inner


total = make_total()
total(15)

# 延迟陷阱

funcs = []
for i in range(3):
    def inner():
        print(i)


    funcs.append(inner)
print('i is:', i)
# print(funcs)
funcs[0]()  # Out: 2
funcs[1]()  # Out: 2
funcs[2]()  # Out: 2
'''
直觉上好像应该输出0,1,2，但实际上是2,2,2。这是因为函数 inner 是延迟执行的。直到真正调用前，都是没进行内部操作的。
解决办法：就是用闭包将 i 的值立即捕获: 
'''
print('*' * 30)
funcs = []
for i in range(3):
    def outer(a):
        def inner():
            print(a)

        return inner


    funcs.append(outer(i))
print('i is:', i)
# print(funcs)
funcs[0]()  # Out: 2
funcs[1]()  # Out: 2
funcs[2]()  # Out: 2

# 6) 组合函数

'''
利用闭包可以捕获参数，从而生成新函数的能力。
被捕获的参数可以是函数
'''


# 利用闭包实现函数拼接
def compose(g, f):
    def inner(*args, **kwargs):
        return g(f(*args, **kwargs))

    return inner


def rem_first(lis):
    return lis[1:]


def rem_last(lis):
    return lis[:-1]


mid = compose(rem_first, rem_last)
new_lis = mid([1, 2, 3, 4])
print(new_lis)
'''
很方便的用二个简单的函数，合成出更复杂一点的新函数，提高代码复用的能力
'''


# 7) 柯里化

# 可里化闭包函数
def curry(f):
    argc = f.__code__.co_argcount
    print('argc参数是：', argc)
    f_args = []
    f_kwargs = {}

    def g(*args, **kwargs):
        nonlocal f_args
        # nonlocal f_kwargs
        # f_args += args
        f_args.extend(args)
        f_kwargs.update(kwargs)
        print(len(f_args))
        if len(f_args) + len(f_kwargs) == argc:
            return f(*f_args, **f_kwargs)
        else:
            return g

    return g


def add(a, b, c):
    return a + b + c

print('*'*30)
c_add = curry(add)
print(add.__code__.co_argcount) # 输出函数参数的个数

# print(add(1, 2, 3))
# print(add(1))
# print(add(1, 2))
# print(c_add(1))
# print(c_add(2))
# print(c_add(3))

'''
柯里化函数的逻辑：
1）它返回一个闭包，并且将闭包接收到的参数记录在自由变量中
2）如果当前参数过少，则返回一个继续接受参数的新函数
3）如果当前参数足够，则执行原函数并且返回结果
'''

# 结论 conclusion

'''
总结一下闭包的几个特性：
1）它是一个嵌套函数
2）它可以访问外部作用域中的自由变量
3）它从外层函数返回
'''