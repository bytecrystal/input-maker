from helper import *


class Build:
    def __init__(self):
        # 笔画数字和字根横、竖、撇、点、折的对应关系
        self.stroke_zm = {'1': '一', '2': '丨', '3': '丿', '4': '丶', '5': '乛'}
        self.stroke_char = read_stroke()
        self.tl = read_cp_file('./asserts/cp.txt')

    def build_brief_code(self, full_code_list):
        """
        构造字->全码的映射表
        Parameters:
            full_code_list: [('渔', 'aaa'), (xx, xx)]

        Returns:
            brief_code_res: [('渔', 'aa'), (xx, xx)]
        """
        brief_code_res = []
        c = {}

        for b_zi, b_code in full_code_list:
            code_1 = b_code[:1]
            code_2 = b_code[:2]
            code_3 = b_code[:3]
            if code_1 not in c:
                c[code_1] = 1
                brief_code_res.append((b_zi, code_1))
            elif code_2 not in c:
                c[code_2] = 1
                brief_code_res.append((b_zi, code_2))
            elif code_3 not in c:
                c[code_3] = 1
                brief_code_res.append((b_zi, code_3))
            else:
                brief_code_res.append((b_zi, b_code))
        return brief_code_res

    def build_full_code(self, component_k, decomposition_lines):
        """
        构造字->全码的映射表
        Parameters:
            component_k: {'氵': 'a'}
            decomposition_lines: 渔	氵	鱼		yu	0

        Returns:
            full_code_list: [('渔', 'aaa'), (xx, xx)]
            full_code_dict: {'渔': 'aaa'}
        """
        full_code_list = []
        full_code_dict = {}
        for de_comp_line in decomposition_lines:
            de_comp_char, s1, s2, s3, py_first_and_last, is_partial = de_comp_line.strip().split('\t')
            if s3:
                c1 = component_k[s1]
                c2 = component_k[s2]
                c3 = component_k[s3]
                qm = c1 + c2 + c3
                full_code_list.append((de_comp_char, qm))
                full_code_dict[de_comp_char] = qm
            elif s2:
                c1 = component_k[s1]
                c2 = component_k[s2]
                c3 = py_first_and_last[0]
                qm = c1 + c2 + c3
                full_code_list.append((de_comp_char, qm))
                full_code_dict[de_comp_char] = qm
            elif s1:
                c1 = component_k[s1]
                c2 = component_k[self.stroke_zm[self.stroke_char[de_comp_char][0]]]
                c3 = py_first_and_last[0]
                qm = c1 + c2 + c3
                full_code_list.append((de_comp_char, qm))
                full_code_dict[de_comp_char] = qm
        return full_code_list, full_code_dict

    def build_ci_by_full_code(self, full_code_map):
        """
        构建词
        """
        cybm = []
        for cp in self.tl:
            ci = cp[0]
            lc = len(ci)
            if lc == 2:
                # 一个字取两码：A1a1B1b1
                cybm.append((full_code_map[ci[0]][:2] + full_code_map[ci[1]][:2], int(cp[1])))
            elif lc == 3:
                # 每个字取首码
                # cybm[ci] = full_code_map[ci[0]][0] + full_code_map[ci[1]][0] + full_code_map[ci[2]][0]
                cybm.append((full_code_map[ci[0]][0] + full_code_map[ci[1]][0] + full_code_map[ci[2]][0], int(cp[1])))
                # 3字词是前两字第一码 + 第三字前两码 cybm.append((full_code_map[ci[0]][0] + full_code_map[ci[1]][0] + full_code_map[
                # ci[2]][:2], int(cp[1])))
            elif lc == 4:
                cybm.append((full_code_map[ci[0]][0] + full_code_map[ci[1]][0] + full_code_map[ci[2]][0] +
                             full_code_map[ci[3]][0], int(cp[1])))
            elif lc > 4:
                cybm.append((full_code_map[ci[0]][0] + full_code_map[ci[1]][0] + full_code_map[ci[2]][0] +
                             full_code_map[ci[-1]][0], int(cp[1])))
        # for char, code in full_code:
        return cybm

    def zu_ci(self, full_code_map):
        ci_map = {}
        for cp in self.tl:
            ci = cp[0]
            lc = len(ci)
            if lc == 2:
                # 一个字取两码：A1a1B1b1
                ci_map[ci] = full_code_map[ci[0]][:2] + full_code_map[ci[1]][:2]
            elif lc == 3:
                # 每个字取首码
                ci_map[ci] = full_code_map[ci[0]][0] + full_code_map[ci[1]][0] + full_code_map[ci[2]][0]
                # 3字词是前两字第一码 + 第三字前两码
                # ci_map[ci] = full_code_map[ci[0]][0] + full_code_map[ci[1]][0] + full_code_map[ci[2]][:2]
            elif lc == 4:
                ci_map[ci] = full_code_map[ci[0]][0] + full_code_map[ci[1]][0] + full_code_map[ci[2]][0] + \
                             full_code_map[ci[3]][0]
            elif lc > 4:
                ci_map[ci] = full_code_map[ci[0]][0] + full_code_map[ci[1]][0] + full_code_map[ci[2]][0] + \
                             full_code_map[ci[-1]][0]
        # for char, code in full_code:
        return ci_map
