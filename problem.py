import random

from simanneal import Annealer

from weight import get_zi_weight, get_ci_weight


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
        # full_c_map = full_res[1]
        # cybm = build.build_ci_by_full_code(full_c_map)
        ci_c = {}
        return self.stats(brief_c, ci_c)

    def move(self):
        lst = list(self.state.keys())
        a = random.choice(lst)
        k = random.choice(self.keys)
        for key_v in self.compose_map.items():
            if a in key_v[1]:
                for b in key_v[1]:
                    self.state[b] = k

    def stats(self, bf_code, cybm):
        stats_map = self.stats_calc.statistics(bf_code)
        weight = get_zi_weight(stats_map, self.weight_map)
        ci_weight = get_ci_weight(cybm)
        return weight + ci_weight
