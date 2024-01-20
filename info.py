char_py = {}

chars_2 = []
with open('asserts/decomposition.txt', encoding='utf-8', mode='r') as f:
    for lin in f:
        arr = lin.strip('\r\n').split('\t')
        chars_2.append(arr[0])

chars_1 = []
with open('asserts/info.txt', encoding='utf-8', mode='r') as f:
    for line in f:
        arr = line.strip('\r\n').split('\t')
        # print(arr)
        char_py[arr[0]] = arr[1]
        chars_1.append(arr[0])

# print(char_py)
# print(len(chars_1))

new_char_py = {}
for c in chars_2:
    new_char_py[c] = char_py[c]

# print(new_char_py)

with open('data/char_py.txt', encoding='utf-8', mode='w') as f:
    for char, py in new_char_py.items():
        f.write('%s\t%s\n' % (char, py))

# test2有而test1没有的元素
difference = list(set(chars_1).difference(set(chars_2)))

# print(difference)
# print(len(difference))

with open('data/char_py_first.txt', encoding='utf-8', mode='w') as f:
    for char, py in new_char_py.items():
        f.write('%s\t%s\n' % (char, py[0]))

with open('data/char_py_last.txt', encoding='utf-8', mode='w') as f:
    for char, py in new_char_py.items():
        f.write('%s\t%s\n' % (char, py[-2]))
