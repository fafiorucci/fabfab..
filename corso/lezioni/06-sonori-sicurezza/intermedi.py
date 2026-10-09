def intermedi(spec):
    for after,qid,t,ps in spec:
        n=len(slides)
        quiz_slide(qid,t,ps,False,'Verifica del paragrafo · quiz ufficiali')
        quiz_slide(qid+'r',t+' · risposte',ps,True)
        new=slides[n:]; del slides[n:]
        i=[s_[0] for s_ in slides].index(after)+1
        slides[i:i]=new
