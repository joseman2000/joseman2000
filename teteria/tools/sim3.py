import math,sys
sys.argv=['x','1e6','0','1','1','5']
from sim2 import runp
R0=1e6
def L(S): # niveles comprables gastando S en coste 3*1.5^L
    l=0;c=3
    while S>=c:S-=c;l+=1;c=3*1.5**l
    return l
def mult(S): return 1+0.30*L(S)
def campaign(cost,wm=1,label=""):
    S=0;T=0;k=0;rows=[]
    while S<cost and k<60:
        target=max(5,int(S*0.5))
        t,s,fu=runp(mult(S)*wm,R0,lambda s,t: s>=target and t>600,limit=4*3600)
        k+=1;S+=s;T+=t;rows.append((k,t/60,s,S,T/3600,fu/60 if fu else -1,mult(S)))
    return rows
for r in campaign(float(sys.argv[1]) if False else 400):
    print("run%d %6.1f min +%d  tot %d  acum %.1f h  renacer@%.0f min mult x%.2f"%r)
