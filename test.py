# 读取keymap_group.json
import json

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

###test2有而test1没有的元素
difference = list(set(ksam).difference(set(sam)))
print(difference)
# for kks in componentKey.keys():
#     ksam.append(kks)
#
# print(ksam)

print(u'\ue843')
print(u'\ue831')
print(u'\ue831')