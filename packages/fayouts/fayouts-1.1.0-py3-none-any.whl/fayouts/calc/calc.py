import math 

e = 2.718281828459045
pi = 3.141592653589793
tau = 6.283185307179586

class doError(Exception):
    pass

def c(num1 = 0, num2 = 0, num3 = 0, num4 = 0, num5 = 0, do = "none"):
    if(do == 'none'):
        raise doError('Поле do равняется none')
    else:
        if(do == 'f'):
            return num1 + num2 + num3 + num4 + num5
        if(do == 's'):
            return num1 - num2 - num3 - num4 - num5
        if(do == 'm'):
            return num1 * num2 * num3 * num4 * num5
        if(do == 'd'):
            return num1 / num2 / num3 / num4 / num5
        else:
            raise doError('Переменная do должна придерживаться одного из типов: f(сложить), s(вычесть), m(умножить), d(разделить)')
