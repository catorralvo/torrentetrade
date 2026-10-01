import fs from 'node:fs/promises';

export async function loadCatalog(){
  const files=['../data/programs.json','../data/programs_2026q4.json'];
  const groups=[];
  for(const file of files){groups.push(JSON.parse(await fs.readFile(new URL(file,import.meta.url),'utf8')));}
  return groups.flat();
}
