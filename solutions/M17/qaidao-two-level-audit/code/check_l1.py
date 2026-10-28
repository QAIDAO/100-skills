"""用显式 Jordan–Wigner 展开核对 pauli_l1 公式，并核对子块 FCI 与作者文档串一致。"""
import sys

import numpy as np
from qiskit.quantum_info import SparsePauliOp

sys.path.insert(0, sys.argv[2])
import m17_two_level as M  # noqa: E402


def annihilator(j, nq):
    z = 'Z' * j
    lab = lambda c: ('I' * (nq - j - 1) + c + z)
    return SparsePauliOp([lab('X'), lab('Y')], [0.5, 0.5j])


def jw_hamiltonian(h, g):
    n = h.shape[0]
    nq = 2 * n
    a = [annihilator(j, nq) for j in range(nq)]
    ad = [x.adjoint() for x in a]
    so = lambda p, s: 2 * p + s
    H = SparsePauliOp(['I' * nq], [0.0])
    for p in range(n):
        for q in range(n):
            for s in range(2):
                if abs(h[p, q]) > 1e-14:
                    H += h[p, q] * (ad[so(p, s)] @ a[so(q, s)])
    for p in range(n):
        for q in range(n):
            for r in range(n):
                for t in range(n):
                    v = g[p, q, r, t]
                    if abs(v) < 1e-14:
                        continue
                    for s in range(2):
                        for u in range(2):
                            if so(p, s) == so(r, u) or so(q, s) == so(t, u):
                                continue
                            H += 0.5 * v * (ad[so(p, s)] @ ad[so(r, u)] @ a[so(t, u)] @ a[so(q, s)])
    return H.simplify(atol=1e-12)


root = sys.argv[1]
h1, eri, nelec = M.load_fcidump(f'{root}/fullci_reference_pyscf/singlet/FCIDUMP.CO2', 0)
act = [6, 7, 8, 9]
for label, (h, g) in {'subblock': (h1[np.ix_(act, act)], eri[np.ix_(act, act, act, act)]),
                      'embedded': M.embed(h1, eri, act, [0, 1, 2, 3, 4, 5])}.items():
    H = jw_hamiltonian(h, g)
    coeffs = {lab: c for lab, c in zip(H.paulis.to_labels(), H.coeffs)}
    ident = coeffs.pop('I' * 8, 0)
    l1 = sum(abs(c) for c in coeffs.values())
    print(label, 'explicit JW l1', l1, 'formula', M.pauli_l1(h, g), 'n_terms', len(coeffs),
          'max imag', max(abs(c.imag) for c in H.coeffs))
    w = np.linalg.eigvalsh(H.to_matrix())
    print('  lowest eig (all sectors)', w[0])
f = M.run_fci(h1[np.ix_(act, act)], eri[np.ix_(act, act, act, act)], 2)
print('subblock FCI', f['E'], 'author', M.AUTHOR_REDUCED_FCI['CO2'])
