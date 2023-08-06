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


def prime_check(n):
    factors = []
    for i in range(n + 1):
        if i != 0 and n % i == 0:
            factors.append(i)
    if len(factors) == 2:
        return True
    else:
        return False


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


def tothepoweranythingroot(tothepowerofwhat, number):
    for ans in range(0, abs(number) + 1):
        if ans ** tothepowerofwhat == abs(number):
            break
    if ans ** tothepowerofwhat != abs(number):
        return 'Not perfect'
    else:
        if number < 0:
            ans = -ans
    return ans


def decimalToBinary(n):
    return bin(n).replace("0b", "")


def binaryToDecimal(n):
    stingn = str(n)
    for character in stingn:
        if character == '.':
            return 'Invalid'
        if character != 0 and character != 1:
            return 'Invalid'
    num = n
    dec_value = 0

    base = 1

    temp = num
    while (temp):
        last_digit = temp % 10
        temp = int(temp / 10)

        dec_value += last_digit * base
        base = base * 2
    return dec_value


def profitpercentcalculator(investment, output):
    profit_or_loss_amount = output - investment
    if profit_or_loss_amount >= 0:
        profit_or_loss = 'profit'
    elif profit_or_loss_amount < 0:
        profit_or_loss = 'loss'
    else:
        return 'Invalid Inputs'
    if profit_or_loss == 'profit':
        return str((profit_or_loss_amount / investment * 100)) + '% Profit'
    elif profit_or_loss == 'loss':
        return str((abs(profit_or_loss_amount) / investment * 100)) + '% Loss'
