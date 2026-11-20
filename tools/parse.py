# Parser de conteúdo programático (mesma lógica do app em JS).
import re, sys, json
def limpa(t):
    t = t.replace('ﬁ','fi').replace('ﬂ','fl').replace('​','')
    t = t.replace('\f','\n')
    t = re.sub(r'(?m)^.*(pciconcursos|pcimarkpci|Página \d+ de \d+).*$','',t)
    t = re.sub(r'(?m)^\s*\d+(\.\d+){2,}\s+[A-ZÀ-Ý ]+$','',t)
    return re.sub(r'-\n(?=[a-zà-ú])', '', t)
CAB = re.compile(r'^[ \t]*([A-ZÀ-Ý][^:\n]{2,90}?)\s*:\s*(?=1(?:[.)\-–]|\s))', re.M)
NUM = re.compile(r'(?<![\w.,/º-])(\d{1,2})(?:\s*[.)\-–]\s+|\s+)(?=[A-ZÀ-Ýa-zà-ý])')
def topicos(corpo):
    corpo = re.sub(r'\s+',' ',corpo).strip()
    esp=1; pos=[]
    for m in NUM.finditer(corpo):
        if int(m.group(1))==esp: pos.append((m.start(),m.end())); esp+=1
    if not pos: return [(corpo.strip(' .;'),'')] if len(corpo)>3 else []
    out=[]
    for i,(a,b) in enumerate(pos):
        fim = pos[i+1][0] if i+1<len(pos) else len(corpo)
        t = re.split(r'\s\d{1,3}\s+[A-ZÀ-Ý][A-ZÀ-Ý ()]{5,}:', corpo[b:fim])[0]
        t = re.sub(r'\s*\d+(\.\d+)+\.?\s*$','',t).strip(' .;')
        if not t or t[0].islower(): continue
        m = re.search(r'\s\d+\.\d+\.?\s', ' '+t)
        if m: ti, dica = t[:m.start()-1].strip(' .;:'), t[m.start()-1:].strip()
        else: ti, dica = t, ''
        out.append((ti,dica))
    return out
def parse(txt):
    txt = limpa(txt); res=[]
    ms = list(CAB.finditer(txt))
    for i,m in enumerate(ms):
        fim = ms[i+1].start() if i+1<len(ms) else len(txt)
        tp = topicos(txt[m.end():fim])
        nome = re.sub(r'\s+',' ',m.group(1)).strip().rstrip('.')
        if tp: res.append({'nome':nome,'topicos':tp})
    return res
if __name__=='__main__':
    f,a,b = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
    L = open(f,encoding='utf-8').read().split('\n')[a-1:b]
    r = parse('\n'.join(L))
    if len(sys.argv)>4: json.dump(r, open(sys.argv[4],'w'), ensure_ascii=False); 
    for s in r:
        print(f"## {s['nome']} ({len(s['topicos'])})")
        for t,d in s['topicos']: print('   -', t[:90], '|', d[:40])
