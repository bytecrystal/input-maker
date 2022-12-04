# 读取keymap_group.json
import json

with open('data/keymap_group.json', encoding='utf-8', mode='r') as f:
    keymap_group = json.load(f)

group = []
for kv in keymap_group.items():
    print(kv[1])
    arr = []
    for k in kv[1]:
        arr.append(k)
    group.append(arr)

print(group)
# component_k = {}
# for kv in keymap_group.items():
#     component_k.update(kv[1])

# print(component_k)
