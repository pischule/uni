import numpy as np
import scipy.integrate


# функция из задания
def func1(t):
    return 3**t

# функция для проверки
def func2(t):
    return t


# степень многочлена
n = 4


# скалярное произведение
def dot_product(x, y):
    def func_product(t): return x(t) * y(t)
    return scipy.integrate.quad(func_product, 0, 1)[0]


# создает многочлен степени power
def build_power_func(power):
    def func(t):
        return t**power
    return func


# выводит многочлен с коэффициентами coeffs
def print_polinomial(coeffs):
    s = []
    for index, c in enumerate(coeffs):
        s.append(f'{c:.5f} t^{index}')
    print(' + '.join(s))


# находит коэффициенты многочлена
def get_coeffs(func):
    A = np.empty((n+1, n+1))
    F = np.empty(n+1)
    for i in range(5):
        F[i] = dot_product(build_power_func(i), func)
        for j in range(5):
            A[i][j] = dot_product(build_power_func(i),
                                  build_power_func(j))
    C = np.linalg.solve(A, F)
    return C


print('Приближение функции x(t) = 3^t')
coeffs1 = get_coeffs(func1)
print_polinomial(coeffs1)

print('Приближение функции x(t) = t')
coeffs2 = get_coeffs(func2)
print_polinomial(coeffs2)

