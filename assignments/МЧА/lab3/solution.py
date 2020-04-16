# To add a new cell, type ''
# To add a new markdown cell, type ' [markdown]'

import numpy as np
import matplotlib.pyplot as plt


def tdma(a, c, b, f):
    """Находит решение системы уравнений методом прогонки

    b - дигональ над главной [0;n-1)
    c - главная диагональ [0;n)
    a - диагональ под главной [0;n-1]
    f - столбец справа
    """
    f_copy = f.copy()

    n = len(c)
    x = [0 for i in range(n)]

    for i in range(1, n):
        m = a[i - 1] / c[i - 1]
        c[i] -= m * b[i - 1]
        f_copy[i] -= m * f_copy[i - 1]

    x[n - 1] = f_copy[n - 1] / c[n - 1]

    for i in reversed(range(n - 1)):
        x[i] = (f_copy[i] - b[i] * x[i + 1]) / c[i]
    return x


pic_count = 1
plt.rcParams['axes.linewidth'] = 0.1


def save_plt(plt):
    """Сохраняет график в файл"""
    global pic_count
    plt.savefig("images/" + str(pic_count) + ".pdf")
    pic_count += 1
    plt.close()


def func(x):
    return x**2/(1 + x**3)


vfunc = np.vectorize(func)

# количество промежутков
n = 15

# начало, конец
start, end = 0, 2

# значения второй производной в точках 0, 2
dd0 = 2
dd2 = 2/81

# значения первой производной в точках 0, 2
d0 = 0
d2 = -4/27


def build_spline(start, end, n, function, kind=3):
    x = np.linspace(start, end, n+1)
    y = function(x)

    a = y[:-1]
    h = (end - start) / n

    # столбец СЛАУ c (n-1) значениями
    F = 3*(y[:-2] - 2*y[1:-1] + y[2:])/h**2

    # диагонали матрицы A
    bottom_diag = np.ones(n)
    upper_diag = np.ones(n)
    main_diag = 4*np.ones(n+1)

    # добавляем граничные условия в зависимости от типа сплайна
    if kind == 1:
        main_diag[0], main_diag[-1] = 2, 2
        upper_diag[0], bottom_diag[-1] = 1, 1
        f_1 = 3*(y[1]-y[0])/h**2 - 3*d0/h
        f_np1 = 3*d2/h - 3*(y[-1] - y[-2])/h**2
    elif kind == 2:
        main_diag[0], main_diag[-1] = 2, 2
        upper_diag[0], bottom_diag[-1] = 0, 0
        f_1, f_np1 = dd0, dd2
    elif kind == 3:
        main_diag[0], main_diag[-1] = 1, 1
        upper_diag[0], bottom_diag[-1] = 0, 0
        f_1, f_np1 = 0, 0
    else:
        raise Exception("there are only 3 kinds of splines")

    # добавим еще 2 значения к столбцу F: f_1, f_{n+1}
    F = np.concatenate([[f_1], F, [f_np1]])


    # решаем СЛАУ методом прогонки
    C = np.array(tdma(bottom_diag, main_diag, upper_diag, F))

    b = (y[1:] - y[:-1])/h - (2*C[:-1] + C[1:])*h/3
    d = (C[1:] - C[:-1])/3/h

    # создаём функцию-сплайн
    def spline(p):
        i = int((p - start)/(end-start)*n)
        i = min(n-1, max(0, i))
        return a[i] + b[i]*(p-x[i]) + C[i]*(p-x[i])**2 + d[i]*(p-x[i])**3
    vspline = np.vectorize(spline)

    return vspline


def demo(kind):
    plt.figure(num=None, figsize=(8, 6), dpi=80, facecolor='w', 
        edgecolor='k')

    # точки для построения графика
    xpoints = np.linspace(start, end, 100)
    ypoints = vfunc(xpoints)

    # узлы интерполирования
    x_interp_points = np.linspace(start, end, n+1)
    y_interp_points = vfunc(x_interp_points)

    # строим сплайн
    spline = build_spline(start, end, n, vfunc, kind)
    y_spline_points = spline(xpoints)

    plt.plot(xpoints, ypoints, label='f')
    plt.plot(x_interp_points, y_interp_points, 'or')
    plt.plot(xpoints, y_spline_points, label=f'S({kind})')

    print('Разность в узлах интерполирования')
    print(y_interp_points - spline(x_interp_points))

    print('Максимальное отклонение в точках между узлами')
    h = (end-start)/n
    middle_points = x_interp_points[:-1] + h/2
    max_dev = np.max(np.abs(vfunc(middle_points) - spline(middle_points)))
    print(f'{max_dev:.12f}')

    plt.legend()
    save_plt(plt)
    plt.show()


def threes_spline_one_plot():
    plt.figure(num=None, figsize=(8, 6), dpi=80, facecolor='w', 
        edgecolor='k')

    # точки для построения графика
    xpoints = np.linspace(start, end, 100)
    ypoints = vfunc(xpoints)

    # узлы интерполирования
    x_interp_points = np.linspace(start, end, n+1)
    y_interp_points = vfunc(x_interp_points)

    # строим сплайны
    spline1 = build_spline(start, end, n, vfunc, 1)
    y_spline1 = spline1(xpoints)

    # строим сплайны
    spline2 = build_spline(start, end, n, vfunc, 2)
    y_spline2 = spline2(xpoints)

    # строим сплайны
    spline3 = build_spline(start, end, n, vfunc, 3)
    y_spline3 = spline3(xpoints)

    plt.plot(xpoints, ypoints, label='f')
    plt.plot(xpoints, y_spline1, label='S(1)')
    plt.plot(xpoints, y_spline2, label='S(2)')
    plt.plot(xpoints, y_spline3, label='S(3)')

    plt.legend()

    save_plt(plt)
    plt.show()


demo(1)
demo(2)
demo(3)
threes_spline_one_plot()

