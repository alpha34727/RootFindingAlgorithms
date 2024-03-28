import sympy as sp

f = sp.symbols('f', cls=sp.Function)
x = sp.symbols('x')

f = x ** 3 + 2 * x - 5
area = (sp.Number(1), sp.Number(2))
n = 10

#加 剪 乘 除 函數
global cnt
cnt = [0, 0, 0, 0, 0]

#統計函數
def Statistic(cnt, movement):
    for i in range(5):
        cnt[i] += movement[i]

def PrintStatistic(cnt):
    name = ['加法', '減法', '乘法', '除法', '函數運算']
    for i in range(5):
        print(name[i], cnt[i], sep=' : ')

#牛頓法（右逼近）
def NewtonMethodRight(f, area, evaluate, statistic):
    an = area[1] - f.subs(x, area[1]) / f.diff().subs(x, area[1])

    statistic = Statistic(statistic, [0, 1, 0, 1, 2])

    if evaluate:
        return area[0], an.evalf(5)
    return area[0], an

#牛頓法（左逼近）
def NewtonMethodLeft(f, area, evaluate, statistic):
    an = area[0] - f.subs(x, area[0]) / f.diff().subs(x, area[0])

    statistic = Statistic(statistic, [0, 1, 0, 1, 2])

    if evaluate:
        return an.evalf(n), area[1]
    return an.evalf(n), area[1]

#二分逼近法
def BisectionMethod(f, area, evalutate, statistic):
    amid = (area[0] + area[1]) / 2
    if f.subs(x, area[0]) > f.subs(x, area[1]):
        if f.subs(x, amid) > 0:
            area = (amid, area[1])
        else:
            area = (area[0], amid)
    else:
        if f.subs(x, amid) > 0:
            area = (area[0], amid)
        else:
            area = (amid, area[1])
    
    statistic = Statistic(statistic, [1, 0, 0, 1, 3])

    if evalutate:
        return area[0].evalf(n), area[1].evalf(n)
    return area


i = 1
print(f'a1 : ({area[0].evalf(n)}, {area[1].evalf(n)})')
while True:
    original_area = area
    print(f'a{i+1} : ({area[0].evalf(n)}, {area[1].evalf(n)})')
    
    area = BisectionMethod(f, area, False, cnt)

    if str(original_area[0].evalf(n)) == str(area[0].evalf(n)) and str(original_area[1].evalf(n)) == str(area[1].evalf(n)):
        break

    i += 1

PrintStatistic(cnt)