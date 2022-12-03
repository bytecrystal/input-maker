# This is a sample Python script.
import json
import random

from simanneal import Annealer

componentKey = {}
componentName = {}
with open('data/new_keymap.txt', encoding='utf-8', mode='r') as keymapFile:
    for line in keymapFile:
        li = line.strip('\r\n')
        arr = li.split('\t')
        component = arr[0]
        key = arr[1]
        componentKey[component] = key
        if (len(arr) < 3):
            componentName[component] = component
        else:
            componentName[component] = arr[2]
small_key_map = {'5': 'a', '4': 'o', '3': 'u', '2': 'i', '1': 'e'}
# big_keymap = {'5': 'v', '4': 'd', '3': 't', '2': 's', '1': 'h'}
stroke_arr_small = {}
stroke_arr_big = {}
stroke_char = {}
with open('asserts/stroke.txt', encoding='utf-8', mode='r') as strokeFile:
    for line in strokeFile:
        arr = line.strip('\r\n').split('\t')
        stroke = arr[1]
        str_small_stroke = ''
        str_big_stroke = ''
        l = len(stroke)
        if (l >= 3):
            str_small_stroke += small_key_map[stroke[0]] + small_key_map[stroke[1]] + small_key_map[stroke[2]]
            # str_big_stroke += big_keymap[stroke[0]] + big_keymap[stroke[1]] + big_keymap[stroke[2]]
        elif (l == 2):
            str_small_stroke += small_key_map[stroke[0]] + small_key_map[stroke[1]] * 2
            # str_big_stroke += big_keymap[stroke[0]] + big_keymap[stroke[1]] * 2
        elif (l == 1):
            str_small_stroke += small_key_map[stroke[0]] * 3
            # str_big_stroke += big_keymap[stroke[0]] * 3
        stroke_arr_small[arr[0]] = str_small_stroke
        stroke_arr_big[arr[0]] = str_big_stroke
        stroke_char[arr[0]] = stroke[0]

stroke_arr_small_last = {}
with open('asserts/stroke.txt', encoding='utf-8', mode='r') as strokeFile:
    for line in strokeFile:
        arr = line.strip('\r\n').split('\t')
        stroke = arr[1]
        # 取末笔画数字
        stroke_arr_small_last[arr[0]] = small_key_map[stroke[-1]]

# print(stroke_arr_small_last)

# 读取字根
with open('asserts/decomposition.txt', encoding='utf-8', mode='r') as componentFile:
    decompositionLines = [line for line in componentFile]

char_py = {}
# 读取字-拼音
with open('data/char_py_first.txt', encoding='utf-8', mode='r') as pinyinFile:
    for line in pinyinFile:
        char, py = line.strip('\r\n').split('\t')
        char_py[char] = py

# char_py_last = {}
# # 读取字-拼音
# with open('data/char_py_last.txt', encoding='utf-8', mode='r') as f:
#     for line in f:
#         char, py = line.strip('\r\n').split('\t')
#         char_py_last[char] = py

def build_full_code(component_k, decomposition_lines):
    fullCode = []
    for line in decomposition_lines:
        char, s1, s2, s3, py, is_partial = line.strip('\r\n').split('\t')
        strokes = stroke_arr_small[char]
        # strokes_last = stroke_arr_small_last[char]
        # 第一码：拼音首字母
        first_code = component_k[s1]
        if (s3):
            # 三个字根，YYYYZ，声形形形+末笔
            c1 = first_code
            c2 = component_k[s1]
            c3 = component_k[s2]
            # c4 = component_k[s3]
            qm = c1 + c2 + c3 + strokes[0]
            fullCode.append((char, qm))
        elif(s2):
            # 两个字根，YY[形形]，声形+末笔
            c1 = first_code
            c2 = component_k[s2]
            # c3 = component_k[s2]
            # c4 = component_k[s2]
            qm = c1 + c2 + strokes[:3]
            fullCode.append((char, qm))
        elif (s1):
            # 一个字根，Y[Y笔]笔笔笔
            c1 = first_code
            c2 = componentKey[stroke_char[char]]
            qm = c1 + c2 + strokes[:3]
            fullCode.append((char, qm))
    return fullCode


fullCode = build_full_code(componentKey, decompositionLines)
with open('data/full_code.txt', encoding='utf-8', mode='w') as fullCodeFile:
    for char, code in fullCode:
        fullCodeFile.write('%s\t%s\n' % (char, code))

small_key = {'a', 'e', 'i', 'o', 'u'}


# 简码
def build_brief_code(fullCode):
    brief_code = []
    c = {}

    for char, code in fullCode:
        code_2 = code[:2]
        code_3 = code[:3]
        code_4 = code[:4]
        code_5 = code[:5]
        if (code_2 not in c):
            c[code_2] = 1
            brief_code.append((char, code_2))
        elif (code_3 not in c and code[2] in small_key):
            c[code_3] = 1
            brief_code.append((char, code_3))
        elif (code_4 not in c):
            c[code_4] = 1
            brief_code.append((char, code_4))
        elif (code_5 not in c and code[2] not in small_key):
            c[code_5] = 1
            brief_code.append((char, code_5))
        else:
            brief_code.append((char, code))
    return brief_code


brief_code = build_brief_code(fullCode)
with open('data/brief_code.txt', encoding='utf-8', mode='w') as briefCodeFile:
    for char, code in brief_code:
        briefCodeFile.write('%s\t%s\n' % (char, code))


def stats(brief_code):
    c = {}
    # 总的重码数
    cm_cnt_a = 0
    # 前1000重码数
    cm_cnt_1000 = 0
    line_index = 0
    # 前650的四码数
    code_cnt_4_650 = 0
    for char, code in brief_code:
        if (line_index <= 650):
            if (len(code) == 4):
                code_cnt_4_650 += 1
        if (code not in c):
            c[code] = 1
        else:
            # print(char, code)
            cm_cnt_a += 1
            if (line_index <= 1000):
                cm_cnt_1000 += 1
        line_index += 1
    print(code_cnt_4_650)
    print("重码数: %d" % cm_cnt_a)

    # print(cm_cnt_1000)
    # print(code_cnt_4_650)
    return code_cnt_4_650 + cm_cnt_a


stats(brief_code)

class ComponentsDistributionProblem(Annealer):
    def __int__(self, state):
        super(ComponentsDistributionProblem, self).__init__(state)

    def energy(self):
        full_c = build_full_code(self.state, decompositionLines)
        brief_c = build_brief_code(full_c)
        return stats(brief_c)

    def move(self):
        l = list(self.state.keys())
        # a = random.choice(l)
        # b = random.choice(l)
        # for i in opti:
        #     self.state[i] = random.choice(choose)
        # self.state['以'] = random.choice(choose)

#
#
if __name__ == '__main__':
    cdp = ComponentsDistributionProblem(componentKey)
    cdp.copy_strategy = "method"
    # auto_schedule = {'tmax': 0.14, 'tmin': 6.7e-07, 'steps': 30000, 'updates': 30000}  # 如果确定用什么参数，就提供
    auto_schedule = {'tmax': 0.14, 'tmin': 6.7e-07, 'steps': 1, 'updates': 1}  # 如果确定用什么参数，就提供
    # auto_schedule = cdp.auto(minutes=1)
    print(auto_schedule)
    cdp.set_schedule(auto_schedule)
    state, dup = cdp.anneal()  # 开始优化
    # print(dup)
    # print(state)
    # state_arr = sorted(state.items(), key=lambda kv: (kv[1], kv[0]))
    # 优化完成，把结果保存下来
    # with open('data/new_keymap.txt', encoding='utf-8', mode='w') as newKeymapFile:
    #     for key, key_map in state:
    #         newKeymapFile.write(key + '\t' + key_map + '\n')
    with open('data/new_keymap.txt', encoding='utf-8', mode='w') as newKeymapFile:
        for key,key_map in state.items():
            newKeymapFile.write(key + '\t' + key_map + '\n')

    # 以键分组存和字典
    key_map = {}
    # with open('data/new_keymap.json', encoding='utf-8', mode='w') as f:
    #     for char, key in state:
    #         key_map[key] = key_map.get(key, []) + [char]
    #     json.dump(key_map, f, ensure_ascii=False)
    with open('data/new_keymap.json', encoding='utf-8', mode='w') as f:
        for char,key in state.items():
            key_map[key] = key_map.get(key, []) + [char]
        json.dump(key_map, f, ensure_ascii=False)

    full_code = build_full_code(state, decompositionLines)
    brief_code = build_brief_code(full_code)
    with open('data/new_brief_code.txt', encoding='utf-8', mode='w') as newBriefCodeFile:
        for char, code in brief_code:
            newBriefCodeFile.write('%s\t%s\n' % (char, code))

    with open('data/new_brief_code_char.txt', encoding='utf-8', mode='w') as newBriefCodeFile:
        for char, code in brief_code:
            newBriefCodeFile.write('%s\n' % (char))

    with open('data/new_brief_code_code.txt', encoding='utf-8', mode='w') as newBriefCodeFile:
        for char, code in brief_code:
            newBriefCodeFile.write('%s\n' % (code))