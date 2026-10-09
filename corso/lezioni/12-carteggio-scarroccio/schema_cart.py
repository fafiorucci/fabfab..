"""Schema delle lezioni di carteggio 10-15: capitoli con apertura, verifica da 2 quiz in fondo a ogni capitolo,
raccolta di 36 quiz negli ultimi 45 minuti. Si esegue con exec() dopo apertura.py ed esame.py."""
SHORT={'1.2.3':'Autonomia e carburante','1.7.1':'Coordinate geografiche','1.7.2':'Carte nautiche','1.7.3':'Navigazione elettronica',
       '1.7.4':'Bussola e rosa dei venti','1.7.5':'Tempo, spazio e velocità','1.7.6':'Navigazione costiera','1.7.7':'Prora, rotta, scarroccio e deriva','1.7.8':'Pubblicazioni nautiche'}
def schema(lez, order, chapters, verifs, racc, steps, plan, notes_quiz, esame=('navigazione',)):
    """chapters: (id, titolo, argomenti, colore, minuti, prima slide, art)
    verifs: un elenco di coppie di quiz, una per capitolo, inserite dopo l'ultima slide del capitolo
    racc: 12 tuple (sezione, [3 quiz])"""
    order=list(order); secs={"s1":{"description":"Apertura","start":"cover"}}
    starts=[c[5] for c in chapters]
    for k,(cid,title,subs,c,mins,start,art) in enumerate(chapters):
        chapter(cid,k+1,title,subs,c,f'Circa {mins} minuti, verifica da 2 quiz compresa.',f'circa {mins} minuti · {len(subs)} argomenti',2 if len(subs)>6 else 1,art=art)
        order.insert(order.index(start),cid)
        secs[f's{k+2}']={"description":title,"start":cid}
    for k,(cid,title,*_ ) in enumerate(chapters):
        nxt=chapters[k+1][0] if k+1<len(chapters) else 'chiusura'
        ps=verifs[k]; qid=f'v{k+1}'
        quiz_slide(qid,f'Verifica · {title}',ps,False,'Verifica del capitolo · quiz ufficiali')
        quiz_slide(qid+'r',f'Verifica · {title} · risposte',ps,True)
        i=order.index(nxt); order[i:i]=[qid,qid+'r']
    QZ=[(f'q{i:02d}',f'Quiz {i} · {SHORT[s]}',ps) for i,(s,ps) in enumerate(racc,1)]
    raccolta(lez,len(chapters)+1,[t.split(' · ',1)[1] for _,t,_ in QZ],QZ,steps,plan,notes_quiz,esame=list(esame))
    i=order.index('chiusura'); order[i:i]=['capquiz','quiz']+[q+s for q,_,_ in QZ for s in ('','r')]
    secs[f's{len(chapters)+2}']={"description":"Raccolta quiz","start":"capquiz"}
    return order,secs
