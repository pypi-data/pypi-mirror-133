# 测试eval函数,eval()函数用来执行一个字符串表达式，并返回表达式的值。另外，可以讲字符串转换成列表或元组或字典
# s = "print('abcde')"
# eval(s)
# a = 10
# b = 20
# c = eval("a+b")
# print(c)
# dict1 = dict(a=100, b=200)
# c = eval("a+b", dict1)
# print(c)

a = "{1: 'a', 2: 'b'}"
print(type(a))
b = eval(a)
print(type(b))
print(b)