#!/usr/bin/python3

import math
import numpy as np
import matplotlib.pyplot as plt

plt.rcParams.update({'font.size': 15})  # шрифт на графике

f1 = lambda x: math.sin(math.cos(x))    # первая функция
f2 = lambda x: abs(abs(x) - 1)          # вторая функция

a, b = -2, 2  # начало, конец отрезка интерполяции

pic_count = 1


def make_points(func, n):
    """Возвращает таблицу значений на равноудалённых точках"""
    delta = (b - a) / (n - 1)
    xs = np.arange(a, b + delta, delta)
    return [(x, func(x)) for x in xs]


def make_chebyshev_points(func, n):
    """Возвращает таблицу значений в точках -- корнях мн. Чебышёва"""
    avr = (a + b) / 2
    dlt = (b - a) / 2
    xs = [avr + dlt * math.cos(math.pi * (2 * i + 1) / (2 * n))
          for i in range(n)]
    return [(x, func(x)) for x in xs]


def make_polynomial(table):
    """Возвращает полином, построенный по таблице значений"""
    n = len(table)                   # количество точек
    xs = [i[0] for i in table]
    fs = [[i[1] for i in table]]     # разделённые разности

    for i in range(n - 1):           # вычисляем разделённые разности
        f_col = []
        for j in range(n - i - 1):
            val = (fs[i][j + 1] - fs[i][j]) / (xs[j + i + 1] - xs[j])
            f_col.append(val)
        fs.append(f_col)

    coeffs = [i[0] for i in fs]     # коэффициенты многочлена Ньютона

    def poly(x):
        result = 0
        for i in range(n):
            term = coeffs[i]
            for j in range(i):
                term *= (x - xs[j])
            result += term
        return result

    return poly


def give_x_y(func):
    """Возвращает набор точек для построения графика"""
    x = np.arange(-2, 2, 0.05)
    fvect = np.vectorize(func)
    y = fvect(x)
    return x, y


def diff_func(func1, func2):
    """Находит модуль остатка интерполирования"""
    def diff(x):
        return abs(func1(x) - func2(x))
    return diff


def save_plt(plt):
    """Сохраняет график в файл"""
    global pic_count
    print(str(pic_count) + ".pdf")
    plt.savefig("../images/" + str(pic_count) + ".pdf")
    pic_count += 1
    plt.close()


def show_for_func(func, s=""):
    """Строит графики для функции func"""

    ns = [3, 5, 7, 10, 15]      # степени многочлена
    for n in ns:
        # генерируем значения
        p = make_points(func, n)
        cp = make_chebyshev_points(func, n)

        # строим полином
        poly = make_polynomial(p)
        poly_c = make_polynomial(cp)

        # строим графики
        plt.plot(*give_x_y(func), label="f(x)")
        plt.plot(*give_x_y(poly), label=f"равноуд.")
        plt.plot(*give_x_y(poly_c), label=f"Чебышёв")
        plt.title(s + f" ({n})")
        plt.legend()
        save_plt(plt)

        # строим график отклонения
        plt.title(f"|r(x)| ({n})")
        poly_diff = diff_func(func, poly)
        poly_c_diff = diff_func(func, poly_c)
        plt.plot(*give_x_y(poly_diff), label=f"равноуд.")
        plt.plot(*give_x_y(poly_c_diff), label=f"Чебышёв")
        plt.legend()
        save_plt(plt)


show_for_func(f1, "sin(cos(x))")
show_for_func(f2, "||x|-1|")
