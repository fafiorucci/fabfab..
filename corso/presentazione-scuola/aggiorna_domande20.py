# Presentazione alla scuola: aggiunge la slide «domande20» (le 20 domande del quiz base per materia, All. C DM 323/2021)
# dopo «percorsi», rinumera, aggiorna il piè di pagina e i tempi delle note. Uso: python3 aggiorna_domande20.py <cartella project>
import os,sys,json,re
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from template import *
P=sys.argv[1]
FOOT_OLD='Fabrizio Fiorucci · Patente nautica Vela/Motore senza limiti dalla costa'
FOOT_NEW='Fabrizio Fiorucci · Patente nautica Vela/Motore entro le 12 miglia e senza limiti dalla costa'
d=json.load(open(P+'/deck.json'))
if 'domande20' not in d['order']:
    d['order'].insert(d['order'].index('percorsi')+1,'domande20')
json.dump(d,open(P+'/deck.json','w'),ensure_ascii=False,indent=1)
M=[('Navigazione cartografica',4,'03 · 04 · 05 · 08','carte e coordinate, bussola e rotta, punto nave, carteggio',CORAL),
   ('Manovra e condotta',4,'03 · 04 · 06','ormeggi e ancoraggi, sottocosta, porti',SEA),
   ('Sicurezza',3,'06','dotazioni, incendio, sinistri, soccorso',PURPLE),
   ('Normativa',3,'07','unità, documenti, patente, autorità, ambiente',BLUE),
   ('COLREG e segnalamento',2,'03 · 05 · 06','fari e IALA, fanali e precedenze, segnali sonori',GREEN),
   ('Meteorologia',2,'07','pressione, venti, fronti, bollettini',SUN),
   ('Teoria dello scafo',1,'01 · 02','scafo e stabilità, elica e timone',CORAL),
   ('Motori',1,'02','motore, avarie, autonomia',SEA)]
th='padding:12px 20px; color:#FFFFFF; background:#16324F; text-align:left; font-size:24px'
rows=f'<tr><th style="{th}; width:30%">Materia (All. C, DM 323/2021)</th><th style="{th}; width:12%; text-align:center">Domande</th><th style="{th}; width:20%">Lezioni</th><th style="{th}">Che cosa si studia</th></tr>'
for k,(t,n,l,w,c) in enumerate(M):
    bg='#FFFFFF' if k%2==0 else '#FBF6EC'
    rows+=(f'<tr style="background:{bg}"><td style="padding:8px 20px; font-weight:800; color:{INK}; border-left:10px solid {c}">{t}</td>'
           f'<td style="padding:8px 20px; text-align:center; font-family:{H}; font-size:32px; font-weight:700; color:{INK}">{n}</td>'
           f'<td style="padding:8px 20px; font-weight:700; color:{INK}">{l}</td><td style="padding:8px 20px; color:{BODY}">{w}</td></tr>')
rows+=(f'<tr style="background:#D5F3F5"><td style="padding:8px 20px; font-weight:900; color:{INK}">Totale quiz base</td>'
       f'<td style="padding:8px 20px; text-align:center; font-family:{H}; font-size:36px; font-weight:700; color:{CORAL}">20</td>'
       f'<td colspan="2" style="padding:8px 20px; font-weight:700; color:{INK}">al massimo 4 errori, 30 minuti</td></tr>')
table=f'<table style="font-size:24px; line-height:1.3; color:{BODY}; width:1664px">{rows}</table>'
nota=p('<b>Ogni materia conta una volta sola</b>, anche se si studia in più lezioni: la somma fa sempre 20. I 5 quiz vela sono una prova a parte.',24,BODY)
notes=('[40 secondi · minuto 3:50] Come sono fatte le 20 domande del quiz base, uguale per entrambe le patenti, entro 12 miglia e senza limiti. L\'Allegato C al DM 323/2021 le ripartisce per materia: navigazione cartografica 4, manovra e condotta 4, sicurezza 3, normativa 3, COLREG e segnalamento 2, meteorologia 2, teoria dello scafo 1, motori 1. '
       'Alcune materie si studiano in più lezioni: la navigazione nelle lezioni 3, 4, 5 e 8; la manovra nelle 3, 4 e 6; COLREG e segnalamento nelle 3, 5 e 6; la teoria dello scafo nelle 1 e 2. Ma all\'esame ogni materia vale sempre lo stesso numero di domande: le 4 domande di navigazione sono 4 in tutto, non 4 per ogni lezione. '
       'Per questo in ogni lezione l\'agenda e la raccolta quiz mostrano questa stessa tabella da 20, con evidenziate le materie del giorno: l\'allievo sa sempre quanto pesa quello che sta studiando.')
inner=header('Quiz base · All. C al DM 323/2021','Le 20 domande, materia per materia','chart',CORAL)+table+nota
html=(f'<section id="domande20" data-transition="fade" style="background:{PAPER}; color:{BODY}; font-family:{B}; padding:128px 128px 160px; display:flex; flex-direction:column; gap:24px">\n{backdrop(False,5)}\n{inner}\n{footer(5,False)}\n<aside>{notes}</aside>\n</section>\n')
open(P+'/slides/domande20.html','w').write(html)
TEMPI={'velamotore':'5:00','allievi':'6:10','materiale':'7:20','perche':'8:20'}
for n,i in enumerate(d['order'],1):
    f=f'{P}/slides/{i}.html'; s=open(f).read()
    s=s.replace(FOOT_OLD,FOOT_NEW)
    s=re.sub(r'(border-radius:20px">)\d\d(</p>)',lambda m:f'{m.group(1)}{n:02d}{m.group(2)}',s)
    if i in TEMPI: s=re.sub(r'(<aside>\[\d+ secondi · minuto )\d+:\d\d',lambda m:m.group(1)+TEMPI[i],s)
    if i=='cover':
        s=s.replace('>Patente nautica Vela/Motore senza limiti dalla costa<','>Patente nautica Vela/Motore entro le 12 miglia e senza limiti dalla costa<')
        s=s.replace('per la patente vela e motore senza limiti dalla costa','per la patente vela e motore entro le 12 miglia e senza limiti dalla costa')
        s=s.replace('In sette slide','In otto slide')
    open(f,'w').write(s)
print(d['order'])
