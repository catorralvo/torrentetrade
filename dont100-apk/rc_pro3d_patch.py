from pathlib import Path
p=Path('dont100-apk/app/src/main/assets/index.html')
s=p.read_text(encoding='utf-8')

s=s.replace('const BUILD="4.2.2-visualpro"','const BUILD="4.3.0-pro3d-final"')
s=s.replace('v4.2.2 VISUAL PRO</span>','v4.3 PRO 3D</span>')

s=s.replace('''ctx.setTransform(dpr,0,0,dpr,0,0);ctx.imageSmoothingEnabled=true;ctx.imageSmoothingQuality="high";return c;''',
'''ctx.setTransform(dpr,0,0,dpr,0,0);ctx.imageSmoothingEnabled=true;ctx.imageSmoothingQuality="high";ctx.lineCap="round";ctx.lineJoin="round";ctx.shadowColor="rgba(20,24,60,.18)";ctx.shadowBlur=3;ctx.shadowOffsetY=1.5;return c;''')

old='''function startArcadeLoop(draw){let raf=0,alive=true;const loop=ts=>{if(!alive||state.resolved||state.failed)return;draw(ts);raf=requestAnimationFrame(loop)};raf=requestAnimationFrame(loop);state.cleanup.push(()=>{alive=false;cancelAnimationFrame(raf)})}'''
new='''function arcadePostFX(ts){
 const c=document.querySelector(".arcade-canvas");if(!c)return;const ctx=c.getContext("2d");ctx.save();ctx.shadowBlur=0;ctx.shadowOffsetY=0;
 const vg=ctx.createRadialGradient(180,95,70,180,110,235);vg.addColorStop(0,"rgba(255,255,255,0)");vg.addColorStop(.72,"rgba(20,24,58,.025)");vg.addColorStop(1,"rgba(12,14,40,.15)");ctx.fillStyle=vg;ctx.fillRect(0,0,360,220);
 const shine=ctx.createLinearGradient(0,0,0,70);shine.addColorStop(0,"rgba(255,255,255,.22)");shine.addColorStop(1,"rgba(255,255,255,0)");ctx.fillStyle=shine;ctx.fillRect(0,0,360,72);
 ctx.strokeStyle="rgba(255,255,255,.36)";ctx.lineWidth=1;ctx.strokeRect(.5,.5,359,219);ctx.restore();
}
function startArcadeLoop(draw){let raf=0,alive=true;const loop=ts=>{if(!alive||state.resolved||state.failed)return;draw(ts);arcadePostFX(ts);raf=requestAnimationFrame(loop)};raf=requestAnimationFrame(loop);state.cleanup.push(()=>{alive=false;cancelAnimationFrame(raf)})}'''
assert old in s
s=s.replace(old,new)

# Star Blaster: solid, glowing 3D-inspired ships and lasers.
old='''ctx.clearRect(0,0,360,220);drawArcadeBackdrop(ctx,"space",ts);ctx.fillStyle="#fff";ctx.strokeStyle="#f7f8ff";ctx.lineWidth=2.2;ctx.beginPath();ctx.moveTo(player.x,196);ctx.lineTo(player.x-13,211);ctx.lineTo(player.x+13,211);ctx.closePath();ctx.stroke();for(const b of bullets){ctx.fillRect(b.x-1,b.y-6,2,8)}for(const e of enemies){ctx.beginPath();ctx.moveTo(e.x-10,e.y);ctx.lineTo(e.x,e.y+8);ctx.lineTo(e.x+10,e.y);ctx.lineTo(e.x+5,e.y+12);ctx.lineTo(e.x-5,e.y+12);ctx.closePath();ctx.stroke()}ctx.font="800 13px system-ui";ctx.fillText(`${hits}/8`,12,20)'''
new='''ctx.clearRect(0,0,360,220);drawArcadeBackdrop(ctx,"space",ts);ctx.lineWidth=2;ctx.shadowColor="#55d9ff";ctx.shadowBlur=13;let pg=ctx.createLinearGradient(player.x,194,player.x,214);pg.addColorStop(0,"#f9feff");pg.addColorStop(.45,"#65d8ff");pg.addColorStop(1,"#6855ff");ctx.fillStyle=pg;ctx.strokeStyle="#fff";ctx.beginPath();ctx.moveTo(player.x,194);ctx.lineTo(player.x-15,212);ctx.lineTo(player.x,207);ctx.lineTo(player.x+15,212);ctx.closePath();ctx.fill();ctx.stroke();ctx.shadowBlur=10;for(const b of bullets){ctx.fillStyle="#fff56b";ctx.fillRect(b.x-1.5,b.y-8,3,10)}for(const e of enemies){const eg=ctx.createLinearGradient(e.x,e.y,e.x,e.y+14);eg.addColorStop(0,"#ff9bd2");eg.addColorStop(1,"#ff4b72");ctx.fillStyle=eg;ctx.strokeStyle="#fff";ctx.beginPath();ctx.moveTo(e.x-11,e.y);ctx.lineTo(e.x,e.y+7);ctx.lineTo(e.x+11,e.y);ctx.lineTo(e.x+6,e.y+13);ctx.lineTo(e.x-6,e.y+13);ctx.closePath();ctx.fill();ctx.stroke()}ctx.shadowBlur=0;ctx.font="900 13px system-ui";ctx.fillStyle="#fff";ctx.fillText(`${hits}/8`,12,20)'''
assert old in s
s=s.replace(old,new)

# Paddle: 3D paddle and ball.
old='''ctx.fillStyle="#ffffff";ctx.strokeStyle="#26213b";ctx.lineWidth=2;ctx.shadowColor="rgba(70,56,255,.32)";ctx.shadowBlur=12;ctx.fillRect(p.x,198,p.w,9);ctx.strokeRect(p.x,198,p.w,9);ctx.shadowBlur=8;ctx.beginPath();ctx.arc(b.x,b.y,7,0,7);ctx.fillStyle="#fff";ctx.fill();ctx.stroke();ctx.shadowBlur=0;'''
new='''ctx.strokeStyle="#26213b";ctx.lineWidth=2;ctx.shadowColor="rgba(70,56,255,.38)";ctx.shadowBlur=14;const pg=ctx.createLinearGradient(p.x,198,p.x,208);pg.addColorStop(0,"#fff");pg.addColorStop(.45,"#77d6ff");pg.addColorStop(1,"#7358ff");ctx.fillStyle=pg;ctx.beginPath();ctx.roundRect(p.x,197,p.w,11,6);ctx.fill();ctx.stroke();ctx.shadowBlur=12;const bg=ctx.createRadialGradient(b.x-3,b.y-4,1,b.x,b.y,9);bg.addColorStop(0,"#fff");bg.addColorStop(.35,"#fff3a6");bg.addColorStop(1,"#ff9d38");ctx.beginPath();ctx.arc(b.x,b.y,8,0,7);ctx.fillStyle=bg;ctx.fill();ctx.stroke();ctx.shadowBlur=0;'''
assert old in s
s=s.replace(old,new)

# Waiter: colored terrace, wood plank, wine glass with red wine.
old='''ctx.clearRect(0,0,360,220);drawArcadeBackdrop(ctx,"terrace",ts);ctx.save();ctx.translate(180,158);ctx.rotate(tilt);ctx.strokeStyle="#2c2118";ctx.lineWidth=4;roughLine(ctx,-110,0,110,0);ctx.beginPath();ctx.arc(0,17,17,Math.PI,0);ctx.stroke();ctx.save();ctx.translate(glass,-7);ctx.strokeRect(-7,-18,14,15);roughLine(ctx,0,-3,0,8);roughLine(ctx,-7,8,7,8);ctx.restore();ctx.restore();drawDoodle(ctx,54,145,.75,"waiter",ts);ctx.fillStyle="#111";ctx.font="800 13px system-ui";ctx.fillText(`${Math.max(0,7-safe).toFixed(1)}s`,300,20)'''
new='''ctx.clearRect(0,0,360,220);drawArcadeBackdrop(ctx,"terrace",ts);ctx.save();ctx.translate(180,158);ctx.rotate(tilt);ctx.shadowColor="rgba(80,45,20,.26)";ctx.shadowBlur=8;const wood=ctx.createLinearGradient(0,-6,0,7);wood.addColorStop(0,"#ffd08b");wood.addColorStop(.5,"#c97a3d");wood.addColorStop(1,"#8f4b26");ctx.fillStyle=wood;ctx.strokeStyle="#633116";ctx.lineWidth=2;ctx.beginPath();ctx.roundRect(-112,-5,224,10,5);ctx.fill();ctx.stroke();ctx.shadowBlur=0;ctx.fillStyle="#ab7547";ctx.beginPath();ctx.arc(0,17,18,Math.PI,0);ctx.fill();ctx.stroke();ctx.save();ctx.translate(glass,-7);ctx.strokeStyle="#f9fbff";ctx.lineWidth=2;ctx.fillStyle="rgba(255,255,255,.20)";ctx.beginPath();ctx.moveTo(-8,-20);ctx.lineTo(-6,-5);ctx.quadraticCurveTo(0,1,6,-5);ctx.lineTo(8,-20);ctx.closePath();ctx.fill();ctx.stroke();ctx.fillStyle="#b72547";ctx.fillRect(-5,-10,10,5);ctx.strokeStyle="#eef7ff";roughLine(ctx,0,-3,0,8);roughLine(ctx,-7,8,7,8);ctx.restore();ctx.restore();drawDoodle(ctx,54,145,.75,"waiter",ts);ctx.fillStyle="#26304b";ctx.font="900 13px system-ui";ctx.fillText(`${Math.max(0,7-safe).toFixed(1)}s`,300,20)'''
assert old in s
s=s.replace(old,new)

# Dodge: shiny hazards.
s=s.replace('''ctx.lineWidth=2;for(const d of drops){ctx.fillStyle="#5964d8";ctx.strokeStyle="#26304a";ctx.beginPath();ctx.arc(d.x,d.y,d.s,0,7);ctx.fill();ctx.stroke()}''',
'''ctx.lineWidth=2;for(const d of drops){const dg=ctx.createRadialGradient(d.x-d.s*.35,d.y-d.s*.4,1,d.x,d.y,d.s);dg.addColorStop(0,"#fff");dg.addColorStop(.3,"#85a2ff");dg.addColorStop(1,"#4a41c9");ctx.fillStyle=dg;ctx.strokeStyle="#26304a";ctx.beginPath();ctx.arc(d.x,d.y,d.s,0,7);ctx.fill();ctx.stroke()}''',1)

# Catch Stars: beveled stars and basket.
old='''for(const it of items){ctx.font="900 22px system-ui";ctx.fillStyle=it.bad?"#ff4f6f":"#ffd33d";ctx.strokeStyle="#28304c";ctx.strokeText(it.bad?"×":"★",it.x-8,it.y);ctx.fillText(it.bad?"×":"★",it.x-8,it.y)}ctx.fillStyle="#fff";ctx.strokeStyle="#28304c";ctx.beginPath();ctx.roundRect(x-32,190,64,16,8);ctx.fill();ctx.stroke();'''
new='''for(const it of items){ctx.font="900 23px system-ui";ctx.shadowColor=it.bad?"rgba(255,79,111,.45)":"rgba(255,211,61,.55)";ctx.shadowBlur=8;ctx.fillStyle=it.bad?"#ff4f6f":"#ffd33d";ctx.strokeStyle="#28304c";ctx.strokeText(it.bad?"×":"★",it.x-8,it.y);ctx.fillText(it.bad?"×":"★",it.x-8,it.y)}ctx.shadowBlur=9;ctx.shadowColor="rgba(63,77,150,.25)";const cg=ctx.createLinearGradient(x,190,x,208);cg.addColorStop(0,"#fff");cg.addColorStop(1,"#91c6ff");ctx.fillStyle=cg;ctx.strokeStyle="#28304c";ctx.beginPath();ctx.roundRect(x-32,190,64,16,8);ctx.fill();ctx.stroke();ctx.shadowBlur=0;'''
assert old in s
s=s.replace(old,new)

# Breakout: stronger 3D bricks/paddle.
s=s.replace('''ctx.fillStyle=row===0?"#45d7ff":"#ffb547";ctx.strokeStyle="#fff";ctx.shadowColor=ctx.fillStyle;ctx.shadowBlur=10;ctx.fillRect(z.x,z.y,z.w,z.h);ctx.strokeRect(z.x,z.y,z.w,z.h)''',
'''const brg=ctx.createLinearGradient(z.x,z.y,z.x,z.y+z.h);brg.addColorStop(0,"#fff");brg.addColorStop(.28,row===0?"#6ee8ff":"#ffd071");brg.addColorStop(1,row===0?"#2aa6ff":"#ff7f3d");ctx.fillStyle=brg;ctx.strokeStyle="#fff";ctx.shadowColor=row===0?"#45d7ff":"#ff9847";ctx.shadowBlur=11;ctx.beginPath();ctx.roundRect(z.x,z.y,z.w,z.h,4);ctx.fill();ctx.stroke()''',1)

# Flappy: richer sky, pipe shading.
old='''ctx.fillStyle="#66c56d";ctx.strokeStyle="#205b2a";ctx.fillRect(g.x-8,0,16,g.g-g.gap/2);ctx.fillRect(g.x-8,g.g+g.gap/2,16,220-(g.g+g.gap/2));ctx.strokeRect(g.x-8,0,16,g.g-g.gap/2);ctx.strokeRect(g.x-8,g.g+g.gap/2,16,220-(g.g+g.gap/2))'''
new='''const pipe=ctx.createLinearGradient(g.x-8,0,g.x+8,0);pipe.addColorStop(0,"#2f9e56");pipe.addColorStop(.45,"#8cf27f");pipe.addColorStop(1,"#277c46");ctx.fillStyle=pipe;ctx.strokeStyle="#1f5d39";ctx.shadowColor="rgba(40,100,60,.25)";ctx.shadowBlur=6;ctx.fillRect(g.x-8,0,16,g.g-g.gap/2);ctx.fillRect(g.x-8,g.g+g.gap/2,16,220-(g.g+g.gap/2));ctx.strokeRect(g.x-8,0,16,g.g-g.gap/2);ctx.strokeRect(g.x-8,g.g+g.gap/2,16,220-(g.g+g.gap/2));ctx.shadowBlur=0'''
assert old in s
s=s.replace(old,new)

# Cup shuffle: stronger 3D cups and floor shadow.
s=s.replace('''ctx.fillStyle=pos===0?"#80d8ff":pos===1?"#9d7cff":"#ffb56b";ctx.strokeStyle="#20233a";ctx.beginPath();ctx.moveTo(x-24,95);ctx.lineTo(x-18,155);ctx.lineTo(x+18,155);ctx.lineTo(x+24,95);ctx.closePath();ctx.fill();ctx.stroke();ctx.fillStyle="rgba(255,255,255,.45)";ctx.fillRect(x-12,103,8,40);''',
'''ctx.shadowColor="rgba(42,43,80,.22)";ctx.shadowBlur=10;ctx.shadowOffsetY=5;const cupg=ctx.createLinearGradient(x-24,0,x+24,0);const base=pos===0?"#43bce8":pos===1?"#7658df":"#f29a4d";cupg.addColorStop(0,base);cupg.addColorStop(.42,"#fff");cupg.addColorStop(.55,base);cupg.addColorStop(1,"#3f3d73");ctx.fillStyle=cupg;ctx.strokeStyle="#20233a";ctx.beginPath();ctx.moveTo(x-24,95);ctx.lineTo(x-18,155);ctx.lineTo(x+18,155);ctx.lineTo(x+24,95);ctx.closePath();ctx.fill();ctx.stroke();ctx.shadowBlur=0;ctx.shadowOffsetY=0;ctx.fillStyle="rgba(255,255,255,.42)";ctx.fillRect(x-13,103,7,39);''',1)

# Keep-up: 3D ball.
old='''ctx.clearRect(0,0,360,220);ctx.strokeStyle="#111";ctx.lineWidth=2;ctx.beginPath();ctx.arc(x,y,12,0,7);ctx.stroke();drawDoodle(ctx,180,190,.55,"run",ts);ctx.fillStyle="#111";'''
new='''ctx.clearRect(0,0,360,220);drawArcadeBackdrop(ctx,"meadow",ts);ctx.strokeStyle="#24304b";ctx.lineWidth=2;ctx.shadowColor="rgba(255,125,65,.35)";ctx.shadowBlur=10;const kg=ctx.createRadialGradient(x-4,y-5,2,x,y,13);kg.addColorStop(0,"#fff");kg.addColorStop(.35,"#ffd171");kg.addColorStop(1,"#ff6b49");ctx.fillStyle=kg;ctx.beginPath();ctx.arc(x,y,12,0,7);ctx.fill();ctx.stroke();ctx.shadowBlur=0;drawDoodle(ctx,180,190,.62,"run",ts);ctx.fillStyle="#24304b";'''
assert old in s
s=s.replace(old,new)

# Laser maze: neon 3D field.
old='''startArcadeLoop(ts=>{ctx.clearRect(0,0,360,220);ctx.fillStyle="#111";for(const w of walls)ctx.fillRect(w.x,w.y,w.w,w.h);ctx.strokeStyle="#111";ctx.strokeRect(330,10,25,35);ctx.beginPath();ctx.arc(x,y,7,0,7);ctx.fill();ctx.font="800 11px system-ui";ctx.fillText(tr("META","GOAL","BUT"),320,60)})'''
new='''startArcadeLoop(ts=>{ctx.clearRect(0,0,360,220);drawArcadeBackdrop(ctx,"neon",ts);ctx.shadowColor="#ff3fc8";ctx.shadowBlur=12;ctx.fillStyle="#ff43cf";for(const w of walls){ctx.fillRect(w.x,w.y,w.w,w.h);ctx.fillStyle="#7d55ff";ctx.fillRect(w.x+4,w.y,w.w-8,w.h);ctx.fillStyle="#ff43cf"}ctx.shadowColor="#62f2ff";ctx.strokeStyle="#62f2ff";ctx.lineWidth=3;ctx.strokeRect(330,10,25,35);ctx.fillStyle="#fff";ctx.beginPath();ctx.arc(x,y,7,0,7);ctx.fill();ctx.shadowBlur=0;ctx.font="900 11px system-ui";ctx.fillStyle="#fff";ctx.fillText(tr("META","GOAL","BUT"),318,60)})'''
assert old in s
s=s.replace(old,new)

# Gate run: glowing gates and player.
old='''ctx.clearRect(0,0,360,220);ctx.strokeStyle="#111";ctx.lineWidth=4;for(const g of gates){roughLine(ctx,0,g.y,g.g-g.gap/2,g.y);roughLine(ctx,g.g+g.gap/2,g.y,360,g.y)}ctx.fillStyle="#111";ctx.beginPath();ctx.arc(x,194,8,0,7);ctx.fill();'''
new='''ctx.clearRect(0,0,360,220);drawArcadeBackdrop(ctx,"space",ts);ctx.strokeStyle="#68e4ff";ctx.shadowColor="#68e4ff";ctx.shadowBlur=10;ctx.lineWidth=5;for(const g of gates){roughLine(ctx,0,g.y,g.g-g.gap/2,g.y);roughLine(ctx,g.g+g.gap/2,g.y,360,g.y)}ctx.fillStyle="#fff";ctx.shadowColor="#ffdd69";ctx.beginPath();ctx.arc(x,194,8,0,7);ctx.fill();ctx.shadowBlur=0;'''
assert old in s
s=s.replace(old,new)

extra=r'''
/* v4.3 PRO 3D — professional depth and arcade polish */
body.arcade-level{background:
  radial-gradient(circle at 12% 5%,rgba(99,77,255,.20),transparent 28%),
  radial-gradient(circle at 88% 7%,rgba(47,199,255,.16),transparent 27%),
  linear-gradient(180deg,#f8fbff,#eef1fb)}
body.arcade-level .game-card{border-color:rgba(31,37,76,.86);box-shadow:0 22px 55px rgba(41,48,103,.18),0 7px 0 rgba(37,42,86,.09);transform:translateZ(0)}
body.arcade-level .arcade-wrap{position:relative;perspective:900px;transform:rotateX(.65deg);transform-origin:center bottom;border:2px solid rgba(27,32,69,.88);box-shadow:0 18px 35px rgba(35,43,108,.22),0 7px 0 rgba(31,35,82,.13),inset 0 0 0 1px rgba(255,255,255,.5)}
body.arcade-level .arcade-wrap::after{content:"";position:absolute;inset:0;border-radius:22px;pointer-events:none;background:linear-gradient(155deg,rgba(255,255,255,.26),transparent 23%,transparent 70%,rgba(255,255,255,.08));mix-blend-mode:screen}
body.arcade-level .arcade-control-deck{transform:perspective(800px) rotateX(1.1deg);transform-origin:center top;border:1px solid rgba(64,64,140,.28);box-shadow:0 11px 0 rgba(44,43,99,.09),0 18px 30px rgba(51,58,130,.14),inset 0 1px 0 #fff}
body.arcade-level .arcade-trackpad{box-shadow:inset 0 4px 12px rgba(61,64,154,.14),inset 0 -2px 0 rgba(255,255,255,.7)}
body.arcade-level .control-thumb{background:linear-gradient(145deg,#a68bff 0%,#6753ff 42%,#3d5de2 100%);box-shadow:0 7px 0 #30399b,0 12px 18px rgba(61,64,154,.24),inset 0 2px 0 rgba(255,255,255,.65)}
body.arcade-level .arcade-fire-btn{background:radial-gradient(circle at 36% 25%,#ff9bb1 0 10%,#ff4d79 32%,#d80f44 100%);box-shadow:0 7px 0 #941534,0 12px 19px rgba(183,24,67,.27),inset 0 2px 0 rgba(255,255,255,.55)}
@media(max-height:760px){body.arcade-level .arcade-wrap{transform:none}body.arcade-level .arcade-control-deck{transform:none}}
'''
s=s.replace('</style>',extra+'\n</style>',1)

p.write_text(s,encoding='utf-8')
assert '4.3.0-pro3d-final' in s
assert 'arcadePostFX' in s
print('PRO3D patch applied',p.stat().st_size)
