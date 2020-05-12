import numpy as np
import math


# интегрируемая функция
def f(x):
    return 1/(1 + np.sin(x) + np.power(x, 2))


# промежуток интегрирования
a, b = 0, math.pi / 4

# точность
eps = 10**(-4)


# коэффициенты для правила Рунге
theta_vals = {'right_rect': 1/3, 'trapezium': 1/3,
              'simps': 1/15}


# коэффициенты для формулы Гаусса
gauss_x = {2: [-0.55773502692, 0.55773502692],
           3: [-0.7745966692, 0, 0.7745966692],
           4: [-0.8611363116, -0.3399810436, 0.3399810436, 0.8611363116]}
gauss_a = {2: [1, 1],
           3: [5/9, 8/9, 5/9],
           4: [0.3478548451, 0.6521451549, 0.6521451549, 0.3478548451]}


# метод правых прямоугольников
def right_rect(n):
    points = np.linspace(a, b, n+1)
    h = points[1:] - points[:-1]
    return np.sum(f(points[1:]) * h)


# метод трапеции
def trapezium(n):
    points = np.linspace(a, b, n+1)
    h = points[1:] - points[:-1]
    return np.sum((f(points[:-1]) + f(points[1:])) / 2 * h)


# метод Симпсона
def simps(n):
    points = np.linspace(a, b, n+1)
    h = points[1:] - points[:-1]
    return np.sum((f(points[:-1]) + f(points[1:]) +
                   4 * f((points[:-1] + points[1:])/2)) * h / 6)


# функция для замены переменной в формуле Гаусса
def scale(x):
    return (a + b) / 2 + (b - a) * x / 2


# формула Гаусса
def gauss(n):
    assert(2 <= n <= 4)
    result = 0
    for (xi, ai) in zip(gauss_x[n], gauss_a[n]):
        result += ai * f(scale(xi))
    return result * (b-a)/2


# оценивает погрешность для шага 2n
# для данного theta по правилу Рунге
def runge(prev, curr, theta):
    return np.abs(curr - prev) * theta


# выводит в консоль таблицу для данного метода
# в формате LaTeX
def show_latex_table(method, method_name):
    theta = theta_vals[method_name]
    n = 1
    h = b - a
    curr = method(n)
    error = math.inf
    print(f'& $h = {h:.6f}$ & $I_h={curr:.6f}$ &  \\\\ \\cline{{2-4}} ')
    while error > eps:
        n *= 2
        h /= 2
        prev, curr = curr, method(n)
        error = runge(prev, curr, theta)
        print(f'& $h/{n} = {h:.6f}$ & $I_{{h/{n}}}={curr:.6f}$ & $R_{{h/{n}}}=\
{error:.6f}$ \\\\ \cline{{2-4}} ')


# выведем таблицу для метода правых прямоугольников
show_latex_table(right_rect, 'right_rect')


# выведем таблицу для метода трапеций
show_latex_table(trapezium, 'trapezium')


# выведем таблицу для метода Симпсона
show_latex_table(simps, 'simps')


# выведем приближенные значения интеграла,
# подсчитанные по формуле Гаусса
for i in range(2, 5):
    print(f'{i}:\t{gauss(i):.10f}')
