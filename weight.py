from helper import xcs, dysc
from stats import jsdl, jqdl


def get_zi_weight(stats_map, w_map):
    xca = stats_map['xca']
    xca_3000 = stats_map['xca_3000']
    jca = stats_map['jca']
    zjdla = stats_map['zjdla']
    jjdla = stats_map['jjdla']
    jca_500 = stats_map['jca_500']
    jca_1500 = stats_map['jca_1500']
    zjdla_500 = stats_map['zjdla_500']
    jjdla_500 = stats_map['jjdla_500']
    hja = stats_map['hja']
    dkpa = stats_map['dkpa']
    dkpa_500 = stats_map['dkpa_500']
    dkpa_1500 = stats_map['dkpa_1500']
    csa_1500 = stats_map['csa_1500']
    xkpa = stats_map['xkpa']
    xzgra = stats_map['xzgra']
    csa = stats_map['csa']
    n4a_500 = stats_map['n4a_500']
    n4a_1500 = stats_map['n4a_1500']
    n4a_3000 = stats_map['n4a_3000']
    # --
    xca_weight = w_map['xca'][0]
    xca_3000_weight = w_map['xca_3000'][0]
    jca_weight = w_map['jca'][0]
    zjdla_weight = w_map['zjdla'][0]
    jjdla_weight = w_map['jjdla'][0]
    jca_500_weight = w_map['jca_500'][0]
    jca_1500_weight = w_map['jca_1500'][0]
    zjdla_500_weight = w_map['zjdla_500'][0]
    jjdla_500_weight = w_map['jjdla_500'][0]
    hja_weight = w_map['hja'][0]
    dkpa_weight = w_map['dkpa'][0]
    dkpa_500_weight = w_map['dkpa_500'][0]
    dkpa_1500_weight = w_map['dkpa_1500'][0]
    csa_1500_weight = w_map['csa_1500'][0]
    xkpa_weight = w_map['xkpa'][0]
    xzgra_weight = w_map['xzgra'][0]
    csa_weight = w_map['csa'][0]
    n4a_500_weight = w_map['n4a_500'][0]
    n4a_1500_weight = w_map['n4a_1500'][0]
    n4a_3000_weight = w_map['n4a_3000'][0]
    weight = (
            (xca * xca_weight) +
            (xca_3000 * xca_3000_weight) +
            (jca * jca_weight) +
            (zjdla * zjdla_weight) +
            (jjdla * jjdla_weight) +
            (jca_500 * jca_500_weight) +
            (jca_1500 * jca_1500_weight) +
            (zjdla_500 * zjdla_500_weight) +
            (jjdla_500 * jjdla_500_weight) +
            (hja * hja_weight) +
            (dkpa * dkpa_weight) +
            (dkpa_500 * dkpa_500_weight) +
            (dkpa_1500 * dkpa_1500_weight) +
            (csa_1500 * csa_1500_weight) +
            (xkpa * xkpa_weight) +
            (xzgra * xzgra_weight) +
            (csa * csa_weight) +
            (n4a_500 * n4a_500_weight) +
            (n4a_1500 * n4a_1500_weight) +
            (n4a_3000 * n4a_3000_weight)
    )
    return weight


def get_ci_weight(cybm):
    ci_weight = 0
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
        ci_weight += x3 * 1.5 + x6 / 60 + d1 * 80 + d2 * 60 + d3 * 50 + d4 * 20 + d5 * 20 + d6 * 20
    print('--------------------------------')
    return ci_weight
