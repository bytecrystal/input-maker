# 读取keymap_group.json
import json
import re

with open('data/keymap_group.json', encoding='utf-8', mode='r') as f:
    keymap_group = json.load(f)

group = []
for kv in keymap_group.items():
    # print(kv[1])
    arr = []
    for k in kv[1]:
        arr.append(k)
    group.append(arr)

# print(group)
# component_k = {}
# for kv in keymap_group.items():
#     component_k.update(kv[1])

# print(component_k)
component_changed = []
component_changed_map = {}
with open('data/changed_components.txt', encoding='utf-8', mode='r') as f:
    for line in f:
        char = line.strip('\r\n')
        comps = char.split('\t')
        component_changed_map[comps[0]] = comps
        component_changed.append(char)

sa = 0
sam = []
for iii in component_changed_map.values():
    sa += len(iii)
    for iiii in iii:
        sam.append(iiii)

# print(sam)

ksam = []
with open('data/new_keymap.txt', encoding='utf-8', mode='r') as f:
    for line in f:
        char = line.strip('\r\n')
        li = line.strip('\r\n')
        arr = li.split('\t')
        component = arr[0]
        ksam.append(component)

# print(ksam)

# test2有而test1没有的元素
difference = list(set(ksam).difference(set(sam)))
print(difference)
# for kks in componentKey.keys():
#     ksam.append(kks)
#
# print(ksam)

print(u'\ue843')
print(u'\ue831')
print(u'\ue831')

a = '中国人好abc,abc'
print(a[0])

all_key = 'abcdefghijklmnopqrstuvwxyz'
all_double_key = [x + y for x in all_key for y in all_key]

# print(all_double_key)

code_map = {}
with open('data/new_brief_code.txt', encoding='utf-8', mode='r') as f:
    for line in f:
        li = line.strip('\r\n')
        arr = li.split('\t')
        char = arr[0]
        code = arr[1]
        code_map[char] = code

codes = {}
jm_cm_cnt = 0
for v in code_map.values():
    if v not in codes.keys():
        codes[v] = 1
    else:
        jm_cm_cnt += 1

print("简码的重码数: %d" % jm_cm_cnt)

my_re = re.compile(r'^[\u4e00-\u9fa5]*\t[0-9]*$', re.S)

dian_ci = []
with open('asserts/dian_ci.txt', encoding='utf-8', mode='r') as f:
    for line in f:
        # 如果line中含有字母
        res = re.match(my_re, line)
        if res:
            dian_ci.append(line)

with open('asserts/dian_ci_no_en.txt', encoding='utf-8', mode='w') as f:
    for line in dian_ci:
        f.write(line)

dian_zi_ci = []
with open('asserts/dian_zici-20180421.txt', encoding='utf-8', mode='r') as f:
    for line in f:
        zici, zp = line.strip('\r\n').split('\t')
        if int(zp) > 15:
            # 如果line中含有字母
            res = re.match(my_re, line)
            if res:
                dian_zi_ci.append(line)

with open('asserts/dian_zi_ci_no_en.txt', encoding='utf-8', mode='w') as f:
    for line in dian_zi_ci:
        f.write(line)
