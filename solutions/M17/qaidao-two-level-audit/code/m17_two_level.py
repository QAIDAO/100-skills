"""M17 示例解法：Fe-MOF-74 + CO2 两级活性空间的吸附能与截断误差。

输入全部来自 qcware/quantum_simulation_MOF @ ad3c6658：
  fullci_reference_pyscf/singlet/FCIDUMP.{CO2,MOF,MOFCO2}   母空间积分
  active_space_generation_vasp/*/OUTCAR.mp2                  NO 阈值阶梯的 VASP MP2
  {Fe,Mg}-MOF-74-vasp/*/*/OUTCAR                             周期 DFT

用法：python -I m17_two_level.py <作者仓库根目录> <输出 results.json>
"""

import json
import re
import sys
import time
from pathlib import Path

import numpy as np
from pyscf import ao2mo, cc, fci, gto, mp, scf

HARTREE_KJ = 2625.4996394798254
EV_KJ = 96.48533212331002
CHEM_ACC = 1.6e-3  # Ha, 化学精度
D_HF_PERIODIC = 17.989924633748213  # kJ/mol，作者 320 eV Γ 点周期 HF（OUTCAR.HF 末步）；420 eV 的值由 vasp_mp2_ladder 另取

# 作者 reducedactive_*.py 中的轨道编号（1 起，母空间编号）
SYSTEMS = {
    'CO2': dict(nfreeze=0, occ=[7, 8], vir=[9, 10]),
    'MOF': dict(nfreeze=142, occ=[7, 8, 9, 10, 11], vir=[12, 13, 14, 15, 16]),
    'MOFCO2': dict(nfreeze=148, occ=[4, 6, 9, 10, 11, 12, 13], vir=[14, 15, 16, 17, 18, 19, 20]),
}
# 作者 reducedactive_*.py 文档串记录的 FCI 总能量，用来验证截取方式
AUTHOR_REDUCED_FCI = {'CO2': -25.762038672940832, 'MOF': -55.274521861916455, 'MOFCO2': -74.70598652625871}
# 本库现有参照（m17-followup/results/final-results.json）中原固定参数 QNP 的相关能
QNP_CORR = {'CO2': -0.04628598789909688, 'MOF': -2.4124948408999884, 'MOFCO2': -2.468420928412229}


def load_fcidump(path, nfreeze):
    with open(path) as f:
        head = f.readline() + f.readline()
        data = np.loadtxt(f)
    norb = int(re.search(r'NORB=\s*(\d+)', head).group(1))
    nelec = int(re.search(r'NELEC=\s*(\d+)', head).group(1)) - 2 * nfreeze
    val, idx = data[:, 0], data[:, 1:].astype(int)
    h1, eri = np.zeros((norb, norb)), np.zeros((norb,) * 4)
    two = idx[:, 2] != 0
    i, j, k, l = (idx[two] - 1).T
    for a, b, c, d in ((i, j, k, l), (j, i, k, l), (i, j, l, k), (j, i, l, k),
                       (k, l, i, j), (l, k, i, j), (k, l, j, i), (l, k, j, i)):
        eri[a, b, c, d] = val[two]
    one = (~two) & (idx[:, 1] != 0)
    i, j = (idx[one, :2] - 1).T
    h1[i, j] = h1[j, i] = val[one]
    return h1, eri, nelec


def embed(h1, eri, active, core):
    """取 active 子块，并把 core 中双占据轨道的平均场加进单体项。"""
    a, c = np.asarray(active), np.asarray(core, dtype=int)
    h = h1[np.ix_(a, a)].copy()
    if len(c):
        h += 2 * np.einsum('pqcc->pq', eri[np.ix_(a, a, c, c)]) - np.einsum('pccq->pq', eri[np.ix_(a, c, c, a)])
    return h, eri[np.ix_(a, a, a, a)].copy()


def hf_energy(h, g, nocc):
    o = slice(0, nocc)
    return 2 * np.trace(h[o, o]) + 2 * np.einsum('iijj', g[o, o, o, o]) - np.einsum('ijji', g[o, o, o, o])


def fock(h, g, nocc):
    return h + 2 * np.einsum('pqii->pq', g[:, :, :nocc, :nocc]) - np.einsum('piiq->pq', g[:, :nocc, :nocc, :])


def fake_rhf(h, g, nocc):
    n = h.shape[0]
    mol = gto.M(verbose=0)
    mol.nelectron, mol.incore_anyway = 2 * nocc, True
    mf = scf.RHF(mol)
    mf.get_hcore = lambda *a: h
    mf.get_ovlp = lambda *a: np.eye(n)
    mf.energy_nuc = lambda *a: 0.0
    mf._eri = ao2mo.restore(8, g, n)
    mf.mo_coeff = np.eye(n)
    mf.mo_occ = np.array([2.0] * nocc + [0.0] * (n - nocc))
    mf.mo_energy = np.diag(fock(h, g, nocc))
    mf.e_tot = hf_energy(h, g, nocc)
    mf.converged = True
    return mf


def run_cc(h, g, nocc):
    t0 = time.process_time()
    mf = fake_rhf(h, g, nocc)
    e_mp2 = mp.MP2(mf).kernel()[0]
    mycc = cc.CCSD(mf)
    mycc.conv_tol, mycc.max_cycle = 1e-9, 200
    mycc.kernel()
    e_t = mycc.ccsd_t()
    return dict(MP2=e_mp2, CCSD=mycc.e_corr, CCSD_T=mycc.e_corr + e_t,
                ccsd_converged=bool(mycc.converged), t1_diag=float(np.sqrt(np.sum(mycc.t1 ** 2) / (2 * nocc))),
                cpu_s=time.process_time() - t0)


def run_fci(h, g, nocc):
    t0 = time.process_time()
    n = h.shape[0]
    solver = fci.direct_spin1.FCI()
    solver.conv_tol, solver.max_cycle, solver.max_space = 1e-10, 300, 12
    e, civec = solver.kernel(h, g, n, (nocc, nocc))
    s2, _ = solver.spin_square(civec, n, (nocc, nocc))
    return dict(E=e, hf_overlap2=float(civec[0, 0] ** 2), S2=float(s2), converged=bool(solver.converged),
                cpu_s=time.process_time() - t0)


def pauli_l1(h, g):
    """JW 下（任何 Pauli 映射同值）去掉恒等项后的 Pauli 系数 1-范数（Koridon 等 2021 的空间轨道式）。"""
    ht = h - 0.5 * np.einsum('prrq->pq', g) + np.einsum('pqrr->pq', g)
    n = h.shape[0]
    p, q, r, s = np.ogrid[:n, :n, :n, :n]
    anti = g - g.transpose(0, 3, 2, 1)
    mask = (p > r) & (s > q)
    return float(np.abs(ht).sum() + 0.5 * np.abs(anti[np.broadcast_to(mask, g.shape)]).sum() + 0.25 * np.abs(g).sum())


def kj(x):
    return float(x * HARTREE_KJ)


def assemble(corr):
    """D = D_HF,periodic + (Ec_MOF + Ec_CO2 − Ec_ads)；正值为有利结合，E_ads = −D。"""
    return D_HF_PERIODIC + kj(corr['MOF'] + corr['CO2'] - corr['MOFCO2'])


def vasp_mp2_ladder(root):
    out = {}
    for d in sorted((root / 'active_space_generation_vasp').iterdir()):
        m = re.match(r'(CO2|MOF|MOFCO2)_ENCUT(\d+)_Natural-Orbital-thr10-(\d)', d.name)
        if not m or not (d / 'OUTCAR.mp2').is_file():
            continue
        text = (d / 'OUTCAR.mp2').read_text(errors='replace')
        e = float(re.findall(r'MP2 correlation energy:\s*(-?\d+\.\d+)', text)[-1])
        nb = int(re.search(r'NBANDS=\s*(\d+)', text).group(1))
        out.setdefault((m.group(2), m.group(3)), {})[m.group(1)] = dict(E_eV=e, NBANDS=nb, HF_eV=last_toten(d / 'OUTCAR.HF'))
    rows = []
    for (encut, thr), v in sorted(out.items()):
        if len(v) == 3:
            dcorr = (v['MOF']['E_eV'] + v['CO2']['E_eV'] - v['MOFCO2']['E_eV']) * EV_KJ
            d_hf = (v['MOF']['HF_eV'] + v['CO2']['HF_eV'] - v['MOFCO2']['HF_eV']) * EV_KJ
            rows.append(dict(ENCUT_eV=int(encut), NO_threshold=f'1e-{thr}', NBANDS={k: v[k]['NBANDS'] for k in v},
                             D_HF_kJ=d_hf, corr_binding_kJ=dcorr, D_kJ=d_hf + dcorr))
    return rows


def last_toten(path):
    vals = re.findall(r'free  energy   TOTEN\s*=\s*(-?\d+\.\d+)', path.read_text(errors='replace'))
    return float(vals[-1])


def dft_table(root):
    rows = []
    for metal in ('Fe', 'Mg'):
        base = root / f'{metal}-MOF-74-vasp'
        for xc in sorted(p.name for p in base.iterdir() if p.is_dir()):
            names = {p.name for p in (base / xc).iterdir() if p.is_dir()}
            pick = {}
            for key, cands in (('CO2', ['CO2']), ('MOF', ['MOF_restart', 'MOF']),
                               ('MOFCO2', ['MOFCO2_relax_restart', 'MOFCO2_restart', 'MOFCO2_relax', 'MOFCO2'])):
                hit = next((c for c in cands if c in names), None)
                if hit:
                    pick[key] = hit
            if len(pick) < 3:
                continue
            e = {k: last_toten(base / xc / v / 'OUTCAR') for k, v in pick.items()}
            rows.append(dict(metal=metal, functional=xc, dirs=pick,
                             E_ads_kJ=(e['MOFCO2'] - e['MOF'] - e['CO2']) * EV_KJ))
    return rows


def main():
    root, out_path = Path(sys.argv[1]), Path(sys.argv[2])
    parent_dir = root / 'fullci_reference_pyscf' / 'singlet'
    res = dict(inputs={}, systems={}, binding={}, notes=[])
    for name, spec in SYSTEMS.items():
        h1, eri, nelec = load_fcidump(parent_dir / f'FCIDUMP.{name}', spec['nfreeze'])
        nocc, norb = nelec // 2, h1.shape[0]
        occ = [i - 1 for i in spec['occ']]
        act = occ + [i - 1 for i in spec['vir']]
        core = [i for i in range(nocc) if i not in occ]
        r = dict(parent=dict(norb=norb, nelec=nelec, qubits=2 * norb), occ_correlated_in_reduced=spec['occ'],
                 occ_meanfield_only_in_reduced=[i + 1 for i in core])
        e_hf_parent = hf_energy(h1, eri, nocc)
        F = fock(h1, eri, nocc)
        r['parent']['E_HF'] = e_hf_parent
        r['parent']['max_abs_F_ov'] = float(np.abs(F[:nocc, nocc:]).max())

        # 第一级 a：作者原样子块（不含 core 平均场），QNP/SQD 所用的 H
        ha, ga = h1[np.ix_(act, act)], eri[np.ix_(act, act, act, act)]
        na = len(occ)
        fa = run_fci(ha, ga, na)
        fa['E_HF_fixed_occ'] = hf_energy(ha, ga, na)
        fa['E_corr'] = fa['E'] - fa['E_HF_fixed_occ']
        fa['author_E_FCI'] = AUTHOR_REDUCED_FCI[name]
        fa['delta_vs_author'] = fa['E'] - AUTHOR_REDUCED_FCI[name]
        fa['pauli_l1'] = pauli_l1(ha, ga)
        fa['qubits'] = 2 * len(act)
        # 子块里固定占据的"HF"是否为自洽解：跑一次真正 SCF 比较
        mfa = fake_rhf(ha, ga, na)
        mfa.max_cycle, mfa.conv_tol = 200, 1e-10
        dm0 = mfa.make_rdm1(np.eye(len(act)), mfa.mo_occ)
        mfa.kernel(dm0)
        fa['E_RHF_selfconsistent'] = float(mfa.e_tot)
        fa['QNP_corr_cited'] = QNP_CORR[name]
        r['level1a_published_subblock'] = fa

        # 第一级 b：同一组轨道、同样比特数，补上 core 平均场（标准冻结芯 CAS）
        hb, gb = embed(h1, eri, act, core)
        fb = run_fci(hb, gb, na)
        fb['E_HF'] = hf_energy(hb, gb, na)
        fb['E_corr'] = fb['E'] - fb['E_HF']
        fb.update({f'cc_{k}': v for k, v in run_cc(hb, gb, na).items()})
        fb['pauli_l1'] = pauli_l1(hb, gb)
        fb['qubits'] = 2 * len(act)
        r['level1b_frozen_core_cas'] = fb

        # 第二级：母空间（作者原样）与虚轨道阶梯
        r['level2_parent'] = run_cc(h1, eri, nocc)
        r['level2_parent']['pauli_l1'] = pauli_l1(h1, eri)
        ladder = []
        nvir = norb - nocc
        for kv in sorted({5, 10, 15, 20, nvir}):
            if kv > nvir:
                continue
            sub = list(range(nocc + kv))
            hh, gg = h1[np.ix_(sub, sub)], eri[np.ix_(sub, sub, sub, sub)]
            ladder.append(dict(n_virtual=kv, **run_cc(hh, gg, nocc)))
        r['level2_virtual_ladder'] = ladder

        # CO2 的平衡版本：只关联 ads 中多出的两个占据轨道（7、8），其余占据只给平均场
        if name == 'CO2':
            keep = occ + list(range(nocc, norb))
            hc, gc = embed(h1, eri, keep, core)
            bal = run_cc(hc, gc, na)
            bal['space'] = f'{2 * na}e{len(keep)}o'
            bal['pauli_l1'] = pauli_l1(hc, gc)
            r['level2_balanced_CO2'] = bal
            bl = []
            for kv in sorted({5, 10, 15, nvir}):
                sub = occ + list(range(nocc, nocc + kv))
                hh, gg = embed(h1, eri, sub, core)
                bl.append(dict(n_virtual=kv, **run_cc(hh, gg, na)))
            r['level2_balanced_CO2_ladder'] = bl
        res['systems'][name] = r
        print(name, 'done', flush=True)

    S = res['systems']
    b = res['binding']
    b['level1a_FCI'] = assemble({k: S[k]['level1a_published_subblock']['E_corr'] for k in S})
    b['level1a_QNP'] = assemble(QNP_CORR)
    b['level1b_FCI'] = assemble({k: S[k]['level1b_frozen_core_cas']['E_corr'] for k in S})
    for m in ('MP2', 'CCSD', 'CCSD_T'):
        b[f'level1b_{m}'] = assemble({k: S[k]['level1b_frozen_core_cas'][f'cc_{m}'] for k in S})
        b[f'level2_published_{m}'] = assemble({k: S[k]['level2_parent'][m] for k in S})
        b[f'level2_balanced_{m}'] = assemble({'CO2': S['CO2']['level2_balanced_CO2'][m],
                                              'MOF': S['MOF']['level2_parent'][m],
                                              'MOFCO2': S['MOFCO2']['level2_parent'][m]})
    # 虚轨道阶梯：三体系取相同虚轨道数（CO2 不足时取其全部）
    lad = []
    for kv in (5, 10, 15, 20, 29):
        row = {}
        for k in ('MOF', 'MOFCO2'):
            hit = [x for x in S[k]['level2_virtual_ladder'] if x['n_virtual'] == kv]
            row[k] = hit[0] if hit else None
        bl = S['CO2']['level2_balanced_CO2_ladder']
        co2 = max((x for x in bl if x['n_virtual'] <= kv), key=lambda x: x['n_virtual'])
        if row['MOF'] and row['MOFCO2']:
            lad.append(dict(n_virtual=kv, CO2_n_virtual=co2['n_virtual'],
                            **{f'D_{m}': assemble({'CO2': co2[m], 'MOF': row['MOF'][m], 'MOFCO2': row['MOFCO2'][m]})
                               for m in ('MP2', 'CCSD', 'CCSD_T')}))
    b['level2_balanced_virtual_ladder'] = lad
    res['vasp_mp2_no_ladder'] = vasp_mp2_ladder(root)
    res['dft'] = dft_table(root)
    res['constants'] = dict(D_HF_periodic_kJ=D_HF_PERIODIC, Hartree_kJ=HARTREE_KJ, eV_kJ=EV_KJ, chem_acc_Ha=CHEM_ACC)
    for name in S:
        res['inputs'][f'FCIDUMP.{name}'] = None
    out_path.write_text(json.dumps(res, ensure_ascii=False, indent=2))
    print(json.dumps(b, indent=1))


if __name__ == '__main__':
    main()
