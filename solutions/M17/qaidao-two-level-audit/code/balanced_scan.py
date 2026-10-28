"""母空间计数平衡扫描：ads(13 占据, 29 虚) 对 MOF(11 占据, k 虚) + CO2(2 占据, 29−k 虚)。

用法：python -I balanced_scan.py <作者仓库根目录> <脚本目录> <输出 json>
"""
import json
import sys

sys.path.insert(0, sys.argv[2])
import m17_two_level as M  # noqa: E402

root = sys.argv[1]
d = f'{root}/fullci_reference_pyscf/singlet'
mof = M.load_fcidump(f'{d}/FCIDUMP.MOF', 142)
co2 = M.load_fcidump(f'{d}/FCIDUMP.CO2', 0)
ads = M.load_fcidump(f'{d}/FCIDUMP.MOFCO2', 148)
e_ads = M.run_cc(ads[0], ads[1], 13)
rows = []
for km in range(11, 30):
    kc = 29 - km
    if kc > 18 or kc < 1:
        continue
    h, g = mof[0][:11 + km, :11 + km], mof[1][:11 + km, :11 + km, :11 + km, :11 + km]
    em = M.run_cc(h, g, 11)
    sub = [6, 7] + list(range(8, 8 + kc))
    hc, gc = M.embed(co2[0], co2[1], sub, [0, 1, 2, 3, 4, 5])
    ec = M.run_cc(hc, gc, 2)
    row = dict(MOF_virtual=km, CO2_virtual=kc,
               **{f'D_{m}': M.assemble({'MOF': em[m], 'CO2': ec[m], 'MOFCO2': e_ads[m]}) for m in ('MP2', 'CCSD', 'CCSD_T')})
    rows.append(row)
    print(row, flush=True)
json.dump(rows, open(sys.argv[3], 'w'), indent=1)
