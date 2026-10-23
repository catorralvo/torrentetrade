#!/usr/bin/env node
// Execute actual arcade functions with a deterministic mocked canvas, without
// external dependencies, paid services or browser downloads.
const fs=require('node:fs'),vm=require('node:vm'),assert=require('node:assert/strict');
const src=fs.readFileSync('dont100-apk/app/src/main/assets/index.html','utf8');
function extract(name){
 const m=new RegExp('function\\s+'+name+'\\s*\\(').exec(src);
 assert(m,'missing '+name);
 let open=src.indexOf('{',m.index),depth=0,quote='',esc=false,comment='';
 for(let i=open;i<src.length;i++){
  const c=src[i],n=src[i+1];
  if(comment==='line'){if(c==='\n')comment='';continue}
  if(comment==='block'){if(c==='*'&&n==='/'){comment='';i++}continue}
  if(quote){if(esc){esc=false;continue}if(c==='\\'){esc=true;continue}if(c===quote)quote='';continue}
  if(c==='/'&&n==='/'){comment='line';i++;continue}
  if(c==='/'&&n==='*'){comment='block';i++;continue}
  if(c==='"'||c==="'"||c==='\x60'){quote=c;continue}
  if(c==='{')depth++;if(c==='}'&&!--depth)return src.slice(m.index,i+1);
 }
 throw Error('unclosed '+name);
}
const gradient={addColorStop(){}};
const canvasContext=new Proxy({}, {get(_t,k){if(k==='createLinearGradient'||k==='createRadialGradient')return ()=>gradient;return ()=>{}},set(){return true}});
function harness(name,seed){
 let now=0,loop=null,result=null,pointer=null,pad=null,timers=[],nextId=0;
 const canvas={getContext:()=>canvasContext,addEventListener(type,fn){if(type==='pointerdown')pointer=fn}};
 const context={
  Math,console,performance:{now:()=>now},state:{resolved:false,failed:false},
  tr:(es)=>es,setChallenge(){},arcadeCanvas:()=>canvas,
  arcadeControlDeck:()=>({pad:{}}),bindRelativePad:(_pad,fn)=>{pad=fn},
  startArcadeLoop:fn=>{loop=fn},drawArcadeBackdrop(){},drawDoodle(){},roughLine(){},tone(){},
  canvasPointerX:e=>e.x,canvasPointerY:e=>e.y,
  rint:(_r,min)=>min,later:(fn,ms)=>timers.push({at:now+ms,fn,id:++nextId}),
  pass:()=>{result='pass';context.state.resolved=true},
  fail:()=>{result='fail';context.state.failed=true}
 };
 vm.createContext(context);vm.runInContext(extract(name),context,{timeout:1000});
 context[name](1,()=>seed,1);
 function tick(dt){now+=dt;for(const t of [...timers]){if(t.at<=now){timers.splice(timers.indexOf(t),1);t.fn()}}
  if(loop&&!result)loop(now)}
 return {tick,tap:(x,y)=>pointer&&pointer({x,y}),slide:dx=>pad&&pad(dx),get result(){return result},get now(){return now}};
}
function check(label,fn){try{fn();console.log('PASS '+label)}catch(e){console.error('FAIL '+label+': '+e.message);process.exitCode=1}}
check('Whack: X ignored does not fail',()=>{
 const h=harness('runWhack',0);for(let i=0;i<15;i++)h.tick(100);assert.equal(h.result,null);
});
check('Whack: tapping X fails',()=>{
 const h=harness('runWhack',0);h.tap(72,72);assert.equal(h.result,'fail');
});
check('Whack: seven correct taps win',()=>{
 const h=harness('runWhack',.99);
 for(let i=0;i<7;i++){h.tick(200);const positions=[[72,72],[180,66]];h.tap(...positions[i%2]);}
 assert.equal(h.result,'pass');
});
check('Waiter: idle loses at 60fps',()=>{
 const h=harness('runWaiterBalance',.99);
 for(let i=0;i<600&&!h.result;i++)h.tick(1000/60);
 assert.equal(h.result,'fail');
});
check('Waiter: responsive control can win',()=>{
 const h=harness('runWaiterBalance',.99);
 // Counter the deterministic bias before the shifts at 4.1s and 6.9s.
 h.slide(-.179*430);
 for(let i=0;i<600&&!h.result;i++){
  if(i===245)h.slide(.3536*430);
  if(i===409)h.slide(-.3492*430);
  h.tick(1000/60);
 }
 assert.equal(h.result,'pass');
});

check('Whack: two missed good targets lose',()=>{
 const h=harness('runWhack',.99);
 h.tick(1600); // first good target expires
 h.tick(200);  // second target appears
 h.tick(1600); // second good target expires
 assert.equal(h.result,'fail');
});
check('Whack: a wrong-location tap does not count as a hit',()=>{
 const h=harness('runWhack',.99);
 h.tap(350,210);
 assert.equal(h.result,null);
});
check('Waiter: idle loses at 30fps',()=>{
 const h=harness('runWaiterBalance',.99);
 for(let i=0;i<360&&!h.result;i++)h.tick(1000/30);
 assert.equal(h.result,'fail');
});
check('Waiter: idle loses at 120fps',()=>{
 const h=harness('runWaiterBalance',.99);
 for(let i=0;i<1200&&!h.result;i++)h.tick(1000/120);
 assert.equal(h.result,'fail');
});
