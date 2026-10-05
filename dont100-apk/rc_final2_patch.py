from pathlib import Path
p=Path('dont100-apk/app/src/main/assets/index.html')
s=p.read_text(encoding='utf-8')

s=s.replace('const BUILD="4.2.0-final"','const BUILD="4.2.1-finalfix"')
s=s.replace('v4.2 FINAL</span>','v4.2.1 FINAL</span>')
s=s.replace('tapcount:"tap",mascottap:"tap",jumprope:"arcade",donttap','tapcount:"tap",mascottap:"tap",jumprope:"tap",donttap')

s=s.replace('.arcade-wrap{width:min(100%,430px);height:auto!important;aspect-ratio:360/220;border:2px solid rgba(14,18,48,.92);border-radius:24px;overflow:hidden;background:#101738;',
            '.arcade-wrap{width:min(100%,430px);height:auto!important;aspect-ratio:360/220;border:2px solid rgba(14,18,48,.92);border-radius:24px;overflow:hidden;background:linear-gradient(180deg,#fafdff,#eef3ff);')
s=s.replace('.arcade-canvas{display:block;width:100%;height:100%!important;background:transparent;touch-action:none}',
            '.arcade-canvas{display:block;width:100%;height:100%!important;background:linear-gradient(180deg,#fbfdff 0%,#edf3ff 100%);touch-action:none}')

old='''ctx.clearRect(0,0,360,220);ctx.strokeStyle="#111";ctx.lineWidth=3;for(let pos=0;pos<3;pos++){const cupId=order[pos],x=xs[pos];ctx.beginPath();ctx.moveTo(x-24,95);ctx.lineTo(x-18,155);ctx.lineTo(x+18,155);ctx.lineTo(x+24,95);ctx.closePath();ctx.stroke();if(step===0&&cupId===ball){ctx.beginPath();ctx.arc(x,174,7,0,7);ctx.fillStyle="#111";ctx.fill()}}ctx.fillStyle="#111";ctx.font="800 13px system-ui";ctx.fillText(ready?tr("ELIGE","CHOOSE","CHOISIS"):tr("MIRA","WATCH","REGARDE"),12,20)'''
new='''ctx.clearRect(0,0,360,220);const cg=ctx.createLinearGradient(0,0,0,220);cg.addColorStop(0,"#fffdf8");cg.addColorStop(1,"#eef4ff");ctx.fillStyle=cg;ctx.fillRect(0,0,360,220);ctx.lineWidth=3;for(let pos=0;pos<3;pos++){const cupId=order[pos],x=xs[pos];ctx.fillStyle=pos===0?"#80d8ff":pos===1?"#9d7cff":"#ffb56b";ctx.strokeStyle="#20233a";ctx.beginPath();ctx.moveTo(x-24,95);ctx.lineTo(x-18,155);ctx.lineTo(x+18,155);ctx.lineTo(x+24,95);ctx.closePath();ctx.fill();ctx.stroke();ctx.fillStyle="rgba(255,255,255,.45)";ctx.fillRect(x-12,103,8,40);if(step===0&&cupId===ball){ctx.beginPath();ctx.arc(x,174,8,0,7);ctx.fillStyle="#5d46ff";ctx.fill();ctx.strokeStyle="#20233a";ctx.stroke()}}ctx.fillStyle="#20233a";ctx.font="900 13px system-ui";ctx.fillText(ready?tr("ELIGE","CHOOSE","CHOISIS"):tr("MIRA","WATCH","REGARDE"),12,20)'''
s=s.replace(old,new)

old='''ctx.clearRect(0,0,360,220);ctx.strokeStyle="#111";ctx.lineWidth=2;for(const it of items){ctx.beginPath();ctx.arc(it.x,it.y,14,0,7);ctx.stroke();if(it.bad){roughLine(ctx,it.x-8,it.y-8,it.x+8,it.y+8);roughLine(ctx,it.x+8,it.y-8,it.x-8,it.y+8)}}ctx.fillStyle="#111";ctx.font="800 13px system-ui";ctx.fillText(`${got}/6`,12,20)'''
new='''ctx.clearRect(0,0,360,220);ctx.fillStyle="#f5f8ff";ctx.fillRect(0,0,360,220);ctx.lineWidth=2;for(const it of items){ctx.beginPath();ctx.arc(it.x,it.y,it.bad?16:15,0,7);ctx.fillStyle=it.bad?"#2b2d42":"#7c5cff";ctx.strokeStyle="#20233a";ctx.fill();ctx.stroke();if(it.bad){ctx.strokeStyle="#ff5a68";ctx.lineWidth=3;roughLine(ctx,it.x-8,it.y-8,it.x+8,it.y+8);roughLine(ctx,it.x+8,it.y-8,it.x-8,it.y+8);ctx.lineWidth=2}else{ctx.fillStyle="rgba(255,255,255,.55)";ctx.beginPath();ctx.arc(it.x-5,it.y-5,4,0,7);ctx.fill()}}ctx.fillStyle="#20233a";ctx.font="900 13px system-ui";ctx.fillText(`${got}/6`,12,20)'''
s=s.replace(old,new)

old='''ctx.clearRect(0,0,360,220);ctx.strokeStyle="#111";ctx.fillStyle="#111";ctx.lineWidth=2;for(const it of items){ctx.beginPath();ctx.arc(it.x,it.y,18,0,7);ctx.stroke();roughLine(ctx,it.x,it.y+18,it.x,it.y+34);ctx.font="900 14px system-ui";ctx.fillText(String(it.v),it.x-4,it.y+5)}ctx.font="800 13px system-ui";ctx.fillText(`${got}/6`,12,20)'''
new='''ctx.clearRect(0,0,360,220);const bg=ctx.createLinearGradient(0,0,0,220);bg.addColorStop(0,"#eef9ff");bg.addColorStop(1,"#fff7ef");ctx.fillStyle=bg;ctx.fillRect(0,0,360,220);ctx.lineWidth=2;for(const it of items){ctx.beginPath();ctx.ellipse(it.x,it.y,17,21,0,0,7);ctx.fillStyle=(it.v%2===0)?"#58c7ff":"#9a6cff";ctx.strokeStyle="#20233a";ctx.fill();ctx.stroke();ctx.strokeStyle="#6a6478";roughLine(ctx,it.x,it.y+20,it.x+Math.sin(it.y*.1)*3,it.y+37);ctx.fillStyle="#fff";ctx.font="900 14px system-ui";ctx.textAlign="center";ctx.fillText(String(it.v),it.x,it.y+5)}ctx.textAlign="left";ctx.fillStyle="#20233a";ctx.font="900 13px system-ui";ctx.fillText(`${got}/6`,12,20)'''
s=s.replace(old,new)

old=''' const c=arcadeCanvas("Flappy doodle"),ctx=c.getContext("2d");let y=105,vy=0,last=performance.now(),passed=0,gates=[],spawn=0;const flap=()=>{vy=-145;tone(520,.025,"square",.012)};c.addEventListener("pointerdown",flap);'''
new=''' const c=arcadeCanvas("Flappy doodle"),ctx=c.getContext("2d");let y=105,vy=0,last=performance.now(),passed=0,gates=[],spawn=0;const flap=()=>{vy=-145;tone(520,.025,"square",.012)};const ctl=arcadeControlDeck("tap",tr("TOCA AQUÍ PARA SUBIR","TAP HERE TO FLAP","TOUCHE ICI POUR MONTER"));ctl.pad.innerHTML=`<b class="flap-pad-label">${tr("TOCA PARA SUBIR","TAP TO FLAP","TOUCHE POUR MONTER")}</b>`;ctl.pad.addEventListener("pointerdown",flap);'''
s=s.replace(old,new)

old='''ctx.clearRect(0,0,360,220);ctx.strokeStyle="#111";ctx.lineWidth=3;for(const g of gates){ctx.beginPath();ctx.moveTo(g.x,0);ctx.lineTo(g.x,g.g-g.gap/2);ctx.moveTo(g.x,g.g+g.gap/2);ctx.lineTo(g.x,220);ctx.stroke()}drawDoodle(ctx,72,y+34,.47,"run",ts);ctx.fillStyle="#111";ctx.font="800 13px system-ui";ctx.fillText(`${passed}/4`,12,20)'''
new='''ctx.clearRect(0,0,360,220);const sky=ctx.createLinearGradient(0,0,0,220);sky.addColorStop(0,"#8ad9ff");sky.addColorStop(.7,"#eefaff");sky.addColorStop(1,"#e5f4db");ctx.fillStyle=sky;ctx.fillRect(0,0,360,220);ctx.fillStyle="rgba(255,255,255,.75)";for(let i=0;i<4;i++){ctx.beginPath();ctx.arc(40+i*95,45+(i%2)*24,18,0,7);ctx.arc(55+i*95,45+(i%2)*24,14,0,7);ctx.fill()}ctx.lineWidth=3;for(const g of gates){ctx.fillStyle="#66c56d";ctx.strokeStyle="#205b2a";ctx.fillRect(g.x-8,0,16,g.g-g.gap/2);ctx.fillRect(g.x-8,g.g+g.gap/2,16,220-(g.g+g.gap/2));ctx.strokeRect(g.x-8,0,16,g.g-g.gap/2);ctx.strokeRect(g.x-8,g.g+g.gap/2,16,220-(g.g+g.gap/2))}drawDoodle(ctx,72,y+34,.68,"run",ts);ctx.fillStyle="#20233a";ctx.font="900 13px system-ui";ctx.fillText(`${passed}/4`,12,20)'''
s=s.replace(old,new)

# Lane dodge contrast on the dark road
s=s.replace('ctx.setLineDash([]);ctx.strokeStyle="#111";for(const o of obs)ctx.strokeRect(lanes[o.lane]-18,o.y,36,18);',
            'ctx.setLineDash([]);ctx.strokeStyle="#ffd65a";ctx.lineWidth=3;for(const o of obs){ctx.fillStyle="#ff725e";ctx.fillRect(lanes[o.lane]-18,o.y,36,18);ctx.strokeRect(lanes[o.lane]-18,o.y,36,18);}ctx.lineWidth=2;')

extra_css = r'''
/* v4.2.1 FINALFIX — screenshot-driven corrections */
.arcade-control-deck.tap{grid-template-columns:1fr}.arcade-control-deck.tap .arcade-trackpad{justify-content:center;background:linear-gradient(90deg,#8d72ff,#45b9ff);color:#fff}.arcade-control-deck.tap .arcade-trackpad::before{display:none}.flap-pad-label{font-size:14px;font-weight:1000;letter-spacing:.5px;color:#fff;text-shadow:0 1px 0 rgba(0,0,0,.18)}
body[data-mechanic="jumprope"] .mascot-zone{display:grid!important;min-height:210px;flex:1}body[data-mechanic="jumprope"] .play-area{min-height:0;flex:0 0 auto;background:transparent;border:0}body[data-mechanic="jumprope"] .stickman{height:min(28dvh,210px);max-height:210px}
'''
s=s.replace('</style>',extra_css+'\n</style>',1)

p.write_text(s,encoding='utf-8')
assert '4.2.1-finalfix' in s
assert 'jumprope:"tap"' in s
assert '#fffdf8' in s and '#8ad9ff' in s
print('FINALFIX applied',p.stat().st_size)
