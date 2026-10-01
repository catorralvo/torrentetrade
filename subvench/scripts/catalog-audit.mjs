import fs from 'node:fs/promises';

const programs=JSON.parse(await fs.readFile(new URL('../data/programs.json',import.meta.url),'utf8'));
const ids=new Set();
const errors=[];
for(const [i,p] of programs.entries()){
  const at=`programs[${i}]${p?.id?` (${p.id})`:''}`;
  for(const key of ['id','name','authority','level','cantons','project_types','keywords','funding','hard_requirements','documents','status','source','verified_on']){
    if(p?.[key]===undefined||p?.[key]===null||p?.[key]==='')errors.push(`${at}: missing ${key}`);
  }
  if(ids.has(p.id))errors.push(`${at}: duplicate id`);ids.add(p.id);
  if(!Array.isArray(p.cantons)||!p.cantons.length)errors.push(`${at}: cantons must be non-empty array`);
  if(!Array.isArray(p.project_types))errors.push(`${at}: project_types must be array`);
  if(!Array.isArray(p.keywords))errors.push(`${at}: keywords must be array`);
  if(!String(p.source||'').startsWith('https://'))errors.push(`${at}: source must be https`);
  if(!/^\d{4}-\d{2}-\d{2}$/.test(String(p.verified_on||'')))errors.push(`${at}: verified_on must be YYYY-MM-DD`);
  if(p.company_profile?.max_fte!=null&&(!Number.isInteger(p.company_profile.max_fte)||p.company_profile.max_fte<1))errors.push(`${at}: invalid max_fte`);
  if(p.funding?.rate_max!=null&&(p.funding.rate_max<=0||p.funding.rate_max>1))errors.push(`${at}: rate_max must be 0..1`);
}
if(errors.length){console.error(`catalog audit: ${errors.length} error(s)`);errors.forEach(e=>console.error(`- ${e}`));process.exit(1)}
console.log(`catalog audit: OK (${programs.length} programmes, ${ids.size} unique ids)`);
