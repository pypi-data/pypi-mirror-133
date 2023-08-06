# 测试阶乘函数函数
def factorial(n):
    if n == 1:
        return 1
    else:
        return n * factorial(n - 1)


for a in range(1, 6):
    # print(a, "!=", factorial(a))
    print("{0}!={1}".format(a, factorial(a)))
