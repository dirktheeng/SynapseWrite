// Sparse ANN inference engine. It evaluates one network and executes the memory
// and image ports the network drives. It contains no application logic.
// v_i(t) = act_i(bias_i + sum_{layer(j)<layer(i)} w_ji v_j(t) + sum_{recurrent} w_ji v_j(t-1))
// All neurons rest at zero, so only neurons with a nonzero input are visited.
typedef unsigned char u8; typedef int i32; typedef float f32; typedef double f64;
extern u8 __heap_base; static u8* hp=&__heap_base;
__attribute__((export_name("alloc"))) void* alloc(i32 n){u8*p=(u8*)(((unsigned long)hp+15)&~15ul);hp=p+n;
  unsigned long need=((unsigned long)hp+65535)/65536, have=__builtin_wasm_memory_size(0);
  if(need>have)__builtin_wasm_memory_grow(0,need-have); __builtin_memset(p,0,n); return p;}
static i32 *istart,*isrc; static f64 *iw; static i32 NI;
static i32 N,E,L,NP; static u8*act; static f64*bias,*v,*acc,*nacc,*w; static i32*ostart,*dst;
static i32*lstart,*lof,*tbuf,*tcnt,*live,*nlist,*ports; static u8*flag,*nflag; static i32 nlive,nnext;
static f32*bank; static u8*fb; enum{W=1280,H=800,YB=4096};
__attribute__((export_name("setup"))) void setup(i32 n,i32 e,i32 l,i32 np,i32 banksize,i32 ni){N=n;E=e;L=l;NP=np;NI=ni;istart=alloc(4*(n+1));isrc=alloc(4*ni+4);iw=alloc(8*ni+8);
 act=alloc(n);bias=alloc(8*n);v=alloc(8*n);acc=alloc(8*n);nacc=alloc(8*n);ostart=alloc(4*(n+1));dst=alloc(4*e+4);w=alloc(8*e+8);
 lstart=alloc(4*(l+1));lof=alloc(4*n);tbuf=alloc(4*n);tcnt=alloc(4*l);live=alloc(4*n);nlist=alloc(4*n);flag=alloc(n);nflag=alloc(n);
 ports=alloc(4*np);bank=alloc(4*banksize);fb=alloc(W*H*4);}
#define PTR(name,x) __attribute__((export_name(name))) void* x##_p(void){return x;}
PTR("p_istart",istart)PTR("p_isrc",isrc)PTR("p_iw",iw)PTR("p_act",act)PTR("p_bias",bias)PTR("p_ostart",ostart)PTR("p_dst",dst)PTR("p_w",w)PTR("p_lstart",lstart)PTR("p_ports",ports)PTR("p_bank",bank)PTR("p_fb",fb)PTR("p_v",v)
__attribute__((export_name("finish"))) void finish(void){for(i32 l=0;l<L;l++)for(i32 i=lstart[l];i<lstart[l+1];i++)lof[i]=l;}
__attribute__((export_name("inject"))) void inject(i32 i,f64 x){nacc[i]+=x;if(!nflag[i]){nflag[i]=1;nlist[nnext++]=i;}}
static inline i32 I(i32 n){return n<0?0:(i32)__builtin_floor(v[n]);}
static inline i32 V(i32 n){return n<0?0:(i32)__builtin_floor(v[n]);}
static inline u8 C(f64 x){x+=.5;return x<0?0:x>255?255:(u8)x;}
static void run_ports(void){ i32*p=ports,*e=ports+NP;
 while(p<e){i32 k=p[0];
  if(k==1){ // block or scalar write: {1,en,addr,data,len,lenN}
   if(v[p[1]]!=0){i32 a=I(p[2]),n=p[5]>=0?I(p[5]):p[4];if(n>p[4])n=p[4];for(i32 j=0;j<n;j++)bank[a+j]=(f32)v[p[3]+j];} p+=6;}
  else if(k==2){ p+=6; }
  else if(k==3){ // rectangle write: {3,en,x,y,w,h,r,g,b,a,y0,y1}
   if(v[p[1]]!=0){i32 x=I(p[2]),y=I(p[3])-YB,w_=I(p[4]),h=I(p[5]);i32 y0=V(p[10]),y1=V(p[11]);if(y1==0){y0=0;y1=H;}
    i32 x1=x+w_,yy1=y+h;if(x<0)x=0;if(x1>W)x1=W;if(y<y0)y=y0;if(yy1>y1)yy1=y1;
    u8 c[4]={C(v[p[6]]),C(v[p[7]]),C(v[p[8]]),C(v[p[9]])};
    for(i32 yy=y;yy<yy1;yy++){u8*q=fb+4*(yy*W+x);for(i32 xx=x;xx<x1;xx++){q[0]=c[0];q[1]=c[1];q[2]=c[2];q[3]=c[3];q+=4;}}} p+=12;}
  else if(k==4){ // patch write, each pixel masked by its nonzero 4th channel: {4,en,x,y,data,pw,ph,y0,y1}
   if(v[p[1]]!=0){i32 x=I(p[2]),y=I(p[3])-YB,pw=p[5],ph=p[6],y0=V(p[7]),y1=V(p[8]);if(y1==0){y0=0;y1=H;}i32 d=p[4];
    for(i32 j=0;j<ph;j++){i32 yy=y+j;if(yy<y0||yy>=y1)continue;for(i32 i=0;i<pw;i++){i32 q=d+4*(j*pw+i);if(v[q+3]!=0){i32 xx=x+i;if(xx>=0&&xx<W){u8*o=fb+4*(yy*W+xx);o[0]=C(v[q]);o[1]=C(v[q+1]);o[2]=C(v[q+2]);}}}}} p+=9;}
  else if(k==6){ // image row copy, packed RGB cells to pixels: {6,en,x,y,addr,n,y0,y1}
   if(v[p[1]]!=0){i32 x=I(p[2]),y=I(p[3])-YB,a=I(p[4]),n=I(p[5]),y0=V(p[6]),y1=V(p[7]);if(y1==0){y0=0;y1=H;}
    if(y>=y0&&y<y1&&y>=0&&y<H)for(i32 j=0;j<n;j++){i32 xx=x+j;if(xx>=0&&xx<W){u8*o=fb+4*(y*W+xx);i32 c=(i32)bank[a+j];o[0]=c>>16;o[1]=(c>>8)&255;o[2]=c&255;o[3]=1;}}} p+=8;}
  else p+=4; }
 p=ports; while(p<e){i32 k=p[0];
  if(k==1)p+=6; else if(k==2){ // read: {2,en,addr,out,len,lenN}
   if(v[p[1]]!=0){i32 a=I(p[2]),n=p[5]>=0?I(p[5]):p[4];if(n>p[4])n=p[4];for(i32 j=0;j<n;j++){f32 x=bank[a+j];if(x!=0)inject(p[3]+j,x);}} p+=6;}
  else if(k==3)p+=12; else if(k==4)p+=9; else if(k==6)p+=8;
  else { // screenshot pixel read: {5,en,xy,out} with xy neuron packed as x+y*65536
   if(v[p[1]]!=0){i32 xy=I(p[2]),x=xy&65535,y=xy>>16;if(x>=0&&x<W&&y>=0&&y<H){u8*o=fb+4*(y*W+x);for(i32 j=0;j<4;j++)if(o[j])inject(p[3]+j,o[j]);}} p+=4;}
 }}
static unsigned long long lmask0,lmask1;
static inline void push(i32 d){i32 l=lof[d];if(!flag[d]){flag[d]=1;tbuf[lstart[l]+tcnt[l]++]=d;if(l<64)lmask0|=1ull<<l;else lmask1|=1ull<<(l-64);}}
static long edges_total=0; __attribute__((export_name("edges"))) f64 edges(void){return (f64)edges_total;}
static void tick(void){
 for(i32 i=0;i<nlive;i++)v[live[i]]=0; nlive=0;
 for(i32 i=0;i<nnext;i++){i32 d=nlist[i];acc[d]=nacc[d];nacc[d]=0;nflag[d]=0;push(d);} nnext=0;
 for(i32 l=0;l<L;l++){if(l<64){if(!(lmask0>>l&1))continue;}else if(!(lmask1>>(l-64)&1))continue;i32 c=tcnt[l];i32*b=tbuf+lstart[l];
  for(i32 t=0;t<c||t<tcnt[l];t++){i32 i=b[t];f64 x=acc[i]+bias[i];acc[i]=0;flag[i]=0;
   {i32 a0=istart[i],a1=istart[i+1];if(a1>a0&&x>-549755813888.0){for(i32 q=a0;q<a1;q++)x+=iw[q]*v[isrc[q]];}}
   f64 o=act[i]==0?x:act[i]==1?(x>1e-9?1:0):(x>0?x:0);
   if(o!=0){v[i]=o;live[nlive++]=i;i32 s=ostart[i],en=ostart[i+1];edges_total+=en-s;
    for(i32 q=s;q<en;q++){i32 d=dst[q];f64 y=o*w[q];if(lof[d]>l){acc[d]+=y;push(d);}else{nacc[d]+=y;if(!nflag[d]){nflag[d]=1;nlist[nnext++]=d;}}}}}
  tcnt[l]=0;}
 lmask0=lmask1=0;run_ports();}
// Run ticks until the halt neuron fires. Returns the tick count.
__attribute__((export_name("run"))) i32 run(i32 halt,i32 maxticks){i32 n=0;while(n<maxticks){tick();n++;if(v[halt]!=0)break;}return n;}
__attribute__((export_name("val"))) f64 val(i32 i){return v[i];}
