# Gera vitrine.js (modelos prontos) a partir dos editais em texto.
import json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from parse import parse
# Pasta com o texto dos editais (pdftotext edital.pdf; os de colunas do DOE sem -layout).
# Uso: EDITAIS=pasta/ python3 tools/build_vitrine.py
E = os.environ.get('EDITAIS', 'editais/')
def faixa(f, a, b):
    return '\n'.join(open(E+f, encoding='utf-8').read().split('\n')[a-1:b])
PEQ = {'de','da','do','das','dos','e','em','a','o','ou','para','com','no','na','à'}
def titulo(n):
    n = re.sub(r'\s+', ' ', n).strip()
    if n != n.upper(): return n[0].upper()+n[1:]
    w = n.lower().split(' ')
    return ' '.join(x if (i and x in PEQ) else (x[:1].upper()+x[1:]) for i,x in enumerate(w)).replace('(Somente Para a Prova Discursiva)','(só discursiva)')
def mats(txt, q=None, renomeia=None, tira=()):
    out = []
    for s in parse(txt):
        nome = titulo(s['nome'])
        if renomeia and nome in renomeia: nome = renomeia[nome]
        if nome in tira: continue
        tps = []
        for t,d in s['topicos']:
            t = re.split(r'\.\s+(?:[A-ZÀ-Ý][a-zà-ý]+ [A-ZÀ-Ý][a-zà-ý]+ de [A-ZÀ-Ý]|Secretári)', t)[0]
            if len(t) > 95:
                m_ = re.search(r'^(.{12,90}?)(?: – | - |: |\. )', t)
                if m_: t, d = m_.group(1).strip(), (t[m_.end():].strip() + (' ' + d if d else '')).strip()
            tps.append([t, d] if d else [t])
        m = {'nome': nome, 'topicos': tps}
        if q and nome in q: m['q'] = q[nome]
        out.append(m)
    return out

LP_AOCP = [x for x in mats(faixa('cbmpe.txt', 3662, 3763)) if x['nome'] == 'Língua portuguesa'][0]
LP_AOCP = {**LP_AOCP, 'nome': 'Língua Portuguesa'}

V = []
# ---------------- PCPE 2026 (Cebraspe) ----------------
pcpe_base = dict(orgao='Polícia Civil de Pernambuco', banca='Cebraspe', uf='PE', ano=2026, esfera='Estadual',
  inscricoes=['2026-10-15','2026-12-16'], taxa='R$ 250,00 (pagar até 18/12/2026)',
  links={'inscricao':'http://www.cebraspe.org.br/concursos/pc_pe_26','edital':'http://www.cebraspe.org.br/concursos/pc_pe_26','banca':'https://www.cebraspe.org.br'},
  datas=[['2026-12-16','Fim das inscrições (18h)'],['2026-12-18','Último dia para pagar a taxa'],['2027-02-22','Edital com os locais de prova'],
         ['2027-03-07','Provas objetivas e discursiva',1],['2027-03-09','Gabarito preliminar das objetivas']])
V.append({**pcpe_base, 'id':'pcpe-agente-2026', 'nome':'PCPE 2026', 'cargo':'Agente de Polícia', 'nivel':'Superior', 'vagas':'1.200',
  'prova':'2027-03-07', 'hora':'Turno da tarde (horário exato no edital de locais)',
  'regras':'P1 Noções de Direito (20 questões) + P2 Conhecimentos Específicos (40 questões) + redação, todas eliminatórias e classificatórias. Depois: exames médicos, capacidade física, investigação social, avaliação psicológica e curso de formação.',
  'materias': mats(faixa('pcpe.txt', 3107, 3215))})
V.append({**pcpe_base, 'id':'pcpe-escrivao-2026', 'nome':'PCPE 2026', 'cargo':'Escrivão de Polícia', 'nivel':'Superior', 'vagas':'70',
  'prova':'2027-03-07', 'hora':'Turno da manhã (horário exato no edital de locais)',
  'regras':'P1 Noções de Direito (20 questões) + P2 Conhecimentos Específicos (40 questões) + redação. Depois: exames, capacidade física, investigação social, avaliação psicológica e curso de formação.',
  'materias': mats(faixa('pcpe.txt', 3451, 3569))})
# ---------------- PMPE 2026 (Instituto AOCP) ----------------
pm = mats(faixa('pmpe.txt', 4045, 4089))
V.append({'id':'pmpe-soldado-2026', 'nome':'PMPE 2026', 'orgao':'Polícia Militar de Pernambuco', 'cargo':'Soldado (QPMG)', 'banca':'Instituto AOCP',
  'nivel':'Médio', 'uf':'PE', 'ano':2026, 'esfera':'Estadual', 'vagas':'1.250', 'inscricoes':['2026-10-05','2026-11-05'],
  'prova':'2027-02-21', 'hora':'Horário no edital de local de prova (sai em 02/02/2027)',
  'links':{'inscricao':'https://www.institutoaocp.org.br','edital':'https://www.institutoaocp.org.br','banca':'https://www.institutoaocp.org.br'},
  'regras':'60 questões de múltipla escolha (A a E) em três blocos + redação. Para passar na objetiva: não zerar nenhuma matéria e fazer pelo menos 30% dos pontos.',
  'datas':[['2026-11-05','Fim das inscrições'],['2026-11-06','Último dia para pagar a taxa'],['2027-02-02','Edital com horário e local da prova'],
           ['2027-02-15','Cartão de informação do candidato'],['2027-02-21','Prova objetiva e redação',1]],
  'materias':[{**LP_AOCP, 'q':10}] + [{**m, 'q':10} for m in pm]})
# ---------------- CBMPE 2026 (Instituto AOCP) ----------------
qcb = {'Língua portuguesa':10,'Informática':5,'Matemática':10,'Raciocínio Lógico':5,'Física':5,'Biologia':5,'Direito Constitucional':10,'Atualidades':5,'História de Pernambuco':5}
cb = mats(faixa('cbmpe.txt', 3662, 3763), q=qcb, renomeia={'Língua portuguesa':'Língua Portuguesa'})
for m in cb:
    if m['nome'] == 'Língua Portuguesa': m['q'] = 10
V.append({'id':'cbmpe-soldado-2026', 'nome':'CBMPE 2026', 'orgao':'Corpo de Bombeiros Militar de Pernambuco', 'cargo':'Soldado (QBMG)', 'banca':'Instituto AOCP',
  'nivel':'Médio', 'uf':'PE', 'ano':2026, 'esfera':'Estadual', 'vagas':'510', 'inscricoes':['2026-10-05','2026-11-05'],
  'prova':'2027-02-28', 'hora':'Horário no edital de local de prova',
  'links':{'inscricao':'https://www.institutoaocp.org.br','edital':'https://www.institutoaocp.org.br','banca':'https://www.institutoaocp.org.br'},
  'regras':'60 questões de múltipla escolha (A a E) em três blocos + redação. Para passar na objetiva: não zerar nenhuma matéria e fazer pelo menos 30% dos pontos.',
  'datas':[['2026-11-05','Fim das inscrições'],['2027-02-28','Prova objetiva e redação',1]],
  'materias': cb})
# ---------------- Câmara de Guarabira 2026 (CPCon/UEPB) ----------------
cg = mats(faixa('cmg.txt', 1094, 1140), q={'Língua Portuguesa':15,'Informática':10}, renomeia={'Auxiliar Administrativo':'Conhecimentos Específicos'})
for m in cg:
    if m['nome'] == 'Conhecimentos Específicos': m['q'] = 15
V.append({'id':'cmg-auxadm-2026', 'nome':'Câmara de Guarabira 2026', 'orgao':'Câmara Municipal de Guarabira', 'cargo':'Auxiliar Administrativo', 'banca':'CPCon / UEPB',
  'nivel':'Médio', 'uf':'PB', 'ano':2026, 'esfera':'Municipal', 'vagas':'2', 'inscricoes':['2026-10-21','2026-11-22'], 'taxa':'R$ 95,00 (pagar até 23/11/2026)',
  'prova':'2027-02-14', 'hora':'14h30 às 18h30 (portões das 13h30 às 14h15)', 'local':'Guarabira/PB',
  'links':{'inscricao':'https://cpcon.uepb.edu.br/pmGuarabira2026','edital':'https://cpcon.uepb.edu.br/pmGuarabira2026','banca':'https://cpcon.uepb.edu.br'},
  'regras':'40 questões objetivas: 15 de Língua Portuguesa, 10 de Informática e 15 de Conhecimentos Específicos. Fase única.',
  'datas':[['2026-11-22','Fim das inscrições'],['2026-11-23','Último dia para pagar o boleto'],['2026-12-16','Inscrições homologadas (após recursos)'],
           ['2027-02-01','Local, sala e carteira da prova'],['2027-02-14','Prova objetiva',1],['2027-02-15','Gabarito provisório']],
  'materias': cg})
# ---------------- IFPB 164/2026 (professor substituto, Informática) ----------------
V.append({'id':'ifpb-164-2026-info', 'nome':'IFPB · Professor Substituto', 'orgao':'Instituto Federal da Paraíba (Campus Monteiro)', 'cargo':'Professor Substituto · Informática (Código 1)', 'banca':'COMPEC / IFPB',
  'nivel':'Superior', 'uf':'PB', 'ano':2026, 'esfera':'Federal', 'vagas':'1', 'inscricoes':['2026-11-23','2026-11-29'], 'taxa':'pagar até 30/11/2026',
  'prova':'2026-12-15', 'hora':'Prova de desempenho didático online, entre 15 e 18/12 (horário na convocação de 11/12)', 'local':'Ambiente virtual',
  'links':{'inscricao':'https://concursos.ifpb.edu.br/','edital':'https://concursos.ifpb.edu.br/','banca':'https://www.ifpb.edu.br'},
  'regras':'Seleção simplificada: prova de desempenho didático (eliminatória e classificatória) e prova de títulos. Envio do plano de aula e do Lattes em 7 e 8/12.',
  'datas':[['2026-11-29','Fim das inscrições (23h59)'],['2026-11-30','Último dia para pagar o boleto'],['2026-12-08','Enviar plano de aula, Lattes e títulos'],
           ['2026-12-11','Convocação com data e hora da aula'],['2026-12-15','Provas de desempenho didático (15 a 18/12)',1],['2026-12-24','Resultado final da prova didática']],
  'materias':[{'nome':'Aula do tema sorteado', 'topicos':[['Plano de aula: Desenvolvimento de API REST com Spring Boot','Arquitetura em camadas (model, repository, service e controller) e mapeamento objeto-relacional'],
      ['Entidade e mapeamento objeto-relacional (JPA)'],['Repository e acesso a dados'],['Service: regras de negócio e injeção de dependências'],['Controller e endpoints HTTP'],['Ensaio cronometrado da aula']]},
    {'nome':'Unidades curriculares', 'topicos':[['Linguagem de programação C e estrutura de dados'],['Programação orientada a objetos'],['Desenvolvimento de aplicações corporativas'],
      ['Programação para dispositivos móveis'],['Desenvolvimento de aplicações web'],['Engenharia de software'],['Montagem, configuração e manutenção de microcomputadores'],
      ['Redes de computadores e infraestrutura'],['Informática básica'],['Banco de dados'],['Metodologia científica']]}]})
# ---------------- PF 2025 (Cebraspe) -> pré-edital ----------------
pf_base = dict(orgao='Polícia Federal', banca='Cebraspe', uf='BR', ano=2025, esfera='Federal', inscricoes=['2025-05-26','2025-06-16'], prova='2025-07-27',
  links={'edital':'http://www.cebraspe.org.br/concursos/pf_25','banca':'https://www.cebraspe.org.br'},
  datas=[['2025-07-27','Prova objetiva e discursiva',1]], nivel='Superior')
REN_PF = {'Noções de Direito Penal e de Direito Processual Penal':'Direito Penal e Processual Penal'}
V.append({**pf_base, 'id':'pf-agente-2025', 'nome':'PF', 'cargo':'Agente de Polícia Federal',
  'regras':'No edital de 2025: 120 itens de certo ou errado (Cebraspe) + discursiva, em 4h30. Um item errado anula um certo.', 'materias': mats(faixa('pf.txt', 3862, 4033), renomeia=REN_PF)})
V.append({**pf_base, 'id':'pf-escrivao-2025', 'nome':'PF', 'cargo':'Escrivão de Polícia Federal',
  'regras':'No edital de 2025: 120 itens de certo ou errado (Cebraspe) + discursiva, em 4h30. Um item errado anula um certo.', 'materias': mats(faixa('pf.txt', 3679, 3861), renomeia=REN_PF)})
# ---------------- PRF 2021 (Cebraspe) -> pré-edital ----------------
prf = mats(faixa('prf.txt', 1684, 1824), renomeia={'Espanhola':'Língua Estrangeira (Inglês ou Espanhol)'})
for m in prf:
    if m['nome'].startswith('Língua Estrangeira'):
        m['topicos'] = [['Compreensão de texto escrito em inglês ou espanhol'],['Itens gramaticais relevantes para a compreensão do texto']]
V.append({'id':'prf-2021', 'nome':'PRF', 'orgao':'Polícia Rodoviária Federal', 'cargo':'Policial Rodoviário Federal', 'banca':'Cebraspe', 'nivel':'Superior',
  'uf':'BR', 'ano':2021, 'esfera':'Federal', 'inscricoes':['2021-01-25','2021-02-12'], 'prova':'2021-03-28',
  'links':{'edital':'http://www.cebraspe.org.br/concursos/prf_21','banca':'https://www.cebraspe.org.br'},
  'regras':'No edital de 2021: prova objetiva de certo ou errado (Cebraspe) com três blocos + discursiva, em 4h30. Depois: aptidão física, avaliação psicológica, saúde, títulos e curso de formação.',
  'datas':[['2021-03-28','Prova objetiva e discursiva',1]], 'materias': prf})

for v in V:
    tot = sum(len(m['topicos']) for m in v['materias'])
    print(f"{v['id']:24} {len(v['materias']):2} matérias {tot:3} tópicos  " + ', '.join(m['nome'][:18] for m in v['materias']))
js = '/* Vitrine de concursos: modelos prontos montados a partir dos editais oficiais.\n   Gerado por tools/build_vitrine.py. Datas e conteúdos conforme cada edital; confira sempre o site da banca. */\nwindow.VITRINE = ' + json.dumps(V, ensure_ascii=False, separators=(',',':')) + ';\n'
open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'vitrine.js'),'w').write(js)
print(len(js), 'bytes')
