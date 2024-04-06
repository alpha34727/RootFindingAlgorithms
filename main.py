import sympy as sp
import matplotlib.pyplot as plt

f = sp.symbols('f', cls=sp.Function)
x = sp.symbols('x')

f = (x ** 3 + 4 * x ** 2 - 10) / (3 * x ** 2 + 8 * x)
area = [sp.Number(1), sp.Number(2)]
n = 10

cnt = [0, 0, 0, 0, 0, 0] # 加 剪 乘 除 函數 迭代數
progress = [tuple(area), tuple(area)]

def Statistic(cnt, movement):
    """統計函數，負責統計運算過程中的加減乘除與函數運算"""

    for i in range(6):
        cnt[i] += movement[i]

def PrintStatistic(cnt):
    """印出統計資料"""

    name = ['加法', '減法', '乘法', '除法', '函數運算', '迭代次數']
    for i in range(6):
        print(name[i], cnt[i], sep=' : ')

def DrawGraph(progress, name='Figure 1'):
    progress = progress[1:]

    left_data = [x for x, y in progress]
    right_data = [y for x, y in progress]

    plt.title(name)
    plt.plot([x for x in range(len(left_data))], left_data, color='red', marker='o')
    plt.plot([x for x in range(len(right_data))], right_data, color='blue', marker='o')
    plt.show()




# 牛頓法（左逼近）
def NewtonMethodLeft(f, x, progress, statistic, evaluate=False):
    area = progress[-1]
    an = area[1] - f.subs(x, area[1]) / f.diff().subs(x, area[1])

    statistic = Statistic(statistic, [0, 1, 0, 1, 2, 1])

    if evaluate:
        progress.append((area[0], an.evalf(n)))
    else:
        progress.append((area[0], an))

# 牛頓法（右逼近）
def NewtonMethodRight(f, x, progress, statistic, evaluate=False):
    area = progress[-1]
    an = area[0] - f.subs(x, area[0]) / f.diff().subs(x, area[0])

    statistic = Statistic(statistic, [0, 1, 0, 1, 2, 1])

    if evaluate:
        progress.append((an.evalf(n), area[1]))
    else:
        progress.append((an, area[1]))

# 二分逼近法
def BisectionMethod(f, x, progress, statistic, evaluate=False):
    area = progress[-1]

    amid = (area[0] + area[1]) / 2

    same_side = f.subs(x, amid) * f.subs(x, area[0])

    if same_side > 0: # 同側
        area = [amid, area[1]]
    elif same_side < 0: # 異側
        area = [area[0], amid]
    else:
        area = [amid, amid]

    statistic = Statistic(statistic, [1, 0, 1, 1, 2, 1])

    if evaluate:
        progress.append((area[0].evalf(n), area[1].evalf(n)))
    else:
        progress.append((area[0], area[1]))

# 割線法（左逼近）
def SecantMethodLeft(f, x, progress, statistic, evaluate=False):
    area = progress[-1]
    xn = area[0] - (area[0] - area[1]) / (f.subs(x, area[0]) - f.subs(x, area[1])) * (f.subs(x, area[0]))
    area = [xn, area[1]]

    statistic = Statistic(statistic, [0, 3, 1, 1, 3, 1])

    if evaluate:
        progress.append((area[0].evalf(n), area[1]))
    else:
        progress.append((area[0], area[1]))

# 割線法（右逼近）
def SecantMethodRight(f, x, progress, statistic, evaluate=False):
    area = progress[-1]
    xn = area[1] - (area[1] - area[0]) / (f.subs(x, area[1]) - f.subs(x, area[0])) * (f.subs(x, area[1]))
    area = [area[0], xn]

    statistic = Statistic(statistic, [0, 3, 1, 1, 3, 1])

    if evaluate:
        progress.append((area[0], xn.evalf(n)))
    else:
        progress.append((area[0], area[1]))

# 固定點迭代法
def FPI(f, x, progress, statistic, evaluate=False):
    area = progress[-1]
    g = x - f

    xn = g.subs(x, area[0])

    statistic = Statistic(statistic, [0, 1, 0, 0, 1, 1])

    if evaluate:
        progress.append((xn.evalf(n), area[1]))
    else:
        progress.append((xn, area[1]))

i = 0
while i < 100:
    # print(progress)
    FPI(f, x, progress, cnt, evaluate=True)
    
    if progress[-1][0].evalf(n) == progress[-2][0].evalf(n) and progress[-1][1].evalf(n) == progress[-2][1].evalf(n):
        break

    i += 1

print(progress)
PrintStatistic(cnt) # 印出統計資訊
DrawGraph(progress, name='SecantMethodRight')

