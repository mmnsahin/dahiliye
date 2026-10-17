import re,sys,glob
pat=re.compile(r'\[([A-Z](?:[^\]\[]{0,60}?))\]')
def fix(m):
    s=m.group(1)
    if not re.fullmatch(r'[A-Z](?:\s*(?:,|·)\s*(?:[A-Z]|el yazısı))*',s): return m.group(0)
    toks=[t.strip() for t in re.split(r'\s*,\s*',s)]
    plain=[];hw=[]
    for t in toks:
        if t.endswith('·el yazısı'): hw.append(t[0])
        elif re.fullmatch(r'[A-Z]',t): plain.append(t)
        else: return m.group(0)
    out=[]
    if plain: out.append('['+', '.join(plain)+']')
    if hw: out.append('['+', '.join(hw)+'·el yazısı]')
    return ' '.join(out)
for f in glob.glob('data/birlesik/*.md'):
    t=open(f,encoding='utf-8').read(); n=pat.sub(fix,t)
    if n!=t: open(f,'w',encoding='utf-8').write(n); print('fixed',f)
