"""Riquadro «All'esame»: le 20 domande del quiz base per materia (All. C al DM 323/2021), con evidenziate le materie della lezione.
Ogni materia conta una volta sola anche se si studia in più lezioni, così il totale fa sempre 20."""
MATERIE=[('navigazione','Navigazione cartografica','Navigazione',4),('manovra','Manovra e condotta','Manovra',4),
         ('sicurezza','Sicurezza','Sicurezza',3),('normativa','Normativa','Normativa',3),('colreg','COLREG e segnalamento','COLREG',2),
         ('meteo','Meteorologia','Meteo',2),('scafo','Teoria dello scafo','Scafo',1),('motori','Motori','Motori',1)]
def esame_box(evid,lez,c=None,extra='',compact=False):
    c=c or SEA
    n=sum(m[3] for m in MATERIE if m[0] in evid)
    rows=''
    for k,t,ts,q in MATERIE:
        on=k in evid
        bg=f'background:{c}; color:#FFFFFF' if on else f'background:#EEF0F2; color:{SOFT}'
        rows+=(f'<div style="display:flex; gap:10px; align-items:center"><p style="width:42px; height:42px; flex:none; border-radius:21px; {bg}; font-family:{H}; font-size:24px; font-weight:700; text-align:center; line-height:42px">{q}</p>'
               f'<p style="font-size:24px; line-height:1.15; font-weight:{800 if on else 600}; color:{INK if on else SOFT}">{ts if compact else t}</p></div>')
    head_=(f'<div style="display:flex; align-items:baseline; gap:14px"><p style="font-family:{H}; font-size:{48 if compact else 64}px; font-weight:700; line-height:1; color:{c}">{n}</p>'
           f'<p style="font-size:26px; font-weight:800; color:{INK}">domande su 20 dalle materie di oggi</p></div>')
    grid=f'<div style="display:grid; grid-template-columns:repeat({4 if compact else 2},1fr); gap:8px 16px">{rows}</div>'
    if compact:
        return card(tag("All'esame · quiz base")+head_+grid,None,26,10,2)
    foot=p('Quiz base: 20 domande, al massimo 4 errori, 30 minuti. Ogni materia conta una volta, anche se la studiamo in più lezioni.'+extra,24,BODY)
    return card(tag("All'esame · le 20 domande del quiz base")+head_+grid+foot,None,28,12,1.6)
