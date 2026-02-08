# ============================================
# Walk-forward phase forecast with hardened nulls
# Target: 8–12 day band
# Surrogates: 2000 (target), 1000 (controls)
# ============================================

import numpy as np
import pandas as pd
from numpy.fft import rfft, irfft, rfftfreq
from scipy.signal import hilbert

# ---------- FILE PATHS ----------
paths = {
    "NIST": "circularT_NIST_extracted.csv",
    "PTB": "circularT_PTB_extracted.csv",
    "NICT": "circularT_NICT_extracted.csv",
    "VSL": "circularT_VSL_extracted.csv",
}

# ---------- LOAD ----------
def load_lab(path):
    df = pd.read_csv(path)
    return (df[["mjd","value_ns"]]
            .dropna()
            .sort_values("mjd")
            .groupby("mjd",as_index=False)["value_ns"].mean())

labs = {k: load_lab(v) for k,v in paths.items()}

# ---------- HELPERS ----------
fs = 1.0
eps = 1e-12
H = 30
W = 730

def detrend(x):
    t = np.arange(len(x))
    A = np.vstack([t, np.ones_like(t)]).T
    c,_ ,_,_ = np.linalg.lstsq(A,x,rcond=None)
    return x - (A@c)

def align(A,B):
    m0 = int(np.ceil(max(A.mjd.min(),B.mjd.min())))
    m1 = int(np.floor(min(A.mjd.max(),B.mjd.max())))
    g = np.arange(m0,m1+1)
    a = np.interp(g,A.mjd,A.value_ns)
    b = np.interp(g,B.mjd,B.value_ns)
    return detrend(a), detrend(b)

def band_mask(n,flo,fhi):
    f = rfftfreq(n,d=1/fs)
    return (f>=flo)&(f<=fhi)

def analytic_from_band(Xmask,n):
    F = np.zeros(n,dtype=complex)
    nh = len(Xmask)-1
    F[0]=Xmask[0]
    if n%2==0:
        F[nh]=Xmask[nh]
        F[1:nh]=2*Xmask[1:nh]
    else:
        F[1:nh+1]=2*Xmask[1:nh+1]
    return ifft(F)

def phasor(zA,zB):
    u = zA*np.conj(zB)
    return u/(np.abs(u)+eps)

def walk_skill(u):
    prod = u[H:]*np.conj(u[:-H])
    ts = np.arange(W,len(u)-H)
    preds=[]; trues=[]
    for t in ts:
        a = np.mean(prod[t-W:t-H+1])
        preds.append(a*u[t])
        trues.append(u[t+H])
    preds=np.array(preds); trues=np.array(trues)
    return float(np.mean(np.real(preds*np.conj(trues))))

def surrogate(XB,mask,rng):
    ph = np.angle(XB)
    ph[mask]=rng.uniform(0,2*np.pi,mask.sum())
    return np.abs(XB)*np.exp(1j*ph)

# ---------- RUN ----------
pairs = [("NIST","PTB"),("NIST","NICT"),("PTB","VSL")]
bands = [
    ("target_8_12d",1/12,1/8,2000),
    ("ctrl_low",0.05,0.07,1000),
    ("ctrl_high",0.13,0.15,1000)
]

rng = np.random.default_rng(0)
rows=[]

for Aname,Bname in pairs:
    A,B = align(labs[Aname],labs[Bname])
    n=len(B)
    XA=rfft(A)
    XB=rfft(B)

    for tag,flo,fhi,Ns in bands:
        mask = band_mask(n,flo,fhi)

        zA = hilbert(irfft(XA*mask,n))
        zB = hilbert(irfft(XB*mask,n))
        u = phasor(zA,zB)

        real = walk_skill(u)

        null=[]
        for i in range(Ns):
            XBn = surrogate(XB,mask,rng)
            zBs = hilbert(irfft(XBn*mask,n))
            us = phasor(zA,zBs)
            null.append(walk_skill(us))

        null=np.array(null)
        p = (np.sum(null>=real)+1)/(Ns+1)

        rows.append({
            "pair":f"{Aname}-{Bname}",
            "band":tag,
            "real_skill":real,
            "null_mean":null.mean(),
            "null_95":np.quantile(null,0.95),
            "p_value":p,
            "surrogates":Ns
        })

df = pd.DataFrame(rows)
print(df)
df.to_csv("final_results.csv",index=False)

print("\nSaved: final_results.csv")


