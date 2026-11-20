// Robô do radar de concursos (roda todo dia no GitHub Actions, de graça).
// Lê algumas páginas públicas, monta cards básicos (nome, UF, vagas, inscrições, link)
// e grava em radar.json, que o app mostra na vitrine. Sem dependências: Node 20+.
//
// Uso:  node tools/robo.mjs            → atualiza radar.json
//       node tools/robo.mjs --teste    → roda os testes com HTML de exemplo
import {readFileSync, writeFileSync, existsSync} from 'node:fs';

export const FONTES = [
  {id:'pci', nome:'PCI Concursos', url:'https://www.pciconcursos.com.br/concursos/nordeste/', tipo:'lista'},
  {id:'gran', nome:'Blog do Gran', url:'https://blog.grancursosonline.com.br/ultimas-noticias/', tipo:'noticias'},
  {id:'estrategia-mapa', nome:'Estratégia · Mapa dos concursos', url:'https://concursos.estrategia.com/blog/mapa-concursos', tipo:'noticias'},
  {id:'estrategia', nome:'Estratégia · Portal', url:'https://concursos.estrategia.com/portal/', tipo:'noticias'},
];
const UFS = new Set('AC AL AP AM BA CE DF ES GO MA MT MS MG PA PB PR PE PI RJ RN RS RO RR SC SP SE TO'.split(' '));
const ENT = {'&amp;':'&','&lt;':'<','&gt;':'>','&quot;':'"','&#39;':"'",'&nbsp;':' ','&#8211;':'–','&#8217;':'’','&#8220;':'“','&#8221;':'”'};
export const texto = h => String(h).replace(/<script[\s\S]*?<\/script>|<style[\s\S]*?<\/style>/gi,' ').replace(/<br\s*\/?>|<\/(div|p|li|span|td|h\d)>/gi,' | ')
  .replace(/<[^>]+>/g,' ').replace(/&#(\d+);/g,(_,n) => String.fromCharCode(+n)).replace(/&[a-z#0-9]+;/gi, e => ENT[e] ?? ' ').replace(/\s+/g,' ').replace(/( \| )+/g,' | ').trim();
const iso = (d,m,y) => `${y}-${String(m).padStart(2,'0')}-${String(d).padStart(2,'0')}`;
export const slug = s => s.normalize('NFD').replace(/[̀-ͯ]/g,'').toLowerCase().replace(/[^a-z0-9]+/g,'-').replace(/^-|-$/g,'').slice(0,80);
const absoluta = (u, base) => {try{return new URL(u.replace(/&amp;/g,'&'), base).href}catch(e){return null}};

/* PCI: cada concurso é um link para /noticias/…; o que vem até o próximo link é o bloco dele */
export function lerPci(html, base){
  const re = /<a[^>]+href="([^"]*\/noticias\/[^"#?]+)"[^>]*>([\s\S]*?)<\/a>/gi, ms = [...html.matchAll(re)], out = [], vistos = new Set();
  ms.forEach((m,i) => {
    const link = absoluta(m[1], base), nome = texto(m[2]);
    if(!link || vistos.has(link) || nome.length < 4 || /apostila/i.test(nome)) return;
    vistos.add(link);
    const bloco = texto(html.slice(m.index + m[0].length, i+1 < ms.length ? ms[i+1].index : m.index + 3000).slice(0, 3000));
    const uf = (bloco.match(/\b[A-Z]{2}\b/g) || []).find(x => UFS.has(x)) || (nome.match(/\b([A-Z]{2})\b/g) || []).find(x => UFS.has(x)) || '';
    const vagas = (bloco.match(/(\d[\d.]*)\s+vagas?/i) || [])[1] || '';
    const salario = (bloco.match(/R\$\s*[\d.]+,\d{2}/) || [])[0] || '';
    const niveis = [...new Set((bloco.match(/Fundamental|Médio|Superior/g) || []))];
    const datas = [...bloco.matchAll(/(\d{1,2})\/(\d{1,2})\/(\d{4})/g)].map(d => iso(d[1],d[2],d[3]));
    const fim = datas.length ? datas.sort().at(-1) : '';
    out.push({id:'pci-'+slug(nome+'-'+uf), nome, uf, vagas:vagas.replace(/\./g,''), salario, niveis, inscricoesAte:fim, link, fonte:'pci', tipo:'inscricoes'});
  });
  return out;
}
/* blogs: títulos de matérias que falam de concurso, edital ou inscrição */
export function lerNoticias(html, base, fonte){
  const host = new URL(base).hostname, out = [], vistos = new Set();
  const re = /<a[^>]+href="([^"]+)"[^>]*>([\s\S]*?)<\/a>/gi;
  for(const m of html.matchAll(re)){
    const link = absoluta(m[1], base), titulo = texto(m[2]).replace(/^\|\s*|\s*\|$/g,'').trim();
    if(!link || new URL(link).hostname !== host || vistos.has(link)) continue;
    if(titulo.length < 25 || titulo.length > 180 || !/concurso|edital|inscri|processo seletivo|sele[çc][ãa]o|vagas/i.test(titulo)) continue;
    if(/^(leia|veja|confira|clique|ver mais|saiba)/i.test(titulo) || /\/(tag|categoria|category|author|page)\//.test(link)) continue;
    vistos.add(link);
    const uf = (titulo.match(/\b[A-Z]{2}\b/g) || []).find(x => UFS.has(x)) || '';
    out.push({id:fonte+'-'+slug(titulo), titulo, uf, link, fonte, tipo:'noticia'});
  }
  return out.slice(0, 40);
}

async function baixar(url){
  const r = await fetch(url, {headers:{'user-agent':'Mozilla/5.0 (radar do Meu Cronograma de Estudo; +https://jacobbv.github.io/meu-cronograma-estudo/)', 'accept-language':'pt-BR'}, signal:AbortSignal.timeout(30000)});
  if(!r.ok) throw new Error('HTTP '+r.status);
  return await r.text();
}
export function juntar(antigo, novos, hoje){
  const porId = new Map((antigo || []).map(x => [x.id, x]));
  for(const n of novos){const a = porId.get(n.id); porId.set(n.id, {...n, visto:a?.visto || hoje})}
  const limite = new Date(Date.parse(hoje) - 30*864e5).toISOString().slice(0,10);
  return [...porId.values()].filter(x => x.tipo === 'inscricoes' ? (x.inscricoesAte ? x.inscricoesAte >= hoje : x.visto >= limite) : x.visto >= limite)
    .sort((a,b) => (b.visto||'').localeCompare(a.visto||'') || (a.inscricoesAte||'9').localeCompare(b.inscricoesAte||'9')).slice(0, 300);
}

async function principal(){
  const arq = new URL('../radar.json', import.meta.url), hoje = new Date(Date.now() - 3*3600e3).toISOString().slice(0,10);
  const antigo = existsSync(arq) ? JSON.parse(readFileSync(arq,'utf8')) : {itens:[], fontes:{}};
  const novos = [], fontes = {...(antigo.fontes || {})};
  for(const f of FONTES){
    try{
      const html = await baixar(f.url), itens = f.tipo === 'lista' ? lerPci(html, f.url) : lerNoticias(html, f.url, f.id);
      novos.push(...itens); fontes[f.id] = {nome:f.nome, url:f.url, ok:hoje, n:itens.length};
      console.log(`${f.nome}: ${itens.length} itens`);
    }catch(e){fontes[f.id] = {...(fontes[f.id] || {nome:f.nome, url:f.url}), erro:String(e.message || e), quando:hoje}; console.log(`${f.nome}: falhou (${e.message})`)}
  }
  const itens = juntar(antigo.itens, novos, hoje);
  const saida = {atualizado:hoje, fontes, itens};
  if(JSON.stringify({...antigo, atualizado:''}) === JSON.stringify({...saida, atualizado:''})){console.log('Nada mudou.'); return}
  writeFileSync(arq, JSON.stringify(saida, null, 1) + '\n');
  console.log(`radar.json: ${itens.length} itens`);
}

function testes(){
  const ok = (c, m) => {if(!c){console.error('FALHOU:', m); process.exitCode = 1} else console.log('ok -', m)};
  const pci = `<h2>BAHIA</h2><div class="na"><div class="ca"><a href="https://www.pciconcursos.com.br/noticias/prefeitura-de-mairi-ba-abre-concurso" title="x">Prefeitura de Mairi</a></div>
    <div class="cc">BA</div><div class="cd">20 vagas até R$ 3.242,00<br><span>Vários Cargos</span><br><span>Fundamental / Médio / Superior</span></div><div class="ce"><span>23/11/2026</span></div></div>
    <div class="na"><div class="ca"><a href="/noticias/camara-de-croata-ce-abre-concurso">Câmara de Croatá</a></div><div class="cc">CE</div><div class="cd">1.015 vagas até R$ 1.621,00</div><div class="ce"><span>Prorrogado até 27/11/2026</span></div>
    <a href="https://www.pciconcursos.com.br/apostilas/x">apostila</a></div>`;
  const r = lerPci(pci, 'https://www.pciconcursos.com.br/concursos/nordeste/');
  ok(r.length === 2, 'PCI acha 2 concursos');
  ok(r[0].uf === 'BA' && r[0].vagas === '20' && r[0].salario === 'R$ 3.242,00' && r[0].inscricoesAte === '2026-11-23', 'PCI lê UF, vagas, salário e data');
  ok(r[1].link === 'https://www.pciconcursos.com.br/noticias/camara-de-croata-ce-abre-concurso' && r[1].vagas === '1015' && r[1].inscricoesAte === '2026-11-27', 'PCI: link relativo, milhar e prorrogado');
  const blog = `<article><h2><a href="https://blog.grancursosonline.com.br/concurso-pc-pb-edital/">Concurso PC PB: edital publicado com 1.400 vagas; veja</a></h2></article>
    <a href="https://blog.grancursosonline.com.br/tag/concursos/">Concursos públicos abertos em todo o Brasil hoje</a><a href="https://outro.com/x">Concurso de fora do site com edital</a>
    <a href="https://blog.grancursosonline.com.br/receita/">Receita de bolo de chocolate fácil e rápida</a>`;
  const n = lerNoticias(blog, 'https://blog.grancursosonline.com.br/ultimas-noticias/', 'gran');
  ok(n.length === 1 && n[0].uf === 'PB', 'Notícias: só a matéria de concurso do próprio site, com UF');
  const j = juntar([{id:'a', tipo:'inscricoes', inscricoesAte:'2026-11-01', visto:'2026-10-01'}, {id:'b', tipo:'noticia', visto:'2026-11-19'}], [{id:'c', tipo:'inscricoes', inscricoesAte:'2026-12-01'}], '2026-11-20');
  ok(j.length === 2 && j.some(x => x.id === 'c' && x.visto === '2026-11-20') && !j.some(x => x.id === 'a'), 'Juntar: tira inscrição encerrada e marca quando viu');
}
if(process.argv.includes('--teste')) testes(); else await principal();
