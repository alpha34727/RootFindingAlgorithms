import sympy as sp

f = sp.symbols('f', cls=sp.Function)
x = sp.symbols('x')

f = x ** 3 + 2 * x - 5
area = (sp.Number(1), sp.Number(2))
n = 50

#牛頓法（右逼近）
def NewtonMethodRight(f, area, evaluate):
    an = area[1] - f.subs(x, area[1]) / f.diff().subs(x, area[1])
    if evaluate:
        return area[0], an.evalf(5)
    return area[0], an

#牛頓法（左逼近）
def NewtonMethodLeft(f, area, evaluate):
    an = area[0] - f.subs(x, area[0]) / f.diff().subs(x, area[0])
    if evaluate:
        return an.evalf(n), area[1]
    return an.evalf(n), area[1]

#二分逼近法
def BisectionMethod(f, a, evalutate):
    pass

for i in range(10):
    original_area = area
    print(f'a{i+1} : ({area[0].evalf(n)}, {area[1].evalf(n)})')
    area = NewtonMethodLeft(f, area, True)

    if str(original_area[0]) == str(area[0]) and str(original_area[1]) == str(area[1]):
        break
    