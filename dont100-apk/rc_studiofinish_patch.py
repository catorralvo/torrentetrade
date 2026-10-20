from pathlib import Path
p=Path('dont100-apk/app/src/main/assets/index.html')
s=p.read_text(encoding='utf-8')
needle='function arcadePostFX(ts){'
assert s.count(needle)==1, 'Expected exactly one arcadePostFX'
start=s.index(needle)
end=s.index('\nfunction startArcadeLoop(',start)
replacement=r'''function arcadePostFX(ts){
 const c=document.querySelector(".arcade-canvas");if(!c)return;
 const ctx=c.getContext("2d");if(!ctx)return;
 ctx.save();ctx.shadowBlur=0;ctx.shadowOffsetX=0;ctx.shadowOffsetY=0;
 // Lightweight, deterministic, theme-aware finishing pass. No textures or network assets.
 const vg=ctx.createRadialGradient(180,92,62,180,110,246);
 vg.addColorStop(0,"rgba(255,255,255,0)");
 vg.addColorStop(.68,"rgba(16,24,54,.012)");
 vg.addColorStop(1,"rgba(12,18,46,.17)");
 ctx.fillStyle=vg;ctx.fillRect(0,0,360,220);
 const gl=ctx.createLinearGradient(0,0,0,64);
 gl.addColorStop(0,"rgba(255,255,255,.20)");
 gl.addColorStop(1,"rgba(255,255,255,0)");
 ctx.fillStyle=gl;ctx.fillRect(0,0,360,64);
 // Keep the animation subtle and honor system reduced-motion settings.
 if(!window.matchMedia||!window.matchMedia("(prefers-reduced-motion: reduce)").matches){
  const phase=ts*.00035;
  for(let i=0;i<7;i++){
   const x=(i*71+29+Math.sin(phase+i*1.9)*11+360)%360;
   const y=(i*43+19+Math.cos(phase*.7+i*2.1)*8+220)%220;
   ctx.globalAlpha=.10+(i%3)*.028;
   ctx.fillStyle="#ffffff";
   ctx.beginPath();ctx.arc(x,y,1.1+(i%3)*.42,0,Math.PI*2);ctx.fill();
  }
  ctx.globalAlpha=1;
 }
 ctx.strokeStyle="rgba(255,255,255,.40)";ctx.lineWidth=1;
 ctx.strokeRect(.5,.5,359,219);
 ctx.restore();
}'''
s=s[:start]+replacement+s[end:]
css=r'''
/* STUDIO FINISH: polish without changing approved mascot or gameplay geometry. */
body.arcade-level .arcade-wrap{
 position:relative;
 isolation:isolate;
 border-radius:22px;
 border:2px solid rgba(38,43,91,.66);
 box-shadow:0 5px 0 rgba(39,45,98,.14),0 17px 36px rgba(23,32,80,.20),inset 0 1px 0 rgba(255,255,255,.55);
}
body.arcade-level .arcade-wrap::after{
 content:"";position:absolute;inset:0;pointer-events:none;border-radius:inherit;
 box-shadow:inset 0 2px 1px rgba(255,255,255,.40),inset 0 -6px 14px rgba(24,30,70,.10);
}
body.arcade-level .arcade-control-deck{
 border-radius:20px;
 box-shadow:0 5px 0 rgba(51,48,116,.09),0 14px 27px rgba(49,56,119,.13);
}
body.arcade-level .arcade-trackpad,body.arcade-level .arcade-fire-btn{
 touch-action:none;-webkit-tap-highlight-color:transparent;user-select:none;
}
body.arcade-level .arcade-trackpad:focus-visible,body.arcade-level .arcade-fire-btn:focus-visible{
 outline:3px solid #ffcb54;outline-offset:4px;
}
@media(prefers-reduced-motion:reduce){
 body.arcade-level .arcade-wrap,body.arcade-level .arcade-control-deck,
 body.arcade-level .arcade-trackpad,body.arcade-level .arcade-fire-btn{
  animation:none!important;transition:none!important;
 }
}
@media(max-width:380px){
 body.arcade-level .arcade-wrap{border-radius:17px}
 body.arcade-level .arcade-control-deck{border-radius:15px}
}
'''
assert s.count('</style>')>=1
s=s.replace('</style>',css+'\n</style>',1)
assert 'STUDIO FINISH' in s and 'prefers-reduced-motion' in s
p.write_text(s,encoding='utf-8')
print('studio visual finishing applied',p.stat().st_size)
