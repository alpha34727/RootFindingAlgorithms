# 匯入函式庫
import sympy as sp                # 負責符號運算
import matplotlib.pyplot as plt   # 負責繪製圖表

# 變數定義
f = sp.symbols('f', cls=sp.Function) # 名為「f」的函數
x = sp.symbols('x')                  # 名為「x」的自變數

# 統計運算次數的函數
cnt = [0, 0, 0, 0, 0] # 加 剪 乘 除 函數

# 每次遞迴後的範圍
progress_x = [] # 左
progress_y = [] # 右


# /--------------設定區域--------------/

f = x ** 3 + 2 * x - 5                # 函數 x^3 + 2x -5
area = (sp.Number(1), sp.Number(2))   # 範圍
n = 10                                # 估計位數（有效位數）

# /-----------------------------------/



# /--------------統計區域--------------/

# 統計函數
def Statistic(cnt, movement):
    """統計函數，負責統計運算過程中的加減乘除與函數運算"""

    for i in range(5):
        cnt[i] += movement[i]

# 印出統計資料
def PrintStatistic(cnt):
    """印出統計資料"""

    name = ['加法', '減法', '乘法', '除法', '函數運算']
    for i in range(5):
        print(name[i], cnt[i], sep=' : ')

# /-----------------------------------/



# /--------------逼近演算法區域--------------/

#牛頓法（右逼近）
def NewtonMethodRight(f, area, evaluate, statistic):
    """牛頓法（右逼近）
    NewtonMethodRight(函數, 範圍, 是否估計, 統計的List)"""

    # 牛頓法：a_n+1 = a_n - f(a_n) / f'(a_n)
    an = area[1] - f.subs(x, area[1]) / f.diff().subs(x, area[1]) 

    # 統計
    statistic = Statistic(statistic, [0, 1, 0, 1, 2])

    # 如果使用估計，則回傳估計後的結果
    if evaluate:
        return area[0], an.evalf(n) 
    return area[0], an

#牛頓法（左逼近）
def NewtonMethodLeft(f, area, evaluate, statistic):
    """牛頓法（左逼近）
    NewtonMethodLeft(函數, 範圍, 是否估計, 統計的List)"""

    # 牛頓法：a_n+1 = a_n - f(a_n) / f'(a_n)
    an = area[0] - f.subs(x, area[0]) / f.diff().subs(x, area[0]) 

    # 統計
    statistic = Statistic(statistic, [0, 1, 0, 1, 2])

    # 如果使用估計，則回傳估計後的結果
    if evaluate:
        return an.evalf(n), area[1]
    return an, area[1]

#二分逼近法
def BisectionMethod(f, area, evalutate, statistic):
    """二分逼近法
    BisectionMethod(函數, 範圍, 是否估計, 統計的List)"""

    # 範圍的中點 = (a0 + a1) / 2
    amid = (area[0] + area[1]) / 2

    # 如果 f(左範圍) > f(右範圍)，即函數 向右下傾斜
    if f.subs(x, area[0]) > f.subs(x, area[1]):
        # 如果 f(中點) > 0，根在 中點 和 左範圍 之間
        if f.subs(x, amid) > 0:
            area = (amid, area[1])
        # 否則，根在 右範圍 和 中點 之間
        else:
            area = (area[0], amid)
    
    # 否則，即函數 向左下傾斜 或 水平
    else:
        # 如果 f(中點) > 0，根在 右範圍 和 中點 之間
        if f.subs(x, amid) > 0:
            area = (area[0], amid)
        # 否則，根在 中點 和 左範圍 之間
        else:
            area = (amid, area[1])
    
    # 統計
    statistic = Statistic(statistic, [1, 0, 0, 1, 3])

    # 如果使用估計，則回傳估計後的結果
    if evalutate:
        return area[0].evalf(n), area[1].evalf(n)
    return area

# /------------------------------------------/



# /--------------主程式--------------/

# 印出a1，紀錄a1
i = 1
print(f'a1 : ({area[0].evalf(n)}, {area[1].evalf(n)})')
progress_x.append(area[0].evalf(n))
progress_y.append(area[1].evalf(n))

while True:
    original_area = area # 紀錄上一次的範圍至 original_area

    area = NewtonMethodLeft(f, area, False, cnt) # 使用逼近演算法計算新的範圍

    # 當新的範圍的估計值 與 上一次範圍的估計值 相等時，迴圈停止
    if str(original_area[0].evalf(n)) == str(area[0].evalf(n)) and str(original_area[1].evalf(n)) == str(area[1].evalf(n)):
        break

    # 印出an，紀錄an
    print(f'a{i+1} : ({area[0].evalf(n)}, {area[1].evalf(n)})')
    progress_x.append(area[0].evalf(n))
    progress_y.append(area[1].evalf(n))

    i += 1

PrintStatistic(cnt) # 印出統計資訊
print(progress_x)   # 印出每次運算的左範圍
print(progress_y)   # 印出每次運算的右範圍

# 繪製圖表
plt.title("NewtonMethodLeft") # 設定圖名
plt.plot([x+1 for x in range(len(progress_x))], progress_x, color='red', marker='o')  # 繪製左範圍
plt.plot([x+1 for x in range(len(progress_y))], progress_y, color='blue', marker='o') # 繪製右範圍
plt.show() # 顯示圖表

# /----------------------------------/
