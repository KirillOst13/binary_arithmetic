# Итоговая проверка всех алгоритмов двоичной арифметики

from conversions import (
    decimal_to_binary_int,
    decimal_to_binary_frac,
    to_q88,
    from_q88
)
from algorithms import (
    binary_add,
    binary_sub,
    binary_mul,
    binary_div,
    q88_add,
    q88_sub,
    q88_mul,
    q88_div
)

print("=" * 70)
print("ИТОГОВАЯ ПРОВЕРКА ВСЕХ АЛГОРИТМОВ ДВОИЧНОЙ АРИФМЕТИКИ")
print("=" * 70)

# --- 1. Перевод целых чисел ---
print("\n1. ПЕРЕВОД ЦЕЛЫХ ЧИСЕЛ (10 → 2)")
print("-" * 70)
int_tests = [
    (13, "1101"),
    (5, "101"),
    (0, "0"),
    (255, "11111111"),
    (-5, "-101")
]
for num, expected in int_tests:
    result = decimal_to_binary_int(num)
    status = "OK" if result == expected else "ОШИБКА"
    print(f"  {num:>4} → {result:<12} (ожидание: {expected:<12}) [{status}]")

# --- 2. Перевод дробных частей ---
print("\n2. ПЕРЕВОД ДРОБНЫХ ЧАСТЕЙ (10 → 2)")
print("-" * 70)
frac_tests = [
    (0.5, 8, "0.1"),
    (0.25, 8, "0.01"),
    (0.625, 8, "0.101"),
    (0.1, 8, "0.00011001")
]
for frac, bits, expected in frac_tests:
    result = decimal_to_binary_frac(frac, bits)
    status = "OK" if result == expected else "ОШИБКА"
    print(f"  {frac:<5} ({bits} бит) → {result:<20} [{status}]")

# --- 3. Формат Q8.8 ---
print("\n3. ФОРМАТ Q8.8 (перевод туда и обратно)")
print("-" * 70)
q88_tests = [
    (1.5, 1.5),
    (-5.25, -5.25),
    (0.0, 0.0),
    (100.5, 100.5)
]
for original, expected in q88_tests:
    q_val = to_q88(original)
    back = from_q88(q_val)
    error = abs(back - expected)
    status = "OK" if error < 0.0001 else "ОШИБКА"
    print(f"  {original:>8} → Q8.8: {q_val:>6} → обратно: {back:>10.4f} [{status}]")

# --- 4. Сложение ---
print("\n4. СЛОЖЕНИЕ")
print("-" * 70)
print("  Целые числа:")
add_int_tests = [(10, 5, 15), (-3, 7, 4), (-8, -5, -13)]
for a, b, expected in add_int_tests:
    result = binary_add(a, b)
    status = "OK" if result == expected else "ОШИБКА"
    print(f"    {a:>5} + {b:>5} = {result:>5} [{status}]")

print("  Дробные числа (Q8.8):")
add_frac_tests = [(3.5, 2.25, 5.75), (-2.5, -1.5, -4.0)]
for a, b, expected in add_frac_tests:
    result = q88_add(a, b)
    error = abs(result - expected)
    status = "OK" if error < 0.005 else "ОШИБКА"
    print(f"    {a:>6} + {b:>6} = {result:>8.4f} [{status}]")

# --- 5. Вычитание ---
print("\n5. ВЫЧИТАНИЕ")
print("-" * 70)
print("  Целые числа:")
sub_int_tests = [(7, 3, 4), (3, 5, -2), (-5, -3, -2)]
for a, b, expected in sub_int_tests:
    result = binary_sub(a, b)
    status = "OK" if result == expected else "ОШИБКА"
    print(f"    {a:>5} - {b:>5} = {result:>5} [{status}]")

print("  Дробные числа (Q8.8):")
sub_frac_tests = [(7.0, 3.0, 4.0), (3.0, 5.0, -2.0)]
for a, b, expected in sub_frac_tests:
    result = q88_sub(a, b)
    error = abs(result - expected)
    status = "OK" if error < 0.005 else "ОШИБКА"
    print(f"    {a:>6} - {b:>6} = {result:>8.4f} [{status}]")

# --- 6. Умножение ---
print("\n6. УМНОЖЕНИЕ")
print("-" * 70)
print("  Целые числа:")
mul_int_tests = [(6, 4, 24), (-3, 4, -12), (-3, -4, 12)]
for a, b, expected in mul_int_tests:
    result = binary_mul(a, b)
    status = "OK" if result == expected else "ОШИБКА"
    print(f"    {a:>5} * {b:>5} = {result:>5} [{status}]")

print("  Дробные числа (Q8.8):")
mul_frac_tests = [(3.0, 2.0, 6.0), (0.5, 0.5, 0.25), (-2.0, 3.0, -6.0)]
for a, b, expected in mul_frac_tests:
    result = q88_mul(a, b)
    error = abs(result - expected)
    status = "OK" if error < 0.005 else "ОШИБКА"
    print(f"    {a:>6} * {b:>6} = {result:>8.4f} [{status}]")

# --- 7. Деление ---
print("\n7. ДЕЛЕНИЕ")
print("-" * 70)
print("  Целые числа:")
div_int_tests = [(10, 3, 3, 1), (7, 2, 3, 1), (-10, 3, -3, -1)]
for a, b, exp_q, exp_r in div_int_tests:
    q, r = binary_div(a, b)
    status = "OK" if q == exp_q and r == exp_r else "ОШИБКА"
    print(f"    {a:>5} / {b:>5} = {q:>5} (ост. {r:>3}) [{status}]")

print("  Дробные числа (Q8.8):")
div_frac_tests = [(6.0, 2.0, 3.0), (7.0, 2.0, 3.5), (-6.0, 2.0, -3.0)]
for a, b, expected in div_frac_tests:
    result = q88_div(a, b)
    error = abs(result - expected)
    status = "OK" if error < 0.01 else "ОШИБКА"
    print(f"    {a:>6} / {b:>6} = {result:>8.4f} [{status}]")

print("\n" + "=" * 70)
print("ПРОВЕРКА ЗАВЕРШЕНА")
print("=" * 70)
