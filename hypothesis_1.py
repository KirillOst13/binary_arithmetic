import random
import time
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
from for_hypothesis_4 import(
    binary_div_restoring_1,
    binary_div_1
)

def test_hypothesis_1():
    """Проверка гипотезы 1: корректность битовых алгоритмов"""
    
    # Счётчики успешных тестов
    add_ok = 0
    sub_ok = 0
    mul_ok = 0
    div_ok = 0
    
    n_tests = 100
    
    for i in range(n_tests):
        # Генерируем случайные числа в диапазоне [-128, 127]
        a = random.randint(-128, 127)
        b = random.randint(-128, 127)
        
        # Для деления избегаем нуля в делителе
        if b == 0:
            b = 1
        
        # --- СЛОЖЕНИЕ ---
        expected_add = a + b
        actual_add = binary_add(a, b)
        if actual_add == expected_add:
            add_ok += 1
        
        # --- ВЫЧИТАНИЕ ---
        expected_sub = a - b
        actual_sub = binary_sub(a, b)
        if actual_sub == expected_sub:
            sub_ok += 1
        
        # --- УМНОЖЕНИЕ ---
        expected_mul = a * b
        actual_mul = binary_mul(a, b)
        if actual_mul == expected_mul:
            mul_ok += 1
        
        # --- ДЕЛЕНИЕ ---
        expected_q = a // b  
        expected_r = a % b
        actual_q, actual_r = binary_div(a, b)
        
        if actual_q == expected_q and actual_r == expected_r:
            div_ok += 1
    
    # Выводим результаты
    print("=" * 60)
    print("ПРОВЕРКА ГИПОТЕЗЫ 1: КОРРЕКТНОСТЬ БИТОВЫХ АЛГОРИТМОВ")
    print("=" * 60)
    print(f"Количество тестов: {n_tests}")
    print(f"Диапазон чисел: [-128, 127]")
    print("-" * 60)
    print(f"Сложение:    {add_ok}/{n_tests} совпадений  ({add_ok}%)")
    print(f"Вычитание:   {sub_ok}/{n_tests} совпадений  ({sub_ok}%)")
    print(f"Умножение:   {mul_ok}/{n_tests} совпадений  ({mul_ok}%)")
    print(f"Деление:     {div_ok}/{n_tests} совпадений  ({div_ok}%)")
    print("-" * 60)
    
    if add_ok == n_tests and sub_ok == n_tests and mul_ok == n_tests and div_ok == n_tests:
        print("ВЫВОД: Гипотеза 1 ПОДТВЕРЖДЕНА")
        
    else:
        print("ВЫВОД: Гипотеза 1 НЕ ПОДТВЕРЖДЕНА")
        print("Обнаружены расхождения между битовыми и обычными операциями.")

# Запуск проверки
test_hypothesis_1()
print()

def test_hypothesis_2():
    """Проверка гипотезы 2: погрешность представления дробных чисел"""
    
    # Дроби, которые будем проверять
    fractions = [0.1, 0.2, 0.3, 0.5, 0.7]
    
    # Количество бит для тестирования
    bit_counts = [4, 8, 16, 32]
    
    print("=" * 70)
    print("ПРОВЕРКА ГИПОТЕЗЫ 2: ПОГРЕШНОСТЬ ПРЕДСТАВЛЕНИЯ ДРОБНЫХ ЧИСЕЛ")
    print("=" * 70)
    print(f"Дроби: {fractions}")
    print(f"Количество бит: {bit_counts}")
    print("-" * 70)
    
    # Словарь для хранения результатов: {дробь: {биты: погрешность}}
    results = {f: {} for f in fractions}
    
    # Для каждой дроби и каждого количества бит считаем погрешность
    for frac in fractions:
        for bits in bit_counts:
            # Переводим дробь в двоичную систему
            binary = decimal_to_binary_frac(frac, bits)
            
            # Обратный перевод: из двоичной строки в десятичное число
            # binary имеет вид "0.XXXXX", убираем "0."
            decimal_back = 0
            for i, bit in enumerate(binary[2:]):  # начинаем с 3-го символа
                if bit == '1':
                    decimal_back += 2 ** -(i + 1)
            
            # Считаем абсолютную погрешность
            error = abs(frac - decimal_back)
            results[frac][bits] = error
    
    # Выводим таблицу результатов
    print(f"\n{'Дробь':<8} | {'4 бита':<12} | {'8 бит':<12} | {'16 бит':<12} | {'32 бита':<12}")
    print("-" * 70)
    
    for frac in fractions:
        row = f"{frac:<8} | "
        for bits in bit_counts:
            error = results[frac][bits]
            row += f"{error:<12.10f} | "
        print(row)
    
    print("-" * 70)
    
    # Выводим двоичные представления для наглядности
    print("\nДвоичные представления (для примера):")
    for frac in fractions:
        print(f"  {frac}:")
        for bits in bit_counts:
            binary = decimal_to_binary_frac(frac, bits)
            print(f"    {bits:>2} бит: {binary}")
    
    # Проверяем гипотезу
    print("\n" + "=" * 70)
    print("АНАЛИЗ РЕЗУЛЬТАТОВ:")
    print("=" * 70)
    
    # Проверяем, уменьшается ли погрешность с ростом бит
    all_decrease = True
    for frac in fractions:
        errors = [results[frac][bits] for bits in bit_counts]
        # Проверяем, что каждое следующее значение меньше или равно предыдущему
        for i in range(len(errors) - 1):
            if errors[i + 1] > errors[i]:
                all_decrease = False
                break
    
    if all_decrease:
        print("\nВЫВОД: Гипотеза 2 ПОДТВЕРЖДЕНА.")
    else:
        print("Погрешность не уменьшается с ростом числа бит.")
        print("\nВЫВОД: Гипотеза 2 НЕ ПОДТВЕРЖДЕНА.")

# Запуск проверки
test_hypothesis_2()
print()

def test_hypothesis_3():
    """Проверка гипотезы 3: накопление ошибки в Q8.8"""
    
    print("=" * 70)
    print("ПРОВЕРКА ГИПОТЕЗЫ 3: НАКОПЛЕНИЕ ОШИБКИ В Q8.8")
    print("=" * 70)
    
    # Начальное значение и шаг
    current_val = 0.0
    step = 0.1
    expected_final = 1.0
    
    print(f"Операция: многократное сложение {step} (10 раз)")
    print(f"Ожидаемый итоговый результат: {expected_final}")
    print("-" * 70)
    print(f"{'Шаг':<5} | {'Результат (Q8.8 -> 10)':<25} | {'Погрешность':<15}")
    print("-" * 70)
    
    for i in range(1, 11):
        # Складываем текущее значение с 0.1 через наш алгоритм
        current_val = q88_add(current_val, step)
        
        # Считаем погрешность относительно идеального математического результата
        expected_val = i * step
        error = abs(current_val - expected_val)
        
        print(f"{i:<5} | {current_val:<25.6f} | {error:<15.6f}")
    
    print("-" * 70)
    
    final_error = abs(current_val - expected_final)
    
    print("\n" + "=" * 70)
    print("АНАЛИЗ РЕЗУЛЬТАТОВ:")
    print("=" * 70)
    print(f"Итоговое значение: {current_val:.6f}")
    print(f"Ожидаемое значение: {expected_final:.6f}")
    print(f"Накопленная погрешность: {final_error:.6f}")
    
    if final_error > 0.01:  # Погрешность стала заметной (> 1%)
        print("\nВЫВОД: Гипотеза 3 ПОДТВЕРЖДЕНА.")
    else:
        print("\nПогрешность не накопилась до заметных величин.")
        print("\nВЫВОД: Гипотеза 3 НЕ ПОДТВЕРЖДЕНА.")

# Запуск проверки
test_hypothesis_3()
print()

def test_hypothesis_4():
    """Проверка гипотезы 4: эффективность безвосстанавливающего деления"""
    
    print("=" * 70)
    print("ПРОВЕРКА ГИПОТЕЗЫ 4: ЭФФЕКТИВНОСТЬ АЛГОРИТМОВ ДЕЛЕНИЯ")
    print("=" * 70)
    
    n_tests = 50
    total_restoring_ops = 0
    total_nonrestoring_ops = 0
    
    # Для наглядности покажем первые 10 примеров
    print(f"\nКоличество тестов: {n_tests}")
    print(f"Диапазон чисел: делимое [1, 1000], делитель [1, 100]")
    print("-" * 70)
    print(f"{'№':<4} | {'Делимое':<8} | {'Делитель':<8} | {'Восст.':<8} | {'Безвосст.':<10}")
    print("-" * 70)
    
    for i in range(n_tests):
        dividend = random.randint(1, 1000)
        divisor = random.randint(1, 100)
        
        # Запускаем оба алгоритма
        q_r, r_r, ops_r = binary_div_restoring_1(dividend, divisor)
        q_nr, r_nr, ops_nr = binary_div_1(dividend, divisor)
        
        total_restoring_ops += ops_r
        total_nonrestoring_ops += ops_nr
        
        # Показываем первые 10 примеров
        if i < 10:
            print(f"{i+1:<4} | {dividend:<8} | {divisor:<8} | {ops_r:<8} | {ops_nr:<10}")
    
    print("-" * 70)
    
    # Считаем среднее
    avg_restoring = total_restoring_ops / n_tests
    avg_nonrestoring = total_nonrestoring_ops / n_tests
    savings = (1 - avg_nonrestoring / avg_restoring) * 100
    
    print("\n" + "=" * 70)
    print("ИТОГОВЫЕ РЕЗУЛЬТАТЫ:")
    print("=" * 70)
    print(f"Всего операций (восстанавливающее):      {total_restoring_ops}")
    print(f"Всего операций (безвосстанавливающее):   {total_nonrestoring_ops}")
    print("-" * 70)
    print(f"Среднее на тест (восстанавливающее):     {avg_restoring:.2f}")
    print(f"Среднее на тест (безвосстанавливающее):  {avg_nonrestoring:.2f}")
    print(f"Экономия операций:                       {savings:.1f}%")
    print("-" * 70)
    
    if avg_nonrestoring < avg_restoring:
        print("\nВЫВОД: Гипотеза 4 ПОДТВЕРЖДЕНА.")
    else:
        print("\nБезвосстанавливающее деление не показало преимущества.")
        print("\nВЫВОД: Гипотеза 4 НЕ ПОДТВЕРЖДЕНА.")

# Запуск проверки
test_hypothesis_4()
print()

def test_hypothesis_5():
    """Проверка гипотезы 5: границы формата Q8.8"""
    
    print("=" * 70)
    print("ПРОВЕРКА ГИПОТЕЗЫ 5: ГРАНИЦЫ ФОРМАТА Q8.8")
    print("=" * 70)
    
    # Тестовые значения: внутри диапазона, на границе и за пределами
    test_values = [
        (0.0, "Ноль"),
        (1.5, "Внутри диапазона"),
        (127.996, "Близко к максимуму"),
        (127.99609375, "Точный максимум Q8.8"),
        (-128.0, "Точный минимум Q8.8"),
        (128.0, "ЗА пределами (чуть больше максимума)"),
        (200.0, "ЗА пределами (далеко за максимумом)"),
        (-128.5, "ЗА пределами (чуть меньше минимума)"),
        (-200.0, "ЗА пределами (далеко за минимумом)")
    ]
    
    print(f"\nДиапазон Q8.8: [-128.0 ; 127.99609375]")
    print("-" * 70)
    print(f"{'Исходное':<12} | {'Q8.8 (целое)':<14} | {'Обратно':<14} | {'Статус':<20}")
    print("-" * 70)
    
    overflow_count = 0
    
    for value, description in test_values:
        # Переводим в Q8.8
        q_val = to_q88(value)
        
        # Переводим обратно
        back = from_q88(q_val)
        
        # Проверяем, совпадает ли результат с исходным числом
        error = abs(back - value)
        
        if error < 0.005:
            status = "OK (в диапазоне)"
        else:
            status = "ПЕРЕПОЛНЕНИЕ!"
            overflow_count += 1
        
        print(f"{value:<12} | {q_val:<14} | {back:<14.6f} | {status:<20}")
    
    print("-" * 70)
    
    # Демонстрация переполнения при сложении
    print("\nДемонстрация переполнения при сложении:")
    print("-" * 70)
    
    a = 100.0
    b = 50.0
    expected = a + b  # 150.0 — за пределами Q8.8!
    
    result = q88_add(a, b)
    error = abs(result - expected)
    
    print(f"  {a} + {b} = {result} (ожидалось {expected})")
    
    if error > 0.01:
        print(f"  → Результат некорректен! Произошло переполнение.")
        overflow_count += 1
    else:
        print(f"  → Результат корректен.")
    
    print("\n" + "=" * 70)
    print("АНАЛИЗ РЕЗУЛЬТАТОВ:")
    print("=" * 70)
    print(f"Обнаружено переполнений: {overflow_count}")
    
    if overflow_count > 0:
        print("\nПри выходе за пределы [-128; 127.996] происходит переполнение.")
        print("\nВЫВОД: Гипотеза 5 ПОДТВЕРЖДЕНА.")
    else:
        print("\nПереполнение не обнаружено.")
        print("\nВЫВОД: Гипотеза 5 НЕ ПОДТВЕРЖДЕНА.")

# Запуск проверки
test_hypothesis_5()
print()

def test_hypothesis_6():
    """Проверка гипотезы 6: сложность умножения"""
    
    print("=" * 70)
    print("ПРОВЕРКА ГИПОТЕЗЫ 6: СЛОЖНОСТЬ УМНОЖЕНИЯ")
    print("=" * 70)
    
    # Размеры чисел, которые будем тестировать
    bit_sizes = [8, 16, 32, 64, 128, 256]
    
    # Количество повторений для точного замера времени
    n_repeats = 1000
    
    print(f"\nКоличество повторений для каждого размера: {n_repeats}")
    print("-" * 70)
    print(f"{'Бит':<6} | {'Время (мкс)':<15} | {'Итераций':<12} | {'Сложений':<12}")
    print("-" * 70)
    
    results_time = []
    results_iterations = []
    results_additions = []
    
    for bits in bit_sizes:
        # Генерируем два случайных числа заданной разрядности
        max_val = (1 << bits) - 1
        a = max_val  # берём максимальное значение для худшего случая
        b = max_val
        
        # --- Замер времени ---
        start_time = time.perf_counter()
        for _ in range(n_repeats):
            binary_mul(a, b, bits=bits)
        end_time = time.perf_counter()
        
        avg_time_us = (end_time - start_time) / n_repeats * 1_000_000  # в микросекундах
        
        # --- Подсчёт итераций и сложений ---
        # В алгоритме binary_mul цикл выполняется ровно bits раз
        iterations = bits
        # Количество сложений = количество единичных бит в b
        additions = bin(b).count('1')
        
        results_time.append(avg_time_us)
        results_iterations.append(iterations)
        results_additions.append(additions)
        
        print(f"{bits:<6} | {avg_time_us:<15.2f} | {iterations:<12} | {additions:<12}")
    
    print("-" * 70)
    
    # --- Проверка линейной зависимости ---
    print("\n" + "=" * 70)
    print("ПРОВЕРКА ЛИНЕЙНОЙ ЗАВИСИМОСТИ:")
    print("=" * 70)
    
    # Если зависимость линейная, то отношение времени к числу бит должно быть примерно постоянным
    ratios = [t / b for t, b in zip(results_time, bit_sizes)]
    avg_ratio = sum(ratios) / len(ratios)
    
    print(f"Среднее отношение (время / биты): {avg_ratio:.4f} мкс/бит")
    print(f"Отношения для каждого размера: {[f'{r:.4f}' for r in ratios]}")
    
    # Проверяем, что все отношения близки к среднему (в пределах 30%)
    is_linear = all(abs(r - avg_ratio) / avg_ratio < 0.3 for r in ratios)
    
    if is_linear:
        print("\nВЫВОД: Гипотеза 6 ПОДТВЕРЖДЕНА.")
    else:
        print("\nЗависимость не является строго линейной.")
        print("\nВЫВОД: Гипотеза 6 НЕ ПОДТВЕРЖДЕНА.")

# Запуск проверки
test_hypothesis_6()