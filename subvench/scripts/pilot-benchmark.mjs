import fs from 'node:fs/promises';
import {matchPrograms} from '../engine.mjs';
import {loadCatalog} from './catalog-loader.mjs';

const programs=await loadCatalog();
const cases=JSON.parse(await fs.readFile(new URL('../data/pilot_cases.json',import.meta.url),'utf8'));
let passed=0;
const rows=[];
for(const c of cases){
  const results=matchPrograms(programs,c.profile);
  const viable=results.filter(x=>x.eligibility!=='not_eligible').slice(0,5);
  const topIds=viable.map(x=>x.program.id);
  const failures=[];
  if(c.expect_top_any?.length&&!c.expect_top_any.some(id=>topIds.includes(id)))failures.push(`expected one of ${c.expect_top_any.join(', ')} in top 5`);
  for(const id of c.expect_excluded||[]){const r=results.find(x=>x.program.id===id);if(!r||r.eligibility!=='not_eligible')failures.push(`${id} should be excluded`);}
  if(!failures.length)passed++;
  rows.push({id:c.id,name:c.name,passed:!failures.length,failures,top5:viable.map(x=>({id:x.program.id,name:x.program.name,eligibility:x.eligibility,relevance:x.relevance,availability:x.availability?.code}))});
}
const report={generated_at:new Date().toISOString(),program_count:programs.length,case_count:cases.length,passed,failed:cases.length-passed,pass_rate:Number((passed/cases.length*100).toFixed(1)),rows};
await fs.writeFile(new URL('../data/pilot-benchmark.latest.json',import.meta.url),JSON.stringify(report,null,2)+'\n');
console.log(`pilot benchmark: ${passed}/${cases.length} passed (${report.pass_rate}%)`);
for(const row of rows.filter(x=>!x.passed))console.error(`- ${row.id}: ${row.failures.join('; ')}`);
if(report.failed)process.exitCode=1;
