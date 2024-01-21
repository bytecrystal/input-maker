import random

from simanneal import Annealer


class ComponentsDistributionProblem(Annealer):
    def __init__(self, st, compose_map, w_map, keys, decomposition_ines, build, stats):
        super(ComponentsDistributionProblem, self).__init__(st)
        self.compose_map = compose_map
        self.weight_map = w_map
        self.keys = keys
        self.decomposition_ines = decomposition_ines
        self.builder = build
        self.stats_calc = stats

    def energy(self):
        full_code_res = self.builder.build_full_code(self.state, self.decomposition_ines)
        full_c = full_code_res[0]
        brief_c = self.builder.build_brief_code(full_c)
        full_c_map = full_code_res[1]
        cybm = self.builder.build_ci_by_full_code(full_c_map)
        return self.stats(brief_c, cybm)

    def move(self):
        lst = list(self.state.keys())
        a = random.choice(lst)
        k = random.choice(self.keys)
        for key_v in self.compose_map.items():
            if a in key_v[1]:
                for b in key_v[1]:
                    self.state[b] = k

    def stats(self, bf_code, cybm):
        stats_map = self.stats_calc.zi_statis(bf_code)
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
        er_ma_500 = stats_map['er_ma_500']

        w_map = self.weight_map
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
        er_ma_500_weight = w_map['er_ma_500'][0]
        zi_weight = (
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
                (n4a_3000 * n4a_3000_weight) -
                (er_ma_500 * er_ma_500_weight)
        )
        zi_weight = round(zi_weight, 2)

        ci_weight = 0
        (x3, x6, d1, d2, d3, d4, d5, d6) = self.stats_calc.ci_statis(cybm)
        ci_x3_weight = self.weight_map['ci_x3'][0]
        ci_x6_weight = self.weight_map['ci_x6'][0]
        ci_d1_weight = self.weight_map['ci_d1'][0]
        ci_d2_weight = self.weight_map['ci_d2'][0]
        ci_d3_weight = self.weight_map['ci_d3'][0]
        ci_d4_weight = self.weight_map['ci_d4'][0]
        ci_d5_weight = self.weight_map['ci_d5'][0]
        ci_d6_weight = self.weight_map['ci_d6'][0]
        ci_weight += \
            ((x3 * ci_x3_weight) +
             (x6 * ci_x6_weight) +
             (d1 * ci_d1_weight) +
             (d2 * ci_d2_weight) +
             (d3 * ci_d3_weight) +
             (d4 * ci_d4_weight) +
             (d5 * ci_d5_weight) +
             (d6 * ci_d6_weight))
        ci_weight = round(ci_weight, 2)
        weight = zi_weight + ci_weight

        print("总选重权重占比：", format(xca * xca_weight / weight, '.2%'))
        print("前3000权重占比：", format(xca_3000 * xca_3000_weight / weight, '.2%'))
        print("总键长权重占比：", format(jca * jca_weight / weight, '.2%'))
        print("总字均当量权重占比：", format(zjdla * zjdla_weight / weight, '.2%'))
        print("总键均当量权重占比：", format(jjdla * jjdla_weight / weight, '.2%'))
        print("前500键长权重占比：", format(jca_500 * jca_500_weight / weight, '.2%'))
        print("前1500键长权重占比：", format(jca_1500 * jca_1500_weight / weight, '.2%'))
        print("前500字均当量权重占比：", format(zjdla_500 * zjdla_500_weight / weight, '.2%'))
        print("前500键均当量权重占比：", format(jjdla_500 * jjdla_500_weight / weight, '.2%'))
        print("总的左右互击数权重占比：", format(hja * hja_weight / weight, '.2%'))
        print("总的同指大跨排权重占比：", format(dkpa * dkpa_weight / weight, '.2%'))
        print("前500同指大跨排权重占比：", format(dkpa_500 * dkpa_500_weight / weight, '.2%'))
        print("前1500同指大跨排权重占比：", format(dkpa_1500 * dkpa_1500_weight / weight, '.2%'))
        print("前1500错手权重占比：", format(csa_1500 * csa_1500_weight / weight, '.2%'))
        print("总的小跨排权重占比：", format(xkpa * xkpa_weight / weight, '.2%'))
        print("总的小指干扰权重占比：", format(xzgra * xzgra_weight / weight, '.2%'))
        print("总的错手权重占比：", format(csa * csa_weight / weight, '.2%'))
        print("前500四码数权重占比：", format(n4a_500 * n4a_500_weight / weight, '.2%'))
        print("前1500四码数权重占比：", format(n4a_1500 * n4a_1500_weight / weight, '.2%'))
        print("前3000四码数权重占比：", format(n4a_3000 * n4a_3000_weight / weight, '.2%'))
        print("前500二码数权重占比：", format(er_ma_500 * er_ma_500_weight / weight, '.2%'))
        print('####################### 词的权重占比 #######################')

        print("前10000词选重权重占比：", format(x3 * ci_x3_weight / weight, '.2%'))
        print("前60000词选重权重占比：", format(x6 * ci_x6_weight / weight, '.2%'))
        print("前2000词的键均当量权重占比：", format(d1 * ci_d1_weight / weight, '.2%'))
        print("2000-5000词的键均当量权重占比：", format(d2 * ci_d2_weight / weight, '.2%'))
        print("5000-10000词的键均当量权重占比：", format(d3 * ci_d3_weight / weight, '.2%'))
        print("1w-2w词的键均当量权重占比：", format(d4 * ci_d4_weight / weight, '.2%'))
        print("2w-4w词的键均当量权重占比：", format(d5 * ci_d5_weight / weight, '.2%'))
        print("4w-6w词的键均当量权重占比：", format(d6 * ci_d6_weight / weight, '.2%'))
        print("--------------------------")
        return weight

    # def print_percent(self, zi_weight, ci_weight, total_weight):
    #     print("字的优化总权重占比：", format(zi_weight / total_weight, ".2%"))
    #     print("词的优化总权重占比：", format(ci_weight / total_weight, ".2%"))
