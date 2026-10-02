"""Appendice G: la normativa del diporto in tabelle (dai quiz ufficiali 1.8.1, 1.8.2, 1.4.1, 1.4.2, 1.3.3, 1.3.4)."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lezione_base import *
import lezione_base as LB
OUT=SP+'/deck/project'
ORANGE='#F28C28'

ORDER=['cover','indice','fonti','unita','documenti','categorie','limiti','quizA','quizAr',
       'patente','motore','validita','visite','contratti','quizB','quizBr',
       'comandante','sanzioni','numeri','porto','costa','quizC','quizCr',
       'sci','subacquei','pesca','amp','dotazioni1','dotazioni2','chiusura']
N=lambda sid: f'{ORDER.index(sid)+1:02d}'
EB='Appendice G · La normativa in tabelle'
LB.ICON_T.update({'Indice':'book','Le fonti delle regole':'book','Natanti, imbarcazioni, navi':'hull','I documenti di bordo':'book',
 'Le categorie di progettazione CE':'wind','Fin dove si può andare':'map','Quando serve la patente':'check','Le soglie del motore':'propeller',
 'Validità, sospensione, revoca':'check','Visite e certificato di sicurezza':'check','Locazione, noleggio, leasing':'pencil',
 'I doveri del comandante':'helm','Le sanzioni':'flag','I numeri della normativa':'star','Entrare e uscire dal porto':'anchor',
 'Sotto costa e d\'estate':'lifebuoy','Lo sci nautico':'wind','Subacquei e pesca subacquea':'flag','La pesca sportiva':'fuel',
 'Aree marine protette e ambiente':'map','Le dotazioni: salvarsi':'lifebuoy','Le dotazioni: navigare e comunicare':'compass'})

# ---------- tabella ----------
def table(head_cells,widths,rows,c=NAVY,size=24,first=None):
    pd='padding:12px 18px; '
    th=''.join(f'<th style="{pd}width:{w}%; color:#FFFFFF; text-align:left">{h}</th>' for h,w in zip(head_cells,widths))
    body=''
    for k,r in enumerate(rows):
        bg='#FFFFFF' if k%2==0 else PAPER
        cells=''
        for j,v in enumerate(r):
            if j==0: cells+=f'<td style="{pd}font-weight:800; color:{first or c}">{v}</td>'
            else: cells+=f'<td style="{pd}color:{INK}">{v}</td>'
        body+=f'<tr style="background:{bg}">{cells}</tr>'
    return f'<table style="font-size:{size}px; line-height:1.3; color:{BODY}; border-radius:18px"><tr style="background:{c}">{th}</tr>{body}</table>'
def tsec(sid,eyebrow,title,c,tab,notes,foot=None,gap=26):
    inner=head(eyebrow,title,c)+tab+(note(foot,c,34) if foot else '')
    sec(sid,inner,notes=notes,gap=gap)

# ============ COPERTINA ============
cover(0,'La normativa in tabelle','Unità, documenti, patente, contratti, doveri, sanzioni, distanze, sci nautico, pesca e aree protette: le regole del diporto da ripassare a colpo d\'occhio',
 'Appendice G al corso. Tutta la normativa dei quiz in tabelle: dati presi dalle risposte ufficiali (DD 131/2022, gruppi 1.8.1, 1.8.2, 1.4.1, 1.4.2, 1.3.3, 1.3.4) e dalle lezioni 3, 6 e 7.')
LB.slides[-1]=('cover',LB.slides[-1][1].replace('Lezione 00 · 2 ore','Appendice G · studio'))
assert 'vele spiegate' in LB.slides[-1][1]

# ============ INDICE ============
IX=[('L\'unità','Fonti, classificazione, documenti, categorie CE, limiti',['fonti','unita','documenti','categorie','limiti','quizA','quizAr'],CORAL),
    ('La patente e i contratti','Quando serve, motore, validità, visite, noleggio',['patente','motore','validita','visite','contratti','quizB','quizBr'],SEA),
    ('Responsabilità','Comandante, sanzioni, numeri da ricordare',['comandante','sanzioni','numeri'],PURPLE),
    ('Dove si naviga','Porti, costa e balneazione',['porto','costa','quizC','quizCr'],BLUE),
    ('Attività in mare','Sci nautico, subacquei, pesca, aree protette',['sci','subacquei','pesca','amp'],GREEN),
    ('Le dotazioni','Le tabelle del DM 133/2024',['dotazioni1','dotazioni2'],ORANGE)]
cards=''.join(f'<div style="display:flex; align-items:center; gap:18px; background:#FFFFFF; border-left:12px solid {c}; border-radius:24px; padding:18px 24px">'
              f'<p style="font-family:{H}; font-size:52px; font-weight:700; line-height:1; color:{c}; width:64px">{i+1:02d}</p>'
              f'<div style="flex:1; display:flex; flex-direction:column; gap:4px">{p(t,32,INK,800,1.2)}{p(d,24,BODY,500,1.3)}</div>'
              f'<p style="font-size:24px; font-weight:900; color:#FFFFFF; background:{c}; padding:4px 14px; border-radius:14px; white-space:nowrap">slide {N(ids[0])}–{N(ids[-1])}</p></div>' for i,(t,d,ids,c) in enumerate(IX))
sec('indice', head(EB,'Indice')+f'<div style="display:grid; grid-template-columns:1fr 1fr; gap:18px">{cards}</div>'
    +note('Ogni tabella riporta nelle note i numeri dei quiz ufficiali da cui viene.',SEA,36),
 notes='Appendice di ripasso: le regole sono le stesse delle lezioni 3 (porti e distanze), 6 (dotazioni) e 7 (normativa), riordinate in tabelle. Dove un dato viene da un quiz, all\'esame vale la risposta dell\'elenco ministeriale.')

# ============ FONTI ============
tsec('fonti','L\'unità','Le fonti delle regole',CORAL,
 table(['Norma','Che cosa regola'],[34,66],[
  ('Codice della nautica da diporto','D.Lgs. 171/2005: unità, documenti, patenti, contratti, sanzioni'),
  ('Regolamento di attuazione','Completa il Codice della nautica'),
  ('Codice della navigazione','Si applica per tutto ciò che il Codice della nautica non prevede'),
  ('DM 133/2024','Nuova tabella delle dotazioni di sicurezza (Allegato V al DM 146/2008)'),
  ('D.Lgs. 209/2005','Assicurazione obbligatoria di responsabilità civile'),
  ('DM 323/2021','Esami per la patente nautica'),
  ('Ordinanze','Regole locali della Capitaneria: rade, spiagge, porti, velocità')],CORAL,28),
 'Quiz 1.8.1-29 e -88 (il Codice della nautica vale per il diporto a scopo ricreativo e commerciale), -34 (regolamento di attuazione), -30 e -35 (per il resto, Codice della navigazione), -31…-33 e -95 (D.Lgs. 209/2005, assicurazione), -18 e -19 (ordinanze: regole locali), 1.4.2-3 (limiti dalla costa e atterraggio: ordinanze dei Capi di circondario), 1.3.3-45 (pronto soccorso: decreto 1° ottobre 2015 del Ministero della Salute).',
 'Dove c\'è un\'ordinanza locale, vale quella.')

# ============ UNITÀ ============
tsec('unita','L\'unità','Natanti, imbarcazioni, navi',CORAL,
 table(['','Natante','Imbarcazione','Nave da diporto'],[22,26,26,26],[
  ('Lunghezza','Fino a 10 m','Oltre 10 e fino a 24 m','Oltre 24 m'),
  ('Iscrizione','Non iscritto (se si iscrive, vale come imbarcazione)','ATCN, tramite qualsiasi STED','ATCN, tramite qualsiasi STED'),
  ('Sigla','—','4 lettere, 4 numeri e la D','—'),
  ('Licenza di navigazione','No','Sì','Sì'),
  ('Certificato di sicurezza','No','Sì','Sì'),
  ('Bandiera nazionale','No','Sì, sempre','Sì, sempre')
  ],CORAL,28),
 'Quiz 1.8.1-56 (classificazione per lunghezza fuori tutto), -57 (9 m: natante), -113 (natante: non iscritto), -21 e -86 (natante iscritto: regime delle imbarcazioni), -13, -24, -77 (iscrizione all\'ATCN tramite qualsiasi STED), -26 (sigla), -99 e -103 (licenza), -100 e 1.3.4-4, -10 (certificato di sicurezza solo a imbarcazioni e navi), -23, -60, -63 (bandiera), -15 (bandiera nella posizione più visibile), -17 (nome non obbligatorio). Marcatura CE: unità da 2,5 a 24 m immesse in commercio dopo il 16/06/1998 (-69).',
 'Si classifica sempre per lunghezza fuori tutto.')

# ============ DOCUMENTI ============
tsec('documenti','L\'unità','I documenti di bordo',CORAL,
 table(['Documento','Chi lo ha a bordo','Che cosa dice'],[28,30,42],[
  ('Licenza di navigazione','Imbarcazioni e navi','Dati dell\'unità e del proprietario; uso per locazione o noleggio'),
  ('Certificato di sicurezza','Imbarcazioni e navi','Che l\'unità è navigabile; scade e si rinnova'),
  ('Dichiarazione di potenza','Natanti a motore, imbarcazioni con fuoribordo','Le caratteristiche del motore'),
  ('Certificato di omologazione','Natanti CE prodotti in serie','Il numero di persone trasportabili'),
  ('Assicurazione RC','Ogni unità con motore','Copre ogni motore, anche fuoribordo e amovibile'),
  ('Contratto di locazione o noleggio','Unità locate o noleggiate','Va tenuto a bordo, in originale o copia conforme')],CORAL,28),
 'Quiz 1.8.1-99, -66, -52 (licenza: dati, validità finché non cambiano elementi strutturali, uso commerciale), -48 (certificato di sicurezza), -49, -98, -115 (dichiarazione di potenza), 1.3.3-37 e 1.8.1-105 (omologazione: persone trasportabili), -73 (manuale del proprietario del natante CE), -31, -32, -33, -95 (assicurazione: ogni motore; escluse solo le unità a remi e a vela senza motore), -46 e -51 (contratti a bordo), -47 e -76 (tra porti italiani bastano le copie conformi), -50 (autorizzazione alla navigazione temporanea: vale come documento di bordo).',
 'Tra porti italiani bastano le copie conformi all\'originale.')

# ============ CATEGORIE CE ============
tsec('categorie','L\'unità','Le categorie di progettazione CE',CORAL,
 table(['Categoria','Vento','Onda significativa','In pratica'],[18,22,26,34],[
  ('A','Oltre forza 8','Oltre 4 m','Traversate d\'altura'),
  ('B','Fino a forza 8','Fino a 4 m','Al largo'),
  ('C','Fino a forza 6','Fino a 2 m','Vicino alla costa, baie, laghi grandi'),
  ('D','Fino a forza 4','Fino a 0,3 m (a volte 0,5 m)','Acque protette')],PURPLE,28),
 'Quiz 1.8.1-12 e -61 (i limiti delle unità CE dipendono da onda significativa e vento), -116 (B: forza 8, 4 m), -117 (C: forza 6, 2 m), -119 (D: forza 4, 0,3 m, occasionalmente 0,5), -64 (all\'estero se la categoria lo consente), -124 (natante CE omologato senza limiti: entro 12 miglia). La categoria A è quella della direttiva 2013/53/UE; la scala Beaufort è nella lezione 7. Le visite di sicurezza dipendono dalla categoria (slide Visite).',
 'Un natante CE, anche «senza limiti», resta entro 12 miglia.')

# ============ LIMITI ============
tsec('limiti','L\'unità','Fin dove si può andare',CORAL,
 table(['Unità','Limite dalla costa'],[50,50],[
  ('Unità a remi: pedalò, jole, pattini, mosconi','Entro 1 miglio'),
  ('Tavola a vela','Entro 1 miglio'),
  ('Natante con vela fino a 4 m²','Entro 1 miglio'),
  ('Moto d\'acqua','Entro 1 miglio; oltre la velocità minima solo oltre 1000 m (500 m dalle coste a picco)'),
  ('Tender dell\'unità madre','Entro 1 miglio dalla costa o dall\'unità madre'),
  ('Natante CE omologato senza limiti','Entro 12 miglia'),
  ('Imbarcazione CE','Secondo la categoria di progettazione')],BLUE,28),
 'Quiz 1.8.1-53 e 1.4.2-24 (unità a remi), 1.4.2-21 (tavola a vela), -23 (vela fino a 4 m²), -20 (moto d\'acqua entro 1 miglio), 1.8.1-122 (moto d\'acqua oltre la velocità minima), 1.4.2-22 e 1.8.1-93 (tender: entro 1 miglio, senza dotazioni tranne i mezzi individuali), 1.8.1-124 (natante CE), -64 (imbarcazione CE all\'estero secondo la categoria). La patente entro 12 miglia permette di comandare un\'unità senza limiti, ma solo entro 12 miglia (-79).')

quiz_slide('quizA','Verifica · l\'unità',['1.8.1-57','1.8.1-98','1.8.1-117'],False)
quiz_slide('quizAr','Verifica · l\'unità',['1.8.1-57','1.8.1-98','1.8.1-117'],True)

# ============ PATENTE ============
tsec('patente','La patente e i contratti','Quando serve la patente',SEA,
 table(['Situazione','Patente','Senza patente'],[46,18,36],[
  ('Oltre 6 miglia dalla costa','Sempre','—'),
  ('Motore oltre 40,8 CV (30 kW) o sopra le soglie di cilindrata','Sì','—'),
  ('Moto d\'acqua','Sempre','—'),
  ('Sci nautico, anche con un natante','Sempre','—'),
  ('Natante entro 6 miglia, motore sotto le soglie','No','Almeno 16 anni'),
  ('Imbarcazione entro 6 miglia, motore sotto le soglie','No','Almeno 18 anni'),
  ('Imbarcazione a vela senza motore, entro 6 miglia','No','Almeno 18 anni'),
  ('Unità noleggiata','Titolo professionale','—')],SEA,28),
 'Quiz 1.8.1-67, -70, -101 (soglia di potenza: 40,8 CV), -111 (35 kW: sempre), -91, -107, -123 (moto d\'acqua), 1.8.2-3, -8, -14 (sci nautico), -118 (natante entro 6 miglia: 16 anni), -68 (imbarcazione entro 6 miglia sotto le soglie: 18 anni), -78 (vela senza motore: 18 anni), -80 (noleggio: titolo professionale), -114 (può reggere il timone anche chi non è abilitato, se a bordo c\'è chi ha la patente e si assume il comando), -72 (un secondo motore è ausiliario se amovibile e non oltre il 20% del principale). Il quiz 1.8.1-54 (16 anni) è oscurato.',
 'Al timone può stare anche chi non ha la patente, se a bordo c\'è chi ce l\'ha e comanda.')

tsec('motore','La patente e i contratti','Le soglie del motore',SEA,
 table(['Tipo di motore','Serve la patente oltre'],[60,40],[
  ('Qualsiasi motore','Oltre 30 kW (40,8 CV) di potenza'),
  ('2 tempi a carburazione','750 cm³'),
  ('2 tempi a iniezione diretta','900 cm³'),
  ('4 tempi fuoribordo','1000 cm³'),
  ('4 tempi entrobordo','1300 cm³'),
  ('Diesel','2000 cm³')],BLUE,28),
 'Codice della nautica (D.Lgs. 171/2005), art. 39: la patente serve se il motore supera anche una sola delle soglie. Quiz coerenti: 1.8.1-68 (29 kW e 750 cm³: non serve), -94 (1398 cm³, 4 tempi entrobordo: serve), -106 (1299 cm³ a iniezione diretta: serve), -110 (1098 cm³, 4 tempi fuoribordo: serve), -118 (998 cm³, 4 tempi fuoribordo: non serve), -101 (conta la potenza massima di esercizio).',
 'Basta superare una sola soglia.')

tsec('validita','La patente e i contratti','Validità, sospensione, revoca',SEA,
 table(['Caso','Che cosa succede'],[40,60],[
  ('Fino a 60 anni','Vale 10 anni'),
  ('Dopo i 60 anni','Vale 5 anni'),
  ('Ebbrezza, droghe, gravi imprudenze','Sospensione'),
  ('Perdita dei requisiti morali o fisici','Revoca'),
  ('Delinquente abituale','Non può conseguirla'),
  ('Comando con patente scaduta','Sanzione amministrativa, senza sospensione'),
  ('Comando senza patente','Da 2.755 a 11.017 euro e licenza sospesa 30 giorni')],SEA,28),
 'Quiz 1.8.1-89, -112, -87 (validità: 10 anni fino a 60, poi 5; a 55 anni il rinnovo vale 10 anni), -55 e -97 (sospensione), -104 (revoca), -62 (delinquente abituale), -71 e -75 (patente scaduta), -6 e -90 (comando senza abilitazione), -79 (patente entro 12 miglia su unità senza limiti: solo entro 12 miglia). Le categorie: A per natanti e imbarcazioni (entro 12 miglia o senza limiti, motore o vela e motore), B per le navi da diporto, C per le persone con disabilità (lezione 7).')

tsec('visite','La patente e i contratti','Visite e certificato di sicurezza',SEA,
 table(['Visita','Quando','Chi la fa'],[26,46,28],[
  ('Iniziale','Al primo rilascio: fissa le persone trasportabili','Organismo tecnico'),
  ('Prima periodica, categorie A e B','8 anni dall\'immatricolazione','Organismo tecnico'),
  ('Prima periodica, categorie C e D','10 anni dall\'immatricolazione','Organismo tecnico'),
  ('Periodiche successive','Ogni 5 anni','Organismo tecnico'),
  ('Occasionale','Dopo danni o modifiche a scafo o motore','Organismo tecnico'),
  ('Convalida del certificato','Dopo la visita','Qualsiasi STED')],SEA,28),
 'Quiz 1.3.4-6 (visita iniziale: persone trasportabili), -14, -15, -17 (prima scadenza 8 anni per A e B, 10 per C e D), -8, -13, -16 (poi ogni 5 anni), -2, -7, -11 (occasionali), -3 (unità CE: periodiche e occasionali), -12 e -18 (organismo tecnico, esito sul certificato), -1, -5, -9 (convalida presso gli STED: si convalida il certificato, non la licenza), -4 e -10 (solo imbarcazioni e navi; i natanti no), -19 (il certificato scade).',
 'Si convalida il certificato, non la licenza.')

tsec('contratti','La patente e i contratti','Locazione, noleggio, leasing',SEA,
 table(['Contratto','Che cosa ottieni','Chi comanda e risponde'],[20,42,38],[
  ('Locazione','L\'unità per un periodo, senza riscatto alla fine','Il conduttore: esercita la navigazione e ne ha i rischi'),
  ('Noleggio','L\'unità con i servizi del proprietario e il suo equipaggio','Il noleggiante, con titolo professionale; anche a cabina'),
  ('Noleggio occasionale','Il proprietario noleggia fino a 42 giorni l\'anno','Comunica ogni contratto ad Agenzia delle Entrate e Autorità marittima'),
  ('Leasing','Un finanziamento: usi l\'unità pagando un canone','L\'utilizzatore: rischi e comando; risponde in solido delle sanzioni')],PURPLE,28),
 'Quiz 1.8.1-81 (locazione: godimento senza riscatto), -44 e -45 (il conduttore esercita la navigazione e usa l\'unità secondo la licenza), -82 e -83 (noleggio: l\'unità resta al noleggiante con l\'equipaggio), -85 (noleggio a cabina), -51 (contratto scritto a pena di nullità, a bordo), -84 (noleggio occasionale: 42 giorni), -80 (titolo professionale), -27 e -28 (uso commerciale: locazione, noleggio, insegnamento, assistenza ai subacquei), -37 e -41 (esercizio abusivo: da 2.755 a 11.017 euro), -38, -39, -40, -42 (leasing), -36 (assistenza e traino: polizza e comunicazione alla Capitaneria).',
 'Locazione: guidi tu. Noleggio: ti portano loro.')

quiz_slide('quizB','Verifica · patente e contratti',['1.8.1-89','1.8.1-81','1.3.4-10'],False)
quiz_slide('quizBr','Verifica · patente e contratti',['1.8.1-89','1.8.1-81','1.3.4-10'],True)

# ============ COMANDANTE ============
tsec('comandante','Responsabilità','I doveri del comandante',PURPLE,
 table(['Dovere','Che cosa fare'],[32,68],[
  ('Comando','Dirige manovra e navigazione; decide l\'equipaggio minimo'),
  ('Dotazioni','Prima di partire le verifica; sostituisce quelle deteriorate'),
  ('Soccorso','Accorre verso chi è in pericolo e tenta il salvataggio, se non mette in grave pericolo la sua unità'),
  ('Urto','Soccorre le altre unità e dà i dati per identificare la sua'),
  ('Evento straordinario','Denuncia entro 3 giorni dall\'arrivo in porto all\'Autorità marittima; all\'estero al Consolato'),
  ('Relitti e ritrovamenti','Denuncia entro 3 giorni all\'Autorità marittima'),
  ('Rischio di inquinamento','Avvisa subito l\'Autorità marittima più vicina')],PURPLE,28),
 'Quiz 1.8.1-3 (direzione della manovra), -121 (equipaggio minimo), -120 e -125 (dotazioni), -7 e -9 (soccorso), -8 (urto), -1, -5, -65, -74, -92, -96, -108 (evento straordinario, per esempio un incaglio: lo denuncia il comandante entro 3 giorni), -2 e -109 (all\'estero: Consolato), -16 e -58 (ritrovamenti e relitti), 1.8.2-44 (sversamento di idrocarburi).',
 'Evento straordinario: 3 giorni.')

tsec('sanzioni','Responsabilità','Le sanzioni',PURPLE,
 table(['Violazione','Sanzione'],[55,45],[
  ('Comando senza patente','Da 2.755 a 11.017 euro e licenza sospesa 30 giorni'),
  ('Attività commerciali abusive','Da 2.755 a 11.017 euro'),
  ('Urto senza dare i dati per l\'identificazione','Da 1.032 a 6.197 euro'),
  ('Superamento dei limiti di velocità','Da 414 a 2.066 euro'),
  ('Mancato soccorso','Reclusione fino a 2 anni'),
  ('Comando con patente scaduta','Sanzione amministrativa'),
  ('Navigare a motore in un\'area marina protetta','Sanzione amministrativa, anche se non la conoscevi')],CORAL,28),
 'Quiz 1.8.1-90 e -6 (comando senza abilitazione), -37 e -41 (esercizio abusivo; il quiz -37 scrive 2.775 euro), -4 e -43 (urto), 1.4.2-10 e 1.4.1-1 (velocità), 1.8.1-10 (mancato soccorso: reato), -75 (patente scaduta), -11 (violare le norme di sicurezza della navigazione è un illecito amministrativo), 1.8.2-45 (area marina protetta).')

NU=[('3','giorni per denunciare un evento straordinario',CORAL),('42','giorni l\'anno di noleggio occasionale',SEA),('40,8','CV oltre i quali serve la patente',PURPLE),
    ('16 · 18','anni per condurre senza patente: natante · imbarcazione',BLUE),('10 · 5','anni di validità della patente: prima e dopo i 60',GREEN),('8 · 10','anni alla prima visita: categorie A e B · C e D',ORANGE),
    ('20%','potenza massima del motore ausiliario rispetto al principale',CORAL),('72','ore di ormeggio in transito nei porti turistici',SEA),('15%','ormeggi per la vela nei campi boe delle aree protette',PURPLE)]
g=''.join(f'<div style="display:flex; flex-direction:column; gap:6px; background:#FFFFFF; border-top:10px solid {c}; border-radius:24px; padding:24px 26px; box-shadow:0px 10px 28px rgba(27,42,65,0.10)"><p style="font-family:{H}; font-size:72px; font-weight:700; line-height:1; color:{c}">{n}</p>{p(d,26,INK,700,1.3)}</div>' for n,d,c in NU)
sec('numeri', head('Responsabilità','I numeri della normativa',PURPLE)+f'<div style="display:grid; grid-template-columns:1fr 1fr 1fr; gap:18px">{g}</div>',
 notes='Quiz 1.8.1-1 e -96 (3 giorni), -84 (42 giorni), -67 (40,8 CV), -118 e -68 (16 e 18 anni), -89 (validità), 1.3.4-14 e -15 (prima visita), 1.8.1-72 (motore ausiliario 20%), 1.4.1-20 (72 ore), 1.8.2-48 (15% alla vela). Da ripassare anche: 200 m dalle spiagge, 100 m dai subacquei, 12 m di cavo per lo sci nautico, 450 anni per la plastica.')

# ============ PORTO ============
tsec('porto','Dove si naviga','Entrare e uscire dal porto',BLUE,
 table(['Situazione','Regola, salvo ordinanze locali'],[38,62],[
  ('A 500 m dall\'ingresso','Riduci la velocità'),
  ('Transito nei 500 m davanti all\'ingresso','Dai precedenza a chi entra e a chi esce'),
  ('Chi entra e chi esce','Precedenza a chi esce'),
  ('Navi grandi in manovra','Hanno la precedenza'),
  ('A vela','In porto non si entra a vela'),
  ('Nel canale','Tieniti vicino al limite di destra'),
  ('Uscendo, se non ti vedono','Un suono prolungato, poi ascolta'),
  ('Porto commerciale senza strutture per il diporto','Avvisa l\'Autorità marittima')],BLUE,28),
 'Quiz 1.4.1-10 (500 m), -17 (transito davanti all\'ingresso), -4 e -9 (precedenza a chi esce), -6 (navi grandi), -12 (non si entra a vela), -19 (canale: a destra), -3 (tenere la dritta dove lo dice l\'ordinanza), -15 (1 suono prolungato), -5 (porto commerciale), -8, -13, -14 (rosso a sinistra, verde a dritta: si punta verso il verde), -20 (ormeggi in transito 72 ore), -21 (ormeggi per persone con disabilità), -16 (danni da moto ondoso), -1 (velocità: da 414 a 2.066 euro). I quiz -2 e -11 sul limite di 3 nodi sono oscurati: lo fissa l\'ordinanza del porto.')

tsec('costa','Dove si naviga','Sotto costa e d\'estate',BLUE,
 table(['Regola','Distanza o segnale'],[46,54],[
  ('Circolare, sostare, ancorare','Oltre 200 m dalle spiagge'),
  ('Limite dei 200 m','Gavitelli rossi ogni 50 m, paralleli alla costa'),
  ('Corridoi di lancio','Gavitelli gialli o arancioni fino a 250 m; bandiere bianche su quelli esterni'),
  ('Raggiungere la riva in emergenza','Piano, a remi, rotta perpendicolare alla costa'),
  ('Boa di un subacqueo','Stai ad almeno 100 m e rallenta'),
  ('Moto d\'acqua oltre la velocità minima','Oltre 1000 m dalla costa, 500 m dalle coste a picco'),
  ('Campo di regata','Cambia rotta e stai a distanza')],BLUE,28),
 'Quiz 1.4.2-4 (200 m), -5 (gavitelli rossi ogni 50 m), -6 e -7 (corridoi di lancio, bandiere bianche), -17 (nei corridoi lancio e atterraggio dei natanti a motore), -11 (emergenza: lento moto, remi, rotta perpendicolare), -2 e -12 (100 m dai subacquei), 1.8.1-122 (moto d\'acqua), 1.4.2-13 (manifestazioni sportive), -25 (la navigazione a motore può essere vietata nella fascia riservata alla balneazione). Il quiz 1.4.2-1 sui 10 nodi è oscurato: i limiti di velocità li fissano le ordinanze.',
 'D\'estate le ordinanze della Capitaneria dicono l\'ultima parola.')

quiz_slide('quizC','Verifica · responsabilità e costa',['1.8.1-96','1.4.2-4','1.4.1-12'],False)
quiz_slide('quizCr','Verifica · responsabilità e costa',['1.8.1-96','1.4.2-4','1.4.1-12'],True)

# ============ SCI NAUTICO ============
tsec('sci','Attività in mare','Lo sci nautico',GREEN_S,
 table(['Voce','Regola'],[30,70],[
  ('Chi guida','Sempre con la patente, anche su un natante'),
  ('A bordo','Oltre a chi guida, una persona esperta nel nuoto'),
  ('Quando','Di giorno, con tempo favorevole e mare calmo'),
  ('Dove','Oltre 200 m dalla spiaggia (100 m dalle coste a picco), lontano da bagnanti e barche'),
  ('Partenza e rientro','Nei corridoi di lancio o in acque libere; rotta perpendicolare alla costa, al massimo 3 nodi'),
  ('Traino','Cavo di almeno 12 m, al massimo 2 sciatori'),
  ('Attrezzatura','Specchietto convesso, gancio di traino, motore con invertitore e folle'),
  ('Dotazioni in più','Pronto soccorso e un salvagente per ogni sciatore')],GREEN_S,28),
 'Quiz 1.8.2-3, -8, -14 (patente), -4, -9, -26 (persona esperta nel nuoto), -7 e -11 (di giorno, mare calmo), -10 e -17 (200 m dalla batimetrica di 1,60 m; 100 m dalle coste a picco), -15 (partenza e recupero), -6 e -19 (3 nodi, rotta perpendicolare), -12 (12 m), -24 (2 sciatori), -23 (specchietto convesso), -16 e -18 (gancio e specchietto riconosciuti dalla Capitaneria), -21 (invertitore e folle), -1, -2, -20, -22 (pronto soccorso e salvagenti), -5 e -25 (le altre unità stanno fuori dalla scia e più lontane della lunghezza del cavo), -13 (qualsiasi unità da diporto).')

tsec('subacquei','Attività in mare','Subacquei e pesca subacquea',GREEN_S,
 table(['Voce','Regola'],[34,66],[
  ('Segnale del subacqueo','Bandiera rossa con striscia diagonale bianca, visibile a 300 m'),
  ('Di notte','Luce gialla lampeggiante, visibile a 300 m'),
  ('Distanza dalla boa','Il subacqueo sta entro 50 m dalla sua boa'),
  ('Con un mezzo di appoggio','La bandiera sta sul mezzo'),
  ('Pesca subacquea: chi','Dai 16 anni, solo in apnea: mai con le bombole'),
  ('Pesca subacquea: quando','Mai dal tramonto all\'alba; nessuna luce tranne la torcia'),
  ('Pesca subacquea: dove','Oltre 500 m dalle spiagge frequentate; 100 m da navi ancorate, impianti fissi e reti'),
  ('Il fucile','Carico solo in immersione')],GREEN_S,28),
 'Quiz 1.8.2-32 (bandiera visibile a 300 m), 1.4.2-8 (unità in attività subacquea: pallone rosso con bandiera), -9 e -16 (di notte: luce gialla lampeggiante a 300 m), -15 e -19 (50 m), 1.8.2-31 (mezzo di appoggio), -27 (16 anni), -28, -41, 1.4.2-31 (solo apnea), 1.8.2-29 e -30, 1.4.2-27 (orari e luci), 1.4.2-26 (500 m dalle spiagge), 1.8.2-34, -35, 1.4.2-30 (100 m), 1.8.2-33 (fucile carico solo in immersione), 1.4.2-14 (bandiera A: palombaro in immersione).')

tsec('pesca','Attività in mare','La pesca sportiva',GREEN_S,
 table(['Voce','Regola'],[30,70],[
  ('Scopo','Solo ricreativo o agonistico: vietato vendere il pescato'),
  ('Quanto','Al massimo 5 kg al giorno, salvo un pesce singolo più pesante; una sola cernia'),
  ('Tonno rosso','Un esemplare; vietato venderlo; le catture si fermano per decreto'),
  ('Attrezzi','Canne fino a 3 ami, correntine fino a 6, bolentini, lenze per cefalopodi'),
  ('Vietato','Reti a circuizione e pesca professionale dal diporto'),
  ('Distanza','Oltre 500 m dalle unità che pescano professionalmente'),
  ('Gare','Servono l\'approvazione e l\'ordinanza del Capo del Compartimento')],GREEN_S,28),
 'Quiz 1.8.2-36 e -37 (scopo, niente vendita), -40 (5 kg e una cernia), -42, -43, -56 (tonno rosso), -38 (attrezzi), 1.4.2-28 e -29 (niente reti a circuizione né pesca professionale), -32 (500 m dalla pesca professionale), 1.8.2-39 (gare), 1.4.2-18 (pesca sportiva con unità da diporto: sì, entro i limiti di cattura).')

tsec('amp','Attività in mare','Aree marine protette e ambiente',GREEN_S,
 table(['Zona o regola','Che cosa si può fare'],[34,66],[
  ('Zona A · riserva integrale','Niente navigazione, niente ancoraggio'),
  ('Zona B · riserva generale','Remi e vela sì; il resto secondo decreto e regolamento'),
  ('Zona C · riserva parziale','Secondo decreto e regolamento; campi boe anche qui e in B'),
  ('Campi boe','Mai ancorare; il 15% degli ormeggi è per la vela'),
  ('Sorveglianza','Capitanerie di porto e polizie degli enti locali delegati'),
  ('Olio e plastica','5 kg di olio inquinano una superficie enorme; la plastica dura fino a 450 anni'),
  ('Razzi e fuochi scaduti','Si riportano al rivenditore')],GREEN_S,28),
 'Quiz 1.8.2-53 e -54 (zone A, B, C, a volte D, delimitate in carta), -49 e -55 (zona A), -50 e -57 (zona B), -47 (campi boe in B e C), -48 (15% alla vela), -59 (niente ancoraggio nei campi boe), -46 (sorveglianza), -45 (sanzione anche se l\'area non è segnalata), -51 (olio), -58 (plastica), -52 (segnali scaduti), -44 (sversamento: avvisare subito l\'autorità).')

# ============ DOTAZIONI (dalla lezione 6) ============
COLS=['oltre 50','entro 50','entro 12','entro 6','entro 3','entro 1','300 m']
def dtable(rows):
    pd='padding:8px 12px; '
    th=''.join(f'<th style="{pd}width:9%; text-align:center; color:#FFFFFF">{c}</th>' for c in COLS)
    h=f'<tr style="background:{ORANGE}"><th style="{pd}width:37%; color:#FFFFFF; text-align:left">Dotazione (miglia dalla costa)</th>'+th+'</tr>'
    body=''
    for k,(name,vals) in enumerate(rows):
        bg=PAPER if k%2 else '#FFFFFF'
        body+=f'<tr style="background:{bg}"><td style="{pd}font-weight:700; color:{INK}">{name}</td>'+''.join(f'<td style="{pd}text-align:center; font-weight:800; color:{SEA if v=="●" else CORAL}">{v}</td>' for v in vals)+'</tr>'
    return f'<table style="font-size:24px; color:{BODY}">{h}{body}</table>'
o='●'; n=''
T1=[('Zattera di salvataggio (tutti a bordo)',[o,o,n,n,n,n,n]),('Zattera costiera',[n,n,o,n,n,n,n]),
    ('Giubbotti 150 N con luce automatica',[o,o,o,n,n,n,n]),('Giubbotti 100 N',[n,n,n,o,o,o,n]),
    ('Salvagente anulare con cima',[o,o,o,o,o,n,n]),('Boetta luminosa per il salvagente',[o,o,o,o,n,n,n]),
    ('Boette fumogene',['2','2','2','2','1',n,n]),('Fuochi a mano a luce rossa',['3','2','2','2','2',n,n]),
    ('Razzi a paracadute a luce rossa',['3','2','2','2',n,n,n]),('Imbragature con safety line (vela)',['2','2','1',n,n,n,n])]
T2=[('Bussola e tabella deviazioni, orologio',[o,o,o,n,n,n,n]),('Tabella dei segnali COLREG',[o,o,o,n,n,n,n]),('Apparato VHF',[o,o,o,n,n,n,n]),
    ('Binocolo, barometro, carte, strumenti da carteggio',[o,o,n,n,n,n,n]),('GPS, scandaglio, riflettore radar, pronto soccorso',[o,o,n,n,n,n,n]),
    ('EPIRB (o telefono satellitare)',[o,n,n,n,n,n,n]),('Fanali regolamentari',[o,o,o,o,o,n,n]),('Fischio e campana (oltre 12 m)',[o,o,o,o,o,n,n]),
    ('Pallone nero di fonda (oltre 7 m)',[o,o,o,o,o,o,n]),('Pompa di sentina',[o,o,o,o,o,o,n])]
sec('dotazioni1', head('Le dotazioni · DM 133/2024','Le dotazioni: salvarsi',ORANGE)+dtable(T1)+p('● obbligatoria · il numero indica quante. Tavole, derive e moto d\'acqua: galleggiante da 50 N sempre indossato.',24,INK,700), gap=22,
 notes='Stessa tabella della lezione 6: Allegato V al DM 146/2008 come sostituito dal DM 17 settembre 2024 n. 133, in vigore dal 21/10/2024. Entro 300 m nessuna dotazione obbligatoria in tabella. Alcuni quiz seguono la tabella precedente e all\'esame vanno risposti come nell\'elenco: 1.3.3-15 (entro 300 m salvagente e cinture), -12 (cinture oltre 300 m). Tavole a vela e moto d\'acqua: mezzo individuale sempre indossato (1.3.3-38, -44). Oscurati: 1.3.3-4, -6, -9, -11, -14, -23, -25, -26, -32, -33, -35, -36, -41, -42.')
sec('dotazioni2', head('Le dotazioni · DM 133/2024','Le dotazioni: navigare e comunicare',ORANGE)+dtable(T2)+p('Estintori: secondo il manuale del proprietario (unità CE); su un natante entro 6 miglia almeno 1.',24,INK,700), gap=22,
 notes='Quiz coerenti: 1.3.3-1 e -40 (VHF oltre 6 miglia), -22 e -34 (EPIRB oltre 50), -24 (riflettore radar oltre 12), -43 (binocolo oltre 12), -39 (entro 12 niente zattera non costiera), -30 (radar non obbligatorio), -5 (bussola e tabelle), -8 (fanali di notte oltre 1 miglio), -48 (pronto soccorso oltre 12), -45…-47 (tabella D del decreto 1° ottobre 2015), 1.3.1-29 e -30 (estintori), 1.3.3-2 (natante entro 6 miglia: almeno un estintore), -21 (segnali: scadenza 4 anni).')

closing(['Natante fino a 10 m, imbarcazione fino a 24, poi nave: si classifica per lunghezza',
         'Patente sempre oltre 6 miglia, oltre 40,8 CV, con moto d\'acqua e sci nautico',
         'Evento straordinario e relitti: denuncia entro 3 giorni',
         'Locazione: comandi tu; noleggio: ti porta il noleggiante; leasing: è un finanziamento',
         '200 m dalle spiagge, 100 m dai subacquei; in zona A delle aree protette non si entra'],
 'Buon vento, e in regola!','Appendice G · La normativa in tabelle')

write_deck(OUT,'Appendice G · La normativa in tabelle',ORDER,
 {"s1":{"description":"Copertina, indice, fonti, unità, documenti, categorie e limiti","start":"cover"},
  "s2":{"description":"Patente, motore, validità, visite e contratti","start":"patente"},
  "s3":{"description":"Comandante, sanzioni e numeri da ricordare","start":"comandante"},
  "s4":{"description":"Porti, costa e balneazione","start":"porto"},
  "s5":{"description":"Sci nautico, subacquei, pesca, aree protette","start":"sci"},
  "s6":{"description":"Le dotazioni di sicurezza e la chiusura","start":"dotazioni1"}})
