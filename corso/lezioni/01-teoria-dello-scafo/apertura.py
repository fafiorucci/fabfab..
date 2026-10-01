"""Slide di apertura dei capitoli, verifiche da 2 quiz dopo i paragrafi e raccolta quiz finale (45 minuti).
Da eseguire con exec(open('apertura.py').read()) dentro genera.py, dopo le funzioni di base (sec, card, p, quiz_slide)."""
if 'ORANGE' not in globals(): ORANGE='#F28C28'
if 'line' not in globals():
    def line(x1,y1,x2,y2,c=NAVY,w=2):
        return f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{c}" stroke-width="{w}" stroke-linecap="round"/>'
# ---- slide di apertura dei capitoli (stesse della lezione 03) ----
GRID='#8FB3C6'; CHART='#FBF8EF'; LAND='#F2E2B3'
if 'glow' not in globals():
    def glow(x,y,c,r=9):
        return f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r*2.6:.0f}" fill="{c}" fill-opacity="0.18"/><circle cx="{x:.0f}" cy="{y:.0f}" r="{r*1.6:.0f}" fill="{c}" fill-opacity="0.35"/><circle cx="{x:.0f}" cy="{y:.0f}" r="{r}" fill="{c}"/>'
def _panel(cid,body): return f'<defs><clipPath id="{cid}"><rect x="0" y="0" width="500" height="220" rx="48"/></clipPath></defs><rect x="0" y="0" width="500" height="220" rx="48" fill="#FFFFFF" fill-opacity="0.06"/><g clip-path="url(#{cid})">{body}<path d="M-20 200 q30 -10 60 0 t60 0 t60 0 t60 0 t60 0 t60 0 t60 0 t60 0 t60 0 L540 220 L-20 220 Z" fill="{WATER}"/></g>'
def compass_scene():
    s=f'<g transform="translate(250 105)"><circle r="82" fill="{CHART}" stroke="{DACC}" stroke-width="8"/>'
    s+=''.join(f'<path d="M0 -82 L0 -70" stroke="{NAVY}" stroke-width="3" transform="rotate({a_})"/>' for a_ in range(0,360,30))
    s+=f'<path d="M0 -66 L12 0 L0 66 L-12 0 Z" fill="{NAVY}"/><path d="M-66 0 L0 12 L66 0 L0 -12 Z" fill="{NAVY}" fill-opacity="0.55"/><path d="M0 -66 L12 0 L-12 0 Z" fill="{CORAL}"/><circle r="7" fill="{DACC}"/></g>'
    s+=f'<text x="250" y="20" text-anchor="middle" font-family="Arial" font-size="18" font-weight="900" fill="{DACC}">N</text>'
    s+=f'<path d="M60 150 L120 120" stroke="{CORAL}" stroke-width="4" stroke-dasharray="8 6"/><path d="M380 140 L450 110" stroke="{CORAL}" stroke-width="4" stroke-dasharray="8 6"/>'
    return _panel('chb',s)
def ring_scene():
    s=f'<g transform="translate(250 120)"><circle r="62" fill="none" stroke="{ORANGE if "ORANGE" in globals() else "#F28C28"}" stroke-width="30"/><circle r="62" fill="none" stroke="#FFFFFF" stroke-width="30" stroke-dasharray="32 33"/></g>'
    s+=f'<path d="M312 120 Q380 90 420 140 Q440 170 470 160" fill="none" stroke="{DACC}" stroke-width="6"/>'
    return _panel('chr',s)
def fire_scene():
    s=f'<g transform="translate(180 30)"><rect x="0" y="40" width="70" height="140" rx="22" fill="{CORAL}"/><rect x="20" y="16" width="30" height="28" rx="6" fill="{NAVY}"/><path d="M50 22 L96 8 L100 20 L56 32 Z" fill="{NAVY}"/><rect x="12" y="80" width="46" height="40" rx="6" fill="#FFFFFF"/></g>'
    s+=f'<g transform="translate(340 140) scale(1.6)"><path d="M0 30 Q-26 10 -12 -22 Q-6 -8 0 -12 Q2 -34 16 -44 Q14 -20 24 -6 Q30 16 0 30 Z" fill="#F28C28"/><path d="M0 26 Q-12 12 -4 -6 Q2 4 6 -2 Q14 10 0 26 Z" fill="{DACC}"/></g>'
    return _panel('chf',s)
def radio_scene():
    s=f'<g transform="translate(205 20)"><rect x="40" y="0" width="12" height="50" rx="5" fill="{NAVY}"/><rect x="10" y="40" width="80" height="150" rx="18" fill="#2A4A6B" stroke="{DACC}" stroke-width="4"/><rect x="24" y="58" width="52" height="34" rx="6" fill="{SEA}"/>'
    s+=f'<text x="50" y="82" text-anchor="middle" font-family="Arial" font-size="20" font-weight="900" fill="#FFFFFF">16</text>'+''.join(f'<circle cx="{30+(i%3)*20}" cy="{112+(i//3)*20}" r="6" fill="{DACC}"/>' for i in range(9))+'</g>'
    s+=''.join(f'<path d="M{330+k*22} {60-k*4} q14 30 0 60" fill="none" stroke="{DACC}" stroke-width="5" stroke-linecap="round" opacity="{1-k*0.25}"/>' for k in range(3))
    return _panel('chv',s)
def chart_scene():
    s=f'<defs><clipPath id="chc"><rect x="0" y="0" width="500" height="220" rx="48"/></clipPath></defs><rect x="0" y="0" width="500" height="220" rx="48" fill="#FFFFFF" fill-opacity="0.06"/><g clip-path="url(#chc)">'
    s+=f'<g transform="rotate(-6 150 120)"><rect x="40" y="40" width="230" height="150" rx="8" fill="{CHART}"/>'
    s+=''.join(line(40+i*46,40,40+i*46,190,GRID,1.5) for i in range(1,5))+''.join(line(40,40+j*37.5,270,40+j*37.5,GRID,1.5) for j in range(1,4))
    s+=f'<path d="M40 150 Q90 120 120 150 Q150 175 190 160 L270 170 L270 190 L40 190 Z" fill="{LAND}"/><path d="M70 70 L230 130" stroke="{CORAL}" stroke-width="4" stroke-dasharray="10 6"/><circle cx="70" cy="70" r="6" fill="{CORAL}"/><circle cx="230" cy="130" r="6" fill="{CORAL}"/>'
    s+=f'<g transform="translate(210 75)"><circle r="24" fill="none" stroke="{NAVY}" stroke-width="2"/><path d="M0 -26 L6 0 L0 26 L-6 0 Z" fill="{NAVY}"/><path d="M-26 0 L0 6 L26 0 L0 -6 Z" fill="{NAVY}" fill-opacity="0.6"/><path d="M0 -26 L6 0 L-6 0 Z" fill="{CORAL}"/></g></g>'
    s+=f'<path d="M330 220 L330 170 Q380 150 430 165 Q470 175 500 168 L500 220 Z" fill="#2A4A6B"/>'
    s+=f'<path d="M395 52 L515 10 L515 100 Z" fill="{DACC}" fill-opacity="0.35"/>'
    s+=f'<path d="M380 168 L386 70 L404 70 L410 168 Z" fill="#FFFFFF"/><rect x="384" y="94" width="22" height="12" fill="{CORAL}"/><rect x="382" y="128" width="26" height="12" fill="{CORAL}"/>'
    s+=f'<rect x="381" y="52" width="28" height="20" rx="4" fill="{DACC}"/><path d="M378 52 L395 38 L412 52 Z" fill="{CORAL}"/>{glow(395,62,DACC,7)}'
    s+=f'<path d="M-20 196 q30 -10 60 0 t60 0 t60 0 t60 0 t60 0 t60 0 t60 0 t60 0 t60 0 L540 220 L-20 220 Z" fill="{WATER}"/></g>'
    return s
def quiz_scene():
    s=f'<defs><clipPath id="chq"><rect x="0" y="0" width="500" height="220" rx="48"/></clipPath></defs><rect x="0" y="0" width="500" height="220" rx="48" fill="#FFFFFF" fill-opacity="0.06"/><g clip-path="url(#chq)">'
    s+=f'<g transform="rotate(-5 160 110)"><rect x="60" y="22" width="200" height="190" rx="14" fill="{CHART}"/><rect x="125" y="12" width="70" height="24" rx="8" fill="{PURPLE}"/>'
    for i,(ok,yy) in enumerate(((1,62),(1,102),(0,142),(1,182))):
        s+=f'<rect x="84" y="{yy-14}" width="26" height="26" rx="6" fill="#FFFFFF" stroke="{NAVY}" stroke-width="3"/>'
        s+=(f'<path d="M89 {yy} l6 7 l12 -14" fill="none" stroke="{GREEN}" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/>' if ok else f'<path d="M90 {yy-8} l14 14 M104 {yy-8} l-14 14" stroke="{CORAL}" stroke-width="5" stroke-linecap="round"/>')
        s+=f'<rect x="124" y="{yy-6}" width="{110-i*12}" height="10" rx="5" fill="{GRID}"/>'
    s+='</g>'
    s+=f'<g transform="translate(380 118)"><rect x="-10" y="-82" width="20" height="16" rx="4" fill="{DACC}"/><circle r="64" fill="#FFFFFF" stroke="{PURPLE}" stroke-width="10"/>'
    s+=f'<path d="M0 0 L0 -64 A64 64 0 1 1 -45.3 -45.3 Z" fill="{PURPLE}" fill-opacity="0.25"/><path d="M0 0 L0 -46" stroke="{NAVY}" stroke-width="6" stroke-linecap="round"/><path d="M0 0 L-30 -30" stroke="{CORAL}" stroke-width="5" stroke-linecap="round"/><circle r="7" fill="{NAVY}"/></g>'
    s+=f'<path d="M-20 200 q30 -10 60 0 t60 0 t60 0 t60 0 t60 0 t60 0 t60 0 t60 0 t60 0 L540 220 L-20 220 Z" fill="{WATER}"/></g>'
    return s
_cid=[0]
def chapter(id_,n,title,subs,c,notes,dur='',cols=2,label=None,big=None,art=None):
    _cid[0]+=1
    rows=-(-len(subs)//cols); fs=30 if len(subs)<=12 else 22; bs=52 if len(subs)<=12 else 40
    items=''.join(f'<div style="display:flex; gap:14px; align-items:center"><p style="width:{bs}px; height:{bs}px; flex:none; border-radius:{bs//2}px; background:{c}; color:#FFFFFF; font-size:{bs*0.45:.0f}px; font-weight:900; text-align:center; line-height:{bs}px">{i}</p><p style="font-size:{fs}px; line-height:1.2; font-weight:700; color:#FFFFFF">{t}</p></div>' for i,t in enumerate(subs,1))
    left=(f'<div style="width:500px; flex:none; display:flex; flex-direction:column; gap:10px">'
          f'<p style="font-size:24px; font-weight:900; letter-spacing:2px; text-transform:uppercase; color:{c}">{label or "Capitolo"}</p>'
          f'<p style="font-family:{H}; font-size:{200 if big is None else 150}px; font-weight:700; line-height:0.9; color:{DACC}">{big or n}</p>'
          f'<h2 style="font-family:{H}; font-size:56px; font-weight:700; line-height:1.08; color:#FFFFFF">{title}</h2>{squiggle(c,220)}'
          f'<p style="font-size:26px; font-weight:700; color:{DSOFT}">{dur}</p>'
          f'<div style="flex:1"></div>'
          f'<svg aria-label="{art[1] if art else "Illustrazione: barca a vela sul mare"}" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 500 220" width="500" height="220" style="width:500px; height:220px">{art[0] if art else sea_scene(500,220,True,True,"ch"+str(_cid[0]))}</svg></div>')
    right=f'<div style="flex:1; display:grid; grid-template-columns:repeat({cols},1fr); grid-template-rows:repeat({rows},auto); grid-auto-flow:column; gap:{24 if len(subs)<=12 else 16}px 32px; align-content:center; background:rgba(255,255,255,0.06); padding:36px; border-radius:32px">{items}</div>'
    sec(id_, f'<div style="display:flex; gap:56px; align-items:stretch; height:792px">{left}{right}</div>', notes=notes, dark=True, gap=0)

def intermedi(spec):
    """Inserisce dopo la slide `after` una verifica da 2 quiz e la slide delle risposte."""
    for after,qid,t,ps in spec:
        n=len(slides)
        quiz_slide(qid,t,ps,False,'Verifica del paragrafo · quiz ufficiali')
        quiz_slide(qid+'r',t+' · risposte',ps,True)
        new=slides[n:]; del slides[n:]
        i=[s_[0] for s_ in slides].index(after)+1
        slides[i:i]=new

def raccolta(lez,nchap,topics,QZ,steps,plan,notes_quiz,before='chiusura'):
    """Apertura «Raccolta quiz», slide di istruzioni e 12 slide da 3 quiz con le risposte, inserite prima di `before`."""
    n0=len(slides)
    chapter('capquiz',nchap,'Raccolta quiz',topics,GREEN,
     'Inizio degli ultimi 45 minuti: 12 slide da 3 quiz ufficiali, ognuna seguita dalle risposte.','36 quiz ufficiali',2,'Ultimi 45 minuti','45′',art=(quiz_scene(),'Illustrazione: scheda di quiz con le risposte segnate e un cronometro sui 45 minuti'))
    cols=[(CORAL,CORAL_T),(SEA,SEA_T),(PURPLE,LILAC_T),(BLUE,BLUE_T)]
    tiles=''.join(f'<div style="display:flex; flex-direction:column; gap:12px; background:{bg}; padding:30px; border-radius:28px"><p style="font-family:{H}; font-size:64px; font-weight:700; line-height:1; color:{c}">{i}</p>{p(t,30,INK,800,1.2)}{p(d,24,INK,500,1.35)}</div>' for i,((t,d),(c,bg)) in enumerate(zip(steps,cols),1))
    exam=card(tag("La prova a quiz")+f'<div style="display:flex; gap:48px; align-items:end"><div>{p("quesiti",24,BODY,700)}<p style="font-family:{H}; font-size:80px; font-weight:700; line-height:1; color:{INK}">20</p></div><div>{p("errori ammessi",24,BODY,700)}<p style="font-family:{H}; font-size:80px; font-weight:700; line-height:1; color:{CORAL}">4</p></div><div>{p("tempo",24,BODY,700)}<p style="font-family:{H}; font-size:80px; font-weight:700; line-height:1; color:{INK}">30′</p></div></div>'+p('Tre risposte, una sola esatta. Oggi 36 quiz ufficiali della banca del DD 131/2022.',24),None,32,16)
    li=''.join(f'<li>{x}</li>' for x in plan)
    pl=card(tag("I 45 minuti",SEA)+f'<ol style="font-size:24px; line-height:1.4; color:#34465E; display:flex; flex-direction:column; gap:6px">{li}</ol>',SEA_T,32,12)
    sec('quiz', head(f'Lezione {lez:02d} · ultimi 45 minuti','Raccolta quiz')+f'<div style="display:grid; grid-template-columns:1fr 1fr 1fr 1fr; gap:20px">{tiles}</div><div style="display:flex; gap:24px">{exam}{pl}</div>',
     notes=notes_quiz, gap=28)
    for id_,t,ps in QZ:
        quiz_slide(id_,t,ps,False,'Raccolta quiz · DD 131/2022')
        quiz_slide(id_+'r',t+' · risposte',ps,True)
    new=slides[n0:]; del slides[n0:]
    ids=[s_[0] for s_ in slides]
    i=ids.index(before) if before in ids else len(slides)
    slides[i:i]=new
