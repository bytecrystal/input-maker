# This is a sample Python script.

# 导入退火算法优化工具
from build import *
from problem import ComponentsDistributionProblem
from stats import *

# 单字优化权重map，只会取第0个，值越大权重越大，调整第0个以改变偏好的优化方向，
weight_map = {
    'xca': [1.0, 1.2, 1.3, 1.4, 1.5],
    'jca': [700, 800, 900, 1000, 1100],
    'zjdla': [700, 800, 900, 1000, 1100],
    'jjdla': [700, 800, 900, 1000, 1100],
    'jca_500': [0],
    'jca_1500': [0],
    'zjdla_500': [0],
    'jjdla_500': [0],
    'hja': [0],
    'dkpa': [0],
    'dkpa_500': [0],
    'dkpa_1500': [0.8, 0.9, 1.0, 1.1, 1.2],
    'csa_1500': [0.9, 1.0, 1, 1.1, 1.2],
    'xkpa': [0],
    'xzgra': [0],
    'csa': [0],
    'n4a_500': [3, 4, 5, 6, 7],
    'n4a_1500': [0.8, 0.9, 1.0, 1.1, 1.2],
    'xca_3000': [2, 1, 1.5, 2, 2.5],
    'n4a_3000': [0.5, 0.8, 1.0, 1.1, 1.2],
}

#
if __name__ == '__main__':
    keys = [
        'q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p',
        'a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l',
        'z', 'x', 'c', 'v', 'b', 'n', 'm'
    ]
    component_key, component_name = read_component_keymap('data/new_keymap.txt')
    decomposition_ines = read_decomposition_line_file('asserts/decomposition.txt')
    component_compose_map = read_component_compose_file('./data/changed_components.txt')
    build = Build()
    stats = Stats()

    cdp = ComponentsDistributionProblem(
        component_key, component_compose_map, weight_map, keys, decomposition_ines, build, stats
    )
    cdp.copy_strategy = "method"
    auto_schedule = {'tmax': 0.14, 'tmin': 6.7e-07, 'steps': 5000, 'updates': 100}  # 如果确定用什么参数，就提供
    # auto_schedule = cdp.auto(minutes=1)
    print(auto_schedule)
    cdp.set_schedule(auto_schedule)
    state, dup = cdp.anneal()  # 开始优化
    # print(dup)
    # print(state)
    full_res = build.build_full_code(state, decomposition_ines)
    full_code, full_code_map = build.build_full_code(state, decomposition_ines)
    brief_code = build.build_brief_code(full_code)
    ci_map = build.zu_ci(full_code_map)

    write_keymap_to_file('data/new_keymap.txt', state)
    write_keymap_json_to_file('data/new_keymap.json', state)
    write_brief_code_to_file('data/new_brief_code.txt',
                             'data/single_brief_code.txt', brief_code)
    write_full_code_to_file('data/full_code.txt', full_code)
    write_ci_code_to_file('data/ci_code.txt', ci_map)
    write_brief_code_char_to_file('data/new_brief_code_char.txt', brief_code)
    write_brief_code_code_to_file('data/new_brief_code_code.txt', brief_code)
