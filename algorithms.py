from conversions import (
    to_q88,
    from_q88
)

def binary_add(a, b, bits=16):
    """Складывает два целых числа побитно с учётом переноса"""
    mask = (1 << bits) - 1
    
    # Преобразуем отрицательные числа в дополнительный код
    if a < 0:
        a = (1 << bits) + a
    if b < 0:
        b = (1 << bits) + b
    
    a &= mask
    b &= mask
    
    result = 0
    carry = 0
    
    for i in range(bits):
        bit_a = (a >> i) & 1
        bit_b = (b >> i) & 1
        sum_bit = bit_a ^ bit_b ^ carry
        carry = (bit_a & bit_b) | (bit_a & carry) | (bit_b & carry)
        result |= (sum_bit << i)
    
    result &= mask
    
    # Преобразуем результат обратно в знаковое число Python
    # Если старший бит равен 1 — число отрицательное
    if result & (1 << (bits - 1)):
        result -= (1 << bits)
    
    return result

def q88_add(a, b):
    """Складывает два дробных числа в формате Q8.8"""
    a_q = to_q88(a)
    b_q = to_q88(b)
    result_q = binary_add(a_q, b_q)
    return from_q88(result_q)

def binary_sub(a, b, bits=16):
    """Вычитает b из a через дополнительный код"""
    mask = (1 << bits) - 1
    
    # Преобразуем отрицательные числа в дополнительный код
    if a < 0:
        a = (1 << bits) + a
    if b < 0:
        b = (1 << bits) + b
    
    a &= mask
    b &= mask
    
    # Получаем -b: инвертируем биты и прибавляем 1
    minus_b = ((~b) + 1) & mask
    
    # Вычитание = сложение с отрицательным числом
    result = binary_add(a, minus_b, bits)
    
    return result

def q88_sub(a, b):
    """Вычитает два дробных числа в формате Q8.8"""
    a_q = to_q88(a)
    b_q = to_q88(b)
    result_q = binary_sub(a_q, b_q)
    return from_q88(result_q)

def binary_mul(a, b, bits=16):
    """Умножает два целых числа через сдвиги и сложение"""
    mask = (1 << bits) - 1
    
    # Определяем знак результата
    negative_result = (a < 0) != (b < 0)
    
    # Работаем с абсолютными значениями
    a = abs(a)
    b = abs(b)
    
    a &= mask
    b &= mask
    
    result = 0
    
    # Пока в множителе есть единичные биты
    while b > 0:
        # Если младший бит множителя равен 1 — прибавляем
        if b & 1:
            result = (result + a) & mask
        # Сдвигаем множимое влево (умножаем на 2)
        a = (a << 1) & mask
        # Сдвигаем множитель вправо (переходим к следующему биту)
        b >>= 1
    
    # Если результат должен быть отрицательным, преобразуем в дополнительный код
    if negative_result and result != 0:
        result = ((~result) + 1) & mask
    
    # Преобразуем в знаковое число Python
    if result & (1 << (bits - 1)):
        result -= (1 << bits)
    
    return result

def q88_mul(a, b):
    """Умножает два дробных числа в формате Q8.8"""
    a_q = to_q88(a)
    b_q = to_q88(b)
    
    # Преобразуем из 16-битного дополнительного кода в знаковые числа Python
    if a_q & 0x8000:
        a_signed = a_q - 0x10000
    else:
        a_signed = a_q
    
    if b_q & 0x8000:
        b_signed = b_q - 0x10000
    else:
        b_signed = b_q
    
    raw_result = binary_mul(a_signed, b_signed, bits=32)
    
    # Сдвигаем вправо на 8 бит, чтобы компенсировать двойное масштабирование
    # Обрезаем до 16 бит для корректной работы from_q88
    result_q = (raw_result >> 8) & 0xFFFF
    
    return from_q88(result_q)

def binary_div(dividend, divisor, bits=16):
    """Делит dividend на divisor, полностью имитируя поведение Python"""
    if divisor == 0:
        raise ValueError("Деление на ноль")
    
    # 1. Работаем с абсолютными значениями (классическое деление в столбик)
    a = abs(dividend)
    b = abs(divisor)
    
    q_abs = 0
    r_abs = 0
    
    for i in range(bits - 1, -1, -1):
        r_abs = (r_abs << 1) | ((a >> i) & 1)
        if r_abs >= b:
            r_abs -= b
            q_abs |= (1 << i)
    
    # 2. Адаптируем результат под правила Python:
    # В Python остаток всегда имеет тот же знак, что и ДЕЛИТЕЛЬ (divisor)
    
    # Если знаки разные и есть остаток, корректируем по правилам Python
    if (dividend < 0) != (divisor < 0) and r_abs != 0:
        q_abs += 1
        r_abs = b - r_abs
    
    # 3. Расставляем правильные знаки
    if dividend < 0 and divisor > 0:
        q = -q_abs
        r = r_abs
    elif dividend > 0 and divisor < 0:
        q = -q_abs
        r = -r_abs
    elif dividend < 0 and divisor < 0:
        q = q_abs
        r = -r_abs
    else:  # оба положительные
        q = q_abs
        r = r_abs
        
    return q, r

def q88_div(a, b):
    """Делит два дробных числа в формате Q8.8"""
    if b == 0:
        raise ValueError("Деление на ноль")
    
    a_q = to_q88(a)
    b_q = to_q88(b)
    
    # Преобразуем из 16-битного дополнительного кода в знаковые числа
    if a_q & 0x8000:
        a_signed = a_q - 0x10000
    else:
        a_signed = a_q
    
    if b_q & 0x8000:
        b_signed = b_q - 0x10000
    else:
        b_signed = b_q
    
    # Сдвигаем делимое влево на 8 бит для сохранения точности дробной части
    a_shifted = a_signed << 8
    
    # Делим с использованием 32 бит, чтобы не потерять старшие разряды
    quotient, remainder = binary_div(a_shifted, b_signed, bits=32)
    
    # Обрезаем результат до 16 бит для корректной работы from_q88
    result_q = quotient & 0xFFFF
    
    return from_q88(result_q)

def binary_div_restoring(dividend, divisor, bits=16):
    """Классическое восстанавливающее деление с подсчётом операций"""
    if divisor == 0:
        raise ValueError("Деление на ноль")
    
    # Работаем с абсолютными значениями
    a = abs(dividend)
    b = abs(divisor)
    
    q_abs = 0
    r_abs = 0
    operations = 0  # счётчик операций вычитания/сложения
    
    for i in range(bits - 1, -1, -1):
        r_abs = (r_abs << 1) | ((a >> i) & 1)
        
        # Пробуем вычесть делитель
        temp = r_abs - b
        operations += 1  # одна операция вычитания
        
        if temp >= 0:
            r_abs = temp
            q_abs |= (1 << i)
        else:
            # Восстанавливаем остаток — прибавляем делитель обратно
            r_abs = temp + b
            operations += 1  # ещё одна операция сложения
    
    # Расставляем знаки (как в binary_div)
    if (dividend < 0) != (divisor < 0) and r_abs != 0:
        q_abs += 1
        r_abs = b - r_abs
    
    if dividend < 0 and divisor > 0:
        q = -q_abs
        r = r_abs
    elif dividend > 0 and divisor < 0:
        q = -q_abs
        r = -r_abs
    elif dividend < 0 and divisor < 0:
        q = q_abs
        r = -r_abs
    else:
        q = q_abs
        r = r_abs
    
    return q, r, operations