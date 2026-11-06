// Debug only, compiled with -DCHECK into build/engine_check.wasm. The shipped engine never includes this file.
// It watches the network from outside: every port access is bounds checked, and after every tick the state
// tokens and the arguments of AND neurons are inspected. It records what it sees and never changes a value,
// except that an out of bounds access is skipped so the harness can report it instead of trashing memory.
enum{DK_WOOB=1,DK_ROOB=2,DK_RECT=3,DK_ROW=4,DK_TOK=5,DK_STB=6,DK_ANDB=7,DK_NAN=8,DK_LOSS=9,DK_XREG=10,DK_ADDR=11,DK_PATCH=12};
typedef struct{i32 kind,tick,a,b;f64 x;}Dlog; enum{DLOGN=8192,DHASH=1<<16};
static Dlog*dlog;static i32 dn_,dcnt[16],*dseen; static i32 dbank,dnst,*dst_,dnr,*dreg; static i32 *wstart,*wargs,*astart,*asrc,*aand,*astamp,*dmark; static f64 *aw,*ac; static i32 dtick; static i32 dmax_tok=1;
static i32 *stk_,nstk; static u8 *stk_f;
static void dnote(i32 k,i32 a,i32 b,f64 x){dcnt[k]++;u64 h=(((u64)k*1000003ull)^((u64)(unsigned)a*2654435761ull)^((u64)(unsigned)b*40503ull))%DHASH;
 for(i32 t=0;t<DHASH;t++){i32 q=dseen[h];if(q==0)break;Dlog*l=dlog+q-1;if(l->kind==k&&l->a==a&&l->b==b)return;h=(h+1)%DHASH;}
 if(dn_<DLOGN){dlog[dn_]=(Dlog){k,dtick,a,b,x};dseen[h]=++dn_;}}
__attribute__((export_name("dbg_init"))) void dbg_init(i32 bank_,i32 nst,i32 nreg,i32 na,i32 nas,i32 nw){dbank=bank_;dnst=nst;dnr=nreg;
 dlog=alloc(sizeof(Dlog)*DLOGN);dseen=alloc(4*DHASH);dst_=alloc(4*nst+4);dreg=alloc(4*nreg+4);
 astart=alloc(4*(na+1));asrc=alloc(4*nas+4);aw=alloc(8*nas+8);ac=alloc(8*na+8);aand=alloc(4*na+4);astamp=alloc(4*na+4);wstart=alloc(4*(N+1));wargs=alloc(4*nw+4);stk_=alloc(4*N);stk_f=alloc(N);}
__attribute__((export_name("d_ptr"))) void* d_ptr(i32 k){return k==0?(void*)dst_:k==1?(void*)dreg:k==2?(void*)astart:k==3?(void*)asrc:k==4?(void*)aw:k==5?(void*)ac:k==6?(void*)aand:k==7?(void*)wstart:k==8?(void*)wargs:k==9?(void*)dlog:(void*)dcnt;}
__attribute__((export_name("d_n"))) i32 d_n(void){return dn_;}
__attribute__((export_name("d_reset"))) void d_reset(void){dn_=0;for(i32 i=0;i<16;i++)dcnt[i]=0;for(i32 i=0;i<DHASH;i++)dseen[i]=0;}
static inline i32 dfin(f64 x){return x==x&&x>-2147483000.0&&x<2147483000.0;}
static i32 dport(i32*p){i32 port=(i32)(p-ports);switch(p[0]){
  case 1:case 2:{i32 w=p[0]==1;f64 ax=v[p[2]];f64 nx=p[5]>=0?v[p[5]]:p[4];
   if(!dfin(ax)||!dfin(nx)){dnote(DK_ADDR,port,0,ax);return 0;}
   i32 a=I(p[2]),n=p[5]>=0?I(p[5]):p[4];if(n>p[4])n=p[4];if(n<=0)return 1;
   if(a<0||a+n>dbank){dnote(w?DK_WOOB:DK_ROOB,port,0,(f64)a);return 0;}
   if(w){f64*d=v+p[3];for(i32 j=0;j<n;j++){f64 x=d[j];if(x!=x||x-x!=0)dnote(DK_NAN,port,1,x);else if((f64)(f32)x!=x)dnote(DK_LOSS,port,0,x);}
    for(i32 r=0;r+1<dnr;r++)if(a<dreg[r+1]&&a+n>dreg[r+1]){dnote(DK_XREG,port,r+1,(f64)a);break;}}
   return 1;}
  case 3:{f64 vals[4]={v[p[2]],v[p[3]],v[p[4]],v[p[5]]};for(i32 j=0;j<4;j++)if(!dfin(vals[j])){dnote(DK_ADDR,port,j,vals[j]);return 0;}
   i32 y0=V(p[10]),y1=H-V(p[11]);i32 y=I(p[3])-YB,h=I(p[5]);
   i32 ya=y<y0?y0:y,yb=y+h>y1?y1:y+h;if(ya<yb&&(ya<0||yb>H)){dnote(DK_RECT,port,0,(f64)y);return 0;}return 1;}
  case 6:{for(i32 j=2;j<8;j++)if(!dfin(v[p[j]])){dnote(DK_ADDR,port,0,v[p[j]]);return 0;}i32 a=I(p[4]),w_=I(p[5]),h=I(p[6]);if(w_>0&&h>0&&(a<0||a+w_*h>dbank||w_*h>100000)){dnote(DK_ROW,port,0,(f64)a);return 0;}return 1;}
  case 4:{if(!dfin(v[p[2]])||!dfin(v[p[3]])){dnote(DK_ADDR,port,0,v[p[2]]);return 0;}return 1;}
  case 5:{if(!dfin(v[p[2]])||!dfin(v[p[3]])){dnote(DK_ADDR,port,0,v[p[2]]);return 0;}return 1;}
 }return 1;}
static f64 pull(i32 i);
static inline void dsticky(i32 i){if(!stk_f[i]){stk_f[i]=1;stk_[nstk++]=i;}}
static i32 datk;
static void dargs(i32 i){for(i32 q=wstart[i],e=wstart[i+1];q<e;q++){i32 g=wargs[q];if(astamp[g]==datk)continue;astamp[g]=datk;f64 x=ac[g];
   for(i32 k=astart[g],ke=astart[g+1];k<ke;k++){i32 s=asrc[k];x+=aw[k]*(s>=0?v[s]:pull(~s));}
   if(x!=0&&x!=1)dnote(DK_ANDB,aand[g],g,x);}}
static void dtick_end(void){dtick++;datk=dtick;i32 tok=0,first=-1,second=-1;
 for(i32 i=0;i<dnst;i++){f64 x=v[dst_[i]];if(x!=0){if(x!=1)dnote(DK_STB,dst_[i],0,x);tok++;if(first<0)first=dst_[i];else if(second<0)second=dst_[i];}}
 if(tok>1)dnote(DK_TOK,first,second,(f64)tok);
 i32 ln=nlive;for(i32 t=0;t<ln;t++){i32 i=live[t];f64 x=v[i];if(x!=x||x-x!=0)dnote(DK_NAN,i,0,x);dargs(i);}
 for(i32 t=0;t<nstk;t++){i32 i=stk_[t];stk_f[i]=0;dargs(i);}nstk=0;}
#define CHK_PORT(p) dport(p)
#define CHK_TICK() dtick_end()
#define CHK_STICKY(i) dsticky(i)
