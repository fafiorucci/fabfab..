"""Flusso potenziale attorno a profili di Joukowski (con condizione di Kutta): linee di corrente,
pressioni sulla superficie e tempi di percorrenza. Scrive flow_lines.json per i disegni dell'appendice M.
Serve numpy e matplotlib solo per rigenerare il JSON."""
import json, math, os
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def case(mu, alpha_deg, nlev=15, span=1.7, xlim=3.4):
    a = math.radians(alpha_deg); U = 1.0
    R = abs(1 - mu)
    # Kutta: velocità nulla in zeta = 1 (bordo d'uscita)
    A = U * (np.exp(-1j*a) - R**2*np.exp(1j*a)/(1-mu)**2); B = 1j/(2*np.pi*(1-mu))
    # dw = A + G*B = 0 con G reale: risolvo sul componente appropriato
    G = -A.imag/B.imag if abs(B.imag) > 1e-12 else -A.real/B.real
    def w(zeta):
        s = zeta - mu
        return U*(s*np.exp(-1j*a) + R**2*np.exp(1j*a)/s) + 1j*G/(2*np.pi)*np.log(s)
    def dw(zeta):
        s = zeta - mu
        return U*(np.exp(-1j*a) - R**2*np.exp(1j*a)/s**2) + 1j*G/(2*np.pi*s)
    J = lambda zeta: zeta + 1/zeta
    dJ = lambda zeta: 1 - 1/zeta**2
    # rotazione: la corrente libera diventa orizzontale
    rot = np.exp(-1j*a)
    th = np.linspace(0, 2*np.pi, 721)
    surf = mu + R*np.exp(1j*th)
    zs = J(surf)*rot
    # griglia polare
    r = np.concatenate([np.linspace(R*1.0005, R*3, 260), np.linspace(R*3.02, R*14, 240)])
    TT, RR = np.meshgrid(th, r)
    ZE = mu + RR*np.exp(1j*TT)
    psi = np.imag(w(ZE))
    ZZ = J(ZE)*rot
    psi0 = float(np.imag(w(np.array([1+0j]))[0]))
    lev = [psi0 + k*span/((nlev-1)/2) for k in range(-(nlev//2), nlev//2+1)]
    cs = plt.contour(TT, RR, psi, levels=sorted(lev))
    lines = []
    for segs, L in zip(cs.allsegs, cs.levels):
        for seg in segs:
            if len(seg) < 5: continue
            zeta = mu + seg[:, 1]*np.exp(1j*seg[:, 0])
            z = J(zeta)*rot
            m = (np.abs(z.real) < xlim) & (np.abs(z.imag) < 2.0)
            z = z[m]; zeta = zeta[m]
            if len(z) < 5: continue
            # velocità locale e tempi
            V = np.abs(dw(zeta)/dJ(zeta))
            order = np.argsort(z.real)
            z = z[order]; V = V[order]
            ds = np.abs(np.diff(z)); t = np.concatenate([[0], np.cumsum(ds/np.maximum((V[1:]+V[:-1])/2, 1e-3))])
            lines.append({'lev': float(L-psi0), 'pts': [[round(float(p.real), 4), round(float(p.imag), 4)] for p in z],
                          't': [round(float(x), 4) for x in t]})
    plt.close('all')
    # pressioni sulla superficie
    Vs = np.abs(dw(surf)/dJ(surf))
    Vs[np.isnan(Vs)] = 0
    Cp = 1 - Vs**2
    # normali esterne
    dz = np.gradient(zs)
    n = -1j*dz/np.abs(dz)
    # orientazione: la normale deve puntare fuori dal profilo
    c = zs.mean()
    if np.mean(np.real(np.conj(n)*(zs-c))) < 0: n = -n
    surface = [[round(float(p.real), 4), round(float(p.imag), 4), round(float(cp), 3), round(float(q.real), 4), round(float(q.imag), 4)]
               for p, cp, q in zip(zs, Cp, n)]
    return {'mu': [mu.real, mu.imag], 'alpha': alpha_deg, 'Gamma': float(G), 'lines': lines, 'surface': surface[::6]}

if __name__ == '__main__':
    out = {
        'profilo': case(-0.09+0.10j, 7),
        'lastra': case(0j + 1e-6, 10, span=1.6),
        'vela': case(0.20j, 6, span=1.6),
        'profilo0': case(-0.09+0.10j, 0),
        'chiglia': case(-0.09+0j, 5),
    }
    here = os.path.dirname(os.path.abspath(__file__))
    json.dump(out, open(os.path.join(here, 'flow_lines.json'), 'w'), separators=(',', ':'))
    for k, v in out.items():
        print(k, len(v['lines']), 'linee', 'Gamma=%.3f' % v['Gamma'])
