import json


def read_component_keymap(file_path):
    """
    # 读取字根按键映射表，士	h
    Returns:
          component_key {'士': 'h'}
          component_name {'士': '士'}
    """
    component_key = {}
    component_name = {}

    with open(file_path, encoding='utf-8') as keymapFile:
        for line in keymapFile:
            li = line.strip('\r\n')
            arr = li.split('\t')
            component = arr[0]  # 字根
            key = arr[1]  # 按键
            component_key[component] = key

            if len(arr) < 3:
                component_name[component] = component
            else:
                component_name[component] = arr[2]

    return component_key, component_name


def process_zp2_file(file_path):
    """
    # 读取字频，这	8182859.026	10
    """
    pl1 = {}
    pl2 = {}
    pl3 = {}
    pl4 = {}
    pl5 = {}
    zp_a = {}

    with open(file_path, encoding='utf-8') as file:
        for line in file:
            z, p, x = line.strip().split('\t')
            x = float(x)
            p = float(p)
            p /= 1_000_000_000  # 将 p 转换为十亿分之一
            zp_a[z] = p

            if x <= 300:
                pl1[z] = p
            elif x <= 500:
                pl2[z] = p
            elif x <= 1500:
                pl3[z] = p
            elif x <= 3000:
                pl4[z] = p
            elif x <= 7000:
                pl5[z] = p

    return pl1, pl2, pl3, pl4, pl5, zp_a


def read_ajew_file(file_path):
    """
    读取按键权重表，wk	1.1
    Returns:
        {'wk': 1.1}
    """
    ajew = {}

    with open(file_path, encoding='utf-8') as file:
        for line in file:
            aj, ew = line.strip().split('\t')
            ajew[aj] = float(ew)

    return ajew


def read_stroke():
    """
    读取汉字笔画顺序表，七	15，stroke_char 只取前两笔用于编码

    """
    stroke_char = {}  # {'七': '15'}
    with open('asserts/stroke.txt', encoding='utf-8', mode='r') as strokeFile:
        for line in strokeFile:
            arr = line.strip().split('\t')
            stroke = arr[1]  # 例如笔画数字：15
            two_stroke = ''
            stroke_len = len(stroke)
            if stroke_len >= 2:
                two_stroke += stroke[0] + stroke[1]  # 取前笔
            elif stroke_len == 1:  # 如果只有一个笔画，就重复该笔画
                two_stroke += stroke[0] * 2
            stroke_char[arr[0]] = two_stroke
    return stroke_char


def read_char_py_first():
    # 读取汉字对应的拼音首字母，{'有': 'y'}
    char_py = {}
    with open('data/char_py_first.txt', encoding='utf-8', mode='r') as pinyinFile:
        for line in pinyinFile:
            char, py = line.strip().split('\t')
            char_py[char] = py
    return char_py


def read_cp_file(file_path):
    # 读取词频
    with open(file_path, encoding='utf-8') as file:
        tl = [line.strip().split('\t') for line in file]

    return tl


def read_component_compose_file(file_path):
    """
     # {'<辰内>': '<辰内>	<辰下>	<畏下>	<衣下>'}
    """
    component_compose_map = {}
    with open(file_path, encoding='utf-8', mode='r') as f:
        for line in f:
            char = line.strip('\r\n')
            comps = char.split('\t')
            component_compose_map[comps[0]] = comps
    return component_compose_map


def read_decomposition_line_file(file_path):
    decomposition_ines = []
    # 读取拆分表到 decomposition_ines 列表，['眼	目	艮		yn	0', 'xxx']
    with open('asserts/decomposition.txt', encoding='utf-8', mode='r') as componentFile:
        decomposition_ines = [line for line in componentFile]
    return decomposition_ines


def write_keymap_to_file(file_path, state):
    with open(file_path, encoding='utf-8', mode='w') as newKeymapFile:
        for key, key_map in state.items():
            newKeymapFile.write(key + '\t' + key_map + '\n')


def write_keymap_json_to_file(file_path, state):
    key_map = {}
    with open(file_path, encoding='utf-8', mode='w') as f:
        for char, key in state.items():
            key_map[key] = key_map.get(key, []) + [char]
        json.dump(key_map, f, ensure_ascii=False)


def write_brief_code_to_file(brief_code_path, single_brief_code_path, brief_code):
    brief_1_code = []
    with open(brief_code_path, encoding='utf-8', mode='w') as newBriefCodeFile:
        for char, code in brief_code:
            newBriefCodeFile.write('%s\t%s\n' % (char, code))
            if len(code) == 1:
                brief_1_code.append((char, code))

    with open(single_brief_code_path, encoding='utf-8', mode='w') as singleCodeFile:
        for char, code in brief_1_code:
            singleCodeFile.write('%s\t%s\n' % (char, code))


def write_brief_code_char_to_file(file_path, brief_code):
    with open(file_path, encoding='utf-8', mode='w') as newBriefCodeFile:
        for char, code in brief_code:
            newBriefCodeFile.write('%s\n' % char)


def write_brief_code_code_to_file(file_path, brief_code):
    with open(file_path, encoding='utf-8', mode='w') as newBriefCodeFile:
        for char, code in brief_code:
            newBriefCodeFile.write('%s\n' % code)


def write_full_code_to_file(file_path, full_code):
    with open(file_path, encoding='utf-8', mode='w') as full_code_listFile:
        for char, code in full_code:
            full_code_listFile.write('%s\t%s\n' % (char, code))


def write_ci_code_to_file(file_path, ci_map):
    with open(file_path, encoding='utf-8', mode='w') as fiCodeFile:
        for kv in ci_map.items():
            fiCodeFile.write('%s\t%s\n' % (kv[0], kv[1]))


def save_to_json(data, filename):
    """
    将数据序列化为JSON并保存到文件

    Parameters:
    - data: 要保存的数据（字典）
    - filename: 要保存到的文件名
    """
    try:
        # 将数据序列化为JSON字符串
        data_json = json.dumps(data, indent=2)

        # 保存JSON字符串到文件
        with open(filename, 'w') as file:
            file.write(data_json)

        # print(f'Data has been saved to {filename}')
    except Exception as e:
        print(f'Error saving data to {filename}: {e}')


def load_from_json(filename):
    """
    从JSON文件中读取数据并反序列化为Python对象

    Parameters:
    - filename: 要读取的文件名

    Returns:
    - data: 反序列化后的数据
    """
    try:
        with open(filename, 'r') as file:
            data = json.load(file)
            print(f'Data loaded from {filename}')
            return data
    except Exception as e:
        print(f'Error loading data from {filename}: {e}')
        return None


# set 函数自动去重，list - set 就是选重数
def xcs(l):
    uni = set(x[0] for x in l)
    return len(l) - len(uni)


def dysc(z):  # 打印后在“结果.txt”里添加字段
    print(z)
    # with open('结果.txt','a',encoding='utf-8') as t:
    #     t.write(z+'\n')


def get_key_category():
    """
    获取按键分类list
    hjzh: 好击key_map
    dkpzh: 大跨排key_map
    xkpzh: 小跨排key_map
    xzgrzh：小指干扰key_map
    cszh: 错手key_map
    """
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
    return hjzh, dkpzh, xkpzh, xzgrzh, cszh
