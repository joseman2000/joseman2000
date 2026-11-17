import math,sys
from sim import B,G
def runp(mult,R0,stopfn,clicks=4,dt=2.0,limit=6*3600,startbonus=0):
    n=[0]*8;leaves=startbonus;total=0;t=0;first_unlock=None
    while t<limit:
        c=sum(n[i]*B[i][1]*2**(n[i]//25) for i in range(8))*mult
        g=(c+clicks*mult*(1+c*0.01))*dt   # clicks scale with 1% cps (upgrade)
        leaves+=g;total+=g;t+=dt
        while True:
            best=min(((B[i][0]*G**n[i])/(B[i][1]),i) for i in range(8))
            i=best[1];cost=B[i][0]*G**n[i]
            if leaves>=cost:leaves-=cost;n[i]+=1
            else:break
        s=math.floor(math.sqrt(total/R0))
        if s>=1 and first_unlock is None:first_unlock=t
        if stopfn(s,t):break
    return t,math.floor(math.sqrt(total/R0)),first_unlock
R0=float(sys.argv[1]); per=float(sys.argv[2]); cost=float(sys.argv[3]); wm=float(sys.argv[4]) if len(sys.argv)>4 else 1
S=0;T=0;k=0
while S<cost and k<40:
    mult=(1+per*S)*wm
    target=max(int(sys.argv[5]),S) # prestige when gain >= current seeds (doubling)
    t,s,fu=runp(mult,R0,lambda s,t: s>=target and t>600)
    k+=1;S+=s;T+=t
    print(f"run{k}: {t/60:6.1f} min  +{s} semillas  total {S}  acumulado {T/3600:5.1f} h  renacer disp. a {fu/60 if fu else -1:.0f} min")
