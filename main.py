import sympy as sp

f = sp.symbols('f', cls=sp.Function)
x = sp.symbols('x')

f = x ** 3 + 2 * x - 5
a = sp.Number(2)

#牛頓法
def NewtonMethod(f, a, evaluate):
    an = a - f.subs(x, a) / f.diff().subs(x, a)
    if evaluate:
        return an.evalf()
    return an

#二分逼近法
def BisectionMethod(f, a, evalutate):
    pass

i = 1
while True:
    print(f'a{i}', a.evalf())
    an = NewtonMethod(f, a, False)
    if a.evalf() == an.evalf():
        break
    a = an
    i += 1
    