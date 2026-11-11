import json, numpy as np
from scipy import stats
r=lambda x,d=4: None if not np.isfinite(x) else round(float(x),d)
Z=[[r(stats.norm.cdf(i/10+j/100)) for j in range(10)] for i in range(35)]
tdf=list(range(1,31))+[40,60,120,"inf"]
ta=[0.10,0.05,0.025,0.01,0.005]
T=[[r(stats.norm.isf(a) if d=="inf" else stats.t.isf(a,d),3) for a in ta] for d in tdf]
cdf_=list(range(1,31))+[40,50,60,80,100]
ca=[0.995,0.99,0.975,0.95,0.90,0.10,0.05,0.025,0.01,0.005]
C=[[r(stats.chi2.isf(a,d),3) for a in ca] for d in cdf_]
f1=[1,2,3,4,5,6,7,8,9,10,12,15,20,"inf"]; f2=list(range(1,31))+[40,60,120,"inf"]
fa=[0.10,0.05,0.025,0.01]
def fq(a,d1,d2):
    if d1=="inf" and d2=="inf": return 1.0
    if d1=="inf": return d2/stats.chi2.ppf(a,d2)   # F(inf,d2) upper = d2/chi2_lower
    if d2=="inf": return stats.chi2.isf(a,d1)/d1
    return stats.f.isf(a,d1,d2)
F={str(a):[[r(fq(a,d1,d2),2 if fq(a,d1,d2)<100 else 1) for d1 in f1] for d2 in f2] for a in fa}
bn=[5,10,15,20]; bp=[0.05,0.10,0.20,0.25,0.30,0.40,0.50]
B={str(n):[[r(stats.binom.cdf(k,n,p)) for p in bp] for k in range(n+1)] for n in bn}
pl=[0.5,1,1.5,2,2.5,3,4,5,6,7,8,9,10]
P=[[r(stats.poisson.cdf(k,l)) for l in pl] for k in range(21)]
D=dict(Z=Z,T=dict(df=tdf,a=ta,v=T),C=dict(df=cdf_,a=ca,v=C),F=dict(d1=f1,d2=f2,a=fa,v=F),B=dict(n=bn,p=bp,v=B),P=dict(l=pl,v=P))
open("data.json","w").write(json.dumps(D,separators=(",",":")))
# checks
print(stats.t.isf(.025,10),stats.chi2.isf(.05,10),stats.f.isf(.05,5,10),stats.norm.cdf(1.96))
print("power n=20",stats.norm.cdf(.5*np.sqrt(20)-1.96)+stats.norm.cdf(-.5*np.sqrt(20)-1.96))
print("power n=60",stats.norm.cdf(.5*np.sqrt(60)-1.96)+stats.norm.cdf(-.5*np.sqrt(60)-1.96))
print("n80",((1.959964+0.841621)/.5)**2)
print("CI",52-1.96*2,52+1.96*2, "F lower", 1/stats.f.isf(.05,10,5), stats.f.ppf(.05,5,10))
print(len(open('data.json').read()))
