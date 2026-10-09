def decimal_to_binary_int(n):
    """Переводит целое десятичное число в двоичную строку"""
    # Особый случай: число 0
    if n == 0:
        return "0"
    
    # Запоминаем знак и работаем с положительным числом
    is_negative = n < 0
    n = abs(n)
    
    binary_digits = []
    
    # Делим на 2, пока число не станет нулём
    while n > 0:
        binary_digits.append(str(n % 2))  # остаток от деления на 2
        n = n // 2                         # целая часть от деления
    
    # Остатки получились в обратном порядке, переворачиваем их
    result = ''.join(reversed(binary_digits))
    
    # Если число было отрицательным, добавляем минус в начало
    if is_negative:
        return "-" + result
    return result

def decimal_to_binary_frac(fraction, max_bits=8):
    """Переводит дробную часть из десятичной системы в двоичную"""
    # Проверяем, что дробь находится в правильном диапазоне
    if fraction < 0 or fraction >= 1:
        raise ValueError("Дробная часть должна быть в диапазоне [0, 1)")
    
    binary_digits = []
    
    # Повторяем max_bits раз или пока дробь не станет нулём
    for _ in range(max_bits):
        fraction *= 2
        
        if fraction >= 1:
            binary_digits.append('1')
            fraction -= 1  # отбрасываем целую часть
        else:
            binary_digits.append('0')
        
        # Если дробь стала нулём — точное представление найдено
        if fraction == 0:
            break
    
    return '0.' + ''.join(binary_digits)

def to_q88(x):
    """Переводит десятичное число в формат Q8.8 (целое представление)"""
    # Умножаем на 256 и округляем до целого
    q_value = int(round(x * 256))
    
    # Для отрицательных чисел используем дополнительный код (16 бит)
    if q_value < 0:
        q_value = (1 << 16) + q_value
    
    # Ограничиваем 16 битами (маска 0xFFFF)
    return q_value & 0xFFFF


def from_q88(q):
    """Переводит число из формата Q8.8 обратно в десятичное"""
    # Если получили знаковое число Python, преобразуем в 16-битное
    if q < 0:
        q = (1 << 16) + q
    
    # Ограничиваем 16 битами
    q &= 0xFFFF
    
    # Проверяем знак по старшему биту
    if q & 0x8000:
        q = q - (1 << 16)
    
    return q / 256.0

