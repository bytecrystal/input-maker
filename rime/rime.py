'''
生成 tuma 码表
'''

import shutil
import json
from os.path import exists
from os import makedirs

ci_list = []
# 读取词表
# with open('asserts/ci.txt', encoding='utf-8', mode='r') as f:
#     for line in f:
#         l_c = line.strip('\r\n')
#         ci_list.append(l_c)

with open('cp.txt',encoding='utf-8') as t:
    for line in t.readlines():
        ciyu = line.strip('\r\n')
        ci_list.append(ciyu)

def build_ci_by_full_code(full_code_map):
    ci_map = {}
    for ci in ci_list:
        lc = len(ci)
        if (lc == 2):
            # 一个字取两码：A1a1B1b1
            ci_map[ci] = full_code_map[ci[0]][:2] + full_code_map[ci[1]][:2]
        elif (lc == 3):
            # 每个字取首码
            ci_map[ci] = full_code_map[ci[0]][0] + full_code_map[ci[1]][0] + full_code_map[ci[2]][0]
            # 3字词是前两字第一码 + 第三字前两码
            # ci_map[ci] = full_code_map[ci[0]][0] + full_code_map[ci[1]][0] + full_code_map[ci[2]][:2]
        elif (lc == 4):
            ci_map[ci] = full_code_map[ci[0]][0] + full_code_map[ci[1]][0] + full_code_map[ci[2]][0] + full_code_map[ci[3]][0]
        elif (lc > 4):
            ci_map[ci] = full_code_map[ci[0]][0] + full_code_map[ci[1]][0] + full_code_map[ci[2]][0] + full_code_map[ci[-1]][0]
    # for char, code in full_code:
    return ci_map


def strB2Q(ustring):
    '''
    将半角转换为全角
    '''
    rstring = ""
    for uchar in ustring:
        inside_code = ord(uchar)
        if inside_code == 32:
            inside_code = 12288
        elif 32 <= inside_code <= 126:
            inside_code += 65248
        rstring += chr(inside_code)
    return rstring

with open('../asserts/rime/tuma.dict.meta.yaml') as tumaDictMetaFile:
    tumaDictMeta = tumaDictMetaFile.read()
with open('../asserts/rime/tuma.phrases.meta.yaml') as tumaDictPhraseMetaFile:
    tumaDictPhraseMeta = tumaDictPhraseMetaFile.read()
with open('../asserts/rime/tuma.words.meta.yaml') as tumaDictWordsMetaFile:
    tumaDictWordsMeta = tumaDictWordsMetaFile.read()
#
# with open('assets/brevity.dat') as brevityFile:
#     brevity = [line.strip('\r\n').split('\t') for line in brevityFile]

componentKey = {}
componentName = {}
with open('../data/new_keymap.txt') as keymapFile:
    for line in keymapFile:
        component, key = line.strip('\r\n').split('\t')
        componentKey[component] = key
        componentName[component] = component

div = []
fullCode = []
charSet = {}
qd = {}
briefCode = []
fullCodeMap = {}

with open('../data/full_code.txt', mode='r') as fullCodeFile:
    for line in fullCodeFile:
        char, code = line.strip('\r\n').split('\t')
        fullCode.append((char, code))
        qd[char] = code
        fullCodeMap[char] = code


with open('../data/new_brief_code.txt', mode='r') as briefCodeFile:
    for line in briefCodeFile:
        char, code = line.strip('\r\n').split('\t')
        briefCode.append((char, code))

stroke_char = {}
with open('../asserts/stroke.txt', encoding='utf-8', mode='r') as strokeFile:
    for line in strokeFile:
        arr = line.strip('\r\n').split('\t')
        stroke = arr[1]
        l = len(stroke)
        stroke_char[arr[0]] = stroke[0]

stroke_zm = {'1': '一', '2': '丨', '3': '丿', '4': '丶', '5': '乛'}
with open('../asserts/decomposition.txt') as decompositionFile:
    for line in decompositionFile:
        char, s1, s2, s3, py, isPartial = line.strip('\r\n').split('\t')
        if isPartial == '0':
            PY = strB2Q(py.upper())


            if (s3):
                c1 = componentName[s1]
                c2 = componentName[s2]
                c3 = componentName[s3]
                diva = c1 + c2 + c3 + PY[0]
            elif (s2):
                c1 = componentName[s1]
                c2 = componentName[s2]
                # c3 = py[0]
                c3 = PY[:2]
                diva = c1 + c2 + c3
            elif (s1):
                c1 = componentName[s1]
                c4 = componentName[stroke_zm[stroke_char[char]]]
                diva = c1 + PY[:2] + c4
            # diva = (componentName[s1] + componentName[s2] + componentName[s3] + PY)[:3]
            div.append((char, diva))
        charSet[char] = []
if not exists('build'): makedirs('build')
if not exists('build/opencc'): makedirs('build/opencc')

with open('build/tuma.dict.yaml', 'w') as dictFile:
    dictFile.write(tumaDictMeta)

with open('build/tuma.words.dict.yaml', 'w') as wordsDictFile:
    wordsDictFile.write(tumaDictWordsMeta)
    for char, code in briefCode:
        wordsDictFile.write('%s\t%s\n' % (char, code))
        # c42Dict.write('　\t%s\n' % code)
    for char, code in fullCode:
        wordsDictFile.write('%s\t%s\n' % (char, code))
        # c42Dict.write('　\t%s\n' % code)

ciMap = build_ci_by_full_code(fullCodeMap)
with open('build/tuma.phrases.dict.yaml', 'w') as phrasesFile:
    phrasesFile.write(tumaDictPhraseMeta)
    for kv in ciMap.items():
        phrasesFile.write('%s\t%s\n' % (kv[0], kv[1]))

with open('build/兔码.txt', 'w') as ziCiFile:
    for char, code in briefCode:
        ziCiFile.write('%s\t%s\n' % (char, code))
    for kv in ciMap.items():
        ziCiFile.write('%s\t%s\n' % (kv[0], kv[1]))

with open('build/opencc/division.txt', 'w') as filterDivision:
    for char, code in div:
        filterDivision.write('%s\t%s\n' % (char, code))

for name in ('tuma.schema', 'symbols_for_c', 'pinyin_simp.dict', 'pinyin_simp.schema'):
    shutil.copyfile('../asserts/rime/%s.yaml' % name, 'build/%s.yaml' % name)
for name in ('division', 'emoji'):
    shutil.copyfile('../asserts/rime/%s.json' % name, 'build/opencc/%s.json' % name)
for name in ('emoji_category', 'emoji_word'):
    shutil.copyfile('../asserts/rime/%s.txt' % name, 'build/opencc/%s.txt' % name)

key = 'abcdefghijklmnopqrstuvwxyz'
# print(all3)
# first_code = {}
# for x in key:
#     for char, code in briefCode:
#         if code == x:
#             first_code[char] = x + "\t" + fullCodeMap[char]
# # print(first_code)
# all2 = [x + y for x in key for y in key]
# # print(all2)
# second_code = {}
# for x in all2:
#     for char, code in briefCode:
#         if code == x:
#             second_code[char] = x + "\t" + fullCodeMap[char]
# # print(second_code)
# all3 = [x + y + z for x in key for y in key for z in key]
# third_code = {}
# for x in all3:
#     for char, code in briefCode:
#         if code == x:
#             third_code[char] = x + "\t" + fullCodeMap[char]
#
# # print(third_code)
# all4 = [x + y + z + w for x in key for y in key for z in key for w in key]
# fourth_code = {}
# for x in all4:
#     for char, code in briefCode:
#         if code == x:
#             fourth_code[char] = x + "\t" + fullCodeMap[char]
# print(fourth_code)