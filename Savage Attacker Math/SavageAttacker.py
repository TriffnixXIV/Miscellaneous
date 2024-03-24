import tkinter as tk
import math
# https://arxiv.org/abs/1202.0228

def get_triangle(width: int = 2, height: int = 10, do_prints: bool = False):
    triangle = [[1]]
    for _ in range(height):
        previous_line = triangle[-1]
        line = []
        for i in range(len(previous_line) + width - 1):
            value = previous_line[i] if i < len(previous_line) else 0
            if i > 0:
                value += line[-1]
                if i - width >= 0:
                    value -= previous_line[i - width]
            line.append(value)
            if do_prints: print(line)
        triangle.append(line)
    return triangle

def get_averages(sides: int = 6, max_number: int = 10, do_prints: bool = False):
    triangle = get_triangle(sides, max_number)
    averages = []
    for i in range(1, len(triangle)):
        line = triangle[i]
        total = 0
        for j in range(len(line)):
            result = j + i
            weight = line[j]
            total += weight * result
        averages.append(total / (sides ** i))
        if do_prints: print(f"{i}d{sides}: {averages[-1]}")
    return averages

def get_savage_averages(sides: int = 6, max_number: int = 10, do_prints: bool = False):
    triangle = get_triangle(sides, max_number)
    averages = []
    for i in range(1, len(triangle)):
        line = triangle[i]
        current_weight_sum = 0
        total = 0
        for j in range(len(line)):
            result = j + i
            weight = line[j]
            total += result * (((current_weight_sum + weight) ** 2) - (current_weight_sum ** 2))
            current_weight_sum += weight
        averages.append(total / (sides ** (2*i)))
        if do_prints: print(f"{i}d{sides}: {averages[-1]:.5f}")
    return averages

def get_compared_averages(sides: int = 6, max_number: int = 10, do_prints: bool = True):
    simple_averages = get_averages(sides, max_number)
    savage_averages = get_savage_averages(sides, max_number)
    compared = []
    for i in range(max_number):
        compared.append((simple_averages[i], savage_averages[i]))
        difference = savage_averages[i] - simple_averages[i]
        if do_prints: print(f"{i+1}d{sides}: {simple_averages[i]:.3f} | +{difference:.3f} | {savage_averages[i]:.3f}")
    return compared

def show_all_comparisons():
    root = tk.Tk()
    root.configure(bg="#606060")

    row = 0
    column = 0

    max_number = 10

    tk.Label(text = "n", fg="#F0F0F0", bg="#101010").grid(row=0, rowspan=2, column=0, sticky="nswe")

    column += 1
    for sides in [4, 6, 8, 10, 12, 20]:
        tk.Label(text = f"d{sides}", fg="#F0F0F0", bg="#101010").grid(row=0, column=column, columnspan=3, sticky="we", padx=(3, 0))
        compared = get_compared_averages(sides, max_number, do_prints=False)
        row = 1
        tk.Label(text = "avg", fg="#F0F0F0", bg="#101010").grid(row=row, column=column, sticky="we", padx=(3, 0), pady=(1, 0))
        tk.Label(text = "savg", fg="#F0F0F0", bg="#101010").grid(row=row, column=column+1, sticky="we", padx=(1, 0), pady=(1, 0))
        tk.Label(text = "diff", fg="#F0F0F0", bg="#101010").grid(row=row, column=column+2, sticky="we", padx=(1, 0), pady=(1, 0))
        row = 2
        for entry in compared:
            tk.Label(text = str(row-1), fg="#F0F0F0", bg="#101010").grid(row=row, column=0, sticky="we", pady=(1, 0))
            tk.Label(text = f"{entry[0]:.3f}", fg="#F0F0F0", bg="#101010").grid(row=row, column=column, sticky="we", padx=(3, 0), pady=(1, 0))
            tk.Label(text = f"{entry[1]:.3f}", fg="#F0F0F0", bg="#101010").grid(row=row, column=column+1, sticky="we", padx=(1, 0), pady=(1, 0))
            tk.Label(text = f"+{(entry[1] - entry[0]):.3f}", fg="#F0F0F0", bg="#101010").grid(row=row, column=column+2, sticky="we", padx=(1, 0), pady=(1, 0))
            row += 1
        column += 3
    
    root.mainloop()

def get_vectors(element_sum, escalating_sum, length, current_escalating_sum = 0, index = 0):
    vectors = []
    if length == 1:
        if current_escalating_sum + index * element_sum == escalating_sum:
            vectors.append([element_sum])
    elif element_sum == 0:
        if current_escalating_sum == escalating_sum:
            vectors.append([0] * length)
    else:
        for part in range(element_sum + 1):
            next_escalating_sum = current_escalating_sum + index * part
            next_element_sum = element_sum - part
            if next_escalating_sum < escalating_sum and next_element_sum > 0:
                for vector in get_vectors(element_sum - part, escalating_sum, length - 1, next_escalating_sum, index + 1):
                    vectors.append([part] + vector)
            elif next_escalating_sum == escalating_sum and next_element_sum == 0:
                vectors.append([part] + [0] * (length - 1))
    return vectors

def get_value(k, n, m):
    total = 0
    for v in get_vectors(k, n, m):
        denominator = 1
        for k_i in v:
            denominator *= math.factorial(k_i)
        total += 1 / denominator
    return round(math.factorial(k) * total)

def get_row(k, m):
    row = []
    for n in range(k * m + 1):
        row.append(get_value(k, n, m+1))
    return row

def build_triangle_using_that_study(m: int = 5, rows: int = 10):
    for k in range(rows + 1):
        print(get_row(k, m))

def get_dicesum_weights(number, sides):
    return get_row(number, sides - 1)

def get_dicesum_weight(number, sides, sum):
    return get_value(number, sum - number, sides)

def get_dice_vectors(number, sides, sum):
    return get_vectors(number, sum - number, sides)

def get_mixed_triangle(pools: list[tuple]):
    triangle = [[1]]
    for number, sides in pools:
        for _ in range(number):
            previous_line = triangle[-1]
            line = []
            for i in range(len(previous_line) + sides - 1):
                value = previous_line[i] if i < len(previous_line) else 0
                if i > 0:
                    value += line[-1]
                    if i - sides >= 0:
                        value -= previous_line[i - sides]
                line.append(value)
            triangle.append(line)
    return triangle

def get_mixed_triangle_vectors(n, pools: list[tuple]):
    # does not work properly
    vector_pairs = []
    number_of_dice = 0
    largest_die = 0
    maximum_dice_threshholds = []
    for number, sides in pools:
        number_of_dice += number
        if sides > largest_die:
            largest_die = sides
        for threshhold in maximum_dice_threshholds:
            threshhold[1] += number
        maximum_dice_threshholds.append([sides, number])

    for vector in get_vectors(number_of_dice, n, largest_die):
        if n == 12: print(vector)
        dice_factors = []
        dice_per_threshhold = [[sides, 0] for sides, _ in maximum_dice_threshholds]
        for i in range(len(vector)):
            previous_entry = [-1, 0]
            for entry in dice_per_threshhold:
                if previous_entry[0] <= i < entry[0]:
                    entry[1] += vector[i]
                previous_entry = entry
        
        if n == 12: print(dice_per_threshhold, "|", maximum_dice_threshholds)
        valid = True
        for i in range(len(maximum_dice_threshholds)):
            if dice_per_threshhold[i][1] > maximum_dice_threshholds[i][1]:
                valid = False
            else:
                if dice_per_threshhold[i][1] > 0:
                    dice_factors.append(max(dice_per_threshhold[i][1], pools[i][0]))
                else:
                    dice_factors.append(0)
        
        if valid:
            if n == 12: print(dice_factors)
            vector_pairs.append((vector, dice_factors))
        else:
            if n == 12: print("denied")
        if n == 12: print()

    return vector_pairs

def get_mixed_triangle_value(n, pools: list[tuple]):
    value = 0
    if n == 12: print("printing for", pools)
    for v, a in get_mixed_triangle_vectors(n, pools):
        numerator = 1
        for a_i in a:
            numerator *= math.factorial(a_i)
        denominator = 1
        for v_i in v:
            denominator *= math.factorial(v_i)
        value += numerator / denominator
    return round(value)

def get_mixed_triangle_row(pools: list[tuple]):
    row = []
    length = 1
    for number, sides in pools:
        length += number * (sides - 1)
    for n in range(length):
        row.append(get_mixed_triangle_value(n, pools))
    return row

def get_mixed_triangle_using_formula(pools: list[tuple]):
    subpools = []
    previous_subpools = []
    for number, sides in pools:
        for i in range(number):
            subpools.append(previous_subpools + [(i+1, sides)])
        previous_subpools.append((number, sides))
    triangle = [[1]]
    for subpool in subpools:
        triangle.append(get_mixed_triangle_row(subpool))
    return triangle

def get_mixed_savage_average(pools: list[tuple]):
    triangle = get_mixed_triangle(pools)
    last_row = triangle[-1]
    total_number_of_dice = 0
    denominator = 1
    for number, sides in pools:
        total_number_of_dice += number
        denominator *= sides ** (2 * number)
    total = 0
    sum_of_weights = 0
    for i in range(len(last_row)):
        weight = last_row[i]
        savage_weight = weight ** 2 + 2 * weight * sum_of_weights
        total += (total_number_of_dice + i) * savage_weight
        sum_of_weights += weight
    return round(total / denominator, 3)

def get_mixed_average(pools: list[tuple]):
    average = 0
    for number, sides in pools:
        average += (number * (sides + 1)) / 2
    return average

if __name__ == "__main__":
    # build_triangle_using_that_study()
    # print(get_dicesum_weights(10, 6))
    # show_all_comparisons()
    # print(get_dicesum_weight(4, 6, 16))
    # print(get_dice_vectors(4, 6, 16))
    # pools = [(4, 6), (2, 4)]
    # print()
    # for row in get_mixed_triangle_using_formula(pools):
    #     print(row)
    # print()
    # for row in get_mixed_triangle(pools):
    #     print(row)
    print(get_mixed_average([(2, 4), (2, 6)]))
    print(get_mixed_savage_average([(2, 4), (2, 6)]))