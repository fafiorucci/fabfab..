"""Le famiglie d'esame dei 135 esercizi ufficiali di carteggio (DD 131/2022), con i nomi usati nei manuali
di preparazione (tabelle «Argomenti principali problemi ...»). Si esegue con exec() dopo lezione_base.
CAT: esercizio → famiglia. FAM: famiglia → (come si risolve, slide o lezione dove è spiegata)."""
ORANGE=globals().get("ORANGE","#F28C28")
_C={
 # navigazione costiera (36): lezioni 10 e 15
 'Passaggio al traverso':['5.3.3-2','5.3.3-3'],
 'Passaggio al traverso + 3 RilB simultanei di 3 punti cospicui':['5.6.3-1'],
 'Trasporto 2 RilB di 1 punto cospicuo':['5.1.3-1','5.1.3-2','5.1.3-4','5.1.3-5','5.2.3-2','5.4.3-1','5.4.3-2','5.4.3-5','5.5.3-1','5.6.3-2'],
 'Trasporto 2 RilP di 1 punto cospicuo':['5.3.3-4'],
 'Trasporto 3 RilB di 1 punto cospicuo':['5.1.3-3'],
 'Trasporto 2 RilV di 2 punti cospicui':['5.2.3-5','5.3.3-5','5.4.3-4'],
 'Trasporto 2 RilB di 2 punti cospicui':['5.2.3-1','5.2.3-3','5.2.3-4','5.3.3-1','5.3.3-7','5.4.3-3','5.7.3-1','5.8.3-1'],
 'Trasporto 2 RilP di 2 punti cospicui':['5.3.3-6'],
 'Intercettazione':['5.1.3-6','5.4.3-6','5.4.3-8','5.5.3-2','5.6.3-3','5.7.3-2','5.8.3-2','5.8.3-3'],
 'Intercettazione su rotte opposte':['5.4.3-7'],
 # calcolo del carburante (23): lezione 11
 'Calcolo carburante':['5.3.2-1','5.3.2-7'],
 'Calcolo carburante e traverso':['5.1.2-1','5.4.2-1'],
 'Calcolo carburante e RilP 45°/90°':['5.1.2-2','5.1.2-3','5.1.2-4','5.1.2-5','5.2.2-1','5.2.2-2','5.2.2-3','5.2.2-4','5.3.2-2','5.4.2-5','5.4.2-6'],
 'Calcolo carburante e RilP 45°/90° e velocità':['5.2.2-5','5.3.2-3','5.3.2-4','5.3.2-5','5.3.2-6','5.4.2-2','5.4.2-3','5.4.2-4'],
 # scarroccio (24): lezione 12
 'Scarroccio prora vera':['5.2.4-5','5.5.4-1'],
 'Scarroccio prora vera · coordinate punto':['5.2.4-1','5.3.4-1','5.3.4-2','5.3.4-3','5.4.4-4'],
 'Scarroccio prora vera · coordinate al traverso':['5.2.4-2','5.2.4-3','5.3.4-4','5.4.4-1','5.4.4-2','5.4.4-5'],
 'Scarroccio prora vera · ora del traverso':['5.1.4-1','5.1.4-2','5.3.4-5','5.7.4-1','5.8.4-1'],
 'Scarroccio rotta vera · coordinate al traverso':['5.1.4-3','5.1.4-4'],
 'Scarroccio rotta vera · ora del traverso':['5.1.4-5'],
 'Scarroccio rotta vera · velocità · coordinate punto':['5.2.4-4','5.6.4-1'],
 'Scarroccio velocità':['5.4.4-3'],
 # correnti (52): lezioni 13, 14 e 15
 '1° problema della corrente':['5.2.1-1','5.3.1-7','5.3.1-9','5.4.1-4','5.4.1-8','5.4.1-17','5.4.1-18','5.7.1-2','5.8.1-2'],
 '2° problema della corrente':['5.1.1-6','5.2.1-2','5.2.1-4','5.3.1-10','5.4.1-2','5.4.1-6','5.4.1-7','5.4.1-11','5.4.1-12','5.5.1-1','5.6.1-1','5.8.1-4','5.8.1-6'],
 '3° problema della corrente':['5.1.1-1','5.2.1-3','5.3.1-5','5.3.1-6','5.4.1-1','5.4.1-13','5.4.1-14','5.8.1-1'],
 '4° problema della corrente':['5.1.1-2','5.1.1-4','5.2.1-5','5.3.1-1','5.3.1-2','5.3.1-3','5.3.1-4','5.3.1-8','5.4.1-3','5.4.1-5','5.4.1-10','5.4.1-15','5.4.1-16','5.5.1-3','5.6.1-2','5.7.1-1','5.8.1-3','5.8.1-5'],
 '4° + 2° problema della corrente':['5.1.1-3'],
 '4° + 3° problema della corrente':['5.1.1-5','5.4.1-9','5.5.1-2'],
}
CAT={e:k for k,v in _C.items() for e in v}
assert len(CAT)==135, len(CAT)
FAM={
 'Passaggio al traverso':'Cerchio della distanza attorno al faro e tangente da A dal lato giusto: è la Pv. Il contatto è il traverso.',
 'Passaggio al traverso + 3 RilB simultanei di 3 punti cospicui':'Tre Rilb → Rilv, tracciati insieme: il punto è il centro del piccolo triangolo. Poi traverso: Rilv = Pv ± 90°.',
 'Trasporto 2 RilB di 1 punto cospicuo':'Rilb → Rilv; il primo rilevamento si sposta del cammino (Pv, V × t) e incrocia il secondo.',
 'Trasporto 2 RilP di 1 punto cospicuo':'Prima Rilv = Pv + ρ, poi come i Rilb: trasporto del primo lungo il cammino.',
 'Trasporto 3 RilB di 1 punto cospicuo':'Primo e secondo trasportati all\'ora del terzo: le tre rette si incontrano nel punto nave.',
 'Trasporto 2 RilV di 2 punti cospicui':'Rilevamenti già veri: si tracciano dai due punti; il primo si trasporta del cammino fino all\'ora del secondo.',
 'Trasporto 2 RilB di 2 punti cospicui':'Come i RilV, dopo Rilv = Rilb + d + δ (declinazione aggiornata all\'anno).',
 'Trasporto 2 RilP di 2 punti cospicui':'Rilv = Pv + ρ per ciascun punto, poi trasporto del primo.',
 'Intercettazione':'Triangolo delle velocità: sua velocità da A, parallela ad AB, arco della tua velocità; la rotta incrocia la sua in C.',
 'Intercettazione su rotte opposte':'A e B sulla stessa linea, rotte opposte: si avvicinano a V1 + V2. t = AB ÷ (V1 + V2), C a V1 × t da A.',
 'Calcolo carburante':'Punto di partenza e d\'arrivo, miglia sulla scala delle latitudini, t = d ÷ V, litri = t × consumo × 1,3.',
 'Calcolo carburante e traverso':'Il punto al traverso è sulla perpendicolare alla rotta passante per il faro (Rilv = Rv ± 90°), alla distanza data.',
 'Calcolo carburante e RilP 45°/90°':'Doppio rilevamento 45°-90°: la distanza al traverso è il cammino percorso tra i due rilevamenti.',
 'Calcolo carburante e RilP 45°/90° e velocità':'Come il 45°-90°, ma la velocità si ricava: V = distanza percorsa sulla carta ÷ tempo tra i rilevamenti.',
 'Scarroccio prora vera':'Si conosce la rotta da fare: Pv = Rv − Sc (prora più al vento).',
 'Scarroccio prora vera · coordinate punto':'Rotta data: Pv = Rv − Sc; i rilevamenti polari si convertono con la Pv (Rilv = Pv + ρ) e si incrociano sulla Rv.',
 'Scarroccio prora vera · coordinate al traverso':'Rotta data: il traverso è Rilv = Pv ± 90°, dove taglia la Rv.',
 'Scarroccio prora vera · ora del traverso':'Come sopra, poi t = distanza sulla Rv ÷ Ve.',
 'Scarroccio rotta vera · coordinate al traverso':'Prora data: Rv = Pv + Sc da tracciare; il traverso Rilv = Pv ± 90° la taglia nel punto cercato.',
 'Scarroccio rotta vera · ora del traverso':'Prora data: Rv = Pv + Sc, traverso dalla Pv, t = distanza ÷ Ve.',
 'Scarroccio rotta vera · velocità · coordinate punto':'Rv = Pv + Sc e Ve = Vp ± variazione: il punto è a Ve × t sulla Rv.',
 'Scarroccio velocità':'Ve = distanza ÷ tempo, poi Vp = Ve corretta della variazione di velocità.',
 '1° problema della corrente':'Noti Pv, Vp, Dc, Vc: si sommano i vettori (un\'ora) e si trovano Rv e Ve.',
 '2° problema della corrente':'Noti Rv, Vp, Dc, Vc: corrente da A, compasso di Vp sulla rotta: Pv e Ve; il tempo è d ÷ Ve.',
 '3° problema della corrente':'Noti Rv e Ve (arrivo a un\'ora data), Dc e Vc: dalla punta della corrente al punto della Ve si leggono Pv e Vp.',
 '4° problema della corrente':'Stimato (Pv, Vp, t) e osservato B: dallo stimato a B c\'è la corrente; Dc è la direzione, Vc = lunghezza ÷ t.',
 '4° + 2° problema della corrente':'Prima la corrente (4°), poi con quella la Pv o il tempo per la nuova destinazione (2°).',
 '4° + 3° problema della corrente':'Prima la corrente (4°), poi Pv e Vp per arrivare all\'ora voluta (3°).',
}
assert set(FAM)==set(_C)
def famiglie_slide(sid, fams, title='Le famiglie d\'esame', note_extra='', where=None, fs=23, promemoria=None):
    """Tabella: famiglia del libro, esercizi ufficiali, come si risolve, e dove (slide)."""
    where=where or {}
    rows=''
    for k in fams:
        ids=_C[k]
        rows+=(f'<tr><td style="font-weight:800; color:{INK}; padding:4px 8px">{k}</td><td style="font-weight:800; color:{CORAL}; text-align:center">{len(ids)}</td>'
               f'<td style="padding:4px 8px">{FAM[k]}</td><td style="font-weight:700; color:{SEA}; padding:4px 8px">{where.get(k,"")}</td></tr>')
    tab=(f'<table style="font-size:{fs}px; line-height:1.3; color:#34465E; width:1664px">'
         f'<tr><th style="width:30%; text-align:left">Famiglia (come nei manuali)</th><th style="width:4%">Es.</th><th style="width:50%; text-align:left">Come si risolve</th><th style="width:16%; text-align:left">Dove</th></tr>{rows}</table>')
    notes='Famiglie e numero di esercizi ufficiali: '+'; '.join(f'{k}: {", ".join(_C[k])}' for k in fams)+'.'+note_extra
    strip=''
    if promemoria is not None:
        items=PROMEMORIA+list(promemoria)
        strip=(f'<div style="display:flex; flex-direction:column; gap:6px; background:{SUN_T}; padding:14px 22px; border-radius:20px">'
               f'<p style="font-size:20px; font-weight:900; letter-spacing:1px; text-transform:uppercase; color:{ORANGE}">Promemoria · gli strumenti di base (lezione 10)</p>'
               f'<p style="font-size:21px; line-height:1.35; font-weight:600; color:{INK}">{" · ".join(items)}</p></div>')
        notes+=' Promemoria degli strumenti di base, spiegati per intero nella lezione 10 (slide «Gli strumenti di base») e nelle lezioni 4 e 8.'
    sec(sid, head('Carteggio · gli esercizi d\'esame',title)+tab+strip, notes=notes, gap=20)

PROMEMORIA=['Coordinate con la squadretta','1° = 60′, 0,3 h = 18 min','miglia sulla scala delle latitudini','T = M ÷ V','declinazione aggiornata all\'anno','Pv = Pb + d + δ','Rilv = Rilb + d + δ','Rilv = Pv + ρ']
BASI=[('Coordinate','Lettura e riporto: squadretta sul punto, latitudine sul bordo verticale, longitudine su quello orizzontale. Lezione 8.'),
      ('Calcoli sessagesimali','1° = 60′; i decimi di primo restano decimi (42°49′,7). Ore: 0,3 h = 18 min, 25 min = 0,42 h. Lezione 4.'),
      ('Rotte','Lettura e tracciamento con le squadrette dalla rosa più vicina; si legge il valore vero. Lezione 4.'),
      ('Miglia','Compasso e scala delle latitudini alla stessa altezza: 1′ = 1 miglio. M = V × T. Lezioni 4 e 8.'),
      ('Tempo e velocità','T = M ÷ V, V = M ÷ T: i minuti si convertono prima in ore. Lezione 4.'),
      ('Declinazione','Si porta all\'anno della traccia: d = d(anno carta) + anni × variazione annua.'),
      ('Prore','Conversione e correzione: Pv = Pb + d + δ, Pb = Pv − d − δ (δ dalla prora magnetica). Lezione 4.'),
      ('Rilevamenti','Rilv = Rilb + d + δ (δ della prora); Rilv = Pv + ρ per i polari. Si tracciano dal punto cospicuo.')]
def basi_slide(sid, extra=(), notes=''):
    items=list(BASI)+list(extra)
    cols=[(CORAL,CORAL_T),(SEA,SEA_T),(PURPLE,LILAC_T),(BLUE,BLUE_T),(GREEN,GREEN_T),(ORANGE,SUN_T)]
    tiles=''.join(f'<div style="display:flex; flex-direction:column; gap:8px; background:{bg}; padding:24px 26px; border-radius:24px"><p style="font-family:{H}; font-size:36px; font-weight:700; line-height:1.05; color:{c}">{t}</p>{p(d,25,INK,600,1.35)}</div>'
                  for (t,d),(c,bg) in zip(items,(cols*3)[:len(items)]))
    sec(sid, head('Carteggio · prima di tracciare','Gli strumenti di base')+f'<div style="display:grid; grid-template-columns:repeat(4,1fr); gap:18px">{tiles}</div>',
        notes=notes or 'Gli argomenti di base che i manuali richiamano prima dei problemi d\'esame: lettura e riporto delle coordinate, calcoli sessagesimali, lettura e tracciamento delle rotte, calcolo delle miglia, del tempo e della velocità, declinazione, conversione e correzione delle prore, tracciamento e correzione dei rilevamenti bussola e polari. Si richiamano in un minuto: sono spiegati nelle lezioni 4 e 8.', gap=24)
