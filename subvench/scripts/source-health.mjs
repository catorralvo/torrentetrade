import fs from 'node:fs/promises';
import crypto from 'node:crypto';

const programs=JSON.parse(await fs.readFile(new URL('../data/programs.json',import.meta.url),'utf8'));
const unique=[...new Map(programs.map(p=>[p.source,p])).entries()];
const rows=[];
for(const [url,p] of unique){
  const started=Date.now();let status=0,ok=false,finalUrl=url,etag=null,lastModified=null,hash=null,error=null;
  try{
    const res=await fetch(url,{redirect:'follow',headers:{'user-agent':'SubvenCH-source-monitor/0.2 (+https://torrentetrade.ch/subvench/)'}});
    status=res.status;ok=res.ok;finalUrl=res.url;etag=res.headers.get('etag');lastModified=res.headers.get('last-modified');
    const text=(await res.text()).replace(/\s+/g,' ').trim();hash=crypto.createHash('sha256').update(text).digest('hex').slice(0,20);
  }catch(e){error=e?.message||String(e)}
  rows.push({program_id:p.id,url,ok,status,final_url:finalUrl,etag,last_modified:lastModified,content_hash:hash,ms:Date.now()-started,error});
}
const report={checked_at:new Date().toISOString(),count:rows.length,healthy:rows.filter(x=>x.ok).length,unhealthy:rows.filter(x=>!x.ok).length,rows};
await fs.writeFile(new URL('../data/source-health.latest.json',import.meta.url),JSON.stringify(report,null,2)+'\n');
console.log(`source health: ${report.healthy}/${report.count} reachable`);
if(report.unhealthy){for(const r of rows.filter(x=>!x.ok))console.error(`${r.program_id}: ${r.status||'ERR'} ${r.url} ${r.error||''}`);process.exitCode=1;}
