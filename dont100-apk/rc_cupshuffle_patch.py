from pathlib import Path
p=Path('dont100-apk/app/src/main/assets/index.html')
s=p.read_text(encoding='utf-8')
start=s.index('function runCupShuffle(')
end=s.index('\nfunction ',start+10)
new=r'''function runCupShuffle(n,r,hard){
 setChallenge(tr("VASOS","CUP SHUFFLE","GOBELETS"),tr("SIGUE LA PELOTA","FOLLOW THE BALL","SUIS LA BALLE"),tr("Sigue el vaso durante los intercambios. Elige al terminar.","Follow the cup during each swap. Choose at the end.","Suis le gobelet pendant les échanges. Choisis à la fin."));
 const c=arcadeCanvas("Cup Shuffle"),ctx=c.getContext("2d"),xs=[90,180,270];
 const ball=rint(r,0,2),order=[0,1,2],swaps=4+Math.min(3,Math.floor(hard/3));
 let step=0,nextSwap=performance.now()+1100,swap=null,ready=false;
 c.addEventListener("pointerdown",e=>{
  if(!ready)return;
  const x=canvasPointerX(e,c),y=canvasPointerY(e,c);
  if(y<72||y>200||x<40||x>320)return;
  const chosen=x<135?0:x>225?2:1;
  order[chosen]===ball?pass():fail(tr("Estaba en otro vaso.","Wrong cup.","Mauvais gobelet."));
 });
 startArcadeLoop(ts=>{
  if(swap&&ts>=swap.end){
   [order[swap.a],order[swap.b]]=[order[swap.b],order[swap.a]];
   swap=null;nextSwap=ts+200;
  }
  if(!ready&&!swap&&ts>=nextSwap){
   if(step>=swaps)ready=true;
   else{
    const a=rint(r,0,2),b=(a+rint(r,1,2))%3;
    swap={a,b,start:ts,end:ts+440};step++;
   }
  }
  ctx.clearRect(0,0,360,220);drawArcadeBackdrop(ctx,"sunset",ts);
  ctx.fillStyle="rgba(35,39,78,.14)";ctx.fillRect(0,182,360,3);
  const smooth=t=>t*t*(3-2*t);
  const progress=swap?smooth(Math.max(0,Math.min(1,(ts-swap.start)/(swap.end-swap.start)))):0;
  for(let pos=0;pos<3;pos++){
   const cupId=order[pos];
   let x=xs[pos],lift=0;
   if(swap&&pos===swap.a){x=xs[swap.a]+(xs[swap.b]-xs[swap.a])*progress;lift=-22*Math.sin(Math.PI*progress)}
   if(swap&&pos===swap.b){x=xs[swap.b]+(xs[swap.a]-xs[swap.b])*progress;lift=22*Math.sin(Math.PI*progress)}
   ctx.save();ctx.translate(x,lift);
   ctx.shadowColor="rgba(42,43,80,.22)";ctx.shadowBlur=9;ctx.shadowOffsetY=5;
   const g=ctx.createLinearGradient(-24,0,24,0);
   const base=["#43bce8","#7658df","#f29a4d"][cupId];
   g.addColorStop(0,base);g.addColorStop(.42,"#fff");g.addColorStop(.55,base);g.addColorStop(1,"#3f3d73");
   ctx.fillStyle=g;ctx.strokeStyle="#20233a";ctx.lineWidth=3;
   ctx.beginPath();ctx.moveTo(-24,95);ctx.lineTo(-18,155);ctx.lineTo(18,155);ctx.lineTo(24,95);ctx.closePath();ctx.fill();ctx.stroke();
   ctx.shadowBlur=0;ctx.shadowOffsetY=0;ctx.fillStyle="rgba(255,255,255,.42)";ctx.fillRect(-13,103,7,39);
   if(step===0&&cupId===ball){ctx.beginPath();ctx.arc(0,174,8,0,7);ctx.fillStyle="#5d46ff";ctx.fill();ctx.strokeStyle="#20233a";ctx.stroke()}
   ctx.restore();
  }
  ctx.fillStyle="#20233a";ctx.font="900 13px system-ui";
  ctx.fillText(ready?tr("ELIGE","CHOOSE","CHOISIS"):tr("MIRA","WATCH","REGARDE"),12,20);
  if(!ready){ctx.font="800 12px system-ui";ctx.fillText(step+"/"+swaps,320,20)}
 });
 // No arbitrary timeout: choosing after the shuffle is a deliberate player action.
}'''
s=s[:start]+new+s[end:]
p.write_text(s,encoding='utf-8')
assert s.count('function runCupShuffle(')==1
print('Cup Shuffle animated swaps applied')
