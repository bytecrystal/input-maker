## 字频转化
zi_set = set()
with open('./asserts/zp.txt', encoding='utf-8', mode='r') as f:
    for line in f:
        z, p, x = line.strip('\r\n').split('\t')
        zi_set.add(z)

# print(zi_set)
decomposition = {}
with open('./asserts/decomposition.txt', encoding='utf-8', mode='r') as f:
    for zi in zi_set:
        for line in f:
            char, s1, s2, s3, py, isPartial = line.strip('\r\n').split('\t')
            decomposition[char] = line

decomposition_res = {}
for zi in zi_set:
    for decomposition_char in decomposition:
        if zi == decomposition_char:
            decomposition_res[zi] = decomposition[decomposition_char]

# print(decomposition_res)
###test2有而test1没有的元素
difference = list(set(list(decomposition.keys())).difference(set(list(decomposition_res.keys()))))
# print(difference)
difference_map = {}
for d in difference:
    for decomposition_char in decomposition:
        if d == decomposition_char:
            difference_map[d] = decomposition[decomposition_char]

# print(difference_map)

with open('./data/new_decomposition.txt', encoding='utf-8', mode='w') as f:
    for zi in decomposition_res:
        f.write(decomposition_res[zi])
    for zi in difference_map:
        f.write(difference_map[zi])
# with open('./data/new_decomposition.txt', encoding='utf-8', mode='w') as f:
#     for k, v in decomposition.items():
#         f.write(k + '\t' + v[0] + '\t' + v[1] + '\t' + v[2] + '\t' + v[3] + '\t' + v[4] + '\n')
# print(decomposition)

