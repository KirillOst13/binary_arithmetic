def binary_div_1(dividend, divisor, bits=16):
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