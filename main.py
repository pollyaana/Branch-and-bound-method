import copy

inf = float('inf')
'''rows = [
    [inf, 7, 16, 21, 2, 17],
    [13, inf, 21, 15, 43, 23],
    [25, 3, inf, 31, 17, 9],
    [13, 10, 27, inf, 33, 12],
    [9, 2, 19, 14, inf, 51],
    [42, 17, 5, 9, 23, inf]
]'''
phi = 0
flag = True
graphs = []
path = []
# 1 вариант
'''rows = [
    [inf, 5, 6, 8, 5, 8],
    [5, inf, 4, 6, 6, 3],
    [4, 3, inf, 1, 9, 2],
    [3, 4, 7, inf, 5, 4],
    [5, 4, 8, 8, inf, 3],
    [1, 6, 0, 3, 7, inf]
]'''
# 2 вариант
rows = [
    [inf, 1, 9, 6, 6, 6],
    [2, inf, 3, 1, 7, 3],
    [5, 3, inf, 5, 0, 4],
    [6, 9, 9, inf, 6, 2],
    [6, 1, 9, 6, inf, 2],
    [4, 4, 4, 2, 6, inf]
]

"""Формируем список дуг"""


def arr_arcs(rows):
    arcs = copy.deepcopy(rows)
    for i in range(0, len(rows)):
        for j in range(0, len((rows[i]))):
            arcs[i][j] = str(i + 1) + '_' + str(j + 1)
    return arcs


"""Формируем список столбцов нашей матрицы"""


def get_columns(rows):
    columns = [] * len(rows)
    for s in rows:
        columns.append([])
    for s in rows:
        for i in range(0, len(s)):
            columns[i].append(s[i])
    return columns


"""Выполняем операцию приведения матрицы по строкам и столбцам"""


def reduction(rows):
    u = []
    v = []
    length = len(rows)
    for s in rows:
        u.append(min(s))
    for i in range(0, length):
        for j in range(0, len(rows[i])):
            rows[i][j] -= u[i]
    columns = get_columns(rows)
    for s in columns:
        v.append(min(s))
    for i in range(0, length):
        for j in range(0, len(rows[i])):
            rows[i][j] -= v[j]
    return u, v


"""Находим оценку решения задачи на текущем этапе"""


def get_phi(u, v, phi):
    phi += sum(u) + sum(v)
    # print("Оценка решения задачи: " + str(phi))
    return phi


"""Находим минимальный элемент в строке/столбце"""


def min_in_line(line):
    min_line = float('inf')
    indexes = [i for i, x in enumerate(line) if x == 0]
    if len(indexes) == 1:
        for el in line:
            if el < min_line and el != 0:
                min_line = el
    else:
        min_line = 0
    return min_line


"""Находим степени нулей"""


def get_powers_of_zeros(rows, arcs):
    zeros = {}
    f = {}
    for i in range(0, len(rows)):
        for j in range(0, len((rows[i]))):
            f[arcs[i][j]] = str(i) + ' ' + str(j)
            if rows[i][j] == 0:
                min_row = min_in_line(rows[i])
                columns = get_columns(rows)
                min_column = min_in_line(columns[j])
                zeros[arcs[i][j] + ',' + str(i) + ' ' + str(j)] = min_row + min_column
    return zeros, f


arcs = arr_arcs(rows)
u, v = reduction(rows)
phi = get_phi(u, v, phi)
print("Оценка решения полной задачи в начале: " + str(phi))

while True:
    zeros, f = get_powers_of_zeros(rows, arcs)
    """Находим дугу для которой степень нуля достигает максимального значения"""
    delta = max(zeros, key=zeros.get)
    row = int(delta.split(',')[1].split()[0])
    column = int(delta.split(',')[1].split()[1])
    v1 = delta.split(',')[0].split('_')[0]
    v2 = delta.split(',')[0].split('_')[1]
    path.append((v1, v2))
    flag = False
    s = ''
    if len(graphs) == 0:
        graphs.append([v1, v2])
        flag = True
    else:
        for graph in graphs:
            for v in graph:
                if v == v1 or v == v2:
                    graph.append(v1)
                    graph.append(v2)
                    cnt = {}
                    for e in graph:
                        s += e
                    for ss in s:
                        cnt[ss] = s.count(ss)
                    max_value = max(cnt.values())
                    final_dict = {k: v for k, v in cnt.items() if v == max_value}
                    for k in final_dict:
                        s = s.replace(k, '')
                    flag = True
                    break
    if not flag:
        graphs.append([v1, v2])
    """Разбиваем множество гамильтоновых контуров на 2 подмножества: решение содержащие/не содержащие переход по дуге"""

    """Получаем матрицу контуров, включающую дугу"""
    omega_with = copy.deepcopy(rows)
    if s == '':
        obr = v2 + '_' + v1
    else:
        obr = s[1] + '_' + s[0]
    try:
        c, r = f[obr].split()
    except KeyError:
        c, r = f[s[0] + '_' + s[1]].split()
    omega_with[int(c)][int(r)] = inf  # Чтобы предотвратить образования цикла
    omega_with.pop(row)  # удаляем строку
    # удаляем столбец
    for s in omega_with:
        s.pop(column)
    u, v = reduction(omega_with)
    left = get_phi(u, v, phi)
    """Получаем матрицу контуров, не включающую дугу"""
    omega_without = copy.deepcopy(rows)
    omega_without[row][column] = inf  # исключаем дугу из решения
    u, v = reduction(omega_without)
    right = get_phi(u, v, phi)
    if left <= right:
        rows = omega_with
        phi = left
    else:
        rows = omega_without
        phi = right
        path.pop(len(path) - 1)
    arcs.pop(row)
    for s in arcs:
        s.pop(column)
    if len(rows) == 2:
        path.append((arcs[0][0].split('_')[0], arcs[1][1].split('_')[1]))
        break
print("Оценка решения:  " + str(phi))
print('---------------------------')
print("Гамильтонов контур")
for el in path:
    print(el)
