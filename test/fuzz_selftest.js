// The checker must fire on planted faults, or its silence means nothing.
const {World,h,states,dbg}=require('./fuzz_lib');
const ok=(n,c)=>{console.log(c?'PASS':'FAIL',n);if(!c)process.exitCode=1;};
{const w=new World({cap:300000});const ids=Object.keys(states);const q=+ids.find(k=>states[k]=='TYPE');w.e.inject(q,1);w.key(97);ok('second token is seen',w.fails.some(f=>f.cls=='TWO_TOKENS'));}
{const w=new World();const pa=new Int32Array(w.e.memory.buffer,w.e.d_ptr(2),dbg.na+1);const sr=new Int32Array(w.e.memory.buffer,w.e.d_ptr(3),dbg.nas);let found=-1;for(let g=0;g<dbg.na;g++){if(pa[g+1]-pa[g]==1&&sr[pa[g]]>=0){found=sr[pa[g]];break;}}
 w.e.inject(found,5);w.e.run(h.halt,1);w.scan();ok('non boolean AND argument is seen',w.fails.some(f=>f.cls=='AND_NONBOOL'));}
{const w=new World();let hit=false;const p=new Int32Array(w.e.memory.buffer,w.e.p_ports(),h.nports);let i=0;while(i<h.nports){const k=p[i];const len=k==1||k==2?6:k==3?12:k==4?9:k==6?8:k==7?8:4;if(k==1&&p[i+5]<0&&!hit){hit=true;w.e.inject(p[i+1],1);w.e.inject(p[i+2],-7);w.e.run(h.halt,1);w.scan();}i+=len;}ok('write below the bank is seen',w.fails.some(f=>f.cls=='OOB_WRITE'||f.cls=='BAD_ADDR'));}
{const w=new World({cap:50});w.paste('aaaa aaaa aaaa\nbbbb');ok('tick cap is a hang',w.fails.some(f=>f.cls=='HANG'));}
