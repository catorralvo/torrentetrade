from pathlib import Path
p=Path('dont100-apk/app/src/main/assets/index.html')
s=p.read_text(encoding='utf-8')
s=s.replace('const BUILD="4.3.0-pro3d-final"','const BUILD="4.3.1-gameplayfix"')
s=s.replace('v4.3 PRO 3D</span>','v4.3.1 GAMEPLAY FIX</span>')

def replace_function(src, name, new_fn):
    start=src.index('function '+name+'(')
    end=src.find('\nfunction ',start+10)
    if end<0: end=len(src)
    return src[:start]+new_fn+src[end:]

whack=r'''function runWhack(n,r,hard){
 setChallenge(tr("GOLPEA","WHACK","TAPE"),tr("GOLPEA 7 CARAS. EVITA LA X","HIT 7 FACES. AVOID X","TOUCHE 7 VISAGES. ÉVITE X"),tr("Las caras cambian de sitio. La X se deja pasar.","Faces move around. Let the X pass.","Les visages changent de place. Laisse passer le X."));
 const c=arcadeCanvas("Whack"),ctx=c.getContext("2d");
 const spots=[[72,72],[180,66],[288,74],[124,150],[238,148]];
 let target=null,got=0,misses=0,lastSpot=-1;
 const spawn=()=>{
   let idx=rint(r,0,spots.length-1);if(idx===lastSpot)idx=(idx+1)%spots.length;lastSpot=idx;
   const [x,y]=spots[idx],bad=r()<.22;
   target={x,y,bad,born:performance.now(),ttl:bad?820:Math.max(1050,1450-hard*28)};
 };
 const next=()=>{target=null;later(spawn,150)};
 spawn();
 c.addEventListener("pointerdown",e=>{
   if(!target)return;
   const x=canvasPointerX(e,c),y=canvasPointerY(e,c);
   if(Math.hypot(x-target.x,y-target.y)>34){tone(150,.035,"square",.008);return}
   if(target.bad)return fail(tr("¡Era la X!","That was X!","C'était X !"));
   got++;tone(390+got*38,.035,"sine",.025);
   if(got>=7)return pass();
   next();
 });
 startArcadeLoop(ts=>{
   if(target&&ts-target.born>target.ttl){
     if(target.bad){tone(250,.025,"sine",.008);next()}
     else{misses++;tone(120,.05,"square",.012);if(misses>=2)return fail(tr("Se escaparon dos caras.","Two faces got away.","Deux visages se sont échappés."));next()}
   }
   ctx.clearRect(0,0,360,220);drawArcadeBackdrop(ctx,"sunset",ts);
   ctx.fillStyle="rgba(255,255,255,.20)";ctx.strokeStyle="rgba(45,42,78,.40)";ctx.lineWidth=2;
   for(const [x,y] of spots){ctx.beginPath();ctx.ellipse(x,y+22,34,10,0,0,7);ctx.fill();ctx.stroke()}
   if(target){
     const age=Math.max(0,ts-target.born),scale=Math.min(1,age/115),rr=27*scale;
     ctx.save();ctx.translate(target.x,target.y);ctx.scale(scale,scale);
     ctx.shadowColor=target.bad?"rgba(255,55,75,.48)":"rgba(65,215,160,.45)";ctx.shadowBlur=14;
     const g=ctx.createRadialGradient(-8,-10,2,0,0,30);
     if(target.bad){g.addColorStop(0,"#ffb5bf");g.addColorStop(.45,"#ff5c70");g.addColorStop(1,"#c91e3d")}
     else{g.addColorStop(0,"#fff");g.addColorStop(.4,"#ffe7a7");g.addColorStop(1,"#ffb85f")}
     ctx.fillStyle=g;ctx.strokeStyle="#252642";ctx.lineWidth=3;ctx.beginPath();ctx.arc(0,0,27,0,7);ctx.fill();ctx.stroke();ctx.shadowBlur=0;
     if(target.bad){ctx.strokeStyle="#fff";ctx.lineWidth=5;roughLine(ctx,-11,-11,11,11);roughLine(ctx,11,-11,-11,11)}
     else{ctx.fillStyle="#252642";ctx.beginPath();ctx.arc(-8,-5,2.8,0,7);ctx.arc(8,-5,2.8,0,7);ctx.fill();ctx.strokeStyle="#252642";ctx.lineWidth=2.4;ctx.beginPath();ctx.arc(0,5,9,0,Math.PI);ctx.stroke()}
     ctx.restore();
   }
   ctx.fillStyle="#252642";ctx.font="900 13px system-ui";ctx.fillText(`${got}/7`,12,20);
   ctx.font="800 11px system-ui";ctx.fillStyle=misses?"#a93649":"#555a77";ctx.fillText(tr(`FALLOS ${misses}/2`,`MISSES ${misses}/2`,`RATÉS ${misses}/2`),270,20);
 });
}'''

waiter=r'''function runWaiterBalance(n,r,hard){
 setChallenge(tr("MESERO","WAITER","SERVEUR"),tr("NO DERRAMES EL VINO","DON'T SPILL THE WINE","NE RENVERSE PAS LE VIN"),tr("La tabla se desequilibra sola. Corrige constantemente con el control.","The board wobbles by itself. Keep correcting with the control.","La planche se déséquilibre seule. Corrige sans arrêt avec le contrôle."));
 const c=arcadeCanvas("Waiter Balance"),ctx=c.getContext("2d");
 let target=0,tilt=0,glass=0,vel=0,last=performance.now(),safe=0,spill=0;
 let side=r()<.5?-1:1,bias=side*(.155+r()*.025),nextShift=performance.now()+4100+rint(r,0,400);
 const ctl=arcadeControlDeck("slide",tr("DESLIZA PARA EQUILIBRAR","SLIDE TO BALANCE","GLISSE POUR ÉQUILIBRER"));
 bindRelativePad(ctl.pad,dx=>target=Math.max(-.30,Math.min(.30,target+dx/430)));
 startArcadeLoop(ts=>{
   const dt=Math.min(.03,(ts-last)/1000||0);last=ts;
   if(ts>=nextShift){side*=-1;bias=side*(.135+r()*.04);nextShift=ts+2800+rint(r,0,600);tone(210,.025,"sine",.008)}
   tilt+=(target+bias-tilt)*Math.min(1,dt*5.0);
   vel+=(tilt*120-glass*.06)*dt;vel*=.992;glass+=vel*dt;
   if(Math.abs(tilt)>.255)spill+=dt;else spill=Math.max(0,spill-dt*1.7);
   safe+=dt;
   if(Math.abs(glass)>64)return fail(tr("¡La copa cayó!","The glass fell!","Le verre est tombé !"));
   if(spill>.42)return fail(tr("¡Derramaste el vino!","You spilled the wine!","Tu as renversé le vin !"));
   if(safe>=8.5)return pass();
   ctx.clearRect(0,0,360,220);drawArcadeBackdrop(ctx,"terrace",ts);
   ctx.save();ctx.translate(180,158);ctx.rotate(tilt);
   ctx.shadowColor="rgba(80,45,20,.28)";ctx.shadowBlur=9;
   const wood=ctx.createLinearGradient(0,-7,0,8);wood.addColorStop(0,"#ffd99c");wood.addColorStop(.5,"#c97a3d");wood.addColorStop(1,"#82401f");
   ctx.fillStyle=wood;ctx.strokeStyle="#5c2c15";ctx.lineWidth=2;ctx.beginPath();ctx.roundRect(-112,-6,224,12,6);ctx.fill();ctx.stroke();ctx.shadowBlur=0;
   ctx.fillStyle="#aa7446";ctx.beginPath();ctx.arc(0,18,19,Math.PI,0);ctx.fill();ctx.stroke();
   ctx.save();ctx.translate(glass,-8);
   ctx.strokeStyle="#f8fbff";ctx.lineWidth=2;ctx.fillStyle="rgba(255,255,255,.24)";
   ctx.beginPath();ctx.moveTo(-9,-21);ctx.lineTo(-6,-5);ctx.quadraticCurveTo(0,2,6,-5);ctx.lineTo(9,-21);ctx.closePath();ctx.fill();ctx.stroke();
   const wineY=-10+Math.min(4,Math.abs(tilt)*14);ctx.fillStyle="#b51f42";ctx.beginPath();ctx.moveTo(-5,wineY);ctx.lineTo(5,wineY);ctx.lineTo(4,-5);ctx.quadraticCurveTo(0,-2,-4,-5);ctx.closePath();ctx.fill();
   ctx.strokeStyle="#eef7ff";roughLine(ctx,0,-3,0,9);roughLine(ctx,-7,9,7,9);ctx.restore();ctx.restore();
   drawDoodle(ctx,54,145,.75,"waiter",ts);
   ctx.fillStyle="#26304b";ctx.font="900 13px system-ui";ctx.fillText(`${Math.max(0,8.5-safe).toFixed(1)}s`,300,20);
   ctx.font="900 18px system-ui";ctx.fillStyle=bias<0?"#6a5cff":"#ff6e55";ctx.fillText(bias<0?"←":"→",172,24);
   ctx.font="800 10px system-ui";ctx.fillStyle="#545b74";ctx.fillText(tr("CORRIGE","CORRECT","CORRIGE"),145,39);
 });
}'''

s=replace_function(s,'runWhack',whack)
s=replace_function(s,'runWaiterBalance',waiter)

p.write_text(s,encoding='utf-8')
assert '4.3.1-gameplayfix' in s
assert 'Se escaparon dos caras' in s
assert 'La tabla se desequilibra sola' in s
assert 'spill>.42' in s
print('gameplay hotfix applied',p.stat().st_size)
