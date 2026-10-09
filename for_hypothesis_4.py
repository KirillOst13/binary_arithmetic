def binary_div_restoring_1(dividend, divisor, bits=16):
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

def binary_div_1(dividend, divisor, bits=16):
    """Безвосстанавливающее деление с подсчётом операций"""
    if divisor == 0:
        raise ValueError("Деление на ноль")
    
    a = abs(dividend)
    b = abs(divisor)
    
    q_abs = 0
    r_abs = 0
    operations = 0  # счётчик операций
    
    for i in range(bits - 1, -1, -1):
        r_abs = (r_abs << 1) | ((a >> i) & 1)
        
        if r_abs >= b:
            r_abs -= b
            q_abs |= (1 << i)
            operations += 1  # одна операция вычитания
    
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