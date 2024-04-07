import sympy as sp
import matplotlib.pyplot as plt
import copy

f = sp.symbols('f', cls=sp.Function)
x = sp.symbols('x')

# f = (x ** 3 + 4 * x ** 2 - 10) / (3 * x ** 2 + 8 * x)
f = sp.sin(x+2)
area = [sp.Number(1), sp.Number(2)]
area_brent = [sp.Number(1), sp.Number(2), sp.Number(1.6)]
n = 10

cnt = [0, 0, 0, 0, 0, 0] # 加 剪 乘 除 函數 迭代數
progress_original = [tuple(area), tuple(area)]
progress_brent = [tuple(area_brent), tuple(area_brent)]

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
    plt.title(name)

    data = []
    for i in range(len(progress[0])):
        tmp = []
        for area in progress[1:]:
            tmp.append(area[i])
        data.append(tmp)

    colors = ['red', 'blue', 'green']
    for i in range(len(progress[0])):
        try:
            plt.plot([x for x in range(len(data[i]))], data[i], color=colors[i], marker='o')
        except:
            pass

    plt.show()

def OutputCSV(progress, name, title):
    if not name.endswith('.csv') or not name.endswith('.txt'):
        name = name + ".csv"
    with open(name, 'w') as file:
        file.write(title + ',\n')
        for area in progress[1:]:
            file.write(f'{area}'[1:-2] + '\n')

def CSVFusion(CSVs):
    output_str = []
    for i in CSVs:
        with open(i.__name__ + '.csv', 'r') as file:
            output_str += file.read()
    
    with open('fusioned.csv', 'w') as file:
        file.writelines(output_str)



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
        progress.append((area[0], area[1].evalf(n)))
    else:
        progress.append((area[0], area[1]))

# 固定點迭代法
def FPILeft(f, x, progress, statistic, evaluate=False):
    area = progress[-1]
    g = x - f

    xn = g.subs(x, area[0])

    statistic = Statistic(statistic, [0, 1, 0, 0, 1, 1])

    if evaluate:
        progress.append((xn.evalf(n), area[1]))
    else:
        progress.append((xn, area[1]))

def FPIRight(f, x, progress, statistic, evaluate=False):
    area = progress[-1]
    g = x - f

    xn = g.subs(x, area[1])

    statistic = Statistic(statistic, [0, 1, 0, 0, 1, 1])

    if evaluate:
        progress.append((area[0], xn.evalf(n)))
    else:
        progress.append((area[0], area[1]))

def BrentMethod(f, x, progress, statistic, evaluate=False):
    a, b, c = progress[-1][0], progress[-1][2], progress[-1][1]

    r = f.subs(x, a) / f.subs(x, c)
    s = f.subs(x, b) / f.subs(x, a)
    t = f.subs(x, a) / f.subs(x, c)
    
    p = s * (t * (r - t) * (c - b) - (1 - r) * (b - a))
    q = (t - 1) * (r - 1) * (s - 1)

    b = b + p / q

    if evaluate:
        progress.append((a, c, b.evalf(n)))
    else:
        progress.append((a, c, b))

def calc(func):
    name=func.__name__
    if not func.__name__ == 'BrentMethod':
        progress = copy.deepcopy(progress_original)
    else:
        progress = copy.deepcopy(progress_brent)

    i = 0
    while i < 30:
        # print(progress)
        func(f, x, progress, cnt, evaluate=True)

        if not func.__name__ == 'BrentMethod':
            if str(progress[-1][0].evalf(n)) == str(progress[-2][0].evalf(n)) and str(progress[-1][1].evalf(n)) == str(progress[-2][1].evalf(n)):
                progress = progress[:-2]
                break
        else:
            if str(progress[-1][2].evalf(n)) == str(progress[-2][2].evalf(n)):
                progress = progress[:-2]
                break

        i += 1

        print(i)

    print(progress)
    # PrintStatistic(cnt) # 印出統計資訊
    # OutputCSV(progress, name, name)
    DrawGraph(progress, name=name)

algorithms = [NewtonMethodLeft,
              NewtonMethodRight,
              BisectionMethod,
              SecantMethodLeft,
              SecantMethodRight,
              FPILeft,
              FPIRight,
              BrentMethod]

for algorithm in algorithms:
    calc(algorithm)

# CSVFusion(algorithms)