import math
from math import sqrt


def hcf_finder(num1, num2):
    num1_factors = []
    num2_factors = []
    common_factors = []
    for i in range(num1 + 1):
        if i != 0 and num1 % i == 0:
            num1_factors.append(i)
    for i in range(num2 + 1):
        if i != 0 and num2 % i == 0:
            num2_factors.append(i)
    for i in range(len(num1_factors)):
        for n in range(len(num2_factors)):
            if num1_factors[i] == num2_factors[n]:
                common_factors.append(num2_factors[n])
    common_factors.reverse()
    return common_factors[0]


def factor_finder(number):
    output = []
    for i in range(number + 1):
        if i != 0 and number % i == 0:
            output.append(i)
    return output


def odd_even_checker(number):
    if number % 2 == 0:
        return "even"
    elif number % 2 == 1:
        return "odd"
    else:
        return "Invalid number"


def square(number):
    return number * number


def cube(number):
    return pow(number, 3)


def find_distance_2_coor(x1, x2, y1, y2):
    return sqrt(pow(x1 - x2, 2) + pow(y1 - y2, 2))


def pythagoras(basesq, perpendicularsq):
    hypotenusesq = basesq + perpendicularsq
    hypotenuse = sqrt(hypotenusesq)
    return hypotenuse


def fibonacci(n):
    thelist = [1, 1]
    while len(thelist) != n:
        thelist.append(thelist[-1] + thelist[-2])
    return thelist


def cuberoot(x):  # Only Compatible with perfect cubes
    for ans in range(0, abs(x) + 1):
        if ans ** 3 == abs(x):
            break
    if ans ** 3 != abs(x):
        return 'Not a perfect cube'
    else:
        if x < 0:
            ans = -ans
    return ans
