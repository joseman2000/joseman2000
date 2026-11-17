import math
B=[(15,.1),(100,1),(1100,8),(12000,47),(130000,260),(1.4e6,1400),(2e7,7800),(3.3e8,44000)]
G=1.15
def run(mult=1.0,seedmult=1.0,clicks=4,R0=1e9,stop_seeds=None,dt=1.0,limit=4*3600*3):
    n=[0]*8; leaves=0;total=0;t=0;mil={}
    def cps():
        s=0
        for i,(c,p) in enumerate(B):
            m=2**(n[i]//25)  # upgrades x2 per 25 owned
            s+=n[i]*p*m
        return s*mult
    while t<limit:
        c=cps()
        g=(c+clicks*(1+0.02*sum(n)**0.5)*mult)*dt
        leaves+=g;total+=g;t+=dt
        # greedy: best payback
        while True:
            best=None
            for i,(bc,p) in enumerate(B):
                cost=bc*G**n[i]
                pb=cost/(p*mult*(2 if (n[i]+1)%25==0 else 1)+1e-9)
                if best is None or pb<best[0]:best=(pb,i,cost)
            if leaves>=best[2]:
                leaves-=best[2];n[best[1]]+=1
            else:break
        for k,th in [("1e6",1e6),("1e8",1e8),("1e9",1e9),("1e10",1e10),("1e11",1e11),("1e12",1e12)]:
            if total>=th and k not in mil:mil[k]=t/60
    return mil,total,n
m,tot,n=run()
print({k:round(v,1) for k,v in m.items()},tot,n)
