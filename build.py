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
with open('data/new_decomposition.txt', encoding='utf-8', mode='r') as componentFile:
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

###
# 1. 选取的字根依次编码后大于等于 3 码，则取前 3 码（超过 3 码的情况是因为有双编码字根）。例：说 = 【讠丷 儿】= 【u k a】= uka；絷 = 【执 幺 小】=【zi s v】= zis ；
# 2. 选取的字根依次编码后为 2 码，则补拼音首字母。例：我 = 【手 戈】 = 【j l】= jlw；占 = 【占】= 【zn】 = znz ；
# 3. 选取的字根依次编码后为 1 码，则补拼音首字母和末字母。例：一 = 【一】 = 【t】= tyi 。

stroke_zm = {'1': '一', '2': '丨', '3': '丿', '4': '丶', '5': '乛'}
def build_full_code(component_k, decomposition_lines):
    fullCode = []
    full_code_map = {}
    for line in decomposition_lines:
        char, s1, s2, s3, py, is_partial = line.strip('\r\n').split('\t')
        # strokes = stroke_arr_small[char]
        # strokes_last = stroke_arr_small_last[char]
        if (s3):
            c1 = component_k[s1]
            c2 = component_k[s2]
            c3 = component_k[s3]
            qm = c1 + c2 + c3 + py[0]
            fullCode.append((char, qm))
            full_code_map[char] = qm
        elif (s2):
            c1 = component_k[s1]
            c2 = component_k[s2]
            # c3 = py[0]
            c3 = py
            qm = c1 + c2 + c3
            fullCode.append((char, qm))
            full_code_map[char] = qm
        elif (s1):
            c1 = component_k[s1]
            c4 = component_k[stroke_zm[stroke_char[char]]]
            qm = c1 + py + c4
            fullCode.append((char, qm))
            full_code_map[char] = qm
    return (fullCode, full_code_map)


small_key = {'a', 'e', 'i', 'o', 'u'}


# 简码
def build_brief_code(fullCode):
    brief_code = []
    c = {}

    for char, code in fullCode:
        code_1 = code[:1]
        code_2 = code[:2]
        code_3 = code[:3]
        # code_4 = code[:4]
        # code_5 = code[:5]
        if (code_1 not in c):
            c[code_1] = 1
            brief_code.append((char, code_1))
        elif (code_2 not in c):
            c[code_2] = 1
            brief_code.append((char, code_2))
        elif (code_3 not in c):
            c[code_3] = 1
            brief_code.append((char, code_3))
        # elif (code_4 not in c):
        #     c[code_4] = 1
        #     brief_code.append((char, code_4))
        # elif (code_5 not in c and code[2] in small_key):
        #     c[code_5] = 1
        #     brief_code.append((char, code_5))
        else:
            brief_code.append((char, code))
    # return fullCode
    return brief_code

def get_brief_code(full_code):
    bf_code = []
    c = {}

    for char, code in full_code:
        code_1 = code[:1]
        code_2 = code[:2]
        code_3 = code[:3]
        # code_4 = code[:4]
        # code_5 = code[:5]
        if (code_1 not in c):
            c[code_1] = 1
            bf_code.append((char, code_1))
        elif (code_2 not in c):
            c[code_2] = 1
            bf_code.append((char, code_2))
        elif (code_3 not in c):
            c[code_3] = 1
            bf_code.append((char, code_3))
        # elif (code_4 not in c):
        #     c[code_4] = 1
        #     brief_code.append((char, code_4))
        # elif (code_5 not in c and code[2] in small_key):
        #     c[code_5] = 1
        #     brief_code.append((char, code_5))
        else:
            bf_code.append((char, code))
    return bf_code


ajew = {}
f = open('test/ew.txt', encoding='utf-8', mode='r')
for line in f:
    aj, ew = line.strip('\r\n').split('\t')
    ajew[aj] = float(ew)
f.close()

f = open('test/zp2.txt', encoding='utf-8', mode='r')
pl1 = {}
pl2 = {}
pl3 = {}
pl4 = {}
pl5 = {}
zp_a = {}
for line in f:
    z, p, x = line.strip('\r\n').split('\t')
    x = float(x)
    p = float(p) / 1000000000
    if x <= 300:
        pl1[z] = p
    elif x <= 500:
        pl2[z] = p
    elif x <= 1500:
        pl3[z] = p
    elif x <= 3000:
        pl4[z] = p
    elif x <= 6000:
        pl5[z] = p

    zp_a[z] = p
f.close()

hjzh = ['ah', 'ai', 'aj', 'ak', 'al', 'am', 'an', 'ao', 'ap', 'au', 'ay', 'a/', 'a;', 'bh', 'bi', 'bj', 'bk', 'bl',
        'bm', 'bn', 'bo', 'bp', 'bu', 'by', 'b/', 'b;', 'ch', 'ci', 'cj', 'ck', 'cl', 'cm', 'cn', 'co', 'cp', 'cu',
        'cy', 'c/', 'c;', 'dh', 'di', 'dj', 'dk', 'dl', 'dm', 'dn', 'do', 'dp', 'du', 'dy', 'd/', 'd;', 'eh', 'ei',
        'ej', 'ek', 'el', 'em', 'en', 'eo', 'ep', 'eu', 'ey', 'e/', 'e;', 'fh', 'fi', 'fj', 'fk', 'fl', 'fm', 'fn',
        'fo', 'fp', 'fu', 'fy', 'f/', 'f;', 'gh', 'gi', 'gj', 'gk', 'gl', 'gm', 'gn', 'go', 'gp', 'gu', 'gy', 'g/',
        'g;', 'ha', 'hb', 'hc', 'hd', 'he', 'hf', 'hg', 'hq', 'hr', 'hs', 'ht', 'hv', 'hw', 'hx', 'hz', 'ia', 'ib',
        'ic', 'id', 'ie', 'if', 'ig', 'iq', 'ir', 'is', 'it', 'iv', 'iw', 'ix', 'iz', 'ja', 'jb', 'jc', 'jd', 'je',
        'jf', 'jg', 'jq', 'jr', 'js', 'jt', 'jv', 'jw', 'jx', 'jz', 'ka', 'kb', 'kc', 'kd', 'ke', 'kf', 'kg', 'kq',
        'kr', 'ks', 'kt', 'kv', 'kw', 'kx', 'kz', 'la', 'lb', 'lc', 'ld', 'le', 'lf', 'lg', 'lq', 'lr', 'ls', 'lt',
        'lv', 'lw', 'lx', 'lz', 'ma', 'mb', 'mc', 'md', 'me', 'mf', 'mg', 'mq', 'mr', 'ms', 'mt', 'mv', 'mw', 'mx',
        'mz', 'na', 'nb', 'nc', 'nd', 'ne', 'nf', 'ng', 'nq', 'nr', 'ns', 'nt', 'nv', 'nw', 'nx', 'nz', 'oa', 'ob',
        'oc', 'od', 'oe', 'of', 'og', 'oq', 'or', 'os', 'ot', 'ov', 'ow', 'ox', 'oz', 'pa', 'pb', 'pc', 'pd', 'pe',
        'pf', 'pg', 'pq', 'pr', 'ps', 'pt', 'pv', 'pw', 'px', 'pz', 'qh', 'qi', 'qj', 'qk', 'ql', 'qm', 'qn', 'qo',
        'qp', 'qu', 'qy', 'q/', 'q;', 'rh', 'ri', 'rj', 'rk', 'rl', 'rm', 'rn', 'ro', 'rp', 'ru', 'ry', 'r/', 'r;',
        'sh', 'si', 'sj', 'sk', 'sl', 'sm', 'sn', 'so', 'sp', 'su', 'sy', 's/', 's;', 'th', 'ti', 'tj', 'tk', 'tl',
        'tm', 'tn', 'to', 'tp', 'tu', 'ty', 't/', 't;', 'ua', 'ub', 'uc', 'ud', 'ue', 'uf', 'ug', 'uq', 'ur', 'us',
        'ut', 'uv', 'uw', 'ux', 'uz', 'vh', 'vi', 'vj', 'vk', 'vl', 'vm', 'vn', 'vo', 'vp', 'vu', 'vy', 'v/', 'v;',
        'wh', 'wi', 'wj', 'wk', 'wl', 'wm', 'wn', 'wo', 'wp', 'wu', 'wy', 'w/', 'w;', 'xh', 'xi', 'xj', 'xk', 'xl',
        'xm', 'xn', 'xo', 'xp', 'xu', 'xy', 'x/', 'x;', 'ya', 'yb', 'yc', 'yd', 'ye', 'yf', 'yg', 'yq', 'yr', 'ys',
        'yt', 'yv', 'yw', 'yx', 'yz', 'zh', 'zi', 'zj', 'zk', 'zl', 'zm', 'zn', 'zo', 'zp', 'zu', 'zy', 'z/', 'z;',
        ',a', ',b', ',c', ',d', ',e', ',f', ',g', ',q', ',r', ',s', ',t', ',v', ',w', ',x', ',z', '/a', '/b', '/c',
        '/d', '/e', '/f', '/g', '/q', '/r', '/s', '/t', '/v', '/w', '/x', '/z', ';a', ';b', ';c', ';d', ';e', ';f',
        ';g', ';q', ';r', ';s', ';t', ';v', ';w', ';x', ';z']
dkpzh = ['br', 'bt', 'ce', 'ec', 'mu', 'my', 'nu', 'ny', 'p/', 'qz', 'rb', 'rv', 'tb', 'tv', 'um', 'un', 'vr', 'vt',
         'wx', 'xw', 'ym', 'yn', 'zq', ',i', '/p']
xkpzh = ['qa', 'za', 'fb', 'gb', 'vb', 'dc', 'cd', 'ed', 'de', 'bf', 'gf', 'rf', 'tf', 'vf', 'bg', 'fg', 'rg', 'tg',
         'vg', 'jh', 'mh', 'nh', 'uh', 'yh', 'ki', 'hj', 'mj', 'nj', 'uj', 'yj', 'ik', 'ol', 'hm', 'jm', 'nm', 'hn',
         'jn', 'mn', 'lo', ';p', 'aq', 'fr', 'gr', 'tr', 'ws', 'xs', 'ft', 'gt', 'rt', 'hu', 'ju', 'yu', 'bv', 'fv',
         'gv', 'sw', 'sx', 'hy', 'jy', 'uy', 'az', 'k,', ';/', 'p;', '/;']
xzgrzh = ['aa', 'ac', 'ad', 'ae', 'aq', 'as', 'aw', 'ax', 'az', 'ca', 'cq', 'cz', 'da', 'dq', 'dz', 'ea', 'eq',
          'ez', 'ip', 'i/', 'i;', 'kp', 'k/', 'k;', 'lp', 'l/', 'l;', 'op', 'o/', 'o;', 'pi', 'pk', 'pl', 'po',
          'pp', 'p;', 'qa', 'qc', 'qd', 'qe', 'qq', 'qs', 'qw', 'qx', 'sa', 'sq', 'sz', 'wa', 'wq', 'wz', 'xa',
          'xq', 'xz', 'za', 'zc', 'zd', 'ze', 'zs', 'zw', 'zx', 'zz', ',p', ',/', ',;', '/i', '/k', '/l', '/o',
          '//', '/;', ';i', ';k', ';l', ';o', ';p', ';/', ';;']
cszh = ['ct', ',y', 'tc', 'y,', 'cr', ',u', 'rc', 'u,', 'cw', ',o', 'wc', 'o,', 'qc', ',p', 'cq', 'p,', 'qx', 'p.',
        'xq', '.p', 'xe', '.i', 'ex', 'i.', 'xr', '.u', 'rx', 'u.', 'xt', '.y', 'tx', 'y.']


all_key = 'abcdefghijklmnopqrstuvwxyz'
all_double_key = [x + y for x in all_key for y in all_key]

dangliang={} # 导入当量数据
with open('./asserts/dlb.txt',encoding='utf-8') as t:
    for line in t.readlines():
        j,v=line.strip('\r\n').split('\t')
        dangliang[j]=float(v)


f = open('./asserts/cp.txt',encoding='utf-8', mode = 'r')
tl = [i.strip('\r\n').split('\t') for i in f]
# f.close()

# ci_list = []
# with open('asserts/cp.txt', encoding='utf-8', mode='r') as f:
#     for line in f:
#         l_c = line.strip('\r\n')
#         ci_list.append(l_c)
# 造词
def build_ci_by_full_code(full_code_map):
    cybm = []
    for cp in tl:
        ci = cp[0]
        lc = len(ci)
        if (lc == 2):
            # 一个字取两码：A1a1B1b1
            cybm.append((full_code_map[ci[0]][:2] + full_code_map[ci[1]][:2], int(cp[1])))
        elif (lc == 3):
            # 每个字取首码
            # ci_map[ci] = full_code_map[ci[0]][0] + full_code_map[ci[1]][0] + full_code_map[ci[2]][0]
            # 3字词是前两字第一码 + 第三字前两码
            cybm.append((full_code_map[ci[0]][0] + full_code_map[ci[1]][0] + full_code_map[ci[2]][:2], int(cp[1])))
        elif (lc == 4):
            cybm.append((full_code_map[ci[0]][0] + full_code_map[ci[1]][0] + full_code_map[ci[2]][0] + full_code_map[ci[3]][0], int(cp[1])))
        elif (lc > 4):
            cybm.append((full_code_map[ci[0]][0] + full_code_map[ci[1]][0] + full_code_map[ci[2]][0] + full_code_map[ci[-1]][0], int(cp[1])))
    # for char, code in full_code:
    return cybm

def jsdl(bm): # 计算一串编码的总当量
    s=0
    for l in range(len(bm)-1):
        u=bm[l]+bm[l+1]
        s=s+dangliang[u]
    return s

# 这个算法就更简单了，set 函数自动去重，list - set 就是选重数
def xcs(l):
    uni = set(x[0] for x in l)
    return len(l) - len(uni)

# 这个算法就是 sum 函数的应用
def jqdl(l):
    zdl = sum(x[0] * x[1] for x in l)
    zp = sum(x[1] for x in l)
    return zdl/zp

def dysc(z): # 打印后在“结果.txt”里添加字段
    print(z)
    # with open('结果.txt','a',encoding='utf-8') as t:
    #     t.write(z+'\n')

def stats(brief_code, cybm):
    dz = {}
    for kv in brief_code:
        z = kv[0]
        m = kv[1]
        if z in dz:
            if len(m) < len(dz[z]):
                dz[z] = m
            else:
                pass
        else:
            dz[z] = m
    l = [[pl1, '300'], [pl2, '500'], [pl3, '1500'], [pl4, '3000'], [pl5, '6000']]
    yl = {'a': 0, 'b': 0, 'c': 0, 'd': 0, 'e': 0, 'f': 0, 'g': 0, 'h': 0, 'i': 0, 'j': 0, 'k': 0, 'l': 0, 'm': 0,
          'n': 0, 'o': 0, 'p': 0, 'q': 0, 'r': 0, 's': 0, 't': 0, 'u': 0, 'v': 0, 'w': 0, 'x': 0, 'y': 0, 'z': 0,
          ',': 0, '.': 0, ';': 0, '/': 0, '\'': 0, '_': 0, '0': 0}
    bm = {}
    n1a, n2a, n3a, n4a, n5a, xca, jca, zjdla, hja, dkpa, xkpa, xzgra, csa, paa, zjja, p1a, p2a, p3a, p4a, p5a = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
    for i in l:
        n1 = 0
        n2 = 0
        n3 = 0
        n4 = 0
        n5 = 0
        p1 = 0
        p2 = 0
        p3 = 0
        p4 = 0
        p5 = 0
        n = [n1, n2, n3, n4, n5]
        hj = 0
        dkp = 0
        xkp = 0
        xzgr = 0
        cs = 0
        xc = 0
        jc = 0
        zjdl = 0
        pa = 0
        zjj = 0
        for j in i[0]:
            pa += i[0].get(j, 0)
            jc += i[0].get(j, 0) * len(dz.get(j, '0000'))
            if dz.get(j, j) not in bm:
                bm[dz.get(j, j)] = 1
            else:
                xc += 1
                if ((int)(i[1]) <= 1500):
                    print(dz.get(j, 0))
            if len(dz.get(j, '0000')) == 1:
                n1 += 1
                p1 += i[0].get(j, '0000')
            if len(dz.get(j, '0000')) == 2:
                n2 += 1
                p2 += i[0].get(j, '0000')
                # if i[1] == '3000' or i[1] == '6000':
                    # print(j + '\t' + dz[j])
            if len(dz.get(j, '0000')) == 3:
                n3 += 1
                p3 += i[0].get(j, '0000')
            if len(dz.get(j, '0000')) == 4:
                # print(dz.get(j,'0000'))
                n4 += 1
                p4 += i[0].get(j, '0000')
            if len(dz.get(j, '0000')) == 5:
                n5 += 1
                p5 += i[0].get(j, '0000')
            zh = []
            for k in dz.get(j, '0000'):
                yl[k] += i[0].get(j, '0000')
            for k in range(len(dz.get(j, '0000')) - 1):
                zh.append(dz.get(j, '0000')[k] + dz.get(j, '0000')[k + 1])
            for k in zh:
                zjdl += i[0].get(j, '0000') * ajew[k]
                zjj += i[0].get(j, '0000')
                if k in hjzh or '_' in k:
                    hj += i[0].get(j, '0000')
                if k in dkpzh:
                    dkp += i[0].get(j, '0000')
                if k in xkpzh:
                    xkp += i[0].get(j, '0000')
                if k in xzgrzh:
                    xzgr += i[0].get(j, '0000')
                if k in cszh:
                    cs += i[0].get(j, '0000')
        jjdl = (zjdl / pa) / ((jc / pa) - 1)
        # f.write(i[1] + '\t' + str(n1) + '\t' + str(n2) + '\t' + str(n3) + '\t' + str(n4) + '\t' + str(n5) + '\t' + str(
        #     xc) + '\t' + str(jc / pa) + '\t' + str(zjdl / pa) + '\t' + str(jjdl) + '\t' + str(hj / zjj) + '\t' + str(
        #     dkp / zjj) + '\t' + str(xkp / zjj) + '\t' + str(xzgr / zjj) + '\t' + str(cs / zjj) + '\n')
        n1a += n1
        n2a += n2
        n3a += n3
        n4a += n4
        n5a += n5
        p1a += p1
        p2a += p2
        p3a += p3
        p4a += p4
        p5a += p5
        xca += xc
        jca += jc
        zjdla += zjdl
        hja += hj
        dkpa += dkp
        xkpa += xkp
        xzgra += xzgr
        csa += cs
        paa += pa
        zjja += zjj
    jjdla = zjdla / (jca - 1)
    print('总选重：%d' % xca)
    print('键长：%f' % jca)
    print('字均当量：%f' % zjdla)
    print('键均当量：%f' % jjdla)
    print('左右互击：%f' % hja)
    print('同指大跨排：%f' % dkpa)
    print('小跨排：%f' % xkpa)
    print('小指干扰：%f' % xzgra)
    print('错手：%f' % csa)
    weight = (jca + zjdla + jjdla) * 500 + xca
    ci_weight = 0
    if len(cybm) > 0:
        cydl = [(jsdl(i[0]), i[1]) for i in cybm]
        j1, j2, j3, j4, j5, j6 = cybm[:2000], cybm[:5000], cybm[:10000], cybm[:20000], cybm[:40000], cybm[:60000]
        k1, k2, k3, k4, k5, k6 = cydl[:2000], cydl[2000:5000], cydl[5000:10000], cydl[10000:20000], cydl[20000:40000], cydl[40000:60000]
        kn3, kn6 = cydl[:10000], cydl[:60000]
        # 前1万
        j3d = {}
        j3dx = j3[::-1]
        for i in j3dx:
            j3d[i[0]] = i[1]
        xc3 = 1 - (sum(j3d.values()) / sum(x[1] for x in j3))
        # 前6万
        j6d = {}
        j6dx = j6[::-1]
        for i in j6dx:
            j6d[i[0]] = i[1]
        xc6 = 1 - (sum(j6d.values()) / sum(x[1] for x in j6))
        # 然后算不加权选重
        x1, x2, x3, x4, x5, x6 = tuple(map(xcs, (j1, j2, j3, j4, j5, j6)))
        xn1 = x1
        xn2 = x2 - x1
        xn3 = x3 - x2
        xn4 = x4 - x3
        xn5 = x5 - x4
        xn6 = x6 - x5
        d1, d2, d3, d4, d5, d6 = tuple(map(jqdl, (k1, k2, k3, k4, k5, k6)))
        dxj = jqdl(kn3)
        dzj = jqdl(kn6)
        dysc(
            '1-2k\t%s\t%.2f\n' % (xn1, d1) +
            '2k-5k\t%s\t%.2f\n' % (xn2, d2) +
            '5k-10k\t%s\t%.2f\n' % (xn3, d3) +
            '小计\t%s\t%.2f\n' % (x3, dxj) +
            '加权比重\t%.2f%%\n\n' % (xc3 * 100) +
            '10k-20k\t%s\t%.2f\n' % (xn4, d4) +
            '20k-40k\t%s\t%.2f\n' % (xn5, d5) +
            '40k-60k\t%s\t%.2f\n' % (xn6, d6) +
            '总计\t%s\t%.2f\n' % (x6, dzj) +
            '加权比重\t%.2f%%\n' % (xc6 * 100)
        )
        ci_weight += x3 / 10 + x6 / 100 + d1 * 80 + d2 * 60 + d3 * 50 + d4 * 20 + d5 * 20 + d6 * 20
    print('--------------------------------')
    return weight + ci_weight

component_changed = []
component_changed_map = {}
with open('data/changed_components.txt', encoding='utf-8', mode='r') as f:
    for line in f:
        char = line.strip('\r\n')
        comps = char.split('\t')
        component_changed_map[comps[0]] = comps
        component_changed.append(char)

keys = [
    'q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p',
    'a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l',
    'z', 'x', 'c', 'v', 'b', 'n', 'm'
]

# ci_list = []
# # 读取词表
# with open('asserts/ci.txt', encoding='utf-8', mode='r') as f:
#     for line in f:
#         l_c = line.strip('\r\n')
#         ci_list.append(l_c)


class ComponentsDistributionProblem(Annealer):
    def __int__(self, state):
        super(ComponentsDistributionProblem, self).__init__(state)

    def energy(self):
        full_res = build_full_code(self.state, decompositionLines)
        full_c = full_res[0]
        brief_c = build_brief_code(full_c)
        full_c_map = full_res[1]
        cybm = build_ci_by_full_code(full_c_map)
        # ci_c = {}
        return stats(brief_c, cybm)

    def move(self):
        l = list(self.state.keys())
        a = random.choice(l)
        k = random.choice(keys)
        for kv in component_changed_map.items():
            if (a in kv[1]):
                for b in kv[1]:
                    self.state[b] = k


def zu_ci(full_code_map):
    ci_map = {}
    for cp in tl:
        ci = cp[0]
        lc = len(ci)
        if (lc == 2):
            # 一个字取两码：A1a1B1b1
            ci_map[ci] = full_code_map[ci[0]][:2] + full_code_map[ci[1]][:2]
        elif (lc == 3):
            # 每个字取首码
            # ci_map[ci] = full_code_map[ci[0]][0] + full_code_map[ci[1]][0] + full_code_map[ci[2]][0]
            # 3字词是前两字第一码 + 第三字前两码
            ci_map[ci] = full_code_map[ci[0]][0] + full_code_map[ci[1]][0] + full_code_map[ci[2]][:2]
        elif (lc == 4):
            ci_map[ci] = full_code_map[ci[0]][0] + full_code_map[ci[1]][0] + full_code_map[ci[2]][0] + \
                         full_code_map[ci[3]][0]
        elif (lc > 4):
            ci_map[ci] = full_code_map[ci[0]][0] + full_code_map[ci[1]][0] + full_code_map[ci[2]][0] + \
                         full_code_map[ci[-1]][0]
    # for char, code in full_code:
    return ci_map


#
if __name__ == '__main__':
    cdp = ComponentsDistributionProblem(componentKey)
    cdp.copy_strategy = "method"
    # auto_schedule = {'tmax': 0.14, 'tmin': 6.7e-07, 'steps': 30000, 'updates': 30000}  # 如果确定用什么参数，就提供
    auto_schedule = {'tmax': 0.14, 'tmin': 6.7e-07, 'steps': 10000, 'updates': 100}  # 如果确定用什么参数，就提供
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
        for key, key_map in state.items():
            newKeymapFile.write(key + '\t' + key_map + '\n')

    # 以键分组存和字典
    key_map = {}
    # with open('data/new_keymap.json', encoding='utf-8', mode='w') as f:
    #     for char, key in state:
    #         key_map[key] = key_map.get(key, []) + [char]
    #     json.dump(key_map, f, ensure_ascii=False)
    with open('data/new_keymap.json', encoding='utf-8', mode='w') as f:
        for char, key in state.items():
            key_map[key] = key_map.get(key, []) + [char]
        json.dump(key_map, f, ensure_ascii=False)

    full_res = build_full_code(state, decompositionLines)
    full_code = full_res[0]
    brief_code = get_brief_code(full_code)
    brief_1_code = []
    with open('data/new_brief_code.txt', encoding='utf-8', mode='w') as newBriefCodeFile:
        for char, code in brief_code:
            newBriefCodeFile.write('%s\t%s\n' % (char, code))
            if (len(code) == 1):
                brief_1_code.append((char, code))

    with open('data/single_brief_code.txt', encoding='utf-8', mode='w') as singleCodeFile:
        for char, code in brief_1_code:
            singleCodeFile.write('%s\t%s\n' % (char, code))

    with open('data/full_code.txt', encoding='utf-8', mode='w') as fullCodeFile:
        for char, code in full_code:
            fullCodeFile.write('%s\t%s\n' % (char, code))

    full_code_map = full_res[1]
    ci_map = zu_ci(full_code_map)
    with open('data/ci_code.txt', encoding='utf-8', mode='w') as fiCodeFile:
        for kv in ci_map.items():
            fiCodeFile.write('%s\t%s\n' % (kv[0], kv[1]))
    # fullCode = build_full_code(componentKey, decompositionLines)[0]

    # brief_code = build_brief_code(fullCode)
    # with open('data/brief_code.txt', encoding='utf-8', mode='w') as briefCodeFile:
    #     for char, code in brief_code:
    #         briefCodeFile.write('%s\t%s\n' % (char, code))

    with open('data/new_brief_code_char.txt', encoding='utf-8', mode='w') as newBriefCodeFile:
        for char, code in brief_code:
            newBriefCodeFile.write('%s\n' % (char))

    with open('data/new_brief_code_code.txt', encoding='utf-8', mode='w') as newBriefCodeFile:
        for char, code in brief_code:
            newBriefCodeFile.write('%s\n' % (code))


    with open('data/new_brief_code_code.txt', encoding='utf-8', mode='w') as newBriefCodeFile:
        for char, code in brief_code:
            newBriefCodeFile.write('%s\n' % (code))
