import numpy as np


def f(x):
    """Исходная функция"""
    return x ** 3 - 2 * x ** 2 - 10 * x + 15


def df(x):
    """Дифференциал функции"""
    return 3 * x ** 2 - 4 * x - 10


def phi(x):
    """Сужающее преобразование"""
    return (2*x**2 - 15) / (x**2 - 10)


def plot_graph():
    """Построение графика"""
    x = np.linspace(-5, 5, 100)
    vf = np.vectorize(f)
    plt.grid(True)
    plt.plot(x, vf(x), )
    plt.plot(x, np.zeros(x.size))
    plt.show()


def mpd(func=f, a=0, b=2, eps=10 ** -2):
    print('Метод деления пополам')
    k = 1

    while True:
        ab = (a + b) / 2
        f_a = func(a)
        f_b = func(b)
        f_ab = func(ab)
        # локализация корня
        a_b = abs(a-b) / 2
        print(f'{k} {a:.4f} {b:.4f} {f_a:.4f} {f_b:.4f} \
{ab:.4f} {f_ab:.4f} {a_b:.4f}')

        if a_b < eps:
            return ab

        if func(a) * func(ab) > 0:
            a = ab
        else:
            b = ab
        k += 1


def newton(x_k, func=f, dfunc=df, eps=10 ** -7):
    print('Метод Ньютона')
    k = 1
    x_k_prev = x_k + 100 + eps
    while True:
        f_xk = func(x_k)
        # Шаг приближения
        accuracy = abs(x_k - x_k_prev)
        print(f'{k} {x_k:.7f} {accuracy:.7f}')

        if accuracy < eps:
            return x_k

        x_k_prev = x_k
        x_k -= func(x_k) / dfunc(x_k)
        k += 1


def mpi(x_k, phi=phi, func=f, eps=10 ** -7):
    print('Метод простой итерации')
    k = 1
    x_k_prev = x_k + 100 + eps

    while True:
        accuracy = abs(x_k - x_k_prev)
        print(f'{k} {x_k:.7f} {accuracy:.7f}')
        if accuracy < eps:
            return x_k

        x_k_prev = x_k
        x_k = phi(x_k)
        k += 1

a = 0
b = 2

x_approx = mpd()
newton(x_approx)
mpi(x_approx)
