from pathlib import Path
p=Path('dont100-apk/app/src/main/assets/index.html')
s=p.read_text(encoding='utf-8')
s=s.replace('const BUILD="4.2.1-finalfix"','const BUILD="4.2.2-visualpro"')
s=s.replace('v4.2.1 FINAL</span>','v4.2.2 VISUAL PRO</span>')

old='''function drawArcadeBackdrop(ctx,kind,ts=0){
 ctx.save();const g=ctx.createLinearGradient(0,0,0,220);if(kind==="space"){g.addColorStop(0,"#07122f");g.addColorStop(1,"#172c67")}else if(kind==="terrace"){g.addColorStop(0,"#78d7ff");g.addColorStop(.58,"#d9f2ff");g.addColorStop(1,"#f8d797")}else if(kind==="road"){g.addColorStop(0,"#97d9ff");g.addColorStop(.55,"#d8eeff");g.addColorStop(1,"#595b6f")}else{g.addColorStop(0,"#0b1641");g.addColorStop(1,"#28195d")}ctx.fillStyle=g;ctx.fillRect(0,0,360,220);if(kind==="space"||kind==="night"){for(let i=0;i<34;i++){const x=(i*83+17)%360,y=(i*47+11)%200;ctx.globalAlpha=.35+((i%4)*.15);ctx.fillStyle=i%7===0?"#ffd85c":"#fff";ctx.beginPath();ctx.arc(x,y,(i%5===0?1.7:1),0,7);ctx.fill()}ctx.globalAlpha=1}if(kind==="space"){ctx.globalAlpha=.28;ctx.fillStyle="#7d62ff";ctx.beginPath();ctx.arc(35,190,60,Math.PI,0);ctx.fill();ctx.fillStyle="#3ac8ff";ctx.beginPath();ctx.arc(330,215,74,Math.PI,0);ctx.fill();ctx.globalAlpha=1}if(kind==="terrace"){ctx.globalAlpha=.5;ctx.fillStyle="#7fc768";ctx.beginPath();ctx.moveTo(0,150);ctx.lineTo(70,95);ctx.lineTo(130,145);ctx.lineTo(220,80);ctx.lineTo(360,148);ctx.lineTo(360,220);ctx.lineTo(0,220);ctx.fill();ctx.globalAlpha=.75;ctx.fillStyle="#67c7e8";ctx.fillRect(0,158,360,62);ctx.globalAlpha=1;ctx.fillStyle="#f4ead9";ctx.fillRect(0,190,360,30)}if(kind==="road"){ctx.fillStyle="#555968";ctx.beginPath();ctx.moveTo(115,220);ctx.lineTo(158,70);ctx.lineTo(202,70);ctx.lineTo(245,220);ctx.fill()}ctx.restore();
}'''
new='''function drawArcadeBackdrop(ctx,kind,ts=0){
 ctx.save();const g=ctx.createLinearGradient(0,0,0,220);
 if(kind==="space"){g.addColorStop(0,"#07122f");g.addColorStop(1,"#243d88")}
 else if(kind==="terrace"){g.addColorStop(0,"#71d5ff");g.addColorStop(.58,"#d8f3ff");g.addColorStop(1,"#ffd8a3")}
 else if(kind==="road"){g.addColorStop(0,"#9be3ff");g.addColorStop(.52,"#e7f7ff");g.addColorStop(1,"#6a6c82")}
 else if(kind==="sunset"){g.addColorStop(0,"#7d78ff");g.addColorStop(.55,"#ff9ab3");g.addColorStop(1,"#ffd88e")}
 else if(kind==="meadow"){g.addColorStop(0,"#8ee0ff");g.addColorStop(.65,"#e8fbff");g.addColorStop(1,"#c5ef9a")}
 else if(kind==="neon"){g.addColorStop(0,"#171d4d");g.addColorStop(1,"#34246f")}
 else {g.addColorStop(0,"#f8fbff");g.addColorStop(1,"#eef2ff")}
 ctx.fillStyle=g;ctx.fillRect(0,0,360,220);
 if(kind==="space"||kind==="neon"){for(let i=0;i<34;i++){const x=(i*83+17)%360,y=(i*47+11)%200;ctx.globalAlpha=.35+((i%4)*.15);ctx.fillStyle=i%7===0?"#ffd85c":"#fff";ctx.beginPath();ctx.arc(x,y,(i%5===0?1.8:1),0,7);ctx.fill()}ctx.globalAlpha=1}
 if(kind==="space"){ctx.globalAlpha=.34;ctx.fillStyle="#8d70ff";ctx.beginPath();ctx.arc(24,205,72,Math.PI,0);ctx.fill();ctx.fillStyle="#45d4ff";ctx.beginPath();ctx.arc(338,216,82,Math.PI,0);ctx.fill();ctx.globalAlpha=1}
 if(kind==="terrace"){ctx.globalAlpha=.62;ctx.fillStyle="#88c86c";ctx.beginPath();ctx.moveTo(0,150);ctx.lineTo(72,92);ctx.lineTo(135,145);ctx.lineTo(222,78);ctx.lineTo(360,148);ctx.lineTo(360,220);ctx.lineTo(0,220);ctx.fill();ctx.globalAlpha=.86;ctx.fillStyle="#65c8e8";ctx.fillRect(0,158,360,62);ctx.globalAlpha=1;ctx.fillStyle="#f7e7cb";ctx.fillRect(0,190,360,30);ctx.fillStyle="#fff";for(let i=0;i<8;i++){ctx.beginPath();ctx.arc(28+i*47,184+(i%2)*4,2.3,0,7);ctx.fill()}}
 if(kind==="road"){ctx.fillStyle="#53586b";ctx.beginPath();ctx.moveTo(112,220);ctx.lineTo(158,65);ctx.lineTo(202,65);ctx.lineTo(248,220);ctx.fill();ctx.strokeStyle="rgba(255,255,255,.8)";ctx.lineWidth=2;ctx.setLineDash([10,10]);roughLine(ctx,180,78,180,220);ctx.setLineDash([])}
 if(kind==="meadow"){ctx.fillStyle="#88ce72";ctx.beginPath();ctx.moveTo(0,170);ctx.quadraticCurveTo(90,128,180,169);ctx.quadraticCurveTo(270,120,360,165);ctx.lineTo(360,220);ctx.lineTo(0,220);ctx.fill();ctx.fillStyle="#fff";for(let i=0;i<10;i++){ctx.beginPath();ctx.arc((i*41+20)%360,182+(i%3)*9,2,0,7);ctx.fill()}}
 ctx.restore();
}'''
assert old in s
s=s.replace(old,new)

replacements = {
'''ctx.clearRect(0,0,360,220);ctx.strokeStyle="#111";ctx.lineWidth=3;ctx.strokeRect(p.x,199,p.w,8);ctx.beginPath();ctx.arc(b.x,b.y,7,0,7);ctx.stroke();ctx.font="900 13px system-ui";ctx.fillStyle="#111";ctx.fillText(`${bounces}/10`,12,20)''':
'''ctx.clearRect(0,0,360,220);drawArcadeBackdrop(ctx,"sunset",ts);ctx.fillStyle="#ffffff";ctx.strokeStyle="#26213b";ctx.lineWidth=2;ctx.shadowColor="rgba(70,56,255,.32)";ctx.shadowBlur=12;ctx.fillRect(p.x,198,p.w,9);ctx.strokeRect(p.x,198,p.w,9);ctx.shadowBlur=8;ctx.beginPath();ctx.arc(b.x,b.y,7,0,7);ctx.fillStyle="#fff";ctx.fill();ctx.stroke();ctx.shadowBlur=0;ctx.font="900 13px system-ui";ctx.fillStyle="#fff";ctx.fillText(`${bounces}/10`,12,20)''',
'''ctx.clearRect(0,0,360,220);ctx.strokeStyle="#111";ctx.fillStyle="#111";ctx.lineWidth=2;for(const it of items){ctx.font="900 20px system-ui";ctx.fillText(it.bad?"×":"★",it.x-7,it.y)}ctx.strokeRect(x-30,193,60,12);ctx.font="800 13px system-ui";ctx.fillText(`${got}/6`,12,20)''':
'''ctx.clearRect(0,0,360,220);drawArcadeBackdrop(ctx,"meadow",ts);ctx.lineWidth=2;for(const it of items){ctx.font="900 22px system-ui";ctx.fillStyle=it.bad?"#ff4f6f":"#ffd33d";ctx.strokeStyle="#28304c";ctx.strokeText(it.bad?"×":"★",it.x-8,it.y);ctx.fillText(it.bad?"×":"★",it.x-8,it.y)}ctx.fillStyle="#fff";ctx.strokeStyle="#28304c";ctx.beginPath();ctx.roundRect(x-32,190,64,16,8);ctx.fill();ctx.stroke();ctx.font="900 13px system-ui";ctx.fillStyle="#27304b";ctx.fillText(`${got}/6`,12,20)''',
'''ctx.clearRect(0,0,360,220);ctx.strokeStyle="#111";ctx.lineWidth=2;for(const d of drops){ctx.beginPath();ctx.arc(d.x,d.y,d.s,0,7);ctx.stroke()}drawDoodle(ctx,x,174,.72,"run",ts);ctx.fillStyle="#111";ctx.font="800 13px system-ui";ctx.fillText(`${Math.max(0,7-elapsed).toFixed(1)}s`,12,20)''':
'''ctx.clearRect(0,0,360,220);drawArcadeBackdrop(ctx,"meadow",ts);ctx.lineWidth=2;for(const d of drops){ctx.fillStyle="#5964d8";ctx.strokeStyle="#26304a";ctx.beginPath();ctx.arc(d.x,d.y,d.s,0,7);ctx.fill();ctx.stroke()}drawDoodle(ctx,x,174,.82,"run",ts);ctx.fillStyle="#27304b";ctx.font="900 13px system-ui";ctx.fillText(`${Math.max(0,7-elapsed).toFixed(1)}s`,12,20)''',
'''ctx.clearRect(0,0,360,220);ctx.strokeStyle="#111";ctx.lineWidth=2;for(const z of br)if(!z.dead)ctx.strokeRect(z.x,z.y,z.w,z.h);ctx.fillStyle="#111";ctx.fillRect(p.x,199,p.w,7);ctx.beginPath();ctx.arc(b.x,b.y,b.r,0,7);ctx.fill();ctx.font="800 13px system-ui";ctx.fillText(`${hits}/8`,12,20)''':
'''ctx.clearRect(0,0,360,220);drawArcadeBackdrop(ctx,"neon",ts);ctx.lineWidth=2;for(const z of br)if(!z.dead){const row=z.y<45?0:1;ctx.fillStyle=row===0?"#45d7ff":"#ffb547";ctx.strokeStyle="#fff";ctx.shadowColor=ctx.fillStyle;ctx.shadowBlur=10;ctx.fillRect(z.x,z.y,z.w,z.h);ctx.strokeRect(z.x,z.y,z.w,z.h)}ctx.shadowBlur=12;ctx.fillStyle="#fff";ctx.fillRect(p.x,198,p.w,8);ctx.shadowBlur=10;ctx.beginPath();ctx.arc(b.x,b.y,b.r,0,7);ctx.fill();ctx.shadowBlur=0;ctx.font="900 13px system-ui";ctx.fillStyle="#fff";ctx.fillText(`${hits}/8`,12,20)''',
}
for a,b in replacements.items():
    assert a in s, a[:80]
    s=s.replace(a,b)

old=''' const c=arcadeCanvas("Dodge Rain"),ctx=c.getContext("2d");let x=180,last=performance.now(),elapsed=0,spawn=0,drops=[];const move=e=>x=canvasPointerX(e,c);c.addEventListener("pointerdown",move);c.addEventListener("pointermove",move);'''
new=''' const c=arcadeCanvas("Dodge Rain"),ctx=c.getContext("2d");let x=180,last=performance.now(),elapsed=0,spawn=0,drops=[];const ctl=arcadeControlDeck("slide",tr("DESLIZA PARA ESQUIVAR","SLIDE TO DODGE","GLISSE POUR ESQUIVER"));bindRelativePad(ctl.pad,dx=>x=Math.max(22,Math.min(338,x+dx*1.5)));'''
assert old in s
s=s.replace(old,new)

extra=r'''
/* v4.2.2 VISUAL PRO — approved colorful arcade direction */
body.arcade-level .game-card{background:linear-gradient(180deg,#ffffff 0%,#fbfcff 100%);box-shadow:0 15px 40px rgba(34,42,92,.14),0 3px 0 rgba(20,25,56,.10)}
body.arcade-level .challenge h1{font-weight:1000;letter-spacing:-1.35px;text-shadow:0 2px 0 #fff}
body.arcade-level .challenge p{background:linear-gradient(90deg,color-mix(in srgb,var(--accent) 12%,#fff),#fff);border-left-width:4px}
body.arcade-level .arcade-wrap{border-color:#222946;box-shadow:0 12px 0 rgba(37,42,86,.10),0 20px 38px rgba(41,53,128,.18),inset 0 0 0 1px rgba(255,255,255,.55)}
body.arcade-level .arcade-control-deck{border-color:rgba(73,70,150,.24);background:linear-gradient(180deg,#fff,#f4f5ff);box-shadow:0 7px 0 rgba(51,48,116,.08),0 15px 28px rgba(58,58,130,.10)}
body.arcade-level .tag{background:linear-gradient(180deg,color-mix(in srgb,var(--accent) 78%,#fff),var(--accent));color:#fff;text-shadow:0 1px 0 rgba(0,0,0,.2)}
'''
s=s.replace('</style>',extra+'\n</style>',1)
p.write_text(s,encoding='utf-8')
print('patched',p.stat().st_size)
