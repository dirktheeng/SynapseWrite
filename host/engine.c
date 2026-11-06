// Sparse ANN inference engine. It evaluates one network and executes the memory
// and image ports the network drives. It contains no application logic.
// v_i(t) = act_i(bias_i + sum_{layer(j)<layer(i)} w_ji v_j(t) + sum_{recurrent} w_ji v_j(t-1))
// All neurons rest at zero, so only neurons with a nonzero input are visited.
// Neurons are numbered in layer order, so a two level bitmap yields them in a valid order.
typedef unsigned char u8; typedef unsigned short u16; typedef int i32; typedef float f32; typedef double f64; typedef unsigned long long u64; typedef unsigned int u32;
extern u8 __heap_base; static u8* hp=&__heap_base;
__attribute__((export_name("alloc"))) void* alloc(i32 n){u8*p=(u8*)(((unsigned long)hp+15)&~15ul);hp=p+n;
  unsigned long need=((unsigned long)hp+65535)/65536, have=__builtin_wasm_memory_size(0);
  if(need>have)__builtin_wasm_memory_grow(0,need-have); return p;}
static u8*z; static i32 *stamp,tickno=1; static i32 *istart,*isrc; static u16 *iwi,*wi; static f64 *wtab; static i32 NI;
static i32 N,E,L,NP,NT; static u8*act; static f64*bias,*v,*acc,*nacc; static i32*ostart,*osplit,*dst;
static i32*lstart,*live,*nlist,*ports,*pen,*pptr; static u8*nflag; static i32 nlive,nnext,nwp,nrp; static u64*bits,*sum; static i32 SWORDS;
static f32*bank; static u8*fb; enum{W=1280,H=800,YB=4096};
__attribute__((export_name("setup"))) void setup(i32 n,i32 e,i32 l,i32 np,i32 banksize,i32 ni,i32 nt,i32 zn){z=alloc(zn+1);N=n;E=e;L=l;NP=np;NI=ni;NT=nt;istart=alloc(4*(n+1));isrc=alloc(4*ni+4);iwi=alloc(2*ni+2);wtab=alloc(8*nt+8);
 act=alloc(n);bias=alloc(8*n);v=alloc(8*n);acc=alloc(8*n);nacc=alloc(8*n);ostart=alloc(4*(n+1));osplit=alloc(4*n);dst=alloc(4*e+4);wi=alloc(2*e+2);
 stamp=alloc(4*n);lstart=alloc(4*(l+1));live=alloc(4*n);nlist=alloc(4*n);nflag=alloc(n);bits=alloc(8*(n/64+2));SWORDS=n/4096+2;sum=alloc(8*SWORDS);
 ports=alloc(4*np);pen=alloc(4*np);pptr=alloc(4*np);bank=alloc(4*banksize);fb=alloc(W*H*4);}
#define PTR(name,x) __attribute__((export_name(name))) void* x##_p(void){return x;}
PTR("p_z",z)PTR("p_bank",bank)PTR("p_fb",fb)PTR("p_v",v)
// The weight file is streams of base 128 integers (see gen/rv_a8_fmt.py); this restores the arrays the tick loop uses.
// Each neuron's targets ascend, so its recurrent targets come first. Ports are indexed by enable.
static u8*zp; static inline u32 R(void){u8*p=zp;u32 x=*p++;if(x>=128){x&=127;i32 sh=7;u32 b;do{b=*p++;x|=(b&127)<<sh;sh+=7;}while(b>=128);}zp=p;return x;}
__attribute__((export_name("finish"))) void finish(void){zp=z;
 {i32 s=0;for(i32 i=0;i<N;i++){ostart[i]=s;s+=R();}ostart[N]=s;}
 {i32 pf=0;for(i32 i=0;i<N;i++)if(ostart[i+1]>ostart[i]){u32 x=R();pf+=(i32)(x>>1)^-(i32)(x&1);dst[ostart[i]]=pf;}}
 for(i32 i=0;i<N;i++)for(i32 k=ostart[i]+1,en=ostart[i+1];k<en;k++)dst[k]=dst[k-1]+R();
 for(i32 k=0;k<E;k++)wi[k]=R();
 {i32 s=0;for(i32 i=0;i<N;i++){istart[i]=s;s+=R();}istart[N]=s;}
 for(i32 i=0;i<N;i++)for(i32 k=istart[i],en=istart[i+1];k<en;k++){u32 x=R();i32 d=(i32)(x>>2)^-(i32)((x>>1)&1),a=i-d;isrc[k]=x&1?~a:a;}
 for(i32 k=0;k<NI;k++)iwi[k]=R();
 __builtin_memcpy(act,zp,N);zp+=N;
 u8*bz=zp;for(i32 i=0;i<N;i++)R();
 for(i32 l=0;l<=L;l++)lstart[l]=R();
 __builtin_memcpy(ports,zp,4*NP);zp+=4*NP;__builtin_memcpy(wtab,zp,8*NT);zp+=8*NT;
 {u8*bt=zp;zp=bz;for(i32 i=0;i<N;i++){f64 b;__builtin_memcpy(&b,bt+8*R(),8);bias[i]=b;}}
 for(i32 l=0;l<L;l++)for(i32 i=lstart[l];i<lstart[l+1];i++){i32 q=ostart[i],en=ostart[i+1],end=l&1?i+1:lstart[l+1];   // even ranges hold registers, odd ranges feed forward
  while(q<en&&dst[q]<end)q++; osplit[i]=q;}
 for(i32 pass=0;pass<2;pass++){i32*p=ports,*e=ports+NP;i32 c=0;
  while(p<e){i32 k=p[0],len=k==1||k==2?6:k==3?12:k==4?9:k==6?8:k==7?8:4;
   if((k==1||k==3||k==4||k==6||k==7)==(pass==0)){pen[(pass?nwp:0)+c]=p[1];pptr[(pass?nwp:0)+c]=(i32)(p-ports);c++;}
   p+=len;}
  if(pass)nrp=c;else nwp=c;}}
__attribute__((export_name("inject"))) void inject(i32 i,f64 x){nacc[i]+=x;if(!nflag[i]){nflag[i]=1;nlist[nnext++]=i;}}
// Rows of the image changed since the last call, as passive bookkeeping for the display.
static u8 drow[801];
__attribute__((export_name("p_drow"))) void* p_drow(void){return drow;}
static inline i32 I(i32 n){return n<0?0:(i32)__builtin_floor(v[n]);}
static inline i32 V(i32 n){return n<0?0:(i32)__builtin_floor(v[n]);}
static inline u8 C(f64 x){x+=.5;return x<0?0:x>255?255:(u8)x;}
static void write_port(i32*p){switch(p[0]){
  case 1:{ // block or scalar write: {1,en,addr,data,len,lenN}
   i32 a=I(p[2]),n=p[5]>=0?I(p[5]):p[4];if(n>p[4])n=p[4];f64*d=v+p[3];f32*b=bank+a;for(i32 j=0;j<n;j++)b[j]=(f32)d[j];break;}
  case 3:{ // rectangle write: {3,en,x,y,w,h,r,g,b,a,y0,y1}
   i32 x=I(p[2]),y=I(p[3])-YB,w_=I(p[4]),h=I(p[5]);i32 y0=V(p[10]),y1=V(p[11]);if(y1==0){y0=0;y1=H;}
   i32 x1=x+w_,yy1=y+h;if(x<0)x=0;if(x1>W)x1=W;if(y<y0)y=y0;if(yy1>y1)yy1=y1;
   u8 c[4]={C(v[p[6]]),C(v[p[7]]),C(v[p[8]]),C(v[p[9]])};
   if(y<yy1&&x<x1){i32 cc;__builtin_memcpy(&cc,c,4);for(i32 yy=y;yy<yy1;yy++){i32*q=(i32*)(fb+4*(yy*W+x));i32 diff=0;for(i32 xx=x;xx<x1;xx++){diff|=(*q^cc)&0xffffff;*q++=cc;}if(diff)drow[yy]=1;}}break;}
  case 4:{ // patch write, each pixel masked by its nonzero 4th channel: {4,en,x,y,data,pw,ph,y0,y1}
   // Only neurons that fired this tick can have a nonzero mask, so the live list gives the pixels.
   i32 x=I(p[2]),y=I(p[3])-YB,pw=p[5],ph=p[6],y0=V(p[7]),y1=V(p[8]);if(y1==0){y0=0;y1=H;}i32 d=p[4];i32 cells=4*pw*ph;
   for(i32 t=0;t<nlive;t++){i32 q=live[t]-d;if((unsigned)q<(unsigned)cells&&(q&3)==3){i32 ix=q>>2,yy=y+ix/pw,xx=x+ix%pw;
     if(yy>=y0&&yy<y1&&yy>=0&&yy<H&&xx>=0&&xx<W){u8*o=fb+4*(yy*W+xx);f64*c=v+d+q-3;o[0]=C(c[0]);o[1]=C(c[1]);o[2]=C(c[2]);drow[yy]=1;}}}break;}
  case 6:{ // image row copy, packed RGB cells to pixels: {6,en,x,y,addr,n,y0,y1}
   i32 x=I(p[2]),y=I(p[3])-YB,a=I(p[4]),n=I(p[5]),y0=V(p[6]),y1=V(p[7]);if(y1==0){y0=0;y1=H;}
   if(y>=y0&&y<y1&&y>=0&&y<H){drow[y]=1;for(i32 j=0;j<n;j++){i32 xx=x+j;if(xx>=0&&xx<W){u8*o=fb+4*(y*W+xx);i32 c=(i32)bank[a+j];o[0]=c>>16;o[1]=(c>>8)&255;o[2]=c&255;o[3]=1;}}}break;}
  case 7:{ // screen colors to or from the bank, alpha untouched: {7,en,x,y,addr,dir,w,h}
   i32 x=I(p[2]),y=I(p[3]),dir=p[5],pw=p[6],ph=p[7];f32*b=bank+p[4];
   for(i32 r=0;r<ph;r++){i32 yy=y+r;for(i32 c=0;c<pw;c++,b++){i32 xx=x+c;if(yy<0||yy>=H||xx<0||xx>=W)continue;u8*o=fb+4*(yy*W+xx);
     if(dir==0)*b=(f32)((o[0]<<16)|(o[1]<<8)|o[2]);else{i32 k=(i32)*b;u8 r_=k>>16,g_=(k>>8)&255,b_=k&255;if(o[0]!=r_||o[1]!=g_||o[2]!=b_){o[0]=r_;o[1]=g_;o[2]=b_;drow[yy]=1;}}}}break;}
 }}
static void read_port(i32*p){ if(p[0]==2){ // read: {2,en,addr,out,len,lenN}
   i32 a=I(p[2]),n=p[5]>=0?I(p[5]):p[4];if(n>p[4])n=p[4];i32 o=p[3];f32*b=bank+a;for(i32 j=0;j<n;j++){f32 x=b[j];if(x!=0)inject(o+j,x);}}
  else { // screenshot pixel read: {5,en,xy,out} with xy neuron packed as x+y*65536
   i32 xy=I(p[2]),x=xy&65535,y=xy>>16;if(x>=0&&x<W&&y>=0&&y<H){u8*o=fb+4*(y*W+x);for(i32 j=0;j<4;j++)if(o[j])inject(p[3]+j,o[j]);}}}
static inline void run_ports(void){
 for(i32 i=0;i<nwp;i++)if(v[pen[i]]!=0)write_port(ports+pptr[i]);
 for(i32 i=nwp,e=nwp+nrp;i<e;i++)if(v[pen[i]]!=0)read_port(ports+pptr[i]);}
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
__attribute__((noinline)) static f64 pull(i32 i){ if(stamp[i]==tickno)return v[i]; CNT(2);CN(i,1); f64 x=bias[i]; i32 ac=act[i],q=istart[i],e=istart[i+1];
 if(ac&4){ac&=3;i32 s=isrc[q];CNT(3);f64 y=s>=0?v[s]:pull(~s);if(y==0){stamp[i]=tickno;return 0;}x+=wtab[iwi[q]]*y;q++;}
 for(;q<e;q++){f64 w_=wtab[iwi[q]];if(x<=-549755813888.0&&w_<549755813888.0&&w_>-549755813888.0)break;i32 s=isrc[q];CNT(3);CN(i,1);x+=w_*(s>=0?v[s]:pull(~s));}
 f64 o=ac==0?x:ac==1?(x>1e-9?1:0):(x>0?x:0); stamp[i]=tickno; if(o!=0){v[i]=o;live[nlive++]=i;} return o;}
__attribute__((noinline)) static void tick(void){ tickno++;
 for(i32 i=0;i<nlive;i++)v[live[i]]=0; nlive=0;
 for(i32 i=0;i<nnext;i++){i32 d=nlist[i];acc[d]=nacc[d];nacc[d]=0;nflag[d]=0;SET(d);} nnext=0;
 for(i32 sw=0;sw<SWORDS;sw++){u64 s;while((s=sum[sw])){i32 wd=sw*64+__builtin_ctzll(s);u64 b;
   while((b=bits[wd])){i32 i=wd*64+__builtin_ctzll(b);bits[wd]=b&(b-1);
    f64 x=acc[i]+bias[i];acc[i]=0;CNT(0);CN(i,1);
    {i32 a0=istart[i],a1=istart[i+1];if(a1>a0&&x>-549755813888.0){for(i32 q=a0;q<a1;q++){i32 s=isrc[q];CNT(1);CN(i,1);x+=wtab[iwi[q]]*(s>=0?v[s]:pull(~s));}}}
    i32 ac=act[i];if(ac==3){v[i]+=x;continue;}f64 o=ac==0?x:ac==1?(x>1e-9?1:0):(x>0?x:0);
    if(o!=0){v[i]=o;live[nlive++]=i;i32 q=ostart[i],sp=osplit[i],en=ostart[i+1];edges_total+=en-q;CN(i,en-q);
     for(;q<sp;q++){i32 d=dst[q];nacc[d]+=o*wtab[wi[q]];if(!nflag[d]){nflag[d]=1;nlist[nnext++]=d;}}
     for(;q<en;q++){i32 d=dst[q];acc[d]+=o*wtab[wi[q]];SET(d);}}}
   sum[sw]&=~(1ull<<(wd&63));}}
 run_ports();}
// Run ticks until the halt neuron fires. Returns the tick count.
__attribute__((export_name("run"))) i32 run(i32 halt,i32 maxticks){i32 n=0;while(n<maxticks){tick();n++;if(v[halt]!=0)break;}return n;}
__attribute__((export_name("val"))) f64 val(i32 i){return v[i];}
