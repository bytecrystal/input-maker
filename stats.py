from helper import *

pl1, pl2, pl3, pl4, pl5, zp_a = process_zp2_file('test/zp2.txt')
# 读取按键权重表，wk	1.1
ajew = read_ajew_file('test/ew.txt')
# 获取按键分类list
hjzh, dkpzh, xkpzh, xzgrzh, cszh = get_key_category()

dangliang = {}  # 导入当量数据
with open('./asserts/dlb.txt', encoding='utf-8') as t:
    for line in t.readlines():
        j, v = line.strip().split('\t')
        dangliang[j] = float(v)


def jsdl(bm):  # 计算一串编码的总当量
    s = 0
    for l in range(len(bm) - 1):
        u = bm[l] + bm[l + 1]
        s = s + dangliang[u]
    return s


# 这个算法就是 sum 函数的应用
def jqdl(l):
    zdl = sum(x[0] * x[1] for x in l)
    zp = sum(x[1] for x in l)
    return zdl / zp


class Stats(object):
    def __init__(self):
        self.a = 10

    def zi_statis(self, brief_code):

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
        yl = {'a': 0, 'b': 0, 'c': 0, 'd': 0, 'e': 0, 'f': 0, 'g': 0, 'h': 0, 'i': 0, 'j': 0, 'k': 0, 'l': 0,
              'm': 0,
              'n': 0, 'o': 0, 'p': 0, 'q': 0, 'r': 0, 's': 0, 't': 0, 'u': 0, 'v': 0, 'w': 0, 'x': 0, 'y': 0,
              'z': 0,
              ',': 0, '.': 0, ';': 0, '/': 0, '\'': 0, '_': 0, '0': 0}
        bm = {}
        n1a, n2a, n3a, n4a, n5a, xca, jca, zjdla, hja, dkpa, xkpa, xzgra, csa, paa, zjja, p1a, p2a, p3a, p4a, p5a = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
        dkpa_500 = 0
        dkpa_1500 = 0
        xkpa_500 = 0
        xkpa_1500 = 0
        xzgra_500 = 0
        xzgra_1500 = 0
        csa_500 = 0
        csa_1500 = 0
        jca_500 = 0
        jca_1500 = 0
        zjdla_500 = 0
        zjdla_1500 = 0
        jjdla_500 = 0
        jjdla_1500 = 0
        hja_500 = 0
        hja_1500 = 0
        n4a_1500 = 0
        n4a_500 = 0
        xca_500 = 0
        xca_3000 = 0
        n4a_3000 = 0
        er_ma_500 = 0
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
            # n = [n1, n2, n3, n4, n5]
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
                    # if ((int)(i[1]) <= 1500):
                    #     print(dz.get(j, 0))
                    if ((int)(i[1]) <= 3000):
                        xca_3000 += 1
                if len(dz.get(j, '0000')) == 1:
                    n1 += 1
                    p1 += i[0].get(j, '0000')
                if len(dz.get(j, '0000')) == 2:
                    n2 += 1
                    p2 += i[0].get(j, '0000')
                    if i[1] == '300' or i[1] == '500':
                        er_ma_500 += 1
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
                        if (int)(i[1]) <= 500:
                            hja_500 += 1
                        if (int)(i[1]) <= 1500:
                            hja_1500 += 1
                    if k in dkpzh:
                        dkp += i[0].get(j, '0000')
                        if (int)(i[1]) <= 500:
                            dkpa_500 += 1
                        if (int)(i[1]) <= 1500:
                            dkpa_1500 += 1
                    if k in xkpzh:
                        xkp += i[0].get(j, '0000')
                        if (int)(i[1]) <= 500:
                            xkpa_500 += 1
                        if (int)(i[1]) <= 1500:
                            xkpa_1500 += 1
                    if k in xzgrzh:
                        xzgr += i[0].get(j, '0000')
                        if (int)(i[1]) <= 500:
                            xzgra_500 += 1
                        if (int)(i[1]) <= 1500:
                            xzgra_1500 += 1
                    if k in cszh:
                        cs += i[0].get(j, '0000')
                        if (int)(i[1]) <= 500:
                            csa_500 += 1
                        if (int)(i[1]) <= 1500:
                            csa_1500 += 1
            jjdl = (zjdl / pa) / ((jc / pa) - 1)
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
            if (int)(i[1]) == 500:
                jca_500 += jc
                zjdla_500 += zjdl
                jjdla_500 += jjdl
                n4a_500 += n4
            if (int)(i[1]) == 1500:
                jca_1500 += jc
                zjdla_1500 += zjdl
                jjdla_1500 += jjdl
            if (int)(i[1]) <= 1500:
                n4a_1500 += n4
            if (int)(i[1]) <= 3000:
                n4a_3000 += n4
        jjdla = zjdla / (jca - 1)
        print('总选重：%d' % xca)
        print('键长：%f' % jca)
        print('字均当量：%f' % zjdla)
        print('键均当量：%f' % jjdla)
        print('前500键长：%f' % jca_500)
        print('前1500键长：%f' % jca_1500)
        print('前500字均当量：%f' % zjdla_500)
        print('前500键均当量：%f' % jjdla_500)
        print('左右互击：%f' % hja)
        print('同指大跨排：%f' % dkpa)
        print('同指大跨排500：%d' % dkpa_500)
        print('同指大跨排1500：%d' % dkpa_1500)
        print('错手1500：%d' % csa_1500)
        print('小跨排：%f' % xkpa)
        print('小指干扰：%f' % xzgra)
        print('错手：%f' % csa)
        print('前500四码数：%d' % n4a_500)
        print('前1500四码数：%d' % n4a_1500)
        print('前3000选重：%d' % xca_3000)
        print('前3000四码数：%d' % n4a_3000)
        print('前500二码数：%d' % er_ma_500)
        print('--------------------------------')
        stats_map = {
            'xca': xca,
            'jca': jca,
            'zjdla': zjdla,
            'jjdla': jjdla,
            'jca_500': jca_500,
            'jca_1500': jca_1500,
            'zjdla_500': zjdla_500,
            'jjdla_500': jjdla_500,
            'hja': hja,
            'dkpa': dkpa,
            'dkpa_500': dkpa_500,
            'dkpa_1500': dkpa_1500,
            'csa_1500': csa_1500,
            'xkpa': xkpa,
            'xzgra': xzgra,
            'csa': csa,
            'n4a_500': n4a_500,
            'n4a_1500': n4a_1500,
            'xca_3000': xca_3000,
            'n4a_3000': n4a_3000,
            'er_ma_500': er_ma_500
        }
        return stats_map

    def ci_statis(self, cybm):
        if len(cybm) > 0:
            cydl = [(jsdl(i[0]), i[1]) for i in cybm]
            j1, j2, j3, j4, j5, j6 = cybm[:2000], cybm[:5000], cybm[:10000], cybm[:20000], cybm[:40000], cybm[:60000]
            k1, k2, k3, k4, k5, k6 = cydl[:2000], cydl[2000:5000], cydl[5000:10000], cydl[10000:20000], cydl[
                                                                                                        20000:40000], cydl[
                                                                                                                      40000:60000]
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
            return x3, x6, d1, d2, d3, d4, d5, d6
        else:
            return 0, 0, 0, 0, 0, 0, 0, 0
