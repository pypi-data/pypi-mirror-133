import calendar
import math

class cal():
    def yr(year):
        user = calendar.calendar(year)
        return print(user)

    def mth(year, month):
        user = calendar.month(year, month)
        return print(user)

class calc():
    def sum(num_1, num_2):
        return num_1 + num_2

    def dif(num_1, num_2):
        return num_1 - num_2

    def mul(num_1, num_2):
        return num_1 * num_2

    def div(num_1, num_2):
        return num_1 / num_2

    def rem(num_1, num_2):
        return num_1 % num_2

    def floor(num_1, num_2):
        return num_1 // num_2

    def sq(num):
        return num * num

    def sqrt(num):
        sqrt = math.sqrt(num)
        return print(sqrt)

    def cube(num):
        return num * num * num

    print(cube(2))


