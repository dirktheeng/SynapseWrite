// Sparse ANN inference engine. It evaluates one network and executes the memory
// and image ports the network drives. It contains no application logic.
// v_i(t) = act_i(bias_i + sum_{layer(j)<layer(i)} w_ji v_j(t) + sum_{recurrent} w_ji v_j(t-1))
// All neurons rest at zero, so only neurons with a nonzero input are visited.
// Neurons are numbered in layer order, so a two level bitmap yields them in a valid order.
typedef unsigned char u8; typedef unsigned short u16; typedef int i32; typedef float f32; typedef double f64; typedef unsigned long long u64;
extern u8 __heap_base; static u8* hp=&__heap_base;
__attribute__((export_name("alloc"))) void* alloc(i32 n){u8*p=(u8*)(((unsigned long)hp+15)&~15ul);hp=p+n;
  unsigned long need=((unsigned long)hp+65535)/65536, have=__builtin_wasm_memory_size(0);
  if(need>have)__builtin_wasm_memory_grow(0,need-have); return p;}
static u8*zb; static i32 zn_; static f64*btab; static i32 *stamp,tickno=1; typedef struct{f64 bias,acc;i32 is,os,sp,act;}Nr; typedef struct{i32 n;unsigned w;}Syn; static Nr*nr; static Syn*lz,*eg; static f64 *wtab; static i32 NI;  // what one visit touches sits on one cache line
static i32 N,E,L,NP,NT; static f64*v,*nacc;
static i32*lstart,*live,*nlist,*ports,*pen,*pptr,*live2,*nlist2; static u8*nflag; static i32 nlive,nnext,nlive2,nnext2,N1,D; static i32 pb[2][3]; static u64*bits,*sum; static i32 SWORDS,sw0[2],sw1[2];
static u8*fb,*img; enum{W=1280,H=800,YB=4096,PG=65536,NPG=1024};
// The memory bank is paged: wasm memory is taken only when a page is first written, and an untouched page reads as zeros.
static f32*pages[NPG];
static inline f32*pg_w(i32 a){unsigned k=(unsigned)a>>16;if(k>=NPG)return 0;if(!pages[k]){unsigned long need=(((unsigned long)hp+15)&~15ul)+PG*4;unsigned long want=(need+65535)/65536,have=__builtin_wasm_memory_size(0);if(want>have&&__builtin_wasm_memory_grow(0,want-have)<0)return 0;pages[k]=alloc(PG*4);}return pages[k];}
__attribute__((export_name("bget"))) f64 bget(i32 a){unsigned k=(unsigned)a>>16;return k<NPG&&pages[k]?pages[k][a&(PG-1)]:0;}
__attribute__((export_name("bset"))) void bset(i32 a,f64 x){f32*p=pg_w(a);if(p)p[a&(PG-1)]=(f32)x;}
__attribute__((export_name("setup"))) void setup(i32 n,i32 e,i32 l,i32 np,i32 banksize,i32 ni,i32 nt,i32 nb,i32 zn,i32 n1){N1=n1;N=n;E=e;L=l;NP=np;NI=ni;NT=nt;nr=(Nr*)(((unsigned long)alloc(32*(n+1)+64)+63)&~63ul);lz=alloc(8*ni+8);wtab=alloc(8*nt+8);btab=alloc(8*nb+8);
 v=alloc(8*n);nacc=alloc(8*n);eg=alloc(8*e+8);
 stamp=alloc(4*n);lstart=alloc(4*(l+1));live=alloc(4*n);nlist=alloc(4*n);live2=alloc(4*(n-n1+1));nlist2=alloc(4*(n-n1+1));nflag=alloc(n);bits=alloc(8*(n/64+2));SWORDS=n/4096+2;sum=alloc(8*SWORDS);sw0[0]=0;sw1[0]=n1/4096+1;sw0[1]=n1/4096;sw1[1]=SWORDS;
 ports=alloc(4*np);pen=alloc(4*np);pptr=alloc(4*np);fb=alloc(W*H*4);img=alloc(W*H*4);zb=alloc(zn+4);zn_=zn;}
#define PTR(name,x) __attribute__((export_name(name))) void* x##_p(void){return x;}
PTR("p_zb",zb)PTR("p_wtab",wtab)PTR("p_btab",btab)PTR("p_lstart",lstart)PTR("p_ports",ports)PTR("p_fb",fb)PTR("p_img",img)PTR("p_v",v)
// The weight file holds variable length integer streams, so that it compresses; this restores the arrays.
// Sizes, then sources of lazy inputs (delta per input position, pull flag in the low bit), then push targets
// (first target delta from the previous neuron's first target, others ascending), weight and bias indices.
static inline unsigned rv(u8**p){unsigned x=0;i32 s=0;u8 b;do{b=*(*p)++;x|=(unsigned)(b&127)<<s;s+=7;}while(b&128);return x;}
static inline i32 uz(unsigned x){return (i32)(x>>1)^-(i32)(x&1);}
__attribute__((export_name("finish"))) void finish(void){
 u8*p_=zb;unsigned ln[12];__builtin_memcpy(ln,p_,12*4);u8*S[12];u8*q0=p_+12*4;for(i32 k=0;k<12;k++){S[k]=q0;q0+=ln[k];}
 {i32 is_=0,os_=0;for(i32 i=0;i<N;i++){nr[i].is=is_;nr[i].os=os_;is_+=rv(&S[0]);os_+=rv(&S[1]);nr[i].act=*S[2]++;nr[i].bias=btab[rv(&S[3])];nr[i].acc=0;}nr[N].is=is_;nr[N].os=os_;}
 {i32 pv[4]={0,0,0,0};for(i32 i=0;i<N;i++)for(i32 q=nr[i].is,e=nr[i+1].is;q<e;q++){i32 c=q-nr[i].is;if(c>3)c=3;unsigned x=rv(&S[4+c]);pv[c]+=uz(x>>1);lz[q].n=x&1?~pv[c]:pv[c];lz[q].w=rv(&S[8]);}}
 {i32 pf=0;for(i32 i=0;i<N;i++){i32 s=nr[i].os,e=nr[i+1].os;if(s<e){pf+=uz(rv(&S[9]));eg[s].n=pf;eg[s].w=rv(&S[11]);for(i32 k=s+1;k<e;k++){eg[k].n=eg[k-1].n+(i32)rv(&S[10]);eg[k].w=rv(&S[11]);}}}}
 for(i32 l=0;l<L;l++)for(i32 i=lstart[l];i<lstart[l+1];i++){i32 q=nr[i].os,e=nr[i+1].os,end=lstart[l+1];
  while(q<e&&eg[q].n<end)q++; nr[i].sp=q;}
 __builtin_memset(zb,0,zn_);hp=zb;
 // Ports are grouped by clock domain, writes first. A port of kind 9 marks the start of domain 1.
 i32 c=0;for(i32 d=0;d<2;d++)for(i32 pass=0;pass<2;pass++){i32*p=ports,*e=ports+NP;i32 cd=0;pb[d][pass]=c;
  while(p<e){i32 k=p[0],len=k==1||k==2?6:k==3?12:k==4||k==11?9:k==6?10:k==8?5+2*p[3]+2*p[4]:k==9?1:k==10?8:k==5?5:4;
   if(k==9)cd=1;else if(cd==d&&(k==1||k==3||k==4||k==11||k==6||k==8)==(pass==0)){pen[c]=p[1];pptr[c]=(i32)(p-ports);c++;}
   p+=len;}
  if(pass)pb[d][2]=c;}}
// Initial values of one clock domain go on that domain's list.
static inline void swap_dom(void){i32*t=live;live=live2;live2=t;t=nlist;nlist=nlist2;nlist2=t;i32 a=nlive;nlive=nlive2;nlive2=a;a=nnext;nnext=nnext2;nnext2=a;D=!D;}
__attribute__((export_name("dom"))) void dom(void){swap_dom();}
__attribute__((export_name("inject"))) void inject(i32 i,f64 x){nacc[i]+=x;if(!nflag[i]){nflag[i]=1;nlist[nnext++]=i;}}
// Rows of the image changed since the last call, as passive bookkeeping for the display.
static u8 drow[801];
__attribute__((export_name("p_drow"))) void* p_drow(void){return drow;}
// The next run of changed rows at or after y is copied to the opaque display image. Returns its first row, or -1; showz gives its end.
static i32 showe; __attribute__((export_name("showz"))) i32 showz(void){return showe;}
__attribute__((export_name("show"))) i32 show(i32 y){while(y<H&&!drow[y])y++;if(y>=H)return -1;i32 z=y;while(drow[z])drow[z++]=0;showe=z;
 unsigned*q=(unsigned*)img+y*W,*f=(unsigned*)fb+y*W;for(i32 i=0,e_=(z-y)*W;i<e_;i++)q[i]=f[i]|0xff000000u;return y;}
static inline i32 I(i32 n){return n<0?0:(i32)__builtin_floor(v[n]);}
static inline i32 V(i32 n){return n<0?0:(i32)__builtin_floor(v[n]);}
static inline u8 C(f64 x){x+=.5;return x<0?0:x>255?255:(u8)x;}
static void call_port(i32*p);
static void write_port(i32*p){switch(p[0]){
  case 8:call_port(p);break;
  case 1:{ // block or scalar write: {1,en,addr,data,len,lenN}
   i32 a=I(p[2]),n=p[5]>=0?I(p[5]):p[4];if(n>p[4])n=p[4];f64*d=v+p[3];
   while(n>0){i32 o=a&(PG-1),m=PG-o;if(m>n)m=n;f32*b=pg_w(a);if(b){b+=o;for(i32 j=0;j<m;j++)b[j]=(f32)d[j];}a+=m;d+=m;n-=m;}break;}
  case 3:{ // rectangle write: {3,en,x,y,w,h,r,g,b,a,y0,y1}
   i32 x=I(p[2]),y=I(p[3])-YB,w_=I(p[4]),h=I(p[5]);i32 y0=V(p[10]),y1=H-V(p[11]);
   i32 x1=x+w_,yy1=y+h;if(x<0)x=0;if(x1>W)x1=W;if(y<y0)y=y0;if(yy1>y1)yy1=y1;
   u8 c[4]={C(v[p[6]]),C(v[p[7]]),C(v[p[8]]),C(v[p[9]])};
   if(v[p[6]]<0){u8 al=c[3];if(y<yy1&&x<x1)for(i32 yy=y;yy<yy1;yy++){u8*q=fb+4*(yy*W+x)+3;for(i32 xx=x;xx<x1;xx++,q+=4)*q=al;}break;} // id plane only, colors stay
   if(y<yy1&&x<x1){i32 cc;__builtin_memcpy(&cc,c,4);for(i32 yy=y;yy<yy1;yy++){i32*q=(i32*)(fb+4*(yy*W+x));i32 diff=0;for(i32 xx=x;xx<x1;xx++){diff|=(*q^cc)&0xffffff;*q++=cc;}if(diff)drow[yy]=1;}}break;}
  case 11:case 4:{ // patch write, each pixel masked by its nonzero 4th channel: {4,en,x,y,data,pw,ph,y0,y1}. Kind 11 keeps the darker of old and new, so overlapping dark letters on a light page stay whole
   // Only neurons that fired this tick can have a nonzero mask, so the live list gives the pixels.
   i32 x=I(p[2]),y=I(p[3])-YB,pw=p[5],ph=p[6],y0=V(p[7]),y1=H-V(p[8]);i32 d=p[4];i32 cells=4*pw*ph;
   for(i32 t=0;t<nlive;t++){i32 q=live[t]-d;if((unsigned)q<(unsigned)cells&&(q&3)==3){i32 ix=q>>2,yy=y+ix/pw,xx=x+ix%pw;
     if(yy>=y0&&yy<y1&&yy>=0&&yy<H&&xx>=0&&xx<W){u8*o=fb+4*(yy*W+xx);f64*c=v+d+q-3;if(p[0]==11){u8 r=C(c[0]),g=C(c[1]),b=C(c[2]);if(r<o[0])o[0]=r;if(g<o[1])o[1]=g;if(b<o[2])o[2]=b;}else{o[0]=C(c[0]);o[1]=C(c[1]);o[2]=C(c[2]);}drow[yy]=1;}}}break;}
  case 6:{ // pixel words between bank and screen, id plane untouched: {6,en,x,y,addr,w,h,dir,y0,y1}
   i32 x=I(p[2]),y=I(p[3])-YB,a=I(p[4]),pw=I(p[5]),ph=I(p[6]),dir=I(p[7]),y0=V(p[8]),y1=H-V(p[9]);
   for(i32 r=0;r<ph;r++){i32 yy=y+r;if(yy<y0||yy>=y1||yy<0||yy>=H)continue;for(i32 c=0;c<pw;c++){i32 xx=x+c;if(xx<0||xx>=W)continue;i32*o=(i32*)fb+yy*W+xx;
     if(dir==0)bset(a+r*pw+c,(f64)(*o&0xffffff));else{i32 k=((i32)bget(a+r*pw+c)^*o)&0xffffff;if(k){*o^=k;drow[yy]=1;}}}}break;}
  }}
static void bread(i32 a,i32 n,i32 o){while(n>0){unsigned k=(unsigned)a/PG;i32 q=a&(PG-1),m=PG-q;if(m>n)m=n;if(k<NPG&&pages[k]){f32*b=pages[k]+q;for(i32 j=0;j<m;j++){f32 x=b[j];if(x!=0)inject(o+j,x);}}a+=m;o+=m;n-=m;}}
static void read_port(i32*p){ if(p[0]==10){ // read through an index cell: {10,en,addr,out,base,mask,stride,len}
   f32 x=(f32)bget(I(p[2]));i32 o=p[3];if(x!=0)inject(o,x);bread(p[4]+(((i32)x)&p[5])*p[6],p[7],o+1);}
  else if(p[0]==2){ // read: {2,en,addr,out,len,lenN}
   i32 a=I(p[2]),n=p[5]>=0?I(p[5]):p[4];if(n>p[4])n=p[4];bread(a,n,p[3]);}
  else { // screenshot pixel read: {5,en,x,y,out}
   i32 x=I(p[2]),y=I(p[3]);if(x>=0&&x<W&&y>=0&&y<H){u8*o=fb+4*(y*W+x);for(i32 j=0;j<4;j++)if(o[j])inject(p[4]+j,o[j]);}}}
#ifdef CHECK
#include "engine_check.h"
#else
#define CHK_PORT(p) 1
#define CHK_TICK()
#define CHK_STICKY(i)
#endif
static inline void run_ports(void){i32 d=D,a=pb[d][0],b=pb[d][1],c=pb[d][2];
 for(i32 i=a;i<b;i++)if(v[pen[i]]!=0&&CHK_PORT(ports+pptr[i]))write_port(ports+pptr[i]);
 for(i32 i=b;i<c;i++)if(v[pen[i]]!=0&&CHK_PORT(ports+pptr[i]))read_port(ports+pptr[i]);}
static long edges_total=0; __attribute__((export_name("edges"))) f64 edges(void){return (f64)edges_total;}
#define SET(d) do{bits[(d)>>6]|=1ull<<((d)&63);sum[(d)>>12]|=1ull<<(((d)>>6)&63);}while(0)
#ifdef COUNT
static double c_ops[4];__attribute__((export_name("ops"))) f64 ops(i32 k){return c_ops[k];}
static f32*c_n;__attribute__((export_name("workp"))) void* workp(void){if(!c_n)c_n=alloc(4*N);return c_n;}
#define CN(i,x) if(c_n)c_n[i]+=(x)
#define CNT(k) c_ops[k]+=1
#else
#define CNT(k)
#define CN(i,x)
#endif
// A pull neuron computes only when a consumer reads it, at most once per tick. Inputs are stored
// with the largest weights first, so a closed gate ends the evaluation at once.
__attribute__((noinline)) static f64 pull(i32 i){ if(stamp[i]==tickno)return v[i]; CNT(2);CN(i,1); Nr*r=nr+i;f64 x=r->bias; i32 ac=r->act,q=r->is,e=r[1].is;
 if(ac&4){ac&=3;i32 s=lz[q].n;CNT(3);f64 y=s>=0?v[s]:pull(~s);if(y==0){stamp[i]=tickno;return 0;}x+=wtab[lz[q].w]*y;q++;}
 for(;q<e;q++){f64 w_=wtab[lz[q].w];if(x<=-549755813888.0&&w_<549755813888.0&&w_>-549755813888.0)break;i32 s=lz[q].n;CNT(3);CN(i,1);x+=w_*(s>=0?v[s]:pull(~s));}
 f64 o=ac==0?x:ac==1?(x>1e-9?1:0):(x>0?x:0); stamp[i]=tickno; if(o!=0){v[i]=o;live[nlive++]=i;} return o;}
__attribute__((noinline)) static void tick(void){ tickno++;
 for(i32 i=0;i<nlive;i++)v[live[i]]=0; nlive=0;
 for(i32 i=0;i<nnext;i++){i32 d=nlist[i];nr[d].acc=nacc[d];nacc[d]=0;nflag[d]=0;SET(d);} nnext=0;
 for(i32 sw=sw0[D],swe=sw1[D];sw<swe;sw++){u64 s;while((s=sum[sw])){i32 wd=sw*64+__builtin_ctzll(s);u64 b;
   while((b=bits[wd])){i32 i=wd*64+__builtin_ctzll(b);bits[wd]=b&(b-1);
    Nr*r=nr+i;f64 x=r->acc+r->bias;r->acc=0;CNT(0);CN(i,1);
    {i32 a0=r->is,a1=r[1].is;if(a1>a0&&x>-549755813888.0){for(i32 q=a0;q<a1;q++){i32 s=lz[q].n;CNT(1);CN(i,1);x+=wtab[lz[q].w]*(s>=0?v[s]:pull(~s));}}}
    i32 ac=r->act;if(ac==3){v[i]+=x;CHK_STICKY(i);continue;}f64 o=ac==0?x:ac==1?(x>1e-9?1:0):(x>0?x:0);
    if(o!=0){v[i]=o;live[nlive++]=i;i32 q=r->os,sp=r->sp,en=r[1].os;edges_total+=en-q;CN(i,en-q);
     for(;q<sp;q++){i32 d=eg[q].n;nacc[d]+=o*wtab[eg[q].w];if(!nflag[d]){nflag[d]=1;nlist[nnext++]=d;}}
     for(;q<en;q++){i32 d=eg[q].n;nr[d].acc+=o*wtab[eg[q].w];SET(d);}}}
   sum[sw]&=~(1ull<<(wd&63));}}
 CHK_TICK();run_ports();}
// A second clock domain. The calling domain's clock stops: its values and lists stay as they are while the
// other domain ticks until its done neuron fires. {8,en,done,nargs,nrets,src,dst,...,src,dst,...}
static void call_port(i32*p){i32 na=p[3],nr=p[4];i32*q=p+5;swap_dom();
 for(i32 k=0;k<na;k++){f64 x=v[q[2*k]];if(x!=0)inject(q[2*k+1],x);}
 i32 n=0;do{tick();}while(v[p[2]]==0&&++n<100000000);
 q+=2*na;f64 r[8];for(i32 k=0;k<nr;k++)r[k]=v[q[2*k]];swap_dom();
 for(i32 k=0;k<nr;k++)if(r[k]!=0)inject(q[2*k+1],r[k]);}
// Run ticks until the halt neuron fires. Returns the tick count.
__attribute__((export_name("run"))) i32 run(i32 halt,i32 maxticks){i32 n=0;while(n<maxticks){tick();n++;if(v[halt]!=0)break;}return n;}
__attribute__((export_name("ostart"))) i32 ostart_(i32 i){return nr[i].os;}
__attribute__((export_name("val"))) f64 val(i32 i){return v[i];}
